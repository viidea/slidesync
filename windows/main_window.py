from PyQt4 import QtGui, QtCore
import logging
import os
from PyQt4.QtGui import QMessageBox, QDialog
from processing.slide_syncer import SlideSyncer
from processing.utils import package_slides
from ui import main_window
from video import VideoFile
from windows.extract_window import ExtractWindow
from windows.file_chooser_window import FileChooserWindow
from windows.match_window import MatchWindow
from windows.review_window import ReviewWindow
from windows.sync_window import SyncWindow

logger = logging.getLogger(__name__)

class ProcessingState(object):
    files = None               # (Original video, Slide video, Slide dir)
    slide_crop_box = None      # Crop box for slide video
    slides = None              # Path to slides
    video_slides = None        # Slides extracted from video
    timings = None             # Fixed timings for video
    matches = None
    synced_slides = None

    def __str__(self):
        return "Files: %s\n Crop box:%s\n Slides: %s \n Video slides: %s\n Matches: %s\n Timings: %s Matches: %s\n Synced slides: %s\n" \
            % (self.files, self.slide_crop_box, self.slides, self.video_slides, self.matches, self.timings, self.matches, self.synced_slides)

class MainWindow(main_window.Ui_MainWindow, QtGui.QMainWindow):
    # State data
    _state = None

    def __init__(self, app):
        super(QtGui.QMainWindow, self).__init__()
        self._app = app
        self.setupUi(self)
        self.btnStart.clicked.connect(self._process)
        self._state = ProcessingState()

    def _process(self):
        self.btnStart.setEnabled(False)

        if not (self._get_files() and
                self._load_slides() and
                self._extract_frames() and
                self._match_slides() and
                self._review_matches() and
                self._sync_with_original() and
                self._package_slides()):

            # User canceled one of the steps
            self._clear_state()

        self.btnStart.setEnabled(True)

    def _get_files(self):
        self._label_set_bold(self.lblLoadFiles, True)
        select_files_window = FileChooserWindow(self)
        select_files_window.exec_()

        if select_files_window.result() == QDialog.Accepted:
            self._state.files = select_files_window.getFiles()
            self._state.slide_crop_box = select_files_window.getSlideCropBox()
            self._label_set_bold(self.lblLoadFiles, False)
            return True

        self._label_set_bold(self.lblLoadFiles, False)
        return False

    def _load_slides(self):
        _, _, dirname = self._state.files
        image_slides = []
        num = 0
        try:
            for file in sorted(os.listdir(dirname)):
                filename, extension = os.path.splitext(file)
                if extension.lower() == ".png" or extension.lower() == ".jpg":
                    image_slides.append((num, os.path.join(dirname, file)))
                    num += 1
        except IOError as e:
            msgBox = QMessageBox(QMessageBox.Critical, "Error :(", "Slides not be loaded.")
            msgBox.setDetailedText(unicode(e))
            msgBox.exec_()
            return False

        if len(image_slides) == 0:
            msgBox = QMessageBox(QMessageBox.Critical, "Error :(", "Chosen slide directory does not contain any slides, aborting...")
            msgBox.exec_()
            return False

        self._state.slides = image_slides
        return True

    def _extract_frames(self):
        self._label_set_bold(self.lblExtractFrames, True)
        video = VideoFile(self._state.files[1], keyframes_only=False)
        extract_window = ExtractWindow(self, video, self._state.slide_crop_box, app=self._app)
        extract_window.exec_()
        self._state.video_slides = extract_window.video_slides
        self._label_set_bold(self.lblExtractFrames, False)
        return True

    def _match_slides(self):
        self._label_set_bold(self.lblMatch, True)
        match_window = MatchWindow(self, self._app, self._state.slides, self._state.video_slides)
        match_window.show()
        match_window.process()
        self._state.matches = match_window.matches
        self._label_set_bold(self.lblMatch, False)
        return True

    def _review_matches(self):
        self._label_set_bold(self.lblReview, True)
        logger.info(self._state)
        review_window = ReviewWindow(self, self._state.slides, self._state.video_slides, self._state.matches)
        review_window.show()
        while not review_window.done:
            self._app.processEvents()
        self._state.matches = review_window.matches
        self._label_set_bold(self.lblReview, False)
        return True

    def _sync_with_original(self):
        self._label_set_bold(self.lblSync, True)
        sync_window = SyncWindow(self, self._app, self._state.files[0], self._state.files[1], self._state.matches)
        sync_window.show()
        self._state.synced_slides = sync_window.process()
        self._label_set_bold(self.lblSync, False)
        return True

    def _package_slides(self):
        self._label_set_bold(self.lblSave, True)
        filename = None
        while filename is None:
            filename = QtGui.QFileDialog().getSaveFileName(self, "Save file...", QtCore.QDir().homePath(), "Zip files (*.zip)")

        if len(filename) == 0:
            return False

        package_slides(unicode(filename), [slide for num, slide in self._state.slides],  self._state.synced_slides)
        self._label_set_bold(self.lblSave, False)
        return True

    def _label_set_bold(self, label, bold=True):
        font = label.font()
        font.setBold(bold)
        label.setFont(font)
        self.update()
        self._app.processEvents()

    def _clear_state(self):
        self._state = ProcessingState()
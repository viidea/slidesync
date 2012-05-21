from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QDialogButtonBox, QMessageBox
import settings
from ui import file_chooser_dialog
from video import VideoFile, VideoLoadException
from windows.load_video_window import LoadVideoWindow

class FileChooserWindow(QtGui.QDialog, file_chooser_dialog.Ui_Dialog):
    _cropbox = None

    def __init__(self, parent):
        super(QtGui.QDialog, self).__init__(parent)
        self.setupUi(self)
        self.btnSlideVideo.clicked.connect(self._select_slide_video)
        self.btnOriginalVideo.clicked.connect(self._select_original_video)
        self.btnSlideDir.clicked.connect(self._select_slide_directory)
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)

        self.cmbSlideVideo.currentIndexChanged.connect(self._check_values)
        self.cmbSlideVideo.activated.connect(self._crop_slide_video)
        self.cmbSlideDirectory.currentIndexChanged.connect(self._check_values)
        self.cmbRenderedVideo.currentIndexChanged.connect(self._check_values)

        self.buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self._pre_close)
        self._load_settings()

    def _select_slide_video(self):
        filename = QtGui.QFileDialog(self).getOpenFileName(self, "Open slide video file", QtCore.QDir().homePath())
        if filename == "":
            return      # User canceled the dialog
        filename = unicode(filename)

        self._push_to_combo_box(self.cmbSlideVideo, filename)
        self._crop_slide_video(0)

    def _crop_slide_video(self, index):
        filename = unicode(self.cmbSlideVideo.itemText(index))

        try:
            video = VideoFile(filename)
        except VideoLoadException as e:
            msgBox = QMessageBox(QMessageBox.Critical, "Error :(", "Failed to load slide video file.")
            msgBox.setDetailedText(unicode(e))
            msgBox.exec_()
            return

        crop_window = LoadVideoWindow(self, video=video)
        crop_window.exec_()
        self._cropbox = crop_window.selected
        self._check_values()

    def _pre_close(self):
        if self._cropbox is None:
            self._crop_slide_video(self.cmbSlideVideo.currentIndex())

    def _select_slide_directory(self):
        dirname = QtGui.QFileDialog().getExistingDirectory(self, "Open slide directory", QtCore.QDir().homePath())
        if dirname == "":
            return
        dirname = unicode(dirname)  # Convert from QString to unicode string
        self._push_to_combo_box(self.cmbSlideDirectory, dirname)
        self._slide_dir = dirname
        self._check_values()

    def _select_original_video(self):
        filename = QtGui.QFileDialog(self).getOpenFileName(self, "Open original video file", QtCore.QDir().homePath())
        if filename == "":
            return      # User canceled the dialog
        filename = unicode(filename)
        self._push_to_combo_box(self.cmbRenderedVideo, filename)
        self._original_video = filename
        self._check_values()

    def _check_values(self):
        if len(unicode(self.cmbRenderedVideo.currentText()).strip()) > 0 and \
           len(unicode(self.cmbSlideVideo.currentText()).strip()) > 0 and \
           len(unicode(self.cmbSlideDirectory.currentText()).strip()) > 0:
            self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)

    def getFiles(self):
        return unicode(self.cmbRenderedVideo.currentText()), unicode(self.cmbSlideVideo.currentText()), unicode(self.cmbSlideDirectory.currentText())

    def getSlideCropBox(self):
        return self._cropbox

    def _push_to_combo_box(self, combo_box, path):
        combo_box.insertItem(0, path)
        combo_box.setCurrentIndex(0)
        self._store_settings()

    def _store_settings(self):
        recent_rendered_videos = []
        for i in range(0, self.cmbRenderedVideo.count()):
            recent_rendered_videos.append(unicode(self.cmbRenderedVideo.itemText(i)))

        recent_slide_videos = []
        for i in range(0, self.cmbSlideVideo.count()):
            recent_slide_videos.append(unicode(self.cmbSlideVideo.itemText(i)))

        recent_slide_dirs = []
        for i in range(0, self.cmbSlideDirectory.count()):
            recent_slide_dirs.append(unicode(self.cmbSlideDirectory.itemText(i)))

        settings.store_recent_files(recent_rendered_videos, recent_slide_videos, recent_slide_dirs)

    def _load_settings(self):
        recent_rendered_videos, recent_slide_videos, recent_slide_dirs = settings.load_recent_files()
        for i in range(0, len(recent_rendered_videos)):
            self.cmbRenderedVideo.insertItem(i, recent_rendered_videos[i])

        for i in range(0, len(recent_slide_videos)):
                    self.cmbSlideVideo.insertItem(i, recent_slide_videos[i])

        for i in range(0, len(recent_slide_dirs)):
                    self.cmbSlideDirectory.insertItem(i, recent_slide_dirs[i])
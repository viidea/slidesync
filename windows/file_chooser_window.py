from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QDialogButtonBox, QMessageBox
from ui import file_chooser_dialog
from video import VideoFile, VideoLoadException
from windows.load_video_window import LoadVideoWindow

class FileChooserWindow(QtGui.QDialog, file_chooser_dialog.Ui_Dialog):
    _original_video = None
    _slide_video = None
    _slide_dir = None
    _cropbox = None

    def __init__(self, parent):
        super(QtGui.QDialog, self).__init__(parent)
        self.setupUi(self)
        self.btnSlideVideo.clicked.connect(self._select_slide_video)
        self.btnOriginalVideo.clicked.connect(self._select_original_video)
        self.btnSlideDir.clicked.connect(self._select_slide_directory)
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)

    def _select_slide_video(self):
        filename = QtGui.QFileDialog(self).getOpenFileName(self, "Open slide video file", QtCore.QDir().homePath())
        if filename == "":
            return      # User canceled the dialog
        filename = unicode(filename)

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

        self.edtSlideVideo.setText(filename)
        self._slide_video = filename
        self._check_values()

    def _select_slide_directory(self):
        dirname = QtGui.QFileDialog().getExistingDirectory(self, "Open slide directory", QtCore.QDir().homePath())
        if dirname == "":
            return
        dirname = unicode(dirname)  # Convert from QString to unicode string
        self.edtSlideDir.setText(dirname)
        self._slide_dir = dirname
        self._check_values()

    def _select_original_video(self):
        filename = QtGui.QFileDialog(self).getOpenFileName(self, "Open original video file", QtCore.QDir().homePath())
        if filename == "":
            return      # User canceled the dialog
        filename = unicode(filename)
        self.edtOriginalVideo.setText(filename)
        self._original_video = filename
        self._check_values()

    def _check_values(self):
        if self._original_video is not None and self._slide_video is not None and self._slide_dir is not None:
            self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)

    def getFiles(self):
        return self._original_video, self._slide_video, self._slide_dir

    def getSlideCropBox(self):
        return self._cropbox

from PyQt4 import QtGui, QtCore
from processing.slide_syncer import SlideSyncer
from ui import progress_window

class SyncWindow(QtGui.QDialog, progress_window.Ui_Dialog):

    def __init__(self, owner, app, original_video, camera_file, slide_data):
        super(QtGui.QDialog, self).__init__(owner)
        self._camera_video = camera_file
        self._original_video = original_video
        self._slide_data = slide_data
        self._app = app
        self.setupUi(self)
        self.setWindowTitle("Syncing videos...")
        self.lblInfo.setText("Syncing videos...")

    def process(self):

        self.close()

    def _update_progress(self, value, min = 0, max = 100):
        if self.prgProgress.minimum() != min:
            self.prgProgress.setMinimum(min)
        if self.prgProgress.maximum() != max:
            self.prgProgress.setMaximum(max)
        self.prgProgress.setValue(value)
        self._app.processEvents()

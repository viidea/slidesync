import os
from PyQt4 import QtGui, uic, QtCore
from PyQt4.QtCore import Qt
from processing.slide_syncer import SlideSyncer
from processing.utils import package_slides

form_class, _ = uic.loadUiType("ui/progress_window.ui")
class SyncWindow(QtGui.QDialog, form_class):

    def __init__(self, owner, app, camera_file, slide_data):
        super(QtGui.QDialog, self).__init__(owner)
        self._camera_video = camera_file
        self._slide_data = slide_data
        self._app = app
        self.setupUi(self)
        self.setWindowTitle("Syncing videos...")
        self.lblInfo.setText("Syncing videos...")

    def process(self):
        self._original_video = QtGui.QFileDialog().getOpenFileName(self, "Open original video", QtCore.QDir().homePath())
        if self._original_video == "":
            return

        slide_syncer = SlideSyncer(unicode(self._original_video), self._camera_video)
        self.timings = slide_syncer.get_synced_timings(self._slide_data)
        self.close()

    def _update_progress(self, value, min = 0, max = 100):
        if self.prgProgress.minimum() != min:
            self.prgProgress.setMinimum(min)
        if self.prgProgress.maximum() != max:
            self.prgProgress.setMaximum(max)
        self.prgProgress.setValue(value)
        self._app.processEvents()

from PyQt4 import QtGui
from PyQt4.QtCore import QThread, pyqtSlot, pyqtSignal
from processing.slide_matcher import SlideMatcher
from ui import progress_window

class MatchWindow(progress_window.Ui_Dialog, QtGui.QDialog):

    class WorkerThread(QThread):
        done = False
        matches = None

        progress_signal = pyqtSignal(int, int, int)

        def __init__(self, video_slides, slides, parent=None, progress_slot = None):
            super(QThread, self).__init__(parent)
            self._video_slides = video_slides
            self._slides = slides

            if not progress_slot is None:
                self.progress_signal.connect(progress_slot)

        def run(self):
            matcher = SlideMatcher(self._video_slides, self._slides, progress_cb=self._update_progress)
            self.matches = matcher.match_slides()
            self.done = True

        def _update_progress(self, value, min = 0, max = 100):
            self.progress_signal.emit(value, min, max)

        def __del__(self):
            self.wait()

    def __init__(self, owner, app, slides, video_frames):
        super(QtGui.QDialog, self).__init__(owner)

        self._slides = slides
        self._video_slides = video_frames
        self._app = app
        self.setupUi(self)

    def process(self):
        thread = self.WorkerThread(self._video_slides, self._slides, progress_slot=self._update_progress, parent=self)
        thread.start()

        while not thread.done:
            self._app.processEvents()

        self.matches = thread.matches
        self.close()

    @pyqtSlot(int, int, int)
    def _update_progress(self, value, min = 0, max = 100):
        if self.prgProgress.minimum() != min:
            self.prgProgress.setMinimum(min)
        if self.prgProgress.maximum() != max:
            self.prgProgress.setMaximum(max)

        self.prgProgress.setValue(value)
        self._app.processEvents()
from PyQt4 import QtGui
from processing.slide_matcher import SlideMatcher
from ui import progress_window

class MatchWindow(progress_window.Ui_Dialog, QtGui.QDialog):

    def __init__(self, owner, app, slides, video_frames):
        super(QtGui.QDialog, self).__init__(owner)

        self._slides = slides
        self._video_slides = video_frames
        self._app = app
        self.setupUi(self)

    def process(self):
        matcher = SlideMatcher(self._video_slides,
                               self._slides,
                               progress_cb=self._update_progress)
        self.matches = matcher.match_slides()
        self.close()

    def _update_progress(self, value, min = 0, max = 100):
        if self.prgProgress.minimum() != min:
            self.prgProgress.setMinimum(min)
        if self.prgProgress.maximum() != max:
            self.prgProgress.setMaximum(max)

        self.prgProgress.setValue(value)
        self._app.processEvents()
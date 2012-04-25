from PyQt4 import uic, QtGui
from processing.slide_matcher import SlideMatcher

form_class, _ = uic.loadUiType("ui/match_window.ui")
class MatchWindow(form_class, QtGui.QDialog):

    def __init__(self, owner, app, slides, video_frames):
        super(QtGui.QDialog, self).__init__(owner)

        self._slides = slides
        self._video_slides = video_frames
        self._app = app
        self.setupUi(self)

    def _process(self):
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

    def showEvent(self, QShowEvent):
        super(QtGui.QDialog, self).showEvent(QShowEvent)
        self._process()
from PyQt4 import QtGui, uic
from PyQt4.QtGui import QLabel
from processing.slide_extractor import SlideExtractor

form_class, _ = uic.loadUiType("ui/extract_dialog.ui")
class ExtractWindow(form_class, QtGui.QDialog):
    _treshold = 10

    def __init__(self, parent, video, crop_box):
        super(QtGui.QDialog, self).__init__(parent)
        self._video = video
        self._crop_box = crop_box
        self.setupUi(self)
        self.prgProgress.setVisible(False)
        self.btnExtract.pressed.connect(self._extract)
        self._update_treshold_label()
        self.sldTreshold.valueChanged.connect(self._update_treshold_label)

    def _extract(self):
        self.prgProgress.setVisible(True)
        self.btnExtract.setEnabled(False)
        extractor = SlideExtractor(self._video,
                                   cropbox=self._crop_box,
                                   grayscale=False,
                                   callback=self._update_progress,
                                   treshold=self._treshold)
        self.video_slides = extractor.extract_slides()
        self.close()

    def _update_progress(self, value, min = 0.0, max = 1.0):
        if self.prgProgress.minimum() != min:
            self.prgProgress.setMinimum(min)
        if self.prgProgress.maximum() != max:
            self.prgProgress.setMaximum(max)

        self.prgProgress.setValue(value)
        self.app.processEvents()

    def _update_treshold_label(self):
        self._treshold = self.sldTreshold.value()
        self.lblTresh.setText(str(self._treshold))
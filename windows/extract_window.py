from PyQt4 import QtGui
from processing.slide_extractor import SlideExtractor
from ui import extract_dialog

class ExtractWindow(extract_dialog.Ui_dlgExtract, QtGui.QDialog):
    _treshold = 10

    def __init__(self, parent, video, crop_box, app = None):
        super(QtGui.QDialog, self).__init__(parent)
        self._video = video
        self._crop_box = crop_box
        self._app = app
        self.setupUi(self)
        self.prgProgress.setVisible(False)
        self.sldTreshold.setEnabled(True)
        self.btnExtract.pressed.connect(self._extract)
        self._update_treshold_label()
        self.sldTreshold.valueChanged.connect(self._update_treshold_label)

    def _extract(self):
        self.sldTreshold.setEnabled(False)
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

        if self._app is not None:
            self._app.processEvents()

    def _update_treshold_label(self):
        self._treshold = self.sldTreshold.value()
        self.lblTresh.setText(str(self._treshold))
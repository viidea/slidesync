from PyQt4 import QtGui, uic
from load_video_window import LoadVideoWindow

form_class, base_class = uic.loadUiType("ui/main_window.ui")
class MainWindow(form_class, base_class):
    # State data
    _video = None
    _slide_crop_box = None      # Crop box for slide video

    def __init__(self, owner):
        super(base_class, self).__init__()
        self.setupUi(self)
        self.btnStart.pressed.connect(self._start)

    def _start(self):
        self.btnStart.setEnabled(False)
        self._label_set_bold(self.lblLoadSlideVideo, True)
        load_video_win = LoadVideoWindow(self)
        load_video_win.exec_()
        self._video = load_video_win.video
        self._slide_crop_box = load_video_win.selected
        self._label_set_bold(self.lblLoadSlideVideo, False)


    def _label_set_bold(self, label, bold=True):
        font = label.font()
        font.setBold(bold)
        label.setFont(font)
from PyQt4 import QtGui
from PyQt4.QtGui import QImage

class VideoView(object):
    def __init__(self, target_widget):
        self.target = target_widget


    def show_frame(self, video_frame):
        assert video_frame.format == "RGB"
        image = QImage(video_frame.data, video_frame.width, video_frame.height, QImage.Format_RGB888)
        self.target.setPixmap(QtGui.QPixmap.fromImage(image))

from PyQt4 import QtGui
from PyQt4.QtGui import QImage, QLabel

class VideoView(QLabel):
    _current_image = None        # Used for resizing
    _selection_box = None        # Relative box to draw on widget
    _selection_in_progress = False
    selected_box = None         # Absolute box in frame coordinates

    def __init__(self, selectable=False):
        super(QLabel, self).__init__()
        self.selectable = selectable
        self.sizePolicy().setHeightForWidth(True)

        self.pen = QtGui.QPen(QtGui.QColor(255, 0, 0))
        self.pen.setWidth(3)

    def show_frame(self, video_frame):
        assert video_frame.format == "RGB"
        self._current_image = QImage(video_frame.data, video_frame.width, video_frame.height, QImage.Format_RGB888)
        self.update()

    def mousePressEvent(self, QMouseEvent):
        if self._current_image is not None and self.selectable and not self._selection_in_progress:
            self._selection_in_progress = True
            self._selection_box = (QMouseEvent.x(), QMouseEvent.y(), QMouseEvent.x(), QMouseEvent.y())

    def mouseMoveEvent(self, QMouseEvent):
        if self._selection_in_progress:
            sx, sy, ex, ey = self._selection_box
            self._selection_box = (sx, sy, QMouseEvent.x(), QMouseEvent.y())
            self.update()

            print self._selection_box

    def mouseReleaseEvent(self, QMouseEvent):
        if self._selection_in_progress:
            sx, sy, ex, ey = self._selection_box
            self._selection_box = (sx, sy, QMouseEvent.x(), QMouseEvent.y())
            self._selection_in_progress = False
            sx, sy, ex, ey = self._selection_box
            # Swap variables to get nice box
            if sx > ex: sx, ex = ex, sx
            if sy > ey: sy, ey = ey, sy

            self.selected_box = (self._translate_coordinate(sx, self.width(), self._current_image.width()),
                                 self._translate_coordinate(sy, self.height(), self._current_image.height()),
                                 self._translate_coordinate(ex, self.width(), self._current_image.width()),
                                 self._translate_coordinate(ey, self.height(), self._current_image.height()))


    def resizeEvent(self, resize_event):
        super(QLabel, self).resizeEvent(resize_event)
        if resize_event.oldSize() != resize_event.size():
            self._selection_box = None
            self.selected_box = None
            self._selection_in_progress = False
            self.update()

    def heightForWidth(self, width):
        if self._current_image is None:
            return width

        height = int(float(self._current_image.height()) / float(self._current_image.width()) * width)
        return height

    def update(self):
        super(QLabel, self).update()

        if self._current_image is not None:
            pixmap = QtGui.QPixmap.fromImage(self._current_image.scaledToWidth(self.width()))
            self.setPixmap(pixmap)
            if self._selection_box is not None:
                painter = QtGui.QPainter(self.pixmap())
                painter.setPen(self.pen)
                sx, sy, ex, ey = self._selection_box
                painter.drawRect(sx, sy, ex, ey)
                painter.end()

    def _translate_coordinate(self, coordinate, current_max, original_max):
        return int((float(coordinate) / float(current_max)) * original_max)

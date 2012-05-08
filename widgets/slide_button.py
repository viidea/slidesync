from PyQt4 import QtGui, QtCore

class SlideButton(QtGui.QLabel, object):
    image_path = None
    selected = False
    disabled = False
    _image = None

    def __init__(self, time=None, image_file=None, parent=None, selectable=False, selected_callback=None, num=None):
        super(SlideButton, self).__init__(parent)
        self.time = time
        self._num = num
        self.selectable = selectable
        self.selected_callback = selected_callback

        # Drawable caches
        self.font = QtGui.QFont()
        self.font.setPointSize(20)
        self.font.setBold(True)

        self.pen = QtGui.QPen(QtGui.QColor(255, 0, 0))
        self.pen.setWidth(5)
        self.box_pen = QtGui.QPen(QtGui.QColor(0, 0, 0))
        self.box_pen.setWidth(2)

        self.disabled_pen = QtGui.QPen(QtGui.QColor(255, 255, 255, 200))
        self.disabled_pen.setWidth(1)
        self.white_brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 200))

        if image_file is not None:
            self.image_path = image_file
            self._image = QtGui.QPixmap(image_file)

        size_policy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
        size_policy.setHeightForWidth(True)
        self.setSizePolicy(size_policy)

    def sizeHint(self):
        return QtCore.QSize(200, self.heightForWidth(200))

    def resizeEvent(self, QResizeEvent):
        super(QtGui.QLabel, self).resizeEvent(QResizeEvent)
        self.update()

    def mouseReleaseEvent(self, QMouseEvent):
        if self.selectable:
            self.selected = not self.selected
            self.update()
            
        if self.selected_callback is not None:
            self.selected_callback(self)

    def update(self):
        super(SlideButton, self).update()
        if self._image is not None:
            self.setPixmap(self._image.scaledToWidth(self.width(), mode=QtCore.Qt.SmoothTransformation))

        painter = None
        if self.disabled or self.selected:
            painter = QtGui.QPainter(self.pixmap())

            painter.setPen(self.pen)
            if self.disabled:
                painter.setBrush(self.white_brush)
                painter.setPen(self.disabled_pen)
                painter.drawRect(0, 0, self.width(), self.heightForWidth(self.width()))
            if self.selected:
                painter.drawRect(2, 2, self.width() - 4, self.heightForWidth(self.width()) - 4)

        if self._num is not None:
            if painter is None:
                painter = QtGui.QPainter(self.pixmap())

            painter.setBrush(self.white_brush)
            painter.setPen(self.box_pen)
            metrics = QtGui.QFontMetrics(self.font)

            if not self.disabled:
                text = str(self._num)
            else:
                text = "XX"

            painter.drawRect(8, 8, 4 + metrics.width(text), 4 + metrics.height())

            if not self.disabled:
                painter.setPen(self.pen)
            painter.setFont(self.font)
            painter.drawText(QtCore.QPoint(10, 6 + metrics.height()), text)


    def heightForWidth(self, width):
        if self._image is None:
            return width

        height = int(float(self._image.height()) / float(self._image.width()) * width)
        return height

    def disable(self):
        self.disabled = True
        self._num_text = QtGui.QStaticText("XX")
        self.update()

    def enable(self):
        self.disabled = False
        self.update()

    def select(self):
        self.selected = True
        self.update()

    def deselect(self):
        self.selected = False
        self.update()

    def setImage(self, image):
        self.image_path = image
        self._image = QtGui.QPixmap(image)
        self.update()

    def _get_num(self):
        return self._num

    def _set_num(self, num):
        self._num = num

    num = property(_get_num, _set_num)

    def __str__(self):
        return "[%s]: %s" % (self.time, self.image_path)

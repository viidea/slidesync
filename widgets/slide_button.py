from PyQt4 import QtGui, QtCore

class SlideButton(QtGui.QLabel):
    image = None
    selected = False
    disabled = True

    def __init__(self, time=None, image_file=None, parent=None, selectable=False, selected_callback=None):
        super(SlideButton, self).__init__(parent)
        self.time = time
        self.selectable = selectable
        self.selected_callback = selected_callback

        # Drawable caches
        self.pen = QtGui.QPen(QtGui.QColor(255, 0, 0))
        self.pen.setWidth(5)
        self.font = QtGui.QFont()
        self.font.setPixelSize(24)
        self.font.setBold(True)
        self.disabled_text = QtGui.QStaticText("X")

        if image_file is not None:
            self.image = QtGui.QPixmap(image_file)

        size_policy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
        size_policy.setHeightForWidth(True)
        self.setSizePolicy(size_policy)

    def sizeHint(self):
        return QtCore.QSize(250, self.heightForWidth(250))

    def resizeEvent(self, QResizeEvent):
        super(QtGui.QLabel, self).resizeEvent(QResizeEvent)
        self.update()

    def mouseReleaseEvent(self, QMouseEvent):
        if self.selectable:
            self.selected = not self.selected
            self.update()
            
            if self.selected and self.selected_callback is not None:
                self.selected_callback(self.time)

    def update(self):
        super(SlideButton, self).update()
        if self.image is not None:
            self.setPixmap(self.image.scaledToWidth(self.width(), mode=QtCore.Qt.SmoothTransformation))

        if self.disabled or self.selected:
            painter = QtGui.QPainter(self.pixmap())
            painter.setPen(self.pen)
            if self.disabled:
                painter.setFont(self.font)
                painter.drawStaticText(10, 10, self.disabled_text)
            if self.selected:
                painter.drawRect(2, 2, self.width() - 4, self.height() - 4)
            painter.end()


    def heightForWidth(self, width):
        if self.image is None:
            return width

        height = int(float(self.image.height()) / float(self.image.width()) * width)
        return height

    def disable(self):
        self.disabled = True
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
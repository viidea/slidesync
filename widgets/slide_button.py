from PyQt4 import QtGui, QtCore

class SlideButton(QtGui.QLabel):
    image = None

    def __init__(self, image_file=None, parent=None):

        super(SlideButton, self).__init__(parent)

        if image_file is not None:
            self.image = QtGui.QPixmap(image_file)
            self.update()

        size_policy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Expanding)
        size_policy.setHeightForWidth(True)
        self.setSizePolicy(size_policy)

    def sizeHint(self):
        return QtCore.QSize(50, self.heightForWidth(50))

    def resizeEvent(self, QResizeEvent):
        super(QtGui.QLabel, self).resizeEvent(QResizeEvent)
        if QResizeEvent.oldSize() != QResizeEvent.size():
            self.update()

    def update(self):
        super(SlideButton, self).update()
        if self.image is not None:
            self.setPixmap(self.image.scaledToWidth(self.width()))

    def heightForWidth(self, width):
        if self.image is None:
            return width

        height = int(float(self.image.height()) / float(self.image.width()) * width)
        return height
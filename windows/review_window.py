from PyQt4 import QtGui

class ReviewWindow(QtGui.QDialog):

    def __init__(self, owner, slides, video_slides, matches):
        super(QtGui.QDialog, self).__init__(owner)
        self._slides = slides
        self._video_slides = video_slides
        self._matches = matches

        self._build_ui()


    def _build_ui(self):
        self.setGeometry(600, 400, 100, 100)



from PyQt4 import QtGui, uic

form_class, base_class = uic.loadUiType("ui/main_window.ui")
class MainWindow(form_class, base_class):
    def __init__(self, owner):
        super(base_class, self).__init__()
        self.setupUi(self)



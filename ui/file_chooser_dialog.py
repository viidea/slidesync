# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'file_chooser_dialog.ui'
#
# Created: Tue May  8 11:23:32 2012
#      by: PyQt4 UI code generator 4.8.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(600, 300)
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Enter required files", None, QtGui.QApplication.UnicodeUTF8))
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setMinimumSize(QtCore.QSize(110, 0))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Slide video:", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.edtSlideVideo = QtGui.QLineEdit(Dialog)
        self.edtSlideVideo.setEnabled(False)
        self.edtSlideVideo.setObjectName(_fromUtf8("edtSlideVideo"))
        self.horizontalLayout.addWidget(self.edtSlideVideo)
        self.btnSlideVideo = QtGui.QPushButton(Dialog)
        self.btnSlideVideo.setText(QtGui.QApplication.translate("Dialog", "Browse...", None, QtGui.QApplication.UnicodeUTF8))
        self.btnSlideVideo.setObjectName(_fromUtf8("btnSlideVideo"))
        self.horizontalLayout.addWidget(self.btnSlideVideo)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setMinimumSize(QtCore.QSize(110, 0))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "Slide dir:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_2.addWidget(self.label_2)
        self.edtSlideDir = QtGui.QLineEdit(Dialog)
        self.edtSlideDir.setEnabled(False)
        self.edtSlideDir.setObjectName(_fromUtf8("edtSlideDir"))
        self.horizontalLayout_2.addWidget(self.edtSlideDir)
        self.btnSlideDir = QtGui.QPushButton(Dialog)
        self.btnSlideDir.setText(QtGui.QApplication.translate("Dialog", "Browse...", None, QtGui.QApplication.UnicodeUTF8))
        self.btnSlideDir.setObjectName(_fromUtf8("btnSlideDir"))
        self.horizontalLayout_2.addWidget(self.btnSlideDir)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setMinimumSize(QtCore.QSize(110, 0))
        self.label_3.setText(QtGui.QApplication.translate("Dialog", "Rendered video:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_3.addWidget(self.label_3)
        self.edtOriginalVideo = QtGui.QLineEdit(Dialog)
        self.edtOriginalVideo.setEnabled(False)
        self.edtOriginalVideo.setObjectName(_fromUtf8("edtOriginalVideo"))
        self.horizontalLayout_3.addWidget(self.edtOriginalVideo)
        self.btnOriginalVideo = QtGui.QPushButton(Dialog)
        self.btnOriginalVideo.setText(QtGui.QApplication.translate("Dialog", "Browse...", None, QtGui.QApplication.UnicodeUTF8))
        self.btnOriginalVideo.setObjectName(_fromUtf8("btnOriginalVideo"))
        self.horizontalLayout_3.addWidget(self.btnOriginalVideo)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        pass


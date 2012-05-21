# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'file_chooser_dialog.ui'
#
# Created: Mon May 21 12:11:22 2012
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
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setMinimumSize(QtCore.QSize(110, 0))
        self.label_3.setText(QtGui.QApplication.translate("Dialog", "Rendered video:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_3.addWidget(self.label_3)
        self.cmbRenderedVideo = QtGui.QComboBox(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbRenderedVideo.sizePolicy().hasHeightForWidth())
        self.cmbRenderedVideo.setSizePolicy(sizePolicy)
        self.cmbRenderedVideo.setEditable(True)
        self.cmbRenderedVideo.setMaxCount(5)
        self.cmbRenderedVideo.setInsertPolicy(QtGui.QComboBox.InsertAtTop)
        self.cmbRenderedVideo.setObjectName(_fromUtf8("cmbRenderedVideo"))
        self.horizontalLayout_3.addWidget(self.cmbRenderedVideo)
        self.btnOriginalVideo = QtGui.QPushButton(Dialog)
        self.btnOriginalVideo.setText(QtGui.QApplication.translate("Dialog", "Browse...", None, QtGui.QApplication.UnicodeUTF8))
        self.btnOriginalVideo.setObjectName(_fromUtf8("btnOriginalVideo"))
        self.horizontalLayout_3.addWidget(self.btnOriginalVideo)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setMinimumSize(QtCore.QSize(110, 0))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Slide video:", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.cmbSlideVideo = QtGui.QComboBox(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbSlideVideo.sizePolicy().hasHeightForWidth())
        self.cmbSlideVideo.setSizePolicy(sizePolicy)
        self.cmbSlideVideo.setEditable(True)
        self.cmbSlideVideo.setMaxCount(5)
        self.cmbSlideVideo.setInsertPolicy(QtGui.QComboBox.InsertAtTop)
        self.cmbSlideVideo.setObjectName(_fromUtf8("cmbSlideVideo"))
        self.horizontalLayout.addWidget(self.cmbSlideVideo)
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
        self.cmbSlideDirectory = QtGui.QComboBox(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbSlideDirectory.sizePolicy().hasHeightForWidth())
        self.cmbSlideDirectory.setSizePolicy(sizePolicy)
        self.cmbSlideDirectory.setEditable(True)
        self.cmbSlideDirectory.setMaxCount(5)
        self.cmbSlideDirectory.setInsertPolicy(QtGui.QComboBox.InsertAtTop)
        self.cmbSlideDirectory.setObjectName(_fromUtf8("cmbSlideDirectory"))
        self.horizontalLayout_2.addWidget(self.cmbSlideDirectory)
        self.btnSlideDir = QtGui.QPushButton(Dialog)
        self.btnSlideDir.setText(QtGui.QApplication.translate("Dialog", "Browse...", None, QtGui.QApplication.UnicodeUTF8))
        self.btnSlideDir.setObjectName(_fromUtf8("btnSlideDir"))
        self.horizontalLayout_2.addWidget(self.btnSlideDir)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
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


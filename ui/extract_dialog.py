# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'extract_dialog.ui'
#
# Created: Mon May 07 10:34:37 2012
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_dlgExtract(object):
    def setupUi(self, dlgExtract):
        dlgExtract.setObjectName(_fromUtf8("dlgExtract"))
        dlgExtract.resize(568, 170)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(dlgExtract.sizePolicy().hasHeightForWidth())
        dlgExtract.setSizePolicy(sizePolicy)
        dlgExtract.setSizeGripEnabled(False)
        self.gridLayout = QtGui.QGridLayout(dlgExtract)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.lblDesc = QtGui.QLabel(dlgExtract)
        self.lblDesc.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblDesc.setObjectName(_fromUtf8("lblDesc"))
        self.horizontalLayout.addWidget(self.lblDesc)
        self.lblTresh = QtGui.QLabel(dlgExtract)
        self.lblTresh.setObjectName(_fromUtf8("lblTresh"))
        self.horizontalLayout.addWidget(self.lblTresh)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.sldTreshold = QtGui.QSlider(dlgExtract)
        self.sldTreshold.setMinimum(1)
        self.sldTreshold.setSliderPosition(10)
        self.sldTreshold.setOrientation(QtCore.Qt.Horizontal)
        self.sldTreshold.setTickPosition(QtGui.QSlider.TicksBelow)
        self.sldTreshold.setTickInterval(10)
        self.sldTreshold.setObjectName(_fromUtf8("sldTreshold"))
        self.verticalLayout.addWidget(self.sldTreshold)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.line = QtGui.QFrame(dlgExtract)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.verticalLayout.addWidget(self.line)
        self.prgProgress = QtGui.QProgressBar(dlgExtract)
        self.prgProgress.setProperty("value", 24)
        self.prgProgress.setObjectName(_fromUtf8("prgProgress"))
        self.verticalLayout.addWidget(self.prgProgress)
        self.btnExtract = QtGui.QPushButton(dlgExtract)
        self.btnExtract.setObjectName(_fromUtf8("btnExtract"))
        self.verticalLayout.addWidget(self.btnExtract)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(dlgExtract)
        QtCore.QMetaObject.connectSlotsByName(dlgExtract)

    def retranslateUi(self, dlgExtract):
        dlgExtract.setWindowTitle(QtGui.QApplication.translate("dlgExtract", "Extract slides from video", None, QtGui.QApplication.UnicodeUTF8))
        self.lblDesc.setText(QtGui.QApplication.translate("dlgExtract", "Image change treshold: ", None, QtGui.QApplication.UnicodeUTF8))
        self.lblTresh.setText(QtGui.QApplication.translate("dlgExtract", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.btnExtract.setText(QtGui.QApplication.translate("dlgExtract", "Extract", None, QtGui.QApplication.UnicodeUTF8))


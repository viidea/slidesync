# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'review_window.ui'
#
# Created: Tue May  8 16:17:10 2012
#      by: PyQt4 UI code generator 4.8.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_mwReview(object):
    def setupUi(self, mwReview):
        mwReview.setObjectName(_fromUtf8("mwReview"))
        mwReview.resize(1200, 860)
        mwReview.setWindowTitle(QtGui.QApplication.translate("mwReview", "Review slide matches", None, QtGui.QApplication.UnicodeUTF8))
        self.centralwidget = QtGui.QWidget(mwReview)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setText(QtGui.QApplication.translate("mwReview", "Matches", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout_2.addWidget(self.label)
        self.scrMatches = QtGui.QScrollArea(self.centralwidget)
        self.scrMatches.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrMatches.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrMatches.setWidgetResizable(True)
        self.scrMatches.setObjectName(_fromUtf8("scrMatches"))
        self.scrollAreaWidgetContents_2 = QtGui.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 870, 815))
        self.scrollAreaWidgetContents_2.setObjectName(_fromUtf8("scrollAreaWidgetContents_2"))
        self.scrMatches.setWidget(self.scrollAreaWidgetContents_2)
        self.verticalLayout_2.addWidget(self.scrMatches)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.lblSlides = QtGui.QLabel(self.centralwidget)
        self.lblSlides.setMaximumSize(QtCore.QSize(16777215, 30))
        self.lblSlides.setText(QtGui.QApplication.translate("mwReview", "Slides", None, QtGui.QApplication.UnicodeUTF8))
        self.lblSlides.setObjectName(_fromUtf8("lblSlides"))
        self.verticalLayout.addWidget(self.lblSlides)
        self.scrSlides = QtGui.QScrollArea(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrSlides.sizePolicy().hasHeightForWidth())
        self.scrSlides.setSizePolicy(sizePolicy)
        self.scrSlides.setMinimumSize(QtCore.QSize(300, 0))
        self.scrSlides.setMaximumSize(QtCore.QSize(300, 16777215))
        self.scrSlides.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrSlides.setWidgetResizable(True)
        self.scrSlides.setObjectName(_fromUtf8("scrSlides"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 298, 782))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.scrSlides.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrSlides)
        self.btnDone = QtGui.QPushButton(self.centralwidget)
        self.btnDone.setText(QtGui.QApplication.translate("mwReview", "Done", None, QtGui.QApplication.UnicodeUTF8))
        self.btnDone.setObjectName(_fromUtf8("btnDone"))
        self.verticalLayout.addWidget(self.btnDone)
        self.horizontalLayout.addLayout(self.verticalLayout)
        mwReview.setCentralWidget(self.centralwidget)

        self.retranslateUi(mwReview)
        QtCore.QMetaObject.connectSlotsByName(mwReview)

    def retranslateUi(self, mwReview):
        pass


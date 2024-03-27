# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ItemSkzMTv.ui'
##
## Created by: Qt User Interface Compiler version 5.14.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
    QRect, QSize, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap, QImage,
    QRadialGradient)
from PySide2.QtWidgets import *


class ItemObject(object):
    def __init__(self, **kwargs):
        # self.playlist_name = kwargs.get('playlist_name', 'My Playlist Replay')
        self.music = kwargs.get('music', '679 (feat . Morty)')
        self.artist = kwargs.get('artist', 'Fetty Wap')
        self.album = kwargs.get('album', 'Fetty Wap (Deluxe Edition)')
        self.duration = kwargs.get('duration', '3:07')
        self.image = kwargs.get('image', None)

class Item(object):
    def setupUi(self, Form, item_object):
        if Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1160, 55)
        Form.setMaximumSize(QSize(16777215, 55))
        self.item_frame = QFrame(Form)
        self.item_frame.setObjectName(u"item_frame")
        self.item_frame.setGeometry(QRect(0, 0, 1160, 55))
        self.item_frame.setMaximumSize(QSize(16777215, 55))
        self.item_frame.setStyleSheet(u"border-radius: 0px; background-color: transparent")
        self.item_frame.setFrameShape(QFrame.StyledPanel)
        self.item_frame.setFrameShadow(QFrame.Raised)
        self.artist_label = QLabel(self.item_frame)
        self.artist_label.setObjectName(u"artist_label")
        self.artist_label.setGeometry(QRect(529, 17, 151, 16))
        font = QFont()
        font.setFamily(u"SF Pro Text")
        font.setPointSize(9)
        self.artist_label.setFont(font)
        self.artist_label.setStyleSheet(u"color: #7e7e7e")
        
        self.image_label = QLabel(self.item_frame)
        self.image_label.setObjectName(u"image_label")
        self.image_label.setGeometry(QRect(25, 7, 40, 40))
        # self.image_label.setStyleSheet(u"border-radius: 5px")
        # self.image_label.setPixmap(QPixmap(u"./images/hittop.jpg"))
        if item_object.image and not isinstance(item_object.image, str):
            image = QImage()
            image.loadFromData(item_object.image)
            self.image_label.setPixmap(QPixmap(image))
        else:
            self.image_label.setStyleSheet(u"border-radius: 5px")
            if (isinstance(item_object.image, str)):
                self.image_label.setPixmap(QPixmap(item_object.image))
            else:
                self.image_label.setPixmap(QPixmap(u"./music/hittop.jpg"))
        self.image_label.setAlignment(Qt.AlignCenter)
        
        self.image_label.setScaledContents(True)
        self.label_115 = QLabel(self.item_frame)
        self.label_115.setObjectName(u"label_115")
        self.label_115.setGeometry(QRect(498, 20, 12, 10))
        self.label_115.setPixmap(QPixmap(u"./images/e.png"))
        self.label_115.setAlignment(Qt.AlignCenter)
        self.dur_label = QLabel(self.item_frame)
        self.dur_label.setObjectName(u"dur_label")
        self.dur_label.setGeometry(QRect(1105, 17, 55, 16))
        self.dur_label.setFont(font)
        self.dur_label.setStyleSheet(u"color: #7e7e7e")
        self.name_label = QLabel(self.item_frame)
        self.name_label.setObjectName(u"name_label")
        self.name_label.setGeometry(QRect(74, 17, 271, 21))
        font1 = QFont()
        font1.setFamily(u"SF Pro Text")
        font1.setPointSize(10)
        self.name_label.setFont(font1)
        self.name_label.setStyleSheet(u"")
        self.album_label = QLabel(self.item_frame)
        self.album_label.setObjectName(u"album_label")
        self.album_label.setGeometry(QRect(830, 17, 261, 21))
        self.album_label.setFont(font1)
        self.album_label.setStyleSheet(u"color: #7e7e7e")

        self.artist_label.setText(item_object.artist)
        self.image_label.setText("")
        self.label_115.setText("")
        self.dur_label.setText(item_object.duration)
        self.name_label.setText(item_object.music)
        self.album_label.setText(item_object.album)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
    # retranslateUi


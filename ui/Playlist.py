# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'playlistFoIkay.ui'
##
## Created by: Qt User Interface Compiler version 5.14.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
    QRect, QSize, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
    QRadialGradient)
from PySide2.QtWidgets import *

from ui.Item import Item
from ui.Item import ItemObject


class PlaylistObject(object):
    def __init__(self, **kwargs):
        self.playlist_name = kwargs.get('playlist_name', 'My Playlist Replay')
        self.music = kwargs.get('music', '679 (feat . Morty)')
        self.artist = kwargs.get('artist', 'Fetty Wap')
        self.album = kwargs.get('album', 'Fetty Wap (Deluxe Edition)')
        self.duration = kwargs.get('duration', '3:07')
        self.image = kwargs.get('image', None)

class Playlist(object):
    def setupUi(self, Form, playlist_objects):
        if Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1219, 848)
        self.widget = QWidget(Form)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(0, 0, 1219, 848))
        self.navbar_3 = QFrame(self.widget)
        self.navbar_3.setObjectName(u"navbar_3")
        self.navbar_3.setGeometry(QRect(0, 0, 1219, 52))
        self.navbar_3.setStyleSheet(u"background-color: #F4F4F4; \n"
"border-radius: 0px; \n"
"border-top-right-radius: 6px")
        self.navbar_3.setFrameShape(QFrame.StyledPanel)
        self.navbar_3.setFrameShadow(QFrame.Raised)
        self.playlist_6 = QLabel(self.navbar_3)
        self.playlist_6.setObjectName(u"playlist_6")
        self.playlist_6.setGeometry(QRect(568, 17, 55, 16))
        font = QFont()
        font.setFamily(u"SF Pro Display")
        font.setPointSize(10)
        self.playlist_6.setFont(font)
        self.playlist_6.setStyleSheet(u"color: #4A4A4A\n"
"")
        self.imageAlbum_2 = QLabel(self.widget)
        self.imageAlbum_2.setObjectName(u"imageAlbum_2")
        self.imageAlbum_2.setGeometry(QRect(50, 100, 270, 270))
        self.imageAlbum_2.setPixmap(QPixmap(u"./images/Hiphop.png"))
        self.imageAlbum_2.setAlignment(Qt.AlignCenter)
        self.nameAlbum_2 = QLabel(self.widget)
        self.nameAlbum_2.setObjectName(u"nameAlbum_2")
        self.nameAlbum_2.setGeometry(QRect(352, 100, 481, 29))
        font1 = QFont()
        font1.setFamily(u"SF Pro Display")
        font1.setPointSize(16)
        self.nameAlbum_2.setFont(font1)
        self.applemusic_2 = QLabel(self.widget)
        self.applemusic_2.setObjectName(u"applemusic_2")
        self.applemusic_2.setGeometry(QRect(352, 137, 481, 29))
        self.applemusic_2.setFont(font1)
        self.applemusic_2.setStyleSheet(u"color: #F7C74E")
        self.playButton_2 = QPushButton(self.widget)
        self.playButton_2.setObjectName(u"playButton_2")
        self.playButton_2.setGeometry(QRect(352, 322, 153, 28))
        font2 = QFont()
        font2.setFamily(u"SF Pro Display")
        font2.setPointSize(9)
        font2.setBold(True)
        font2.setWeight(75)
        self.playButton_2.setFont(font2)
        self.playButton_2.setStyleSheet(u"border: none;\n"
"border-radius: 3px;\n"
"background-color: #F8C84E;\n"
"color: #fff")
        icon = QIcon()
        icon.addFile(u"./images/play_white.png", QSize(), QIcon.Normal, QIcon.Off)
        self.playButton_2.setIcon(icon)
        self.shuffleButton_2 = QPushButton(self.widget)
        self.shuffleButton_2.setObjectName(u"shuffleButton_2")
        self.shuffleButton_2.setGeometry(QRect(515, 322, 153, 28))
        self.shuffleButton_2.setFont(font2)
        self.shuffleButton_2.setStyleSheet(u"border: none;\n"
"border-radius: 3px;\n"
"background-color: #F8C84E;\n"
"color: #fff")
        icon1 = QIcon()
        icon1.addFile(u"./images/shuffle_white.png", QSize(), QIcon.Normal, QIcon.Off)
        self.shuffleButton_2.setIcon(icon1)
        self.titlebar_3 = QFrame(self.widget)
        self.titlebar_3.setObjectName(u"titlebar_3")
        self.titlebar_3.setGeometry(QRect(98, 409, 1117, 16))
        self.titlebar_3.setFrameShape(QFrame.StyledPanel)
        self.titlebar_3.setFrameShadow(QFrame.Raised)
        self.label_17 = QLabel(self.titlebar_3)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setGeometry(QRect(0, 0, 111, 16))
        self.label_17.setFont(font)
        self.label_17.setStyleSheet(u"color: #808080")
        self.label_18 = QLabel(self.titlebar_3)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setGeometry(QRect(455, 0, 111, 16))
        self.label_18.setFont(font)
        self.label_18.setStyleSheet(u"color: #808080")
        self.label_19 = QLabel(self.titlebar_3)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setGeometry(QRect(755, 0, 111, 16))
        self.label_19.setFont(font)
        self.label_19.setStyleSheet(u"color: #808080")
        self.label_20 = QLabel(self.titlebar_3)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setGeometry(QRect(1031, 0, 111, 16))
        self.label_20.setFont(font)
        self.label_20.setStyleSheet(u"color: #808080")
        self.listWidget_2 = QListWidget(self.widget)
        self.listWidget_2.setObjectName(u"listWidget_2")
        self.listWidget_2.setGeometry(QRect(24, 433, 1160, 400))
        self.listWidget_2.setStyleSheet(u"QListWidget {\n"
"	border: none;\n"
"}\n"
"\n"
"QListWidget:select {\n"
"	background-color: rgb(0, 20, 163)\n"
"}")
        
        newItem = QListWidgetItem()
        newItem.setSizeHint(QSize(0, 55)) 

        songW = QWidget()

        for playlist_object in playlist_objects:
            item_data = {
                'music': playlist_object.music,
                'artist': playlist_object.artist,
                'album': playlist_object.album,
                'duration': playlist_object.duration,
                'image': playlist_object.image
            }

            if playlist_object.music:
                pitem_object = ItemObject(**item_data)

                my_item = Item()
                my_item.setupUi(songW, pitem_object)

                # Tạo một QListWidgetItem mới cho mỗi Item và gắn Item vào nó
                item_widget = QListWidgetItem()
                item_widget.setSizeHint(newItem.sizeHint())  # Đảm bảo kích thước của QListWidgetItem phù hợp với kích thước đã thiết lập
                self.listWidget_2.insertItem(self.listWidget_2.count(), item_widget)
                self.listWidget_2.setItemWidget(item_widget, my_item.item_frame)
                self.listWidget_2.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
                self.listWidget_2.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.playlist_6.setText(QCoreApplication.translate("Form", u"Playlist", None))
        self.imageAlbum_2.setText("")
        self.nameAlbum_2.setText(QCoreApplication.translate("Form", u"My Playlist Replay", None))
        self.applemusic_2.setText(QCoreApplication.translate("Form", u"Apple Music My Playlist", None))
        self.playButton_2.setText(QCoreApplication.translate("Form", u"Play", None))
        self.shuffleButton_2.setText(QCoreApplication.translate("Form", u"Add", None))
        self.label_17.setText(QCoreApplication.translate("Form", u"SONG", None))
        self.label_18.setText(QCoreApplication.translate("Form", u"ARTIST", None))
        self.label_19.setText(QCoreApplication.translate("Form", u"ALBUM", None))
        self.label_20.setText(QCoreApplication.translate("Form", u"DUR", None))
    # retranslateUi


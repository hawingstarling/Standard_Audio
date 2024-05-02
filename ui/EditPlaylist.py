# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'designergkNAua.ui'
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
from database.db import connect

class EditPlaylistObject(object):
    def __init__(self, **kwargs):
        self.playlist_id = kwargs.get('playlist_id', '')
        self.playlist_name = kwargs.get('playlist_name', 'My Playlist Replay')

class Ui_MainWindow(object):
    def setupUi(self, MainWindow, playlist_objects):
        if MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(452, 143)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.editPlaylist = QLineEdit(self.centralwidget)
        self.editPlaylist.setObjectName(u"editPlaylist")
        self.editPlaylist.setGeometry(QRect(20, 30, 411, 31))
        self.editPlaylist.setText(playlist_objects.playlist_name)
        self.savePlaylist = QPushButton(self.centralwidget)
        self.savePlaylist.setObjectName(u"savePlaylist")
        self.savePlaylist.setGeometry(QRect(20, 100, 93, 28))
        self.savePlaylist.clicked.connect(lambda: self.UpdatePlaylist(self.editPlaylist.text(), playlist_objects.playlist_id))
        self.deletePlaylist = QPushButton(self.centralwidget)
        self.deletePlaylist.setObjectName(u"deletePlaylist")
        self.deletePlaylist.setGeometry(QRect(133, 100, 93, 28))
        self.deletePlaylist.clicked.connect(lambda: self.DeletePlaylist(playlist_objects.playlist_id))
        MainWindow.setCentralWidget(self.centralwidget)

        self.MainWindow = MainWindow

        self.cursor = None
        self.conn_mysql = None
        
        self.cursor, self.conn_mysql = self.ConnectMySql()

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def ConnectMySql(self):
        cursor, conn_mysql = connect()
        return cursor, conn_mysql
    
    def UpdatePlaylist(self, new_playlist, playlist_id):
        update_playlist = ("UPDATE playlist "
                    "SET PlaylistName = %s "
                    "WHERE PlaylistID = %s")
        
        # Insert new playlist
        self.cursor.execute(update_playlist, (new_playlist, playlist_id))

        # Make sure data is committed to the database
        self.conn_mysql.commit()
        self.MainWindow.hide()

    def DeletePlaylist(self, playlist_id):
        # Xóa tất cả các bài hát từ playlist_song
        delete_playlist_song_query = "DELETE FROM playlist_song WHERE idPlaylist = %s"
        self.cursor.execute(delete_playlist_song_query, (playlist_id,))
        self.conn_mysql.commit()
        print(self.cursor.rowcount, "Deleted records from playlist_song for playlist with id:", playlist_id)

        # Xóa playlist
        delete_playlist_query = "DELETE FROM playlist WHERE PlaylistID = %s"
        self.cursor.execute(delete_playlist_query, (playlist_id,))
        self.conn_mysql.commit()
        print(self.cursor.rowcount, "Records deleted from playlist with id:", playlist_id)

        self.MainWindow.hide()

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.savePlaylist.setText(QCoreApplication.translate("MainWindow", u"Edit", None))
        self.deletePlaylist.setText(QCoreApplication.translate("MainWindow", u"Delete", None))
    # retranslateUi


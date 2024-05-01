from functools import partial
import sys
import random
import platform
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, QEvent, Slot)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient, QIcon)
from PySide2.QtWidgets import *
from PySide2.QtMultimedia import QMediaPlayer, QAudioOutput, QMediaContent
from PySide2.QtCore import QUrl, QTimer
import os
# DURATION
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC
# GUI FILE
from ui.AppleMusic import Ui_MainWindow
from ui.Item import Item
from ui.Item import ItemObject
# CONNECT DB
from database.db import connect
from ui.Playlist import Playlist, PlaylistObject
import requests

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        self.cursor = None
        self.conn_mysql = None

        self.cursor, self.conn_mysql = self.ConnectMySql()

        # Init
        self.current_songs = []
        self.loop_Enable = False
        self.current_volume = 50
        #  Position player 
        self.current_position = 0
        self.isPaused = False

        # Media
        self.player = QMediaPlayer()
        self.player.setVolume(self.current_volume)
        self.timer = QTimer(self)
        self.timer.start(1000)
        self.timer.timeout.connect(self.move_Slider)

        self.audio = QAudioOutput()

        global stopped
        stopped = False

        ## HDI 4K and Hidden Window Flag
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True) #enable highdpi scaling
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True) #use highdpi icons

        ## SCROLL PLAYLIST
        self.scroll_Playlist = QScrollArea(self.sidebar_2)
        self.scroll_Playlist.setObjectName(u"scroll_Playlist")
        self.scroll_Playlist.setGeometry(QRect(10, 340, 200, 300))
        self.scroll_Playlist.setWidgetResizable(True)
        # self.scrollAreaWidgetContents_2 = QWidget()
        # self.scrollAreaWidgetContents_2.setObjectName(u"scrollAreaWidgetContents_2")
        # self.scrollAreaWidgetContents_2.setGeometry(QRect(0, 0, 200, 300))
        # self.scroll_Playlist.setWidget(self.scrollAreaWidgetContents_2)

        self.widget_Playlist = QWidget()
        self.vBox_Playlist = QVBoxLayout()
        self.vBox_Playlist.setObjectName(u"vBox_Playlist")
        self.vBox_Playlist.setContentsMargins(0, 0, 0, 0)
        self.vBox_Playlist.addStretch()
        
        self.widget_Playlist.setLayout(self.vBox_Playlist)
        #Scroll Area Properties
        self.scroll_Playlist.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_Playlist.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_Playlist.setWidgetResizable(True)
        self.scroll_Playlist.setWidget(self.widget_Playlist)

        ## PAGES
        ########################################################################
        self.stackedWidget.setCurrentWidget(self.page_3)
        # PAGE 1
        self.pushButton_ListenNow.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_3))  
        # PAGE 2
        self.pushButton_Favourite.clicked.connect(lambda: (self.stackedWidget.setCurrentWidget(self.page_4), self.GetAllSongs()))
 
        # Style Active Button Menu
        for w in self.AppleMusic_3.findChildren(QPushButton):
            w.clicked.connect(self.applyStyleButton)
        
        # # Connections
        self.songSlider.sliderMoved[int].connect(lambda: self.player.setPosition(self.songSlider.value()))
        self.volumeSlider.sliderMoved[int].connect(lambda: self.volume_Changed())
        self.buttonAddSong.clicked.connect(self.add_Song)
        self.resumeButtonSong.clicked.connect(lambda: self.togglePauseResume(self.listWidget))
        self.nextButtonSong.clicked.connect(lambda: self.next_Song(self.listWidget))
        self.prevButtonSong.clicked.connect(lambda: self.prev_Song(self.listWidget))

        # Media Player Signals
        self.player.stateChanged.connect(self.mediaState_Changed)

        # Media Change
        self.player.mediaStatusChanged.connect(lambda status: self.AutoNextMusic(status, self.listWidget))

        # Add Playlist
        self.buttonAddPlaylist.clicked.connect(self.CreateNewPage)

        # TrafficLight Window
        self.TrafficLight_ED695E_6.clicked.connect(self.close_Window)
        self.TrafficLight_62C554_5.clicked.connect(self.hide_Window)

        # Context Menu Right Click ListWidget
        self.listWidget.installEventFilter(self)

        # Get All Playlists
        self.GetPages()
        self.SpotifyChart()


        ## SHOW ==> MAIN WINDOW
        ########################################################################
        self.show()
        ## ==> END ##

    def SetPixmapFromUrl(self, url, label):
        res = requests.get(url)
        image = QPixmap()
        image.loadFromData(res.content)
        label.setPixmap(image)
        label.setScaledContents(True)  # Cài đặt thuộc tính này để phù hợp với nội dung của QLabel
        label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # Set size policy to expanding

    def SpotifyChart(self):
        # URL của API bạn muốn gọi
        url = 'https://charts-spotify-com-service.spotify.com/public/v0/charts'

        # Gọi API sử dụng phương thức GET
        response = requests.get(url)

        # Kiểm tra xem request có thành công không
        if response.status_code == 200:
            # Xử lý dữ liệu trả về ở đây
            data = response.json()
            
            # Top track
            most_track_0 = data['chartEntryViewResponses'][0]['entries'][0]
            rank_0 = most_track_0['chartEntryData']
            track_0 = most_track_0['trackMetadata']
            self.label_49.setText(str(rank_0['currentRank']))
            self.label_48.setText(track_0['trackName'])
            self.label_44.setText(track_0['artists'][0]['name'])
            self.label_47.setText(str(rank_0['previousRank']))
            self.SetPixmapFromUrl(track_0['displayImageUri'], self.label_45)

            most_track_1 = data['chartEntryViewResponses'][0]['entries'][1]
            rank_1 = most_track_1['chartEntryData']
            track_1 = most_track_1['trackMetadata']
            self.label_55.setText(str(rank_1['currentRank']))
            self.label_54.setText(track_1['trackName'])
            self.label_50.setText(track_1['artists'][0]['name'])
            self.label_53.setText(str(rank_1['previousRank']))
            self.SetPixmapFromUrl(track_1['displayImageUri'], self.label_51)

            most_track_2 = data['chartEntryViewResponses'][0]['entries'][2]
            rank_2 = most_track_2['chartEntryData']
            track_2 = most_track_2['trackMetadata']
            self.label_61.setText(str(rank_2['currentRank']))
            self.label_60.setText(track_2['trackName'])
            self.label_56.setText(track_2['artists'][0]['name'])
            self.label_59.setText(str(rank_2['previousRank']))
            self.SetPixmapFromUrl(track_2['displayImageUri'], self.label_57)

            most_track_3 = data['chartEntryViewResponses'][0]['entries'][3]
            rank_3 = most_track_3['chartEntryData']
            track_3 = most_track_3['trackMetadata']
            self.label_67.setText(str(rank_3['currentRank']))
            self.label_66.setText(track_3['trackName'])
            self.label_62.setText(track_3['artists'][0]['name'])
            self.label_65.setText(str(rank_3['previousRank']))
            self.SetPixmapFromUrl(track_3['displayImageUri'], self.label_63)

            most_track_4 = data['chartEntryViewResponses'][0]['entries'][4]
            rank_4 = most_track_4['chartEntryData']
            track_4 = most_track_4['trackMetadata']
            self.label_73.setText(str(rank_4['currentRank']))
            self.label_72.setText(track_4['trackName'])
            self.label_68.setText(track_4['artists'][0]['name'])
            self.label_71.setText(str(rank_4['previousRank']))
            self.SetPixmapFromUrl(track_4['displayImageUri'], self.label_69)

            most_track_5 = data['chartEntryViewResponses'][0]['entries'][5]
            rank_5 = most_track_5['chartEntryData']
            track_5 = most_track_5['trackMetadata']
            self.label_79.setText(str(rank_5['currentRank']))
            self.label_78.setText(track_5['trackName'])
            self.label_74.setText(track_5['artists'][0]['name'])
            self.label_77.setText(str(rank_5['previousRank']))
            self.SetPixmapFromUrl(track_5['displayImageUri'], self.label_75)

            # Top artist
            most_artist = data['chartEntryViewResponses'][2]['entries'][0]
            artist = most_artist['artistMetadata']
            self.SetPixmapFromUrl(artist['displayImageUri'], self.label_2)
            self.label_16.setText(artist['artistName'])

            most_artist_1 = data['chartEntryViewResponses'][2]['entries'][1]
            artist_1 = most_artist_1['artistMetadata']
            self.SetPixmapFromUrl(artist_1['displayImageUri'], self.label_3)
            self.label_17.setText(artist_1['artistName'])

            most_artist_2 = data['chartEntryViewResponses'][2]['entries'][2]
            artist_2 = most_artist_2['artistMetadata']
            self.SetPixmapFromUrl(artist_2['displayImageUri'], self.label_4)
            self.label_18.setText(artist_2['artistName'])

            most_artist_3 = data['chartEntryViewResponses'][2]['entries'][3]
            artist_3 = most_artist_3['artistMetadata']
            self.SetPixmapFromUrl(artist_3['displayImageUri'], self.label_13)
            self.label_19.setText(artist_3['artistName'])

            most_artist_4 = data['chartEntryViewResponses'][2]['entries'][4]
            artist_4 = most_artist_4['artistMetadata']
            self.SetPixmapFromUrl(artist_4['displayImageUri'], self.label_14)
            self.label_20.setText(artist_4['artistName'])

            most_artist_5 = data['chartEntryViewResponses'][2]['entries'][5]
            artist_5 = most_artist_5['artistMetadata']
            self.SetPixmapFromUrl(artist_5['displayImageUri'], self.label_15)
            self.label_21.setText(artist_5['artistName'])

        else:

            print("Đã có lỗi xảy ra:", response.status_code)

    def eventFilter(self, source, event):
        fontMenu = QFont()
        fontMenu.setFamily(u"SF Pro Display")
        fontMenu.setPointSize(15)
        fontMenu.setWeight(50)
        if event.type() == QEvent.ContextMenu and source is self.listWidget:
            menu = QMenu()
            menu.setFont(fontMenu)
            menu.setWindowFlag(Qt.FramelessWindowHint)
            menu.setAttribute(Qt.WA_TranslucentBackground)
            menu.setWindowOpacity(0.6)
            menu.setStyleSheet("""
                QMenu {
                    width: 200px;
                    border-color: rgba(199, 199, 199, 1);
                    border-style: solid;
                    border-width: 0px;
                    background-color: #F7F7F7;
                    color: #202124;
                    border-radius: 8px;
                    font-family: "SF Pro Display";
                }
                QMenu::item {
                    width: 190px;
                    background-color: transparent;
                    font-size: 18px;
                    padding-left: 10px;
                }
                QMenu::icon {
                    padding-right: 15px;
                }
                QMenu::item:selected {
                    background-color: #3e92f8;
                    color: #fff;
                }
                QMenu::item:selected:disabled {
                    background-color: transparent;
                    color: #202124;
                }

                QMenu::right-arrow {
                    image: url("./images/chevronright.svg")
                }
   
            """)
            menu_1 = menu.addAction("Delete")
            menu_1.setIcon(QIcon("./images/remove.svg"))
            menu_1.triggered.connect(lambda: self.DeleteSong(source.currentItem().data(Qt.UserRole)))

            menu_2 = menu.addMenu("Add to Playlist")
            menu_2.setIcon(QIcon("./images/playlist.svg"))

            playlists = self.GetAllPlaylists()
            for playlist in playlists:
                playlist_id = playlist[0]
                playlist_name = playlist[1]
                print('playlist ', playlist_id)
                action = QAction(QIcon("./images/playlist.svg"), playlist_name, self)
                action.setFont(fontMenu)
                action.setData(playlist_id)
                action.triggered.connect(lambda playlist_id=playlist_id, song_data=source.currentItem().data(Qt.UserRole): self.AddSongToPlaylist(playlist_id, song_data))
                menu_2.addAction(action)

            if menu.exec_(event.globalPos()):
                item = source.itemAt(event.pos())
            return True
        return super().eventFilter(source, event)

    def AddSongToPlaylist(self, idPlaylist, idSong):
        add_playlist_song = ("INSERT INTO playlist_song "
                    "(idPlaylist, idSong) "
                    "VALUES (%(idPlaylist)s, %(idSong)s)")
        data_playlist_song = {
            'idPlaylist': idPlaylist,
            'idSong': idSong,
        }

        # Insert new song
        self.cursor.execute(add_playlist_song, data_playlist_song)

        # Make sure data is committed to the database
        self.conn_mysql.commit()

        print("Play_song Added!!")

    def ConnectMySql(self):
        cursor, conn_mysql = connect()
        return cursor, conn_mysql
    
    def check_singer(self, singer_name):
        query = "SELECT id FROM singer WHERE name = %s"
        self.cursor.execute(query, (singer_name,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            insert_query = "INSERT INTO singer (name) VALUES (%s)"
            self.cursor.execute(insert_query, (singer_name,))
            self.conn_mysql.commit()
            return self.cursor.lastrowid
    
    def check_album(self, album_name):
        query = "SELECT id FROM album WHERE name = %s"
        self.cursor.execute(query, (album_name,))
        result = self.cursor.fetchone()
    
        if result:
            return result[0]
        else:
            insert_query = "INSERT INTO album (name) VALUES (%s)"
            self.cursor.execute(insert_query, (album_name,))
            self.conn_mysql.commit()
            return self.cursor.lastrowid
        
    def GetAllSongs(self):
        self.current_songs = []
        # Double Clicked QListWidget
        self.connect(self.listWidget, QtCore.SIGNAL("itemDoubleClicked(QListWidgetItem *)"), lambda: self.play_Song(self.listWidget))

        self.resumeButtonSong.clicked.disconnect(self.togglePauseResume(self.listWidget))
        self.nextButtonSong.clicked.disconnect(self.next_Song(self.listWidget))
        self.prevButtonSong.clicked.disconnect(self.prev_Song(self.listWidget))

        self.resumeButtonSong.clicked.connect(lambda: self.togglePauseResume(self.listWidget))
        self.nextButtonSong.clicked.connect(lambda: self.next_Song(self.listWidget))
        self.prevButtonSong.clicked.connect(lambda: self.prev_Song(self.listWidget))

        # CONNECTION BUTTONS MUSIC
        # self.songSlider.sliderMoved[int].connect(lambda: self.player.setPosition(self.songSlider.value()))
        # self.volumeSlider.sliderMoved[int].connect(lambda: self.volume_Changed())
        # self.buttonAddSong.clicked.connect(self.add_Song)
        # self.resumeButtonSong.clicked.connect(lambda: self.togglePauseResume(self.listWidget))
        # self.nextButtonSong.clicked.connect(lambda: self.next_Song(self.listWidget))
        # self.prevButtonSong.clicked.connect(lambda: self.prev_Song(self.listWidget))

        query = ("SELECT song.id, song.name, song.link, song.image, song.dur, album.name, singer.name FROM song, album, singer WHERE song.idSinger = singer.id AND song.idAlbum = album.id")
        self.cursor.execute(query)
        songs = self.cursor.fetchall()
        for song in songs:
            song_id = song[0]
            song_name = song[1]
            song_link = song[2]
            song_image = song[3]
            song_dur = song[4]
            album_name = song[5]
            singer_name = song[6]

            self.current_songs.append(song_link)
            # Item data
            item_data = {
                'id': song_id,
                'music': song_name,
                'artist': singer_name,
                'album': album_name,
                'duration': song_dur,
                'image': song_image
            }
            self.add_ItemSong(item_data)

    def DeleteSong(self, song_no):
        delete_playlist_song_query = "DELETE FROM playlist_song WHERE idSong = %s"
        self.cursor.execute(delete_playlist_song_query, (song_no,))
        self.conn_mysql.commit()
        print(self.cursor.rowcount, "Delete record playlist_song.")

        delete_song_query = "DELETE FROM song WHERE id = %s"
        self.cursor.execute(delete_song_query, (song_no,))
        self.conn_mysql.commit()
        print(self.cursor.rowcount, "Records deleted from song with id:", song_no)

        self.UpdateListWidget()

    def UpdateListWidget(self):
        self.listWidget.clear()
        self.GetAllSongs()
            

    def CreateNewSongs(self, name, link, image, dur, singer_name, album_name):
        singer_no = self.check_singer(singer_name)
        album_no = self.check_album(album_name)
        
        add_song = ("INSERT INTO song "
                    "(name, link, image, dur, idSinger, idAlbum) "
                    "VALUES (%(name)s, %(link)s, %(image)s, %(dur)s, %(idSinger)s, %(idAlbum)s)")
        data_song = {
            'name': name,
            'link': link,
            'image': image,
            'dur': dur,
            'idSinger': singer_no,
            'idAlbum': album_no
        }

        # Insert new song
        self.cursor.execute(add_song, data_song)

        # Make sure data is committed to the database
        self.conn_mysql.commit()

        return self.cursor.lastrowid

    def CreateNewPlaylist(self):
        add_playlist = ("INSERT INTO playlist "
                    "(PlaylistName) "
                    "VALUES (%s)")
        
        # Insert new playlist
        self.cursor.execute(add_playlist, ('My Playlist Replay',))

        # Make sure data is committed to the database
        self.conn_mysql.commit()

        while self.vBox_Playlist.count() > 0:
            item = self.vBox_Playlist.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        self.vBox_Playlist.setContentsMargins(0, 0, 0, 0)
        self.vBox_Playlist.addStretch()
        self.GetPages()

    def GetAllPlaylists(self):
        query = """SELECT * FROM playlist"""
        self.cursor.execute(query)
        playlists = self.cursor.fetchall()

        return playlists


    def GetPages(self):
        playlists = self.GetAllPlaylists()

        for playlist in playlists:
            playlist_id = playlist[0]
            playlist_name = playlist[1]

            font = QFont()
            font.setFamily(u"SF Pro Display")
            font.setPointSize(10)

            newPlaylistButton = QPushButton()
            newPlaylistButton.setObjectName(playlist_name)
            newPlaylistButton.setSizeIncrement(QSize(0, 0))
            newPlaylistButton.setBaseSize(QSize(0, 0))
            newPlaylistButton.setFixedSize(200, 28)
            newPlaylistButton.setFont(font)
            newPlaylistButton.setText(playlist_name)
            newPlaylistButton.setCursor(QCursor(Qt.PointingHandCursor))
            newPlaylistButton.setLayoutDirection(Qt.LeftToRight)
            newPlaylistButton.setStyleSheet(u"border-radius: 6px;\n"
            "text-align: left;\n"
            "padding-left: 16px;\n"
            "")
            newIcon = QIcon()
            newIcon.addFile(u"./images/playlist.svg", QSize(), QIcon.Normal, QIcon.Off)
            newPlaylistButton.setIcon(newIcon)
            newPlaylistButton.setIconSize(QSize(16, 16))
            newPlaylistButton.setCheckable(False)
            newPlaylistButton.setAutoDefault(False)
            newPlaylistButton.setFlat(False)

            self.vBox_Playlist.insertWidget(0, newPlaylistButton)

            newPlaylistButton.clicked.connect(self.applyStyleButton)
            # Connect event clicked for newPlaylistButton after init.
            # newPlaylistButton.clicked.connect(lambda: (self.add_Playlist(playlist_id, newPlaylistButton)))
            newPlaylistButton.clicked.connect(lambda playlist_id=playlist_id, newPlaylistButton=newPlaylistButton: self.add_Playlist(playlist_id, newPlaylistButton))
            
    # # FIX
    def add_Playlist(self, playlist_id, newButtonPage): 
        self.current_songs = []

        query = """
            SELECT
                playlist.PlaylistID, 
                playlist.PlaylistName, 
                song.id,
                song.name, 
                song.link, 
                song.image, 
                song.dur, 
                album.name AS album_name, 
                singer.name AS singer_name 
            FROM 
                playlist 
            LEFT JOIN 
                playlist_song ON playlist.PlaylistID = playlist_song.idPlaylist 
            LEFT JOIN 
                song ON playlist_song.idSong = song.id 
            LEFT JOIN 
                singer ON song.idSinger = singer.id 
            LEFT JOIN 
                album ON song.idAlbum = album.id where playlist.PlaylistID = %s;
        """
        self.cursor.execute(query, (playlist_id,))
        playlists = self.cursor.fetchall()

        playlist_objects = []
        # my_playlist = Playlist()

        for playlist in playlists:
            item_data = {
                'playlist_id': playlist[0],
                'playlist_name': playlist[1],
                'id': playlist[2],
                'music': playlist[3],
                'artist': playlist[8],
                'album': playlist[7],
                'duration': playlist[6],
                'image': playlist[5]
            }
            self.current_songs.append(playlist[4])
            item_object = PlaylistObject(**item_data)
            playlist_objects.append(item_object)

            playlist_widget = QWidget()
            my_playlist = Playlist()
            my_playlist.setupUi(playlist_widget, playlist_objects)

            self.resumeButtonSong.clicked.connect(lambda: self.togglePauseResume(my_playlist.listWidget_2))

            self.stackedWidget.addWidget(playlist_widget)
            newButtonPage.clicked.connect(self.stackedWidget.setCurrentWidget(playlist_widget))

        # Double Clicked QListWidget
        self.connect(my_playlist.listWidget_2, QtCore.SIGNAL("itemDoubleClicked(QListWidgetItem *)"), lambda: self.play_Song(my_playlist.listWidget_2))
        # CONNECTION BUTTONS MUSIC
        self.songSlider.sliderMoved[int].connect(lambda: self.player.setPosition(self.songSlider.value()))
        self.volumeSlider.sliderMoved[int].connect(lambda: self.volume_Changed())
        self.nextButtonSong.clicked.connect(lambda: self.next_Song(my_playlist.listWidget_2))
        self.prevButtonSong.clicked.connect(lambda: self.prev_Song(my_playlist.listWidget_2))

    def close_Window(self):
        self.close()
    
    def hide_Window(self):
        # self.hide()
        pass

    def togglePauseResume(self, listWidget):
        self.isPaused = not self.isPaused

        if self.isPaused:
            self.play_Song(listWidget)
        else:
            self.pause_AndUnPause()
    
    def applyStyleButton(self, event):
        sender_button = self.sender()

        # Xóa bỏ thuộc tính styleSheet của các nút không phải là sender_button trong self.AppleMusic_3
        for w in self.AppleMusic_3.findChildren(QPushButton):
            if w.objectName() != self.sender().objectName():
                defaultStyle = w.styleSheet().replace("background-color: #C8C8C8;", "")
                w.setStyleSheet(defaultStyle)

        # Xóa bỏ thuộc tính styleSheet của các nút không phải là sender_button trong self.vBox_Playlist
        for i in range(self.vBox_Playlist.count()):
            widget = self.vBox_Playlist.itemAt(i).widget()
            if isinstance(widget, QPushButton) and w.objectName() != self.sender().objectName():
                defaultStyle = widget.styleSheet().replace("background-color: #C8C8C8;", "")
                widget.setStyleSheet(defaultStyle)

        # Xóa bỏ thuộc tính styleSheet của sender_button
        newStyle = self.sender().styleSheet() + ("background-color: #C8C8C8;")
        sender_button.setStyleSheet(newStyle)
        return
    
    def add_ItemSong(self, item_data):
        newItem = QListWidgetItem()
        newItem.setSizeHint(QSize(0, 55)) 

        songW = QWidget()
        # songW.setStyleSheet(u"border: none")

        item_object = ItemObject(**item_data)

        my_item = Item()
        my_item.setupUi(songW, item_object)

        # Tạo một QListWidgetItem mới cho mỗi Item và gắn Item vào nó
        item_widget = QListWidgetItem()
        item_widget.setData(Qt.UserRole, item_data['id'])
        item_widget.setSizeHint(newItem.sizeHint())  # Đảm bảo kích thước của QListWidgetItem phù hợp với kích thước đã thiết lập
        self.listWidget.insertItem(self.listWidget.count(), item_widget)
        self.listWidget.setItemWidget(item_widget, my_item.item_frame)
        self.listWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.listWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def add_Song(self):
        fileName, _ = QFileDialog.getOpenFileNames(self, caption='Add Song', dir=':\\', filter='Supported Files (*.mp3;*.mprg;*.ogg;*.m4a;*.MP3;*.wma;*.acc;*.amr)')
        if fileName:
            for file in fileName:
                self.current_songs.append(file)
                file_path = os.path.relpath(file, os.getcwd())
                audio = MP3(file, ID3=ID3)
                duration_sec = audio.info.length
                # Chuyển đổi sang định dạng phút:giây
                minutes = int(duration_sec // 60)
                seconds = int(duration_sec % 60)

                tags = audio.tags
                # Lấy tên bài hát và nghệ sĩ từ tag ID3
                name_music = tags.get('TIT2', ['Unknown'])[0]
                artist_music = tags.get('TPE1', ['Unknown'])[0]
                album_music = tags.get('TALB', ['Unknown'])[0]

                # Lấy hình ảnh album từ tag ID3 (nếu có)
                image_data = tags.get('APIC:', None)
                image_path = 'music\hittop.jpg'
                if image_data:
                    image_mime = image_data.mime
                    image_data = image_data.data

                    # Lưu hình ảnh vào thư mục images cùng cấp với file đang chạy
                    current_directory = os.path.dirname(__file__)
                    image_filename = os.path.join(current_directory, 'music', f'{name_music}_{artist_music}.jpg')
                    with open(image_filename, 'wb') as img_file:
                        img_file.write(image_data)

                    # Lấy đường dẫn của hình ảnh
                    image_path = os.path.relpath(image_filename, current_directory)
                    # print("Đường dẫn của hình ảnh:", image_path)
                else:
                    image_mime = None

                # Format lại chuỗi
                duration_str = "{}:{:02d}".format(minutes, seconds)

                song_id = self.CreateNewSongs(name_music, file_path, image_path, duration_str, artist_music, album_music)

                # Item data
                item_data = {
                    'id': song_id,
                    'music': name_music,
                    'artist': artist_music,
                    'album': album_music,
                    'duration': duration_str,
                    'image': image_data
                }
                self.add_ItemSong(item_data)

    def move_Slider(self):
        if stopped:
            return
        else:
            if self.player.state() == QMediaPlayer.PlayingState:
                self.songSlider.setMinimum(0)
                self.songSlider.setMaximum(self.player.duration())
                slider_position = self.player.position()
                self.songSlider.setValue(slider_position)
    
    def shuffle_Song(self):
        random.shuffle(self.current_songs)

    def toggle_Loop(self):
        self.loop_Enable = not self.loop_Enable

    def play_Song(self, listWidget):
        try:
            global stopped
            stopped = False

            current_selection = listWidget.currentRow()
            current_song = self.current_songs[current_selection]
            print('Current Selection -> ', current_selection)
            song_url = QMediaContent(QUrl.fromLocalFile(current_song))
            self.player.setMedia(song_url)

            #  position player 
            self.player.setPosition(self.current_position) 

            self.player.play()
            self.move_Slider()

            current_item = listWidget.item(current_selection)
            current_widget = listWidget.itemWidget(current_item)
            label_namemusic = current_widget.findChild(QLabel, "name_label")
            label_artistmusic = current_widget.findChild(QLabel, "artist_label")
            label_albummusic = current_widget.findChild(QLabel, "album_label")
            label_imagemusic = current_widget.findChild(QLabel, "image_label")
            self.label_24.setPixmap(QPixmap(label_imagemusic.pixmap()))
            self.label_25.setText(label_namemusic.text())
            self.label_26.setText(label_artistmusic.text() + " - " + label_albummusic.text())
        except Exception as e:
            print(f"Play song error: {e}")
        
    def volume_Changed(self):
        try:
            self.current_volume = self.volumeSlider.value()
            self.player.setVolume(self.current_volume)
        except Exception as e:
            print(f"Changing volume error: {e}")
    
    def mediaState_Changed(self, state):
        if self.player.state() == QMediaPlayer.PlayingState:
            icon = QIcon("./images/Resume.svg")
        else:
            icon = QIcon("./images/Pause.png")
        self.resumeButtonSong.setIcon(icon)
    
    def pause_AndUnPause(self):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()
            self.current_position = self.player.position()
        else:
            self.player.play()
    
    def AutoNextMusic(self, status, listWidget):
        if status == QMediaPlayer.EndOfMedia:
            self.next_Song(listWidget)
    
    def next_Song(self, listWidget):
        try:
            print('Click Next_Song')
            current_selection = listWidget.currentRow()

            if current_selection + 1 == len(self.current_songs):
                next_index = 0
            else:
                next_index = current_selection + 1

            current_song = self.current_songs[next_index]
            listWidget.setCurrentRow(next_index)
            song_url = QMediaContent(QUrl.fromLocalFile(current_song))
            self.player.setMedia(song_url)
            self.player.play()
            self.move_Slider()

            # Lấy thông tin của bài hát và gán vào biến label_namemusic
            current_item = listWidget.item(next_index)
            current_widget = listWidget.itemWidget(current_item)
            label_namemusic = current_widget.findChild(QLabel, "name_label")
            label_artistmusic = current_widget.findChild(QLabel, "artist_label")
            label_albummusic = current_widget.findChild(QLabel, "album_label")
            label_imagemusic = current_widget.findChild(QLabel, "image_label")
            self.label_24.setPixmap(QPixmap(label_imagemusic.pixmap()))
            self.label_25.setText(label_namemusic.text())
            self.label_26.setText(label_artistmusic.text() + " - " + label_albummusic.text())

        except Exception as e:
            print(f"Next song error: {e}")
    
    def prev_Song(self, listWidget):
        try:
            print('Click Previous_Song')
            current_selection = listWidget.currentRow()

            if current_selection == 0:
                prev_index = len(self.current_songs) - 1
            else:
                prev_index = current_selection - 1
            
            current_song = self.current_songs[prev_index]
            listWidget.setCurrentRow(prev_index)
            song_url = QMediaContent(QUrl.fromLocalFile(current_song))
            self.player.setMedia(song_url)
            self.player.play()
            self.move_Slider()

            # Lấy thông tin của bài hát và gán vào biến label_namemusic
            current_item = listWidget.item(prev_index)
            current_widget = listWidget.itemWidget(current_item)
            label_namemusic = current_widget.findChild(QLabel, "name_label")
            label_artistmusic = current_widget.findChild(QLabel, "artist_label")
            label_albummusic = current_widget.findChild(QLabel, "album_label")
            label_imagemusic = current_widget.findChild(QLabel, "image_label")
            self.label_24.setPixmap(QPixmap(label_imagemusic.pixmap()))
            self.label_25.setText(label_namemusic.text())
            self.label_26.setText(label_artistmusic.text() + " - " + label_albummusic.text())
        except Exception as e:
            print(f"Previous song error: {e}")

    def CreateNewPage(self):
#         font = QFont()
#         font.setFamily(u"SF Pro Display")
#         font.setPointSize(10)

#         newPlaylistButton = QPushButton()
#         newPlaylistButton.setObjectName(u"newPlaylistButton")
#         newPlaylistButton.setSizeIncrement(QSize(0, 0))
#         newPlaylistButton.setBaseSize(QSize(0, 0))
#         newPlaylistButton.setFixedSize(200, 28)
#         newPlaylistButton.setFont(font)
#         newPlaylistButton.setText("My Playlist Replay")
#         newPlaylistButton.setCursor(QCursor(Qt.PointingHandCursor))
#         newPlaylistButton.setLayoutDirection(Qt.LeftToRight)
#         newPlaylistButton.setStyleSheet(u"border-radius: 6px;\n"
# "text-align: left;\n"
# "padding-left: 16px;\n"
# "")
#         newIcon = QIcon()
#         newIcon.addFile(u"./images/playlist.svg", QSize(), QIcon.Normal, QIcon.Off)
#         newPlaylistButton.setIcon(newIcon)
#         newPlaylistButton.setIconSize(QSize(16, 16))
#         newPlaylistButton.setCheckable(False)
#         newPlaylistButton.setAutoDefault(False)
#         newPlaylistButton.setFlat(False)

#         self.vBox_Playlist.insertWidget(0, newPlaylistButton)

#         # Connect event clicked for newPlaylistButton after init.
#         newPlaylistButton.clicked.connect(self.applyStyleButton)

#         # Save playlist to database
        self.CreateNewPlaylist()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
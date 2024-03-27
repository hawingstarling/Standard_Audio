from functools import partial
import sys
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


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.cursor = None

        self.conn_mysql = None
        self.cursor, self.conn_mysql = self.ConnectMySql()


        # Init
        self.current_songs = []
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
        # self.frameMusic.mousePressEvent = partial(lambda event, ui: ui.stackedWidget.setCurrentWidget(ui.page_4), ui=self)
        self.pushButton_Favourite.clicked.connect(lambda: (self.stackedWidget.setCurrentWidget(self.page_4), self.GetAllSongs()))

        # Style Active Button Menu
        for w in self.AppleMusic_3.findChildren(QPushButton):
            w.clicked.connect(self.applyStyleButton)
        
        # # Connections
        # self.songSlider.sliderMoved[int].connect(lambda: self.player.setPosition(self.songSlider.value()))
        # self.volumeSlider.sliderMoved[int].connect(lambda: self.volume_Changed())
        # self.buttonAddSong.clicked.connect(self.add_Song)
        # self.resumeButtonSong.clicked.connect(lambda: self.togglePauseResume(self.listWidget))
        # self.nextButtonSong.clicked.connect(lambda: self.next_Song(self.listWidget))
        # self.prevButtonSong.clicked.connect(lambda: self.prev_Song(self.listWidget))

        # Media Player Signals
        self.player.stateChanged.connect(self.mediaState_Changed)

        # Add Playlist
        self.buttonAddPlaylist.clicked.connect(self.create_new_page)

        # TrafficLight Window
        self.TrafficLight_ED695E_6.clicked.connect(self.close_Window)
        self.TrafficLight_62C554_5.clicked.connect(self.hide_Window)

        # Context Menu Right Click ListWidget
        self.listWidget.installEventFilter(self)

        # Get All Playlists
        self.GetAllPlaylists()

        ## SHOW ==> MAIN WINDOW
        ########################################################################
        self.show()
        ## ==> END ##

    def eventFilter(self, source, event):
        if event.type() == QEvent.ContextMenu and source is self.listWidget:
            menu = QMenu()
            menu.addAction('Delete')
            menu.addAction('Playlist')

            if menu.exec_(event.globalPos()):
                item = source.itemAt(event.pos())
            return True
        return super().eventFilter(source, event)

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
        # Double Clicked QListWidget
        self.connect(self.listWidget, QtCore.SIGNAL("itemDoubleClicked(QListWidgetItem *)"), lambda: self.play_Song(self.listWidget))

        # CONNECTION BUTTONS MUSIC
        self.songSlider.sliderMoved[int].connect(lambda: self.player.setPosition(self.songSlider.value()))
        self.volumeSlider.sliderMoved[int].connect(lambda: self.volume_Changed())
        self.buttonAddSong.clicked.connect(self.add_Song)
        self.resumeButtonSong.clicked.connect(lambda: self.togglePauseResume(self.listWidget))
        self.nextButtonSong.clicked.connect(lambda: self.next_Song(self.listWidget))
        self.prevButtonSong.clicked.connect(lambda: self.prev_Song(self.listWidget))


        self.current_songs = []
        query = ("SELECT song.name, song.link, song.image, song.dur, album.name, singer.name FROM song, album, singer "
                "WHERE song.idSinger = singer.id AND song.idAlbum = album.id")
        self.cursor.execute(query)
        songs = self.cursor.fetchall()
        for song in songs:
            song_name = song[0]
            song_link = song[1]
            song_image = song[2]
            song_dur = song[3]
            album_name = song[4]
            singer_name = song[5]

            self.current_songs.append(song_link)
            # Item data
            item_data = {
                'music': song_name,
                'artist': singer_name,
                'album': album_name,
                'duration': song_dur,
                'image': song_image
            }
            self.add_ItemSong(item_data)


    def DeleteSong(self, song_no):
        query = "DELETE FROM song WHERE id = %s"

        self.cursor.execute(query, (song_no,))
        self.conn_mysql.commit()
        print(self.cursor.rowcount, "Delete record.")

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

    def CreateNewPlaylist(self):
        add_playlist = ("INSERT INTO playlist "
                    "(PlaylistName) "
                    "VALUES (%s)")
        
        # Insert new playlist
        self.cursor.execute(add_playlist, ('My Playlist Replay',))

        # Make sure data is committed to the database
        self.conn_mysql.commit()

    def GetAllPlaylists(self):
        query = """SELECT * FROM playlist"""
        self.cursor.execute(query)
        playlists = self.cursor.fetchall()


        for playlist in playlists:
            playlist_id = playlist[0]
            playlist_name = playlist[1]

            newButtonPage = self.GetPages(playlist_name, playlist_id)

            # # self.current_songs.append(song_link)
            # # Item data
            # item_data = {
            #     'playlist_name': playlist_name,
            #     'music': song_name,
            #     'artist': singer_name,
            #     'album': album_name,
            #     'duration': song_dur,
            #     'image': song_image
            # }
            # self.add_Playlist(playlist_id, newButtonPage) // FIX


    def GetPages(self, playlist_name, playlist_id):
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
        newPlaylistButton.clicked.connect(lambda: (self.add_Playlist(playlist_id, newPlaylistButton)))

        return newPlaylistButton

    # FIX
    def add_Playlist(self, playlist_id, newButtonPage): 
    
        self.current_songs = []
        query = """
            SELECT
                playlist.PlaylistID, 
                playlist.PlaylistName, 
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
        my_playlist = Playlist()

        for playlist in playlists:
            item_data = {
                'playlist_name': playlist[1],
                'music': playlist[2],
                'artist': playlist[7],
                'album': playlist[6],
                'duration': playlist[5],
                'image': playlist[4]
            }
            self.current_songs.append(playlist[3])

            item_object = PlaylistObject(**item_data)
            playlist_objects.append(item_object)

            playlist_widget = QWidget()
            # my_playlist = Playlist()
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
                audio = MP3(file)
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

                # Item data
                item_data = {
                    'music': name_music,
                    'artist': artist_music,
                    'album': album_music,
                    'duration': duration_str,
                    'image': image_data
                }
                self.add_ItemSong(item_data)

                self.CreateNewSongs(name_music, file_path, image_path, duration_str, artist_music, album_music)

    def move_Slider(self):
        if stopped:
            return
        else:
            if self.player.state() == QMediaPlayer.PlayingState:
                self.songSlider.setMinimum(0)
                self.songSlider.setMaximum(self.player.duration())
                slider_position = self.player.position()
                self.songSlider.setValue(slider_position)
    
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
    
    
    def next_Song(self, listWidget):
        try:
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

    def create_new_page(self):
        font = QFont()
        font.setFamily(u"SF Pro Display")
        font.setPointSize(10)

        # new_page = QWidget()
        # self.stackedWidget.addWidget(new_page)
        # self.stackedWidget.setCurrentWidget(new_page)

        newPlaylistButton = QPushButton()
        newPlaylistButton.setObjectName(u"newPlaylistButton")
        newPlaylistButton.setSizeIncrement(QSize(0, 0))
        newPlaylistButton.setBaseSize(QSize(0, 0))
        newPlaylistButton.setFixedSize(200, 28)
        newPlaylistButton.setFont(font)
        newPlaylistButton.setText("My Playlist Replay")
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

        # Connect event clicked for newPlaylistButton after init.
        newPlaylistButton.clicked.connect(self.applyStyleButton)

        # Save playlist to database
        self.CreateNewPlaylist()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
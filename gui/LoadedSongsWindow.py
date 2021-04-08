import sys
from math import floor
from threading import Thread
from typing import List

from PySide6.QtCore import Signal
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (QWidget, QPushButton, QMainWindow, QScrollArea, QVBoxLayout, QApplication)

from LoadedSongs import LoadedSongs
from Song import Song
from gui.LoadSongsDialog import LoadSongsDialog
from gui.OrderableListItem import LoadedSongListItem
from gui.OrderableListWidget import OrderableListWidget
from gui.ProgressBar import ProgressBar
from gui.SongDetailsDialog import SongDetailsDialog


class LoadedSongsWindow(QMainWindow):
    def __init__(self, loaded_songs_list):
        """Show and modify the list of all loaded songs
        :type loaded_songs_list: LoadedSongs
        :param loaded_songs_list: All currently loaded songs"""
        super().__init__()

        # Main layout
        self.resize(450, 600)
        self.setWindowTitle("Loaded Songs")
        self._list_widget = OrderableListWidget()
        self.setCentralWidget(self._list_widget)

        # Setup parameters
        self._song_list: LoadedSongs = loaded_songs_list
        self._song_list.subscribe(LoadedSongs.ADDED, self._song_added)
        self._song_list.subscribe(LoadedSongs.DELETED, self._song_deleted)
        self._song_list.subscribe(LoadedSongs.UPDATED, self._song_updated)
        self._song_gui_list: dict[Song: QWidget] = {}
        self._progress_bar = ProgressBar()
        self._load_songs_dialog = LoadSongsDialog(self, self._progress_bar)

        self._signal_song_added.connect(self._song_added_function)

        # Setup gui
        self._create_menu_bar()
        self._status_bar.addPermanentWidget(self._progress_bar)

    def _create_menu_bar(self):
        """Build the windows menu bar"""
        menu_bar = self.menuBar()
        # Load songs action
        self._load_songs_action: QAction = QAction("&Load Files", self)
        self._load_songs_action.triggered.connect(self._do_load_songs_gui_action)
        self._load_song_dir_action: QAction = QAction("Load &Directory", self)
        self._load_song_dir_action.triggered.connect(self._do_load_song_dir_gui_action)
        # Song menu
        songs_menu = menu_bar.addMenu("&Songs")
        songs_menu.addActions([
            self._load_songs_action,
            self._load_song_dir_action,
        ])

        # Status bar
        self._status_bar = self.statusBar()

    def _do_load_songs_gui_action(self):
        """Show a popup dialog to select songs to load"""
        song_list = self._load_songs_dialog.get_songs_by_file()
        thread: Thread = Thread(target=self._add_song_list, args=(song_list,))
        thread.start()

    def _do_load_song_dir_gui_action(self):
        """Show a popup dialog to select songs to load"""
        song_list = self._load_songs_dialog.get_songs_by_dir()
        thread: Thread = Thread(target=self._add_song_list, args=(song_list,))
        thread.start()

    def _add_song_list(self, song_list):
        """Add a list of new songs to the list
        :type song_list: list[Song]
        :param song_list: The list of songs to add"""
        # Setup parameters
        song: Song
        total_song_count: int = len(song_list)
        song_num: int = 0
        self._progress_bar.startTimer()
        # Load songs
        for song in song_list:
            self._song_list.add(song)
            song_num += 1
            percentage_done = floor(song_num / total_song_count * 100)
            self._progress_bar.set_progress.emit(percentage_done)

    def _song_added(self, song):
        self._signal_song_added.emit(song)

    _signal_song_added: Signal = Signal(Song)

    def _song_added_function(self, song):
        """Add a new song was added to the list
        :type song: Song
        :param song: The song that was added"""
        # Add to gui
        list_item: LoadedSongListItem = LoadedSongListItem(song)
        self._list_widget.add(list_item)
        self._song_gui_list[song] = list_item

    def _song_deleted(self, song):
        """A song was deleted from the list
        :type song: Song
        :param song: The song that was deleted"""
        # Remove from gui
        list_item: LoadedSongListItem = self._song_gui_list[song]
        self._song_gui_list.pop(song)
        self._list_widget.delete_item(list_item)

    def _song_updated(self, song):
        """A songs info was updated
        :type song: Song
        :param song: The songs whose info was updated"""
        raise NotImplementedError()


if __name__ == '__main__':
    app = QApplication()
    loaded_songs = LoadedSongs()
    window = LoadedSongsWindow(loaded_songs)
    window.show()
    sys.exit(app.exec_())

import sys
from typing import List

from PySide2.QtWidgets import (QWidget, QPushButton, QMainWindow, QAction, QScrollArea, QVBoxLayout, QApplication)

from Song import Song
from gui.LoadSongsDialog import LoadSongsDialog
from gui.ProgressBar import ProgressBar
from gui.SongDetailsDialog import SongDetailsDialog


class LoadedSongsWindow(QMainWindow):
    def __init__(self):
        """Show and modify the list of all loaded songs"""
        super().__init__()

        # Main layout
        self.resize(450, 600)
        self.setWindowTitle("Loaded Songs")
        self.scrollableWrapper = QScrollArea()
        self.setCentralWidget(self.scrollableWrapper)

        self.centralLayout = QVBoxLayout()
        self.centralWidget = QWidget()
        self.centralWidget.setLayout(self.centralLayout)

        self.scrollableWrapper.setWidget(self.centralWidget)
        self.scrollableWrapper.setWidgetResizable(True)

        # Setup parameters
        self._song_list: List[Song] = []
        self._song_gui_list: dict[Song: QWidget] = {}
        self._progress_bar = ProgressBar()
        self._load_songs_dialog = LoadSongsDialog(self, self._progress_bar)

        # Setup gui
        self._create_menu_bar()

    def _create_menu_bar(self):
        """Build the windows menu bar"""
        menu_bar = self.menuBar()
        # Load songs action
        self._load_songs_action: QAction = QAction("&Load Files", self)
        self._load_songs_action.triggered.connect(self.do_load_songs_gui_action)
        self._load_song_dir_action: QAction = QAction("Load &Directory", self)
        self._load_song_dir_action.triggered.connect(self.do_load_song_dir_gui_action)
        # Song menu
        songs_menu = menu_bar.addMenu("&Songs")
        songs_menu.addActions([
            self._load_songs_action,
            self._load_song_dir_action,
        ])

        # Status bar
        self._status_bar = self.statusBar()

    def do_load_songs_gui_action(self):
        """Show a popup dialog to select songs to load"""
        self._status_bar.addPermanentWidget(self._progress_bar)
        song_list = self._load_songs_dialog.get_songs_by_file()
        self._progress_bar.set_progress()
        self.add_song_list(song_list)

    def do_load_song_dir_gui_action(self):
        """Show a popup dialog to select songs to load"""
        song_list = self._load_songs_dialog.get_songs_by_dir()
        self.add_song_list(song_list)

    def add_song_list(self, song_list):
        """Add a list of new songs to the list
        :type song_list: list[Song]
        :param song_list: The list of songs to add"""
        song: Song
        for song in song_list:
            self.add_song(song)

    def add_song(self, song):
        """Add a new song to the list
        :type song: Song
        :param song: The song to add"""
        # Only add mew songs
        if song not in self._song_list:
            self._song_list.append(song)
            # Add to gui
            button = QPushButton(song.get_name(), self)
            button.clicked.connect(lambda: self._show_song_details(song))
            self.centralLayout.addWidget(button)
            self._song_gui_list[song] = button

    def _show_song_details(self, song):
        """Show a songs details
        :type song: Song
        :param song: The song to show the details about"""
        details_gui = SongDetailsDialog(song, self, self.remove_song)
        details_gui.show()

    def remove_song(self, song):
        """Remove a song from the list
        :type song: Song
        :param song: The song to remove"""
        # Remove from list
        try:
            self._song_list.remove(song)
        # Song doesn't exist anymore
        except ValueError:
            return
        # Remove from gui
        song_widget: QWidget = self._song_gui_list[song]
        self._song_gui_list.pop(song)
        song_widget.deleteLater()

    def get_loaded_song_list(self):
        """Get a list of all loaded songs
        :return List[Song]: The list of all loaded songs"""
        return self._song_list


if __name__ == '__main__':
    app = QApplication()
    window = LoadedSongsWindow()
    window.show()
    sys.exit(app.exec_())

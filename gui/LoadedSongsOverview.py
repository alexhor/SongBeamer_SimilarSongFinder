from PySide2.QtWidgets import (QHBoxLayout, QWidget, QPushButton)

from Song import Song
from gui.SongDetails import SongDetails


class LoadedSongsOverview(QWidget):
    def __init__(self):
        """Show and modify the list of all loaded songs"""
        QWidget.__init__(self)

        # Main layout
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.resize(1280, 720)
        self.setWindowTitle("Loaded Songs")

        # Setup parameters
        self._song_list: list[Song] = []
        self._song_gui_list: dict[Song: QWidget] = {}

        # Setup gui


    def add_song_list(self, song_list: list[Song]):
        """Add a list of new songs to the list
        :param song_list: The list of songs to add"""
        song: Song
        for song in song_list:
            self.add_song(song)

    def add_song(self, song: Song):
        """Add a new song to the list
        :param song: The song to add"""
        # Only add mew songs
        if song not in self._song_list:
            self._song_list.append(song)
            # Add to gui
            button = QPushButton(song.get_name(), self)
            button.clicked.connect(lambda: self._show_song_details(song))
            self.layout.addWidget(button)
            self._song_gui_list[song] = button

    def _show_song_details(self, song: Song):
        """Show a songs details
        :param song: The song to show the details about"""
        details_gui = SongDetails(song, self, self.remove_song)
        details_gui.show()

    def remove_song(self, song: Song):
        """Remove a song from the list
        :param song: The song to remove"""
        # Remove from list
        self._song_list.remove(song)
        # Remove from gui
        song_widget: QWidget = self._song_gui_list[song]
        song_widget.deleteLater()
        self._song_gui_list.pop(song_widget)

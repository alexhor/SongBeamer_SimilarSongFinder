from typing import List

from PySide6.QtWidgets import (QLabel, QPushButton, QHBoxLayout, QWidget, QMainWindow, QScrollArea, QVBoxLayout)

from Song import Song
from gui.SongDiffWindow import SongDiffWindow


class SongSimilarityWindow(QMainWindow):
    def __init__(self, song_orig, song_similarity_list):
        """Display all songs similar to one song
        :type song_orig: Song
        :param song_orig: The referenced song
        :type song_similarity_list: list[dict[str, Song]]
        :param song_similarity_list: All songs similar to the reference one"""
        super().__init__()
        self._song_orig: Song = song_orig
        self._song_similarity_list: List[dict[str, Song]] = song_similarity_list
        self._similar_song_gui_list: dict[Song, QWidget] = {}
        self._song_diff_gui_list: List[SongDiffWindow] = []

        # Main layout
        self.resize(450, 600)
        self.setWindowTitle(self._song_orig.get_name() + ' - Similar Songs')
        self.scrollableWrapper = QScrollArea()
        self.setCentralWidget(self.scrollableWrapper)

        self.centralLayout = QVBoxLayout()
        self.centralWidget = QWidget()
        self.centralWidget.setLayout(self.centralLayout)

        self.scrollableWrapper.setWidget(self.centralWidget)
        self.scrollableWrapper.setWidgetResizable(True)

        # Add all similar songs
        for similarity in self._song_similarity_list:
            similar_song: Song = similarity['song']
            button: QPushButton = QPushButton(similar_song.get_name() + ' - ' + str(similarity['score']), self)
            button.clicked.connect(lambda: self._show_song_diff(similar_song))
            self.centralLayout.addWidget(button)
            self._similar_song_gui_list[similar_song] = button

    def _show_song_diff(self, similar_song):
        """
        :type similar_song: Song.Song
        :param similar_song: The song to diff the original song against
        """
        diff_gui = SongDiffWindow(self._song_orig, similar_song)
        diff_gui.show()
        diff_gui.activateWindow()
        self._song_diff_gui_list.append(diff_gui)

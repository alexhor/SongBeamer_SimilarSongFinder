from functools import partial
from typing import List

from PySide6.QtWidgets import (QLabel, QPushButton, QHBoxLayout, QWidget, QMainWindow, QScrollArea, QVBoxLayout,
                               QGridLayout, QLayout)

from Song import Song
from gui.SongDiffWindow import SongDiffWindow


class SongSimilarityWindow(QMainWindow):
    """A list of similar songs in this group"""
    _song_similarity_list: List[Song]
    """The similarity scores for each song pair"""
    _similarity_scores: dict[tuple[Song, Song], int]
    """Parking space for all song diff guis"""
    _diff_window_list: List[SongDiffWindow]

    def __init__(self, song_similarity_list, similarity_scores):
        """Display all songs similar to one song
        :type song_similarity_list: list[Song]
        :param song_similarity_list: A list of similar songs
        :type similarity_scores: dict[tuple[Song, Song], int]
        :param similarity_scores: The similarity scores for each song pair"""
        super().__init__()
        self._song_similarity_list = song_similarity_list
        self._similarity_scores = similarity_scores
        self._diff_window_list = []

        # Main layout
        self.resize(450, 600)
        self.setWindowTitle(self._song_similarity_list[0].get_name() + ' - Similar Songs')
        self.scrollableWrapper = QScrollArea()
        self.setCentralWidget(self.scrollableWrapper)

        self.centralLayout: QGridLayout = QGridLayout()
        self.centralWidget = QWidget()
        self.centralWidget.setLayout(self.centralLayout)

        self.scrollableWrapper.setWidget(self.centralWidget)
        self.scrollableWrapper.setWidgetResizable(True)

        # Add all similar songs
        row_num: int = 0
        for song in self._song_similarity_list:
            button: QPushButton = QPushButton(song.get_name(), self)
            button.clicked.connect(partial(self.show_other_songs, song))
            song.subscribe(Song.UPDATED, partial(self._song_updated, button))
            self._song_updated(button, song)
            self.centralLayout.addWidget(button, row_num, 0)
            row_num += 1

    @staticmethod
    def _song_updated(button, song):
        """The given song was updated
        :type button: QPushButton
        :param button: The button associated with this song
        :type song: Song
        :param song: The song that changed"""
        if song.is_marked_for_keeping():
            button.setStyleSheet('background-color: green')
        elif song.is_marked_for_deleting():
            button.setStyleSheet('background-color: red')

    def _clear_column(self, col_id):
        """Clear a column of all its widgets
        :type col_id: int
        :param col_id: The columns id"""
        for row_id in range(self.centralLayout.rowCount()):
            item = self.centralLayout.itemAtPosition(row_id, col_id)
            if item is not None:
                item.widget().deleteLater()
                self.centralLayout.removeItem(item)

    def show_other_songs(self, song):
        """Show all other songs to compare them
        :type song: Song
        :param song: The song to compare to"""
        # Clear old gui
        self._clear_column(1)

        # Add new gui elements
        row_num: int = -1
        for similar_song in self._song_similarity_list:
            row_num += 1
            if similar_song == song:
                self.centralLayout.addWidget(QWidget(), row_num, 1)
                continue

            similarity_score: float
            if (song, similar_song) in self._similarity_scores.keys():
                similarity_score = self._similarity_scores[(song, similar_song)]
            else:
                similarity_score = self._similarity_scores[(similar_song, song)]
            button: QPushButton = QPushButton(similar_song.get_name() + ' (' + str(similarity_score) + ')', self)
            button.clicked.connect(partial(self._show_song_diff, song, similar_song))
            self._song_updated(button, similar_song)
            similar_song.subscribe(Song.UPDATED, partial(self._song_updated, button))
            self.centralLayout.addWidget(button, row_num, 1)

    def _show_song_diff(self, orig_song, similar_song):
        """
        :type orig_song: Song
        :param orig_song: First song to compare with
        :type similar_song: Song
        :param similar_song: Second song to compare with"""
        diff_gui = SongDiffWindow(orig_song, similar_song)
        diff_gui.show()
        diff_gui.activateWindow()
        # Keep the window open
        self._diff_window_list.append(diff_gui)

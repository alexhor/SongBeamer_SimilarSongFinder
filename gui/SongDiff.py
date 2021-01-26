from difflib import Differ
from typing import List

from PySide2.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QListWidget, QScrollArea


class SongDiff(QMainWindow):
    def __init__(self, song_orig, song_similar):
        """Displays the difference between two songs
        :type song_orig: Song.Song
        :param song_orig: The original song
        :type song_similar: Song.Song
        :param song_similar: The similar song
        """
        super().__init__()
        self._song_orig = song_orig
        self._song_similar = song_similar

        # Setup gui
        self.resize(800, 550)
        self.setWindowTitle(self._song_orig.get_name() + ' - Similar Songs')
        self.scrollableWrapper = QScrollArea()
        self.setCentralWidget(self.scrollableWrapper)

        self.centralLayout = QHBoxLayout()
        self.centralWidget = QWidget()
        self.centralWidget.setLayout(self.centralLayout)

        self.scrollableWrapper.setWidget(self.centralWidget)
        self.scrollableWrapper.setWidgetResizable(True)

        self._left_diff: QListWidget = QListWidget()
        self.centralLayout.addWidget(self._left_diff)
        self._right_diff: QListWidget = QListWidget()
        self.centralLayout.addWidget(self._right_diff)

        # Show diff
        self._show_diff()

    def _show_diff(self):
        """Calculate the diff between the two songs
        :return: list[str]"""
        song_orig_line_str_list: List[str] = [str(line) for line in self._song_orig.get_line_list()]
        song_similar_line_str_list: List[str] = [str(line) for line in self._song_similar.get_line_list()]
        # Compare
        comparison = [l for l in Differ().compare(song_orig_line_str_list, song_similar_line_str_list)
                      if not l.startswith('?')]
        song_orig_diff_list = [l if l.startswith((' ', '-')) else '' for l in comparison]
        song_similar_diff_list = [l if l.startswith((' ', '+')) else '' for l in comparison]
        # Add to gui
        self._left_diff.addItems(song_orig_diff_list)
        self._right_diff.addItems(song_similar_diff_list)

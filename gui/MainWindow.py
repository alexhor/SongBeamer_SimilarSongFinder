from functools import partial
from typing import List

from PySide2.QtCore import Signal
from PySide2.QtWidgets import (QWidget, QVBoxLayout, QScrollArea, QMainWindow,
                               QAction, QPushButton)

from SimilarityFinder import SimilarityFinder
from Song import Song
from gui.LoadedSongsOverview import LoadedSongsOverview
from gui.ProgressBar import ProgressBar
from gui.SongSimilarity import SongSimilarity


class MainWindow(QMainWindow):
    # Incoming progress updates
    _calculating_similarities_done: Signal = Signal()

    def __init__(self):
        """The main window displaying all song similarities"""
        super().__init__()

        # Setup parameters
        self._similarity_finder: SimilarityFinder
        self._song_similarity_gui_list: List[SongSimilarity] = []
        self._song_gui_list: dict[Song, QPushButton] = {}

        # Setup signal callbacks
        self._calculating_similarities_done.connect(self._do_calculating_similarities_done)

        # Main layout
        self.resize(450, 600)
        self.setWindowTitle("SongBeamer Song Similarity Finder")
        self.scrollableWrapper = QScrollArea()
        self.setCentralWidget(self.scrollableWrapper)

        self.centralLayout = QVBoxLayout()
        self.centralWidget = QWidget()
        self.centralWidget.setLayout(self.centralLayout)

        self.scrollableWrapper.setWidget(self.centralWidget)
        self.scrollableWrapper.setWidgetResizable(True)

        # Setup gui
        self._create_menu_bar()

        # Show the page with all loaded songs on startup
        self._loaded_songs_window = LoadedSongsOverview()
        self._do_show_loaded_songs_gui_action()

    def _do_calculating_similarities_done(self):
        """Handle similarities calculation is done"""
        if self._similarity_finder is None:
            return
        # Get the calculated similarities
        similarities = self._similarity_finder.get_similarities()
        # Display them
        self._build_similarities_gui(similarities)

    def _build_similarities_gui(self, similarities):
        """Build a gui for a list of similarities
        :type similarities: dict[Song, list[Song]"""
        # Setup gui
        self.scrollableWrapper = QScrollArea()
        self.setCentralWidget(self.scrollableWrapper)

        self.centralLayout = QVBoxLayout()
        self.centralWidget = QWidget()
        self.centralWidget.setLayout(self.centralLayout)

        self.scrollableWrapper.setWidget(self.centralWidget)
        self.scrollableWrapper.setWidgetResizable(True)

        # Add all songs to gui
        for song in similarities.keys():
            song: Song
            button: QPushButton = QPushButton(song.get_name(), self)
            button.clicked.connect(partial(self._show_similar_songs, song, similarities[song]))
            self.centralLayout.addWidget(button)
            self._song_gui_list[song] = button

    def _show_similar_songs(self, song, similar_song_list):
        """Show all a songs similarities
        :type song: Song.Song
        :param song: The main song
        :type similar_song_list: list[Song.Song]
        :param similar_song_list: The list of similar songs"""
        song_similarity_gui: SongSimilarity = SongSimilarity(song, similar_song_list)
        song_similarity_gui.show()
        song_similarity_gui.activateWindow()
        self._song_similarity_gui_list.append(song_similarity_gui)

    def _create_menu_bar(self):
        """Build the windows menu bar"""
        menu_bar = self.menuBar()
        # Show loaded songs
        self._show_loaded_songs_action: QAction = QAction("Show &loaded", self)
        self._show_loaded_songs_action.triggered.connect(self._do_show_loaded_songs_gui_action)
        self._find_similarities_action: QAction = QAction("&Find similarities", self)
        self._find_similarities_action.triggered.connect(self._do_find_similarities_gui_action)
        # Song menu
        songs_menu = menu_bar.addMenu("&Songs")
        songs_menu.addActions([
            self._show_loaded_songs_action,
            self._find_similarities_action,
        ])

    def _do_show_loaded_songs_gui_action(self):
        """Show the window with all loaded songs"""
        self._loaded_songs_window.show()
        self._loaded_songs_window.activateWindow()

    def _do_find_similarities_gui_action(self):
        """Calculate the similarities between all currently loaded songs and display them"""
        progress_bar = ProgressBar()
        loaded_song_list = self._loaded_songs_window.get_loaded_song_list()
        self.setCentralWidget(progress_bar)
        self._similarity_finder = SimilarityFinder(loaded_song_list, progress_bar, self._calculating_similarities_done)

    def closeEvent(self, event):
        """Handle close event
        :type event: QCloseEvent
        :param event: The triggered event"""
        # Close any other open windows first
        self._loaded_songs_window.close()
        for window in self._song_similarity_gui_list:
            window: LoadedSongsOverview
            window.close()
        # Now close this one
        super().closeEvent(event)

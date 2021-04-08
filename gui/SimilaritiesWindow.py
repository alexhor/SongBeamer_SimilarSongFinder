from functools import partial
from typing import List

from PySide2.QtCore import Signal
from PySide2.QtWidgets import (QWidget, QVBoxLayout, QScrollArea, QMainWindow,
                               QAction, QPushButton)

from LoadedSongs import LoadedSongs
from SimilarityFinder import SimilarityFinder
from Song import Song
from gui.LoadedSongsWindow import LoadedSongsWindow
from gui.OrderableListItem import SongSimilarityListItem
from gui.OrderableListWidget import OrderableListWidget
from gui.ProgressBar import ProgressBar
from gui.SongSimilarityWindow import SongSimilarityWindow


class SimilaritiesWindow(QMainWindow):
    """Incoming progress updates"""
    _calculating_similarities_done: Signal = Signal()
    """All loaded songs"""
    _loaded_song_list: LoadedSongs
    """Central widget"""
    centralWidget: OrderableListWidget

    def __init__(self):
        """The main window displaying all song similarities"""
        super().__init__()

        # Setup parameters
        self._similarity_finder: SimilarityFinder
        self._song_similarity_gui_list: List[SongSimilarityWindow] = []
        self._song_gui_list: dict[Song, QPushButton] = {}
        self._loaded_song_list = LoadedSongs()

        # Setup signal callbacks
        self._calculating_similarities_done.connect(self._do_calculating_similarities_done)

        # Setup gui
        self.resize(450, 600)
        self.setWindowTitle("SongBeamer Song Similarity Finder")
        self._create_menu_bar()
        self._build_similarities_gui({})

        # Show the page with all loaded songs on startup
        self._loaded_songs_window = LoadedSongsWindow(self._loaded_song_list)
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
        :type similarities: dict[Song, list[dict[str, Song]]]"""
        # Setup gui
        self.centralWidget = OrderableListWidget()
        self.setCentralWidget(self.centralWidget)

        # Add all songs to gui
        song: Song
        similar_songs: list
        for song, similar_songs in similarities.items():
            song_similarity_list_item: SongSimilarityListItem = SongSimilarityListItem(song, similar_songs)
            self._song_gui_list[song] = song_similarity_list_item
            self.centralWidget.add(song_similarity_list_item)

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
        self.setCentralWidget(progress_bar)
        self._similarity_finder = SimilarityFinder(self._loaded_song_list, progress_bar,
                                                   self._calculating_similarities_done)

    def closeEvent(self, event):
        """Handle close event
        :type event: QCloseEvent
        :param event: The triggered event"""
        # Close any other open windows first
        self._loaded_songs_window.close()
        for window in self._song_similarity_gui_list:
            window: LoadedSongsWindow
            window.close()
        # Now close this one
        super().closeEvent(event)

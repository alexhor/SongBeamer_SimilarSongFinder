import math

from PySide2.QtCore import Qt
from PySide2.QtGui import QResizeEvent
from PySide2.QtWidgets import (QPushButton, QHBoxLayout, QWidget, QVBoxLayout, QScrollArea, QLayout, QMainWindow,
                               QAction)

from Song import Song
from gui.LoadedSongsOverview import LoadedSongsOverview
from gui.ProgressBar import ProgressBar
from gui.SongSimilarity import SongSimilarity


class MainWindow(QMainWindow):
    def __init__(self):
        """The main window displaying all song similarities"""
        super().__init__()

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
        self.do_show_loaded_songs_gui_action()

    def _create_menu_bar(self):
        """Build the windows menu bar"""
        menu_bar = self.menuBar()
        # Show loaded songs
        self._show_loaded_songs_action: QAction = QAction("Show &loaded", self)
        self._show_loaded_songs_action.triggered.connect(self.do_show_loaded_songs_gui_action)
        self._find_similarities_action: QAction = QAction("&Find similarities", self)
        self._find_similarities_action.triggered.connect(self.do_find_similarities_gui_action)
        # Song menu
        songs_menu = menu_bar.addMenu("&Songs")
        songs_menu.addActions([
            self._show_loaded_songs_action,
            self._find_similarities_action,
        ])

    def do_show_loaded_songs_gui_action(self):
        """Show the window with all loaded songs"""
        self._loaded_songs_window.show()
        self._loaded_songs_window.activateWindow()

    def do_find_similarities_gui_action(self):
        """Calculate the similarities between all currently loaded songs and display them"""
        progress_bar = ProgressBar()
        loaded_song_list = self._loaded_songs_window.get_loaded_song_list()

    def closeEvent(self, event):
        """Handle close event
        :type event: QCloseEvent
        :param event: The triggered event"""
        # Close any other open windows first
        self._loaded_songs_window.close()
        # Now close this one
        super().closeEvent(event)

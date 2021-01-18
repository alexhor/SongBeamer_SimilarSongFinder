import sys
import threading

from PySide2.QtCore import Signal
from PySide2.QtWidgets import (QApplication, QFileDialog, QWidget, QVBoxLayout)

import gui.MainWindow as MainWindow
from SimilarityFinder import SimilarityFinder
from gui.LoadedSongsOverview import LoadedSongsOverview
from gui.ProgressBar import ProgressBar


class Main(QWidget):
    # Incoming progress updates
    song_loading_done = Signal()
    collecting_similarities_done = Signal()

    def __init__(self):
        """Show the main application window"""
        super().__init__()
        # Set layout
        self._layout = QVBoxLayout()
        self.setLayout(self._layout)
        self.setWindowTitle("Main")

        self._loaded_songs_overview = LoadedSongsOverview()
        self._loaded_songs_overview.show()

        # Get the working directory
        #self._song_folder = self._choose_song_folder()
        # Calculate similarities between all songs in the working directory
        #self._calc_similarities()

    def _choose_song_folder(self):
        """Select a working directory, where all SongBeamer songs are saved
        :return str: The selected working directory"""
        # Show directory selection dialog
        chooser = QFileDialog(self, 'SongBeamer Files', 'D:\\nc.kircheneuenburg.de\\Technik\\Songbeamer\\Songs',
                              filter='SongBeamer Files (*.sng)')
        chooser.setFileMode(QFileDialog.DirectoryOnly)
        chooser.setOption(QFileDialog.DontUseNativeDialog, True)
        chooser.setOption(QFileDialog.ShowDirsOnly, False)

        # Make sure a working directory has been selected
        if not chooser.exec_():
            exit()
        return chooser.selectedFiles()[0]

    def _calc_similarities(self):
        """Calculate similarities between all songs in the working directory"""
        # Open up a progress bar widget
        self._progress_bar_dialog = ProgressBar()
        self._layout.addWidget(self._progress_bar_dialog)
        # Get the similarity finder
        self._similarity_finder = SimilarityFinder(self._song_folder, self._progress_bar_dialog, self)
        # Start similarity calculation
        finder_thread = threading.Thread(target=self._similarity_finder.run)
        finder_thread.name = "Similarity Finder"
        finder_thread.start()
        # Show the main window
        self.show()
        # Handle progress updates
        # noinspection PyUnresolvedReferences
        self.song_loading_done.connect(self._song_loading_done)
        # noinspection PyUnresolvedReferences
        self.collecting_similarities_done.connect(lambda: self._collecting_similarities_done())

    @staticmethod
    def _song_loading_done():
        """Handle the event, that all songs have been loaded"""
        print("SONGS DONE LOADING")

    def _collecting_similarities_done(self):
        """Handle the event, that the similarities between all songs have been calculated"""
        self._show_main_window()

    def _show_main_window(self):
        """Show the main window displaying all songs with similarities"""
        self._main_window = MainWindow.MainWindow()
        self.hide()
        self._main_window.load_similarities(self._similarity_finder.get_similarities(),
                                            self._similarity_finder.get_loaded_song_dict())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = Main()
    sys.exit(app.exec_())

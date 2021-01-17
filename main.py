import sys
import threading

from PySide2.QtCore import Signal
from PySide2.QtWidgets import (QApplication, QFileDialog, QWidget, QVBoxLayout)

import gui.mainwindow as main_window
from Finder import Finder
from gui.progress_bar import progress_bar


class Main(QWidget):
    song_loading_done = Signal()
    collecting_similarities_done = Signal()

    def __init__(self):
        super().__init__()

        self._layout = QVBoxLayout()
        self.setLayout(self._layout)

        self._song_folder = self._choose_song_folder()[0]
        self._load_songs()

    def _choose_song_folder(self):
        chooser = QFileDialog(self, 'SongBeamer Files', 'D:\\nc.kircheneuenburg.de\\Technik\\Songbeamer\\Songs', filter='SongBeamer Files (*.sng)')
        chooser.setFileMode(QFileDialog.DirectoryOnly)
        chooser.setOption(QFileDialog.DontUseNativeDialog, True)
        chooser.setOption(QFileDialog.ShowDirsOnly, False)

        if not chooser.exec_():
            exit()
        return chooser.selectedFiles()

    def _load_songs(self):
        self._progress_bar_dialog = progress_bar()
        self._layout.addWidget(self._progress_bar_dialog)
        self._similarity_finder = Finder(self._song_folder, self._progress_bar_dialog, self)

        finder_thread = threading.Thread(target=self._similarity_finder.run)
        finder_thread.name = "Similarity Finder"
        finder_thread.start()

        self.show()
        self.song_loading_done.connect(self._song_loading_done)
        self.collecting_similarities_done.connect(lambda: self._collecting_similarities_done())

    @staticmethod
    def _song_loading_done():
        print("SONGS DONE LOADING")

    def _collecting_similarities_done(self):
        self._show_main_window()

    def _show_main_window(self):
        self._main_window = main_window.show()
        self.hide()
        self._main_window.load_similarities(self._similarity_finder.get_similarities(),
                                            self._similarity_finder.get_loaded_song_dict())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    Main()
    sys.exit(app.exec_())

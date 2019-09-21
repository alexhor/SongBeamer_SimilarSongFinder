import gui.main_window as main_window
from gui.progress_bar import progress_bar
from Finder import Finder
from PySide2.QtWidgets import (QApplication, QFileDialog, QWidget, QVBoxLayout)
from PySide2.QtCore import Signal, QThread
import sys, threading


class main(QWidget):
    song_loading_done = Signal()

    def __init__(self):
        super().__init__()

        self._layout = QVBoxLayout()
        self.setLayout(self._layout)

        self._song_folder = self._choose_song_folder()[0]
        self._load_songs()

    def _choose_song_folder(self):
        chooser = QFileDialog()
        chooser.setFileMode(QFileDialog.Directory)

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

    def _song_loading_done(self):
        self.song_loading_done.disconnect()
        self._show_main_window()

    def _show_main_window(self):
        self._main_window = main_window.show()
        self.hide()
        self._main_window.load_similarities(self._similarity_finder.get_similarities())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main()
    sys.exit(app.exec_())

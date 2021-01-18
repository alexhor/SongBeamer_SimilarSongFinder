from PySide2.QtCore import Qt
from PySide2.QtWidgets import QWidget, QDialog, QPushButton, QVBoxLayout, QLabel

from Song import Song


class SongDetails(QDialog):
    def __init__(self, song: Song, parent: QWidget, remove_callback=None):
        """Show a popup with a songs details
        :param song: The song whose details should be shown
        :param parent: The parent widget
        :param remove_callback: A function to call when the song should be removed"""
        super().__init__(parent)
        # Set parameters
        self._song = song
        self._parent = parent
        self._remove_callback = remove_callback
        # Set gui
        self.setWindowTitle(song.get_name())
        self.setWindowModality(Qt.ApplicationModal)
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)
        # Remove action
        if remove_callback is not None:
            remove_button = QPushButton("Remove", self)
            remove_button.clicked.connect(lambda: remove_callback(song))
            self.layout.addWidget(remove_button)
        # Song text
        label = QLabel(song.get_text(), self)
        self.layout.addWidget(label)

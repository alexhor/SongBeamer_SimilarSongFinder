from PySide2.QtWidgets import (QLabel, QPushButton, QHBoxLayout, QWidget)


class SongSimilarity:
    def __init__(self, song_orig, song_similarity_list):
        """Display all songs similar to one song"""
        self._song_orig = song_orig
        self._song_similarity_list = song_similarity_list
        self._button = QPushButton()
        self._window = None
        self.__valid = False

    def get_button_widget(self):
        """Get the button to click on to show all similar songs
        :return QButton: The button to click"""
        self._button.setText(str(self._song_orig))
        self._button.clicked.connect(lambda: self.button_clicked())
        return self._button

    def button_clicked(self):
        """Handle button clicked event"""
        # The preview element has to be passed to generate a preview
        if not self.__valid:
            return
        # Show all similar songs
        self._window.clear_text_preview()
        self.show_similar_songs()
        # Highlight the selected song
        self._button.setStyleSheet("background-color: red")

    def show_similar_songs(self):
        """Show all similar songs"""
        if self._window is None:
            return

        # Add song titles

        # Add each similar song
        for similar_song in self._song_similarity_list:
            # Create text widgets
            left = QLabel(str(similar_song))
            right = QLabel("EMPTY")
            # Add the elements to the widget
            layout = QHBoxLayout()
            layout.addWidget(left)
            layout.addWidget(right)
            # Add the layout to the text preview
            wrapper = QWidget()
            wrapper.setLayout(layout)
            self._window.add_widget_to_text_preview(wrapper)

    def set_window(self, window):
        """Set the parent window"""
        self._window = window

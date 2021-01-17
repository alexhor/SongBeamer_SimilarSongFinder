from PySide2.QtWidgets import (QLabel, QPushButton, QHBoxLayout, QWidget)


class SongSimilarity:
    def __init__(self, song_orig, song_similarity_list):
        self._song_orig = song_orig
        self._song_similarity_list = song_similarity_list
        self._button = QPushButton()
        self.__valid = False

    def get_button_widget(self):
        self._button.setText(str(self._song_orig))
        self._button.clicked.connect(lambda: self.button_clicked())
        return self._button

    def button_clicked(self):
        # the preview element has to be passed to generate a preview
        if not self.__valid:
            return

        self._window.clear_text_preview()
        self.show_similar_songs()
        self._button.setStyleSheet("background-color: red")

    def show_similar_songs(self):
        if not self.__valid:
            return

        # add song titles

        # add each similar song
        for similar_song in self._song_similarity_list:
            # create text widgets
            left = QLabel(str(similar_song))
            right = QLabel("EMPTY")
            # add the elements to the widget
            layout = QHBoxLayout()
            layout.addWidget(left)
            layout.addWidget(right)
            # add the layout to the text preview
            wrapper = QWidget()
            wrapper.setLayout(layout)
            self._window.add_widget_to_text_preview(wrapper)

    def set_window(self, window):
        self._window = window
        self.__valid = True
import math

from PySide2.QtCore import Qt
from PySide2.QtWidgets import (QPushButton, QHBoxLayout, QWidget, QVBoxLayout, QScrollArea)

from gui.songsimilarity import SongSimilarity


class MainWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        # similarity selection
        self.similarity_list_wrapper_widget = QWidget()
        self.similarity_list_layout = QVBoxLayout()
        self.similarity_list_scroll = QScrollArea()

        self.generate_scroll_area(self.similarity_list_layout,
                                  self.similarity_list_wrapper_widget, self.similarity_list_scroll)

        # text preview
        self.text_preview_wrapper_widget = QWidget()
        self.text_preview_layout = QVBoxLayout()
        self.text_preview_scroll = QScrollArea()

        self.generate_scroll_area(self.text_preview_layout,
                                  self.text_preview_wrapper_widget, self.text_preview_scroll)

        # left song preview
        self._left_song_preview_wrapper_widget = QWidget()
        self._left_song_preview = QVBoxLayout()
        self._left_song_preview_scroll = QScrollArea()

        self.generate_scroll_area(self._left_song_preview,
                                  self._left_song_preview_wrapper_widget, self._left_song_preview_scroll)

        # right song preview
        self._right_song_preview_wrapper_widget = QWidget()
        self._right_song_preview = QVBoxLayout()
        self._right_song_preview_scroll = QScrollArea()

        self.generate_scroll_area(self._right_song_preview,
                                  self._right_song_preview_wrapper_widget, self._right_song_preview_scroll)

        # main layout
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.similarity_list_scroll)
        self.layout.addWidget(self.text_preview_scroll)
        self.layout.addWidget(self._left_song_preview_scroll)
        self.layout.addWidget(self._right_song_preview_scroll)
        self.setLayout(self.layout)

        # adjust the layouts sizes
        self.adjustSize()

    def resizeEvent(self, event):
        output = super().resizeEvent(event)
        self.adjustSize()
        return output

    @staticmethod
    def generate_scroll_area(layout, wrapper_widget, scroll_area):
        layout.addStretch()
        layout.setAlignment(Qt.AlignTop)
        wrapper_widget.setLayout(layout)

        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(wrapper_widget)

    def adjustSize(self):
        width = self.width()

        self.similarity_list_scroll.setFixedWidth(math.floor(width * 0.2))
        self.text_preview_scroll.setFixedWidth(math.floor(width * 0.3))
        self._left_song_preview_scroll.setFixedWidth(math.floor(width * 0.2))
        self._right_song_preview_scroll.setFixedWidth(math.floor(width * 0.2))

    def load_similarities(self, similarity_list, loaded_song_dict):
        for song_orig, similar_songs_list in similarity_list.items():
            # Replace song file names with actual songs objects
            song_orig = loaded_song_dict[song_orig]
            for i in range(len(similar_songs_list)):
                similar_songs_list[i] = loaded_song_dict[similar_songs_list[i]]

            similarity = SongSimilarity(song_orig, similar_songs_list)
            similarity.set_window(self)
            self.similarity_list_layout.addWidget(similarity.get_button_widget(),
                                                  self.similarity_list_layout.count() - 1)

    def get_preview_text_element_left(self):
        return self.text_preview_left

    def get_preview_text_element_right(self):
        return self.text_preview_right

    def clear_text_preview(self):
        # clear highlighted buttons
        button_list = self.similarity_list_wrapper_widget.children()
        for button in button_list:
            if type(button) is QPushButton:
                button.setStyleSheet("background-color: #F5F5F5")

        # clear text preview
        self.clear_layout(self.text_preview_layout)
        self.text_preview_layout.addStretch()

        # clear song previews
        self.clear_layout(self._left_song_preview)
        self._left_song_preview.addStretch()
        self.clear_layout(self._right_song_preview)
        self._right_song_preview.addStretch()

    def clear_layout(self, layout):
        if layout is None:
            return
        while layout.count():
            child = layout.takeAt(0)
            if child.widget() is not None:
                child.widget().deleteLater()
            elif child.layout() is not None:
                self.clear_layout(child.layout())

    def add_widget_to_text_preview(self, widget):
        self.text_preview_layout.addWidget(widget, self.text_preview_layout.count() - 1)

    def add_widget_to_left_song_preview(self, widget):
        self._left_song_preview.addWidget(widget)

    def add_widget_to_right_song_preview(self, widget):
        self._right_song_preview.addWidget(widget)


def show():
    widget = MainWindow()
    widget.resize(1280, 720)
    widget.show()
    return widget


if __name__ == "__main__":
    show()

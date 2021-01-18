import math

from PySide2.QtCore import Qt
from PySide2.QtGui import QResizeEvent
from PySide2.QtWidgets import (QPushButton, QHBoxLayout, QWidget, QVBoxLayout, QScrollArea, QLayout)

from Song import Song
from gui.SongSimilarity import SongSimilarity


class MainWindow(QWidget):
    def __init__(self):
        """The main window displaying all song similarities"""
        QWidget.__init__(self)

        # Similarity selection
        self.similarity_list_wrapper_widget = QWidget()
        self.similarity_list_layout = QVBoxLayout()
        self.similarity_list_scroll = QScrollArea()

        self.generate_scroll_area(self.similarity_list_layout,
                                  self.similarity_list_wrapper_widget, self.similarity_list_scroll)

        # Text preview
        self.text_preview_wrapper_widget = QWidget()
        self.text_preview_layout = QVBoxLayout()
        self.text_preview_scroll = QScrollArea()

        self.generate_scroll_area(self.text_preview_layout,
                                  self.text_preview_wrapper_widget, self.text_preview_scroll)

        # Left song preview
        self._left_song_preview_wrapper_widget = QWidget()
        self._left_song_preview = QVBoxLayout()
        self._left_song_preview_scroll = QScrollArea()

        self.generate_scroll_area(self._left_song_preview,
                                  self._left_song_preview_wrapper_widget, self._left_song_preview_scroll)

        # Right song preview
        self._right_song_preview_wrapper_widget = QWidget()
        self._right_song_preview = QVBoxLayout()
        self._right_song_preview_scroll = QScrollArea()

        self.generate_scroll_area(self._right_song_preview,
                                  self._right_song_preview_wrapper_widget, self._right_song_preview_scroll)

        # Main layout
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.similarity_list_scroll)
        self.layout.addWidget(self.text_preview_scroll)
        self.layout.addWidget(self._left_song_preview_scroll)
        self.layout.addWidget(self._right_song_preview_scroll)
        self.setLayout(self.layout)

        # Adjust the layouts sizes
        self.adjustSize()
        self.resize(1280, 720)
        self.show()

    def resizeEvent(self, event):
        """Always match the columns size to the windows
        :type event: QResizeEvent
        :param event: Resize event"""
        super().resizeEvent(event)
        self.adjustSize()

    @staticmethod
    def generate_scroll_area(layout, wrapper_widget, scroll_area):
        """Add a scroll area to the given layout
        :type layout: QLayout
        :param layout: The layout the scroll area should be added to
        :type wrapper_widget: QWidget
        :param wrapper_widget: The widget wrapping the layout
        :type scroll_area: QScrollArea
        :param scroll_area: The scroll area to add"""
        layout.addStretch()
        layout.setAlignment(Qt.AlignTop)
        wrapper_widget.setLayout(layout)

        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(wrapper_widget)

    def adjustSize(self):
        """Fit all columns to the windows width"""
        width = self.width()

        self.similarity_list_scroll.setFixedWidth(math.floor(width * 0.2))
        self.text_preview_scroll.setFixedWidth(math.floor(width * 0.3))
        self._left_song_preview_scroll.setFixedWidth(math.floor(width * 0.2))
        self._right_song_preview_scroll.setFixedWidth(math.floor(width * 0.2))

    def load_similarities(self, similarity_list, loaded_song_dict):
        """Show all songs with similarities in the gui
        :type similarity_list: dict[str: list[str]]
        :param similarity_list: All similarities between songs
        :type loaded_song_dict: dict[str: Song]
        :param loaded_song_dict: All loaded song objects"""
        for song_orig, similar_songs_list in similarity_list.items():
            # Replace song file names with actual songs objects
            song_orig = loaded_song_dict[song_orig]
            for i in range(len(similar_songs_list)):
                similar_songs_list[i] = loaded_song_dict[similar_songs_list[i]]
            # Create an object for each similarity
            similarity = SongSimilarity(song_orig, similar_songs_list)
            similarity.set_window(self)
            # Add a button to the 1st column
            self.similarity_list_layout.addWidget(similarity.get_button_widget(),
                                                  self.similarity_list_layout.count() - 1)

    def add_widget_to_text_preview(self, widget):
        """Add a widget to the 2nd column"""
        self.text_preview_layout.addWidget(widget, self.text_preview_layout.count() - 1)

    def clear_text_preview(self):
        """Clear everything from the 2nd column and the selection from the 1st"""
        # Clear highlighted buttons
        button_list = self.similarity_list_wrapper_widget.children()
        for button in button_list:
            if type(button) is QPushButton:
                button.setStyleSheet("background-color: #F5F5F5")

        # Clear text preview
        self.clear_layout(self.text_preview_layout)
        self.text_preview_layout.addStretch()

        # Clear song previews
        self.clear_layout(self._left_song_preview)
        self._left_song_preview.addStretch()
        self.clear_layout(self._right_song_preview)
        self._right_song_preview.addStretch()

    def clear_layout(self, layout):
        """Clear everything from the given layout column"""
        if layout is None:
            return
        while layout.count():
            child = layout.takeAt(0)
            if child.widget() is not None:
                child.widget().deleteLater()
            elif child.layout() is not None:
                self.clear_layout(child.layout())

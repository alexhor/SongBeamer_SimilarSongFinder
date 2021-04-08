from abc import abstractmethod
from typing import List

from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLayout, QLayoutItem
from enum import Enum

from Song import Song
from Subscribable import Subscribable
from gui.SongDetailsDialog import SongDetailsDialog
from gui.SongSimilarityWindow import SongSimilarityWindow


class OrderableListItem(QWidget, Subscribable):
    """Available subscription types"""
    DELETED = 1
    UPDATED = 2
    """Registered subscription callbacks"""
    _subscriptions: dict[int, list[callable]]
    """The widgets layout"""
    _layout: QLayout
    """The items id"""
    id = 0

    def __init__(self):
        # Init QWidget
        super().__init__()
        # Init Subscribable
        Subscribable.__init__(self, (OrderableListItem.DELETED, OrderableListItem.UPDATED))
        self._layout = QVBoxLayout()
        self.setLayout(self._layout)
        # Set and increase id
        self.id = OrderableListItem.id
        OrderableListItem.id += 1

    def delete(self):
        """Delete this item"""
        # Perform deletion subscriptions
        self._trigger_subscriptions(OrderableListItem.DELETED, item=self)
        # Delete all children
        while self._layout.count():
            child: QLayoutItem = self._layout.takeAt(0)
            child_widget: QWidget = child.widget()
            child_widget.deleteLater()
        # Delete the item itself
        self.deleteLater()

    @abstractmethod
    def get_order_string(self):
        """Get the string that this item can be ordered by
        :returns str: The string to order this item by"""
        return ""


class LoadedSongListItem(OrderableListItem):
    """The loaded song"""
    _song: Song
    """The button opening the songs details"""
    _button: QPushButton

    def __init__(self, song):
        """Init gui
        :type song: Song
        :param song: The loaded song
        """
        super().__init__()
        # Add song
        self._song = song
        self._song.subscribe(Song.DELETED, self.delete)
        self._song.subscribe(Song.UPDATED, self._song_updated)
        # Build gui
        self._button = QPushButton(self._song.get_name(), self)
        self._button.clicked.connect(self._show_details_dialog)
        self._layout.addWidget(self._button)
        self._layout.addWidget(self._button)

    def _song_updated(self, song):
        """A song was updated"""
        if song == self._song:
            self._trigger_subscriptions(OrderableListItem.UPDATED, item=self)

    def delete(self, song=None):
        """Delete this item
        :type song: Song
        :param song: This parameter is passed, when the delete call is coming directly from a song
        """
        if None is song or song == self._song:
            super().delete()

    def _show_details_dialog(self):
        """Show the songs details"""
        details_gui = SongDetailsDialog(self._song, self, self.remove_song)
        details_gui.show()

    def remove_song(self):
        """Remove this song from the program"""
        self._song.unload()

    def get_order_string(self):
        """Get the song title this item is ordered by
        :returns str: The song title this item is ordered by"""
        return self._song.get_name().lower()


class SongSimilarityListItem(OrderableListItem):
    """The original song"""
    _song: Song
    """All similar songs"""
    _similar_songs_list: List[Song]
    """The button opening the similarity details"""
    _button: QPushButton

    def __init__(self, similar_songs_list):
        """Init gui
        :type similar_songs_list: List[Song]
        :param similar_songs_list: A group of songs that are similar
        """
        super().__init__()
        # Add similar songs
        self._similar_songs_list = similar_songs_list
        # TODO: Subscribe to song changes
        # Build gui
        self._button = QPushButton(self._similar_songs_list[0].get_name() + '(' + str(len(self._similar_songs_list))
                                   + ')', self)
        self._button.clicked.connect(self._show_details_dialog)
        self._layout.addWidget(self._button)
        self._layout.addWidget(self._button)

    def _song_updated(self, song):
        """A song was updated"""
        if song == self._song:
            self._trigger_subscriptions(OrderableListItem.UPDATED, item=self)

    def delete(self, song=None):
        """Delete this item
        :type song: Song
        :param song: This parameter is passed, when the delete call is coming directly from a song
        """
        if None is song or song == self._song:
            super().delete()

    def _show_details_dialog(self):
        """Show the similarity details"""
        #song_similarity_gui: SongSimilarityWindow = SongSimilarityWindow(self._song, self._similar_songs_list)
        #song_similarity_gui.show()
        #song_similarity_gui.activateWindow()
        pass

    def remove_song(self):
        """Remove this song from the program"""
        self._song.unload()

    def get_order_string(self):
        """Get the song title this item is ordered by
        :returns str: The song title this item is ordered by"""
        return self._similar_songs_list[0].get_name().lower()

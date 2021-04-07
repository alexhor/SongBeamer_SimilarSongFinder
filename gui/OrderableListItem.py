from abc import abstractmethod

from PySide2.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLayout, QLayoutItem
from enum import Enum

from Song import Song
from Subscribable import Subscribable
from gui.SongDetailsDialog import SongDetailsDialog


class OrderableListItem(QWidget, Subscribable):
    """Available subscription types"""
    DELETED = 1
    CHANGED = 2
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
        Subscribable.__init__(self, (OrderableListItem.DELETED, OrderableListItem.CHANGED))
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
        :param song:
        """
        super().__init__()
        self._song = song
        self._button = QPushButton(self._song.get_name(), self)
        self._button.clicked.connect(self._show_details_dialog)
        self._layout.addWidget(self._button)
        self._layout.addWidget(self._button)

    def _show_details_dialog(self):
        """Show the songs details"""
        details_gui = SongDetailsDialog(self._song, self, self.remove_song)
        details_gui.show()

    def remove_song(self):
        """Remove this song from the list"""
        self.delete()
        del self._song

    def get_order_string(self):
        """Get the song title this item is ordered by
        :returns str: The song title this item is ordered by"""
        return self._song.get_name().lower()

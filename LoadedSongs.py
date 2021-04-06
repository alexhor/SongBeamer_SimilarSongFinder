from PySide2.QtCore import Signal

from Song import Song
from Subscribable import Subscribable


class LoadedSongs(Subscribable):
    """Available subscription types"""
    DELETED = 1
    UPDATED = 2
    ADDED = 3
    """All currently loaded song objects"""
    _loadedSongs: dict[str: Song]

    def __init__(self):
        """Init variables"""
        super().__init__((self.DELETED, self.UPDATED, self.ADDED))
        self._loadedSongs = {}
        self.songAdded = Signal(Song)

    def add(self, song):
        """Add a new song
        :type song: Song
        :param song: The song to add"""
        if self._get_song_key(song) not in self._loadedSongs.keys():
            self._loadedSongs[self._get_song_key(song)] = song
            # Subscribe to song changes
            song.subscribe(song.DELETED, self._song_deleted)
            song.subscribe(song.UPDATED, self._song_updated)
            # Trigger own subscriptions
            self._trigger_subscriptions(self.ADDED)

    @staticmethod
    def _get_song_key(song):
        """Get a songs key for the internal list
        :type song: Song
        :param song: The song to get the key for"""
        return str(song)

    def _song_deleted(self, song):
        """A song should be deleted. This is triggered by deleting the song object
        :type song: Song
        :param song: The song to delete"""
        self._loadedSongs.pop(self._get_song_key(song))
        self._trigger_subscriptions(self.DELETED, song=song)

    def _song_updated(self, song):
        """A song was updated
        :type song: Song
        :param song: The song that was updated"""
        self._trigger_subscriptions(self.UPDATED, song=song)

class SongLine:
    # Uniquely ids all song lines
    next_id = 0

    def __init__(self, song_text: str, song):
        """A song line of a song
        :type song_text: str
        :param song_text: The lines text
        :type song: Song.Song
        :param song: The song this line is a part of
        """
        # Set unique id
        self.id = self.next_id
        SongLine.next_id += 1
        # Setup the song line
        self._text = song_text
        self.song = song

    def get_text(self):
        """Get the lines song text
        :return str: The lines song text"""
        return self._text

    def __repr__(self):
        return self._text

    def __eq__(self, other_line):
        return self.id == other_line.id

    def __hash__(self):
        return self.id

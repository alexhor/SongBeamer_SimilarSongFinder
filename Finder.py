from Song import Song
from pathlib import Path

class Finder:
    def __init__(self, song_dir):
        # get all song files in the given directory
        song_file_list = list(Path(song_dir).rglob("*.[[sS][nN][gG]"))
        # convet the files to song objects to hadle them
        self._songs = []
        for song_file in song_file_list:
            self._songs.append(Song(song_file))
            break

Finder("Songs")

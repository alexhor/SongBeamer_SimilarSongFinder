from pathlib import Path

from PySide6.QtWidgets import QWidget, QFileDialog

from Song import Song
from gui.ProgressBar import ProgressBar


class LoadSongsDialog(QFileDialog):
    def __init__(self, parent=None, progress_bar=None):
        """Show a popup with a songs details
        :type parent: QWidget
        :param parent: Parent widget
        :type progress_bar: ProgressBar
        :param progress_bar: The progress bar object tracking the loading progress"""
        # Setup dialog
        super().__init__(parent, 'SongBeamer Files', filter='SongBeamer Files (*.sng)')
        self._progress_bar: ProgressBar = progress_bar
        #self.setWindowModality(Qt.ApplicationModal)

    def get_songs_by_dir(self):
        """Let the user select a directory to load songs from, recursively
        :return List[Song]: All selected song files"""
        self.setFileMode(QFileDialog.Directory)
        self.setOption(QFileDialog.DontUseNativeDialog, True)
        self.setOption(QFileDialog.ShowDirsOnly, False)
        # Make sure a working directory has been selected
        if not self.exec_():
            return []
        working_dir = Path(self.selectedFiles()[0])
        song_file_list = list(working_dir.rglob("*.sng"))
        return self._load_song_file_list(song_file_list)

    def get_songs_by_file(self):
        """Let the user select specific song files to load
        :return List[Song]: All selected song files"""
        self.setFileMode(QFileDialog.ExistingFiles)
        # Make sure files have been selected
        if not self.exec_():
            return []
        song_file_list = self.selectedFiles()
        return self._load_song_file_list(song_file_list)

    def _load_song_file_list(self, song_file_list):
        """Load song objects for the given list of song files
        :type song_file_list: List[str | Path]
        :param song_file_list: The list of song files to load
        :return List[Song]: The list of loaded song objects"""
        song_object_list = []
        song_file: str
        song_count: int = len(song_file_list)
        songs_loaded: int = 0

        for song_file in song_file_list:
            songs_loaded += 1
            # Convert the song file to a path object if necessary
            if type(song_file) == str:
                song_path = Path(song_file)
            else:
                song_path = song_file
            # Load song objects from song files
            song = Song(song_path)
            # Only keep valid song objects
            if not song.valid:
                continue
            song_object_list.append(song)

            # Calculate progress
            percentage_done = songs_loaded / song_count
            percentage_done_nice = round(percentage_done * 100, 2)
            # Command line output
            if self._progress_bar is None:
                print(percentage_done_nice, '%')
            # Gui progress bar
            else:
                self._progress_bar.set_progress.emit(percentage_done_nice)
        # Return collected song objects
        return song_object_list

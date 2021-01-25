import math
import timeit
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from Song import Song
from gui.ProgressBar import ProgressBar


class SimilarityFinder:
    def __init__(self, song_dir, progress_bar=None, main=None):
        """Find similarities between songs in a directory
        :type song_dir: str
        :param song_dir: Directory containing all song files
        :type progress_bar: ProgressBar
        :param progress_bar: The progress bar object tracking the calculation progress
        :type main: Main.Main
        :param main: The programs main class, handling callbacks
        """
        # Init parameters
        self._similarities = {}
        self._loaded_song_dict = {}
        self._songs = pd.DataFrame(columns=['name', 'text'])
        # similarity threshold
        self._cosine_threshold = 0.8
        # Get passed parameters
        self._song_dir = song_dir
        self._progress_bar = progress_bar
        self._main = main

    def run(self):
        """Start the calculations"""
        self.reload_songs()

        # Notify the user that all songs are loaded
        if self._main is not None:
            self._main.song_loading_done.emit()

        # Do the actual calculations
        self.collect_similarities()

        # Notify the user that all calculations have been done
        if self._main is not None:
            self._main.collecting_similarities_done.emit()

    def reload_songs(self):
        """Get all SongBeamer files from the working directory"""
        # Get all song files in the given directory
        song_file_list = list(Path(self._song_dir).rglob("*.[[sS][nN][gG]"))
        # Init parameters
        count = 0
        song_dict = {'name': [], 'text': []}
        # Get the texts from all songs
        for song_file in song_file_list:
            # Parse the song file
            song = Song(song_file)
            # Only process valid song files
            if not song.valid:
                continue
            # Save the song for later use
            self._loaded_song_dict[str(song)] = song
            song_dict['name'].append(str(song))
            song_dict['text'].append(song.get_text_as_line())
            count += 1
        # Prepare all valid songs
        self._songs.name = pd.Series(song_dict['name'])
        self._songs.text = pd.Series(song_dict['text'])

    def replace_indices(self, idx):
        """Replace the indices in all songs
        :type idx: int
        :param idx: Indices to replace"""
        return self._songs['name'].values[idx]

    def collect_similarities(self):
        """Calculate the similarities between all loaded songs"""
        # Prepare for calculations
        timer_start = timeit.default_timer()

        # Transform song vectors
        tfidf = TfidfVectorizer()
        tfidf.fit(self._songs.text)
        tfidf_transform = tfidf.transform(self._songs.text)

        # Subdivide data in batches and process each batch
        batch_size = 2048
        total_batches = math.floor(tfidf_transform.shape[0] / batch_size)
        batch_num = 0
        processing_not_finished = True
        self._similarities = {}
        # Run each bach
        while processing_not_finished:
            start = batch_num * batch_size
            end = start + batch_size
            if end + 1 >= tfidf_transform.shape[0]:
                end = tfidf_transform.shape[0] - 1
                processing_not_finished = False
            song_vec = tfidf_transform[start:end]
            similarities = cosine_similarity(tfidf_transform, song_vec) > self._cosine_threshold
            # Only look at lower triangle of matrix
            similarities = np.tril(similarities, -1)

            if 0 < np.sum(similarities):
                # Get song indices of matching songs
                indices = np.argwhere(similarities)
                # Add start value of batch to column ids for correct ids in dataframe
                indices[:, 1] += batch_num * batch_size
                names = self.replace_indices(indices)
                # Create dict with matching songs
                for song_tuple in names:
                    song_orig = song_tuple[0]
                    song_copy = song_tuple[1]
                    # Add the similarity to the first song
                    if song_orig not in self._similarities:
                        self._similarities[song_orig] = [song_copy]
                    else:
                        self._similarities[song_orig].append(song_copy)
                    # Add the similarity to the second song
                    if song_copy not in self._similarities:
                        self._similarities[song_copy] = [song_orig]
                    else:
                        self._similarities[song_copy].append(song_orig)

            # Update progress if not finished
            if processing_not_finished:
                # Calculate progress
                percentage_done = (batch_num + 1) / total_batches
                percentage_done_nice = round(percentage_done * 100, 2)
                time_elapsed = math.floor(timeit.default_timer() - timer_start)
                time_remaining = math.floor(time_elapsed / percentage_done) - time_elapsed

                # Command line output
                if self._progress_bar is None:
                    print(percentage_done_nice, "%")
                    print('Time: ', time_elapsed, "s")
                # Gui progress bar
                else:
                    self._progress_bar.set_progress.emit(percentage_done_nice, time_elapsed, time_remaining)
            batch_num += 1
        # Get final calculation duration
        timer_stop = timeit.default_timer()
        time_elapsed = math.floor(timer_stop - timer_start)

        # Command line output
        if self._progress_bar is None:
            print("100 %")
            print('Time: ', time_elapsed)
        # Gui progress bar
        else:
            self._progress_bar.set_progress.emit(100, time_elapsed, 0)
            self._progress_bar.close_with_delay()

    def get_similarities(self):
        """Get a list of all calculated similarities
        :return list[list[str]]: All calculated similarities"""
        return self._similarities

    def get_loaded_song_dict(self):
        """All loaded song objects
        :return dict{str: Song.Song}"""
        return self._loaded_song_dict


if __name__ == "__main__":
    finder = SimilarityFinder("Songs")
    finder.run()

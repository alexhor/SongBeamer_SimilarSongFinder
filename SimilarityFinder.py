import math
import timeit
from pathlib import Path
from threading import Thread
from typing import List

import numpy as np
import pandas as pd
from PySide2.QtCore import Signal
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from Song import Song
from gui.ProgressBar import ProgressBar


class SimilarityFinder:
    def __init__(self, song_list, progress_bar=None, calculations_done_signal=None, similarity_threshold=0.4):
        """Find similarities between songs in a directory
        :type song_list: list[Song]
        :param song_list: All song files to compare
        :type progress_bar: ProgressBar
        :param progress_bar: The progress bar object tracking the calculation progress
        :type calculations_done_signal: Signal
        :param calculations_done_signal: The signal to emit to when calculations are done
        :type similarity_threshold: float
        :param similarity_threshold: The threshold of what counts as "similar"
        """
        # Init parameters
        self._similarities = {}
        self._song_lookup = {}
        self._songs = pd.DataFrame(columns=['name', 'text'])
        # Get passed parameters
        self._song_list: List[Song] = song_list
        self._progress_bar: ProgressBar = progress_bar
        self._calculations_done_signal: Signal = calculations_done_signal
        self._cosine_threshold: float = similarity_threshold

        # Run calculations
        finder_thread = Thread(target=self.run, name="Similarity Finder")
        finder_thread.start()

    def run(self):
        """Start the calculations"""
        # Prepare songs
        self.__prepare_songs()
        # Do the actual calculations
        self._collect_similarities()

        # Notify the user that all calculations have been done
        if self._calculations_done_signal is not None:
            self._calculations_done_signal.emit()

    def __prepare_songs(self):
        """Prepare all songs for calculation"""
        # Init parameters
        song_dict: dict = {'name': [], 'text': []}
        # Get the texts from all songs
        for song in self._song_list:
            song: Song
            song_dict['name'].append(str(song))
            song_dict['text'].append(song.get_text_as_line())
            self._song_lookup[str(song)] = song
        # Prepare songs with pandas
        self._songs.name = pd.Series(song_dict['name'])
        self._songs.text = pd.Series(song_dict['text'])

    def __replace_indices(self, idx):
        """Replace the indices in all songs
        :type idx: int
        :param idx: Indices to replace"""
        return self._songs['name'].values[idx]

    def _collect_similarities(self):
        """Calculate the similarities between all loaded songs"""
        # Prepare for calculations
        timer_start = timeit.default_timer()
        self._similarities = {}

        # Transform song vectors
        tfidf = TfidfVectorizer()
        tfidf.fit(self._songs.text)
        tfidf_transform = tfidf.transform(self._songs.text)

        # Subdivide data into batches and process each batch
        batch_size = 2048
        total_batches = math.floor(tfidf_transform.shape[0] / batch_size)
        batch_num = 0
        processing_not_finished = True

        # Run each bach
        while processing_not_finished:
            # Check if this is the last batch
            start = batch_num * batch_size
            end = start + batch_size
            if end + 1 >= tfidf_transform.shape[0]:
                end = tfidf_transform.shape[0] - 1
                processing_not_finished = False

            # Get cosine similarity between songs
            song_vec = tfidf_transform[start:end]
            similarities = cosine_similarity(tfidf_transform, song_vec) > self._cosine_threshold
            # Only look at lower triangle of matrix
            similarities = np.tril(similarities, -1)

            if 0 < np.sum(similarities):
                # Get song indices of matching songs
                indices = np.argwhere(similarities)
                # Add start value of batch to column ids for correct ids in dataframe
                indices[:, 1] += batch_num * batch_size
                names = self.__replace_indices(indices)

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
                    print(percentage_done_nice, '%')
                    print('Time: ', time_elapsed, 's - Left:', time_remaining, 's')
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
            print('Time: ', time_elapsed, 's')
        # Gui progress bar
        else:
            self._progress_bar.set_progress.emit(100, time_elapsed, 0)

    def get_similarities(self):
        """Get a list of all calculated similarities
        :return dict[Song, list[Song]]: All calculated similarities"""
        # Get the corresponding objects to the calculated similarities
        similarities = {}
        for key, similar_song_list in self._similarities.items():
            # Get all similar songs
            song_list = []
            for similar_song in similar_song_list:
                song_list.append(self._song_lookup[similar_song])
            # Add the song and its similarities
            similarities[self._song_lookup[key]] = song_list
        return similarities

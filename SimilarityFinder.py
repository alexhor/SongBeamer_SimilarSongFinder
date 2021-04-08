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

from LoadedSongs import LoadedSongs
from Song import Song
from gui.ProgressBar import ProgressBar


class SimilarityFinder:
    def __init__(self, song_list, progress_bar=None, calculations_done_signal=None, similarity_threshold=0.95):
        """Find similarities between songs in a directory
        :type song_list: LoadedSongs
        :param song_list: All songs to compare
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
        self._song_list: LoadedSongs = song_list
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
        song: Song
        for song in self._song_list:
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
            similarities = cosine_similarity(tfidf_transform, song_vec)
            # Only look at lower triangle of matrix
            similarities = np.tril(similarities, -1)

            if 0 < np.sum(similarities):
                # Get song indices of matching songs
                indices = np.argwhere(similarities > self._cosine_threshold)

                # Add start value of batch to column ids for correct ids in dataframe
                names = indices.copy()
                names[:, 1] += batch_num * batch_size
                names = self.__replace_indices(names)

                # Create dict with matching songs
                for i in range(len(names)):
                    song_tuple = names[i]
                    score_index = indices[i]
                    similarity_score = similarities[score_index[0]][score_index[1]]
                    if not 0.999 > similarity_score:
                        continue
                    song_orig = self._song_lookup[song_tuple[0]]
                    song_copy = self._song_lookup[song_tuple[1]]

                    # Add the similarity to the first song
                    if song_orig not in self._similarities:
                        self._similarities[song_orig] = [{
                            'song': song_copy,
                            'score': similarity_score
                        }]
                    else:
                        self._similarities[song_orig].append({
                            'song': song_copy,
                            'score': similarity_score
                        })
                    # Add the similarity to the second song
                    if song_copy not in self._similarities:
                        self._similarities[song_copy] = [{
                            'song': song_orig,
                            'score': similarity_score
                        }]
                    else:
                        self._similarities[song_copy].append({
                            'song': song_orig,
                            'score': similarity_score
                        })

            # Update progress if not finished
            if processing_not_finished:
                # Calculate progress
                percentage_done = (batch_num + 1) / total_batches
                percentage_done_nice = round(percentage_done * 100, 2)

                # Command line output
                if self._progress_bar is None:
                    print(percentage_done_nice, '%')
                # Gui progress bar
                else:
                    self._progress_bar.set_progress.emit(percentage_done_nice)
            batch_num += 1

        # Command line output
        if self._progress_bar is None:
            print("100 %")
        # Gui progress bar
        else:
            self._progress_bar.set_progress.emit(100)

    def get_similarities(self):
        """Get a list of all calculated similarities
        :return dict[Song, list[dict[str, Song]]]: All calculated similarities"""
        return self._similarities

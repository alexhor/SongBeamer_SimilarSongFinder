import math
import threading
import timeit
from pathlib import Path

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from Song import Song


class Finder:
    def __init__(self, song_dir, progress_bar=None, main=None):
        self._similarities = {}
        self._calculations_done = 0
        self._songs = pd.DataFrame(columns=['name', 'text'])
        # similarity threshold
        self._cosine_threshold = 0.8

        self._progress_bar = progress_bar
        self._main = main
        self._print_lock = threading.Lock()
        self._song_dir = song_dir

    def run(self):
        self.reload_songs()
        self.collect_similarities()

        if self._main is not None:
            self._main.song_loading_done.emit()

    def reload_songs(self):
        # get all song files in the given directory
        song_file_list = list(Path(self._song_dir).rglob("*.[[sS][nN][gG]"))
        # convert the files to song objects to handle them
        count = 0
        song_dict = {'name': [], 'text': []}
        for song_file in song_file_list:
            # if count >= 1000: break
            song = Song(song_file)
            if song.valid:
                song_dict['name'].append(str(song))
                song_dict['text'].append(song.get_text_as_line())
                count += 1

        self._songs.name = pd.Series(song_dict['name'])
        self._songs.text = pd.Series(song_dict['text'])

    def collect_similarities(self):
        # prepare for calculations
        self._calculations_done = 0
        timer_start = timeit.default_timer()

        # calculate similarities
        tfidf = TfidfVectorizer()
        tfidf.fit(self._songs.text)
        tfidf_transform = tfidf.transform(self._songs.text)

        # subdivide data in batches and process each batch
        batch_size = 2048
        total_batches = math.floor(tfidf_transform.shape[0] / batch_size)
        batch_num = 0
        processing_not_finished = True
        self._similarities = {}
        while processing_not_finished:
            start = batch_num * batch_size
            end = start + batch_size
            if end + 1 >= tfidf_transform.shape[0]:
                end = tfidf_transform.shape[0] - 1
                processing_not_finished = False
            song_vec = tfidf_transform[start:end]
            similarities = cosine_similarity(tfidf_transform, song_vec) > self._cosine_threshold
            # only look at lower triangle of matrix
            similarities = np.tril(similarities, -1)

            if np.sum(similarities) > 0:
                # get song indices of matching songs
                indices = np.argwhere(similarities == True)
                # add start value of batch to column ids for correct ids in dataframe
                indices[:, 1] += batch_num * batch_size
                replace_indices = lambda idx: self._songs['name'].values[idx]
                names = replace_indices(indices)
                # create dict with matching songs
                for song_tuple in names:
                    song_orig = song_tuple[0]
                    song_copy = song_tuple[1]
                    if song_orig not in self._similarities:
                        self._similarities[song_orig] = [song_copy]
                    else:
                        self._similarities[song_orig].append(song_copy)

                    if song_copy not in self._similarities:
                        self._similarities[song_copy] = [song_orig]
                    else:
                        self._similarities[song_copy].append(song_orig)

            # update progress if not finished
            if processing_not_finished:
                progress = batch_num * 100 / total_batches
                timer_lap = timeit.default_timer()
                time_elapsed = math.floor(timer_lap - timer_start)
                # command line output
                if self._progress_bar is None:
                    print("comparing songs %d %%" % progress)
                # gui progress bar
                else:
                    self._progress_bar.set_progress.emit(100, time_elapsed, 0)
                    self._progress_bar.close_with_delay()
            batch_num += 1

        timer_stop = timeit.default_timer()
        time_elapsed = math.floor(timer_stop - timer_start)
        self._calculations_done = 1

        # command line output
        if self._progress_bar is None:
            print("100 %")
            print('Time: ', time_elapsed)
        # gui progress bar
        else:
            self._progress_bar.set_progress.emit(100, time_elapsed, 0)
            self._progress_bar.close_with_delay()

    def get_similarities(self):
        return self._similarities


if __name__ == "__main__":
    finder = Finder("Songs")
    finder.run()

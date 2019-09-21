from Song import Song
from pathlib import Path
import timeit, math, pickle, threading
from time import sleep
from gui.song_similarity import song_similarity


class Finder:
    def __init__(self, song_dir, progress_bar=None, main=None):
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
        # convet the files to song objects to hadle them
        self._songs = []
        count = 0
        for song_file in song_file_list:
            #if (count >= 100): break
            song = Song(song_file)
            if (song.valid):
                self._songs.append(song)
                count += 1
        self.calc_similarities()

    def calc_similarities(self):
        # fetch all lines
        self._all_lines_list = []
        for song in self._songs:
            self._all_lines_list.extend(song._song_line_list)

        # prepare for calculationsself
        self._required_calculations = len(self._all_lines_list) ** 2
        self._calculations_done = 0
        self._start = timeit.default_timer()
        # start calculation
        for song in self._songs:
            thread = threading.Thread(target=self.__compare_line, args=(song,))
            thread.setName(song)
            thread.start()
        # wait for calculations to finish
        while True:
            calculation_thread_count = 0
            for thread in threading.enumerate():
                if hasattr(thread, '_target') and thread._target == self.__compare_line:
                    calculation_thread_count += 1
            # no more running threads were found
            if calculation_thread_count == 0:
                break

            sleep(1)

        stop = timeit.default_timer()
        time_elapsed = math.floor(stop - self._start)
        # command line output
        if self._progress_bar is None:
            print("100 %")
            print('Time: ', time_elapsed)
        # gui progress bar
        else:
            self._progress_bar.set_progress.emit(100, time_elapsed, 0)
            self._progress_bar.close_with_delay()

    def __compare_line(self, song):
        for line in song._song_line_list:
            for comparision_line in self._all_lines_list:
                line.similarity(comparision_line)
                self._calculations_done += 1
                # show progress
                if (self._calculations_done % 10000000 == 0 and not self._print_lock.locked()):
                    self._print_lock.acquire()
                    self._update_progress_display()
                    self._print_lock.release()

    def _update_progress_display(self):
        percentage_done = self._calculations_done / self._required_calculations
        percentage_done_nice = round(percentage_done * 100, 2)
        time_elapsed = math.floor(timeit.default_timer() - self._start)
        time_remaining = math.floor(time_elapsed / percentage_done) - time_elapsed

        # command line output
        if self._progress_bar is None:
            print(percentage_done_nice, "%")
            print('Time: ', time_elapsed, "s")
        # gui progress bar
        else:
            self._progress_bar.set_progress.emit(percentage_done_nice, time_elapsed, time_remaining)

    def collect_similarities(self):
        self._similarities = {}

        for song in self._songs:
            for compare_song in self._songs:
                for line in song._song_line_list:
                    if compare_song in line._similarities:
                        if song in self._similarities:
                            similarity = self._similarities[song]
                        elif compare_song in self._similarities:
                            similarity = self._similarities[compare_song]
                        else:
                            similarity = self._similarities[song] = song_similarity(song, compare_song)

                        similarity.addSimilarities(line, line._similarities[compare_song])

    def get_similarities(self):
        return self._similarities.values()


    def __debug(self):
        song = self._songs[0]
        print(song)
        song_line = song._song_line_list[0]
        print(song_line._similarities)


if __name__ == "__main__":
    Finder("Songs")

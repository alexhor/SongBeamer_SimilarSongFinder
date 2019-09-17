from Song import Song
from pathlib import Path
import timeit, math, pickle, threading
from time import sleep


class Finder:
    def __init__(self, song_dir):
        self._print_lock = threading.Lock()
        self._song_dir = song_dir
        self.reload_songs()

    def reload_songs(self):
        # get all song files in the given directory
        song_file_list = list(Path(self._song_dir).rglob("*.[[sS][nN][gG]"))
        # convet the files to song objects to hadle them
        self._songs = []
        count = 0
        for song_file in song_file_list:
            #if (count >= 300): break
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

            sleep(5)

        # display final runtime
        print("100 %")
        stop = timeit.default_timer()
        print('Time: ', math.floor(stop - self._start))

    def __compare_line(self, song):
        for line in song._song_line_list:
            for comparision_line in self._all_lines_list:
                if (line.similarity(comparision_line) != -1):
                    self._calculations_done += 1
                # show progress
                if (self._calculations_done % 1000000 == 0 and not self._print_lock.locked()):
                    self._print_lock.acquire()
                    print(self._calculations_done / self._required_calculations * 100, "%")
                    print('Time: ', math.floor(timeit.default_timer() - self._start))
                    self._print_lock.release()

    def __debug(self):
        song = self._songs[0]
        print(song)
        song_line = song._song_line_list[0]
        print(song_line._similarities)

Finder("Songs")

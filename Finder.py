from Song import Song
from pathlib import Path
import timeit, math, pickle


class Finder:
    def __init__(self, song_dir):
        self._song_dir = song_dir
        # check if there are any old results to load
        try:
            with open("save.txt", "rb") as fp:
                self._songs = pickle.load(fp)
                pass
        except:
            self.reload_songs()

    def reload_songs(self):
        # get all song files in the given directory
        song_file_list = list(Path(self._song_dir).rglob("*.[[sS][nN][gG]"))
        # convet the files to song objects to hadle them
        self._songs = []
        for song_file in song_file_list:
            song = Song(song_file)
            if (song.valid):
                self._songs.append(song)
            count += 1
        self.calc_similarities()
        self.save_results()

    def calc_similarities(self):
        # fetch all lines
        all_lines_list = []
        count = 0
        for song in self._songs:
            if (count >= 100): break
            all_lines_list.extend(song._song_line_list)
            count += 1

        # prepare for calculations
        required_calculations = len(all_lines_list) ** 2
        calculations_done = 0
        start = timeit.default_timer()
        # start calculation
        for line in all_lines_list:
            for comparision_line in all_lines_list:
                line.similarity(comparision_line)
                calculations_done += 1
                # show progress
                if (calculations_done % 1000000 == 0):
                    print(calculations_done / required_calculations * 100, "%")
                    print('Time: ', math.floor(timeit.default_timer() - start))
        # wrap up calculation
        stop = timeit.default_timer()
        print('Time: ', math.floor(stop - start))

    def save_results(self):
        with open("save.txt", "wb") as fp:
            pickle.dump(self._songs, fp)

    def __debug(self):
        song = self._songs[0]
        print(song)
        song_line = song._song_line_list[0]
        print(song_line._similarities)

Finder("Songs")

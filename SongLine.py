import Levenshtein

class Line:
    def __init__(self, song_text, song):
        self._text = song_text
        self.song = song

    def get_text(self):
        return self._text
    
    def similarity(self, line_to_compare_to):
        # comparing two lines of the same song is stupid
        if(self.song == line_to_compare_to.song): return 0
        # get a comparisin score
        return Levenshtein.ratio(self.get_text(), line_to_compare_to.get_text())

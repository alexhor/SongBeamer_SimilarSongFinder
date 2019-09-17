import Levenshtein


class Line:
    def __init__(self, song_text, song):
        self._text = song_text
        self.song = song
        self._similarities = {}

    def get_text(self):
        return self._text

    def similarity(self, line_to_compare_to):
        # comparing two lines of the same song is stupid
        if(self.song == line_to_compare_to.song):
            return 0

        # get a comparison score
        similarity = Levenshtein.ratio(self.get_text(), line_to_compare_to.get_text())

        if (similarity <= 0.8): return 0

        # remember this comparison
        self._save_line_comparison(self, line_to_compare_to, similarity)
        self._save_line_comparison(line_to_compare_to, self, similarity)

        return similarity

    def _save_line_comparison(self, original_line, comparison_line, score):
        # create an dictionary entry for the compared song
        if (comparison_line.song not in original_line._similarities):
            original_line._similarities[comparison_line.song] = {}
        # add the lines score
        if (comparison_line not in original_line._similarities[comparison_line.song]):
            original_line._similarities[comparison_line.song][comparison_line] = score

    def __repr__(self):
        return self._text

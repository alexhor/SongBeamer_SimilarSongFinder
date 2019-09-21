from SongLine import Line
import re


class Song:
    supported_verse_heading_list = ["Unbekannt", "Unbenannt", "Unknown",
                                    "Intro", "Vers", "Verse", "Strophe",
                                    "Pre-Bridge", "Bridge", "Misc",
                                    "Pre-Refrain", "Refrain", "Pre-Chorus",
                                    "Chorus", "Pre-Coda", "Zwischenspiel",
                                    "Instrumental", "Interlude", "Coda",
                                    "Ending", "Outro", "Teil", "Part", "Chor",
                                    "Solo"]

    def __init__(self, song_file):
        self.valid = False
        self._song_file = song_file
        self._song_line_list = []
        # read file line by line and convert them into song lines
        try:
            with open(song_file, encoding='Windows-1252') as file:
                content = file.readlines()
            self.read_lines(content)
            self.valid = True
        except:
            print("Error reading file", song_file._str)

    def read_lines(self, content):
        header_has_ended = False
        verse_ended_in_last_line = False

        for line in content:
            line_is_songtext = True
            line = line.strip()

            # skip empty lines
            if(line == ""): continue

            # check if we are still in the heading
            if(not header_has_ended and line[0] == "#"): continue
            else: header_has_ended = True

            # check if a verse has just ended
            if(line == "--" or line == "---"):
                verse_ended_in_last_line = True
                continue

            # check if this is a verse heading
            if(verse_ended_in_last_line):
                # filter out custom marker
                if(line[0:3] == "$$M="):
                    line_is_songtext = False
                else:
                    split_line = line.split(' ', 1 )
                    # check for a verse heading
                    verse_heading = split_line[0]

                    if(len(split_line) == 2): heading_number = split_line[1]
                    else: heading_number = ""

                    if((verse_heading in self.supported_verse_heading_list and
                            (heading_number == "" or re.search("^[0-9][a-z]?$", heading_number))) or
                            ((verse_heading == "Part" or verse_heading == "Teil") and
                            re.search("^[A-Z]$", heading_number))):
                        line_is_songtext = False

            # remove markers
            if(line_is_songtext):
                if(line[0:3] == "#C " or line[0:3] == "#H "):
                    line = line[3:]
                elif(re.search("^##[0-9] ", line)):
                    line = line[4:]

            # check if the line has passed all tests and can be converted to a song line
            if(line_is_songtext):
                self._song_line_list.append(Line(line, self))

            # reset variables
            verse_ended_in_last_line = False

    def __repr__(self):
        return self._song_file.name

    def __add__(self, other):
        return self.__repr__() + other

    def __radd__(self, other):
        return other + self.__repr__()

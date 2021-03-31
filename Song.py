from pathlib import Path

from SongLine import SongLine
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
    # To uniquely identify each song
    next_id = 0

    def __init__(self, song_file):
        """Extract a song from the given file
        :type song_file: Path
        :param song_file: Path to the file to extract from"""
        # Set unique id
        self.id = self.next_id
        Song.next_id += 1
        # Setup song
        self.valid = False
        self._song_file = song_file
        self._song_line_list = []
        # Read file line by line and convert them into song lines
        try:
            with open(song_file, encoding='Windows-1252') as file:
                content = file.readlines()
            self._read_lines(content)
            # After
            self.valid = True
        except (UnicodeDecodeError, FileNotFoundError):
            print("Error reading file", song_file)

    def _read_lines(self, content):
        """Parse the given song file content into valid song lines
        :type content: list[str]
        :param content: All lines of a song file"""
        header_has_ended = False
        verse_ended_in_last_line = False

        # Go through the file line by line
        line: str
        for line in content:
            line_is_song_text = True
            line = line.strip()

            # Skip empty lines
            if "" == line:
                continue

            # Check if we are still in the heading
            if not header_has_ended and "#" == line[0]:
                continue
            else:
                header_has_ended = True

            # Check if a verse has just ended
            if "--" == line or "---" == line:
                verse_ended_in_last_line = True
                continue

            # Check if this is a verse heading
            if verse_ended_in_last_line:
                # Filter out custom marker
                if "$$M=" == line[0:3]:
                    line_is_song_text = False
                else:
                    split_line = line.split(' ', 1)
                    # Check for a verse heading
                    verse_heading = split_line[0]

                    if 2 == len(split_line):
                        heading_number = split_line[1]
                    else:
                        heading_number = ""

                    if ((verse_heading in self.supported_verse_heading_list and
                         ("" == heading_number or re.search("^[0-9][0-9]?[a-z]?$", heading_number))) or
                            (("Part" == verse_heading or "Teil" == verse_heading) and
                             re.search("^[A-Z]$", heading_number))):
                        line_is_song_text = False

            # Remove markers
            if line_is_song_text:
                if "#C " == line[0:3] or "#H " == line[0:3]:
                    line = line[3:]
                elif re.search("^##[0-9] ", line):
                    line = line[4:]

            # Check if the line has passed all tests and can be converted to a song line
            if line_is_song_text:
                self._song_line_list.append(SongLine(line, self))

            # Reset variables
            verse_ended_in_last_line = False

    def get_line_list(self):
        """Get the list of all song lines
        :return list[SongLine]: The song line list
        :raises ReferenceError"""
        if not self.valid:
            raise ReferenceError('Song is not valid')
        return self._song_line_list

    def get_text(self):
        """Get the songs text as a multiline text
        :return str: The songs text as multiline
        :raises ReferenceError"""
        if not self.valid:
            raise ReferenceError('Song is not valid')
        return '\n'.join(str(line) for line in self._song_line_list)

    def get_text_as_line(self):
        """Get the songs text as one line
        :return str: The songs text as one line
        :raises ReferenceError"""
        if not self.valid:
            raise ReferenceError('Song is not valid')
        return ' '.join(str(line) for line in self._song_line_list)

    def get_name(self):
        """Get the songs name
        :return str: The songs name
        :raises ReferenceError"""
        if not self.valid:
            raise ReferenceError('Song is not valid')
        return self._song_file.name

    def __repr__(self):
        if not self.valid:
            raise ReferenceError('Song is not valid')
        return str(self._song_file)

    def __hash__(self):
        if not self.valid:
            raise ReferenceError('Song is not valid')
        return self.id

    def __eq__(self, other_song):
        # Only valid songs can be compared
        if not self.valid:
            return False
        # Compare to other song object
        if type(other_song) == Song:
            other_song: Song
            return self._song_file == other_song._song_file
        # Compare to string
        elif type(other_song) == str:
            other_song: str
            return self._song_file == other_song
        # Default
        else:
            return False

    def unload(self):
        """Unload this song from the program"""
        self.valid = False
        self._song_file = ''
        self._song_line_list = []

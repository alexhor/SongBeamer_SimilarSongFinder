﻿using Eto.Forms;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading.Tasks;

namespace SongSimilarityFinder
{
    public class SongLoader
    {
        /// <summary>
        /// A dialog to select a folder to load songs from
        /// </summary>
        protected OpenFileDialog fileDialog = new OpenFileDialog()
        {
            CheckFileExists = true,
            Title = "Load Songs",
            MultiSelect = true,
        };

        /// <summary>
        /// A parent control for a SelectFolderDialog
        /// </summary>
        protected readonly Control ParentControl;

        /// <summary>
        /// Manager for tracking song loading tasks
        /// </summary>
        protected readonly TaskTrackerManager TaskTrackerManager;

        /// <summary>
        /// A handler class to load song files into song classes
        /// </summary>
        /// <param name="parentControl">A parent control for a the file dialog</param>
        /// <param name="taskTrackerManager">Manager for tracking song loading tasks</param>
        public SongLoader(Control parentControl, TaskTrackerManager taskTrackerManager)
        {
            ParentControl = parentControl;
            TaskTrackerManager = taskTrackerManager;

            // Allow only SongBeamer files to be selected
            FileFilter fileFilter = new FileFilter("SongBeamer files (*.sng)", "*.sng");
            fileDialog.Filters.Insert(0, fileFilter);
        }

        protected IList<Song> LoadedSongList = new List<Song>();

        /// <summary>
        /// Show a dialog to load song files
        /// </summary>
        public void LoadSongs()
        {
            // Let the user choose song files
            DialogResult result = fileDialog.ShowDialog(ParentControl);

            // Only continue if files were selected
            if (DialogResult.Ok != result && DialogResult.Yes != result || 0 == fileDialog.Filenames.Count())
            {
                return;
            }

            // Run async
            Task.Factory.StartNew(() =>
            {
                int fileCount = fileDialog.Filenames.Count();

                // Start tracking this task
                TaskTracker tracker = TaskTrackerManager.NewTask(string.Format("Loading {0:D} songs", fileCount));
                tracker.SetMaxSteps(fileCount);

                // Load all selected filenames
                foreach (string fileLocation in fileDialog.Filenames)
                {
                    LoadedSongList.Add(LoadSong(fileLocation));
                    // Update the task tracker
                    tracker.DoStep();
                }

                // Terminate the task tracker
                tracker.TaskDone();
            });
        }

        /// <summary>
        /// Load a song class from the given file location
        /// </summary>
        /// <param name="fileLocation">Location to load a song class from</param>
        /// <exception cref="FileNotFoundException">If the given songfile doesn't exist</exception>
        /// <returns>An object representing the songfile</returns>
        protected Song LoadSong(string fileLocation)
        {
            // Make sure the file exists
            if (!File.Exists(fileLocation)) throw new FileNotFoundException();

            // Create the song
            Song song = new Song(fileLocation);
            IList<SongLine> songLines = new List<SongLine>();

            State readerState = State.SongHeading;
            bool readNextLine = true;
            string currentLine = "";
            using (StreamReader reader = new StreamReader(fileLocation, CodePagesEncodingProvider.Instance.GetEncoding(1252)))
            {
                // Loop the file line by line
                while (!reader.EndOfStream)
                {
                    if (readNextLine) currentLine = reader.ReadLine();
                    readNextLine = true;

                    // skip empty lines
                    if (currentLine == "") continue;

                    if (State.SongHeading == readerState)
                    {
                        // Another heading line
                        if ('#' == currentLine[0])
                        {
                            FilterSongInfo(currentLine);
                            continue;
                        }
                        // The heading has ended and we can now read verses
                        else
                        {
                            readerState = State.VerseEnded;
                            readNextLine = false;
                            continue;
                        }
                    }

                    // Skip verse headings
                    if (State.VerseEnded == readerState && IsVerseHeading(currentLine))
                    {
                        readerState = State.VerseHeading;
                        continue;
                    }

                    if (State.VerseEnded == readerState || State.VerseHeading == readerState)
                    {
                        // Check if a verse has just ended
                        if (currentLine.StartsWith("---") || currentLine.StartsWith("--"))
                        {
                            readerState = State.VerseEnded;
                            continue;
                        }

                        // Ignore custom markers
                        if (currentLine.StartsWith("$$M=")) continue;

                        // At this point it is a valid song line

                        // Strip markers
                        if (currentLine.StartsWith("#C ") || currentLine.StartsWith("#H ")) currentLine = currentLine.Substring(3);
                        else if (Regex.IsMatch(currentLine, "^##[0-9] ")) currentLine = currentLine.Substring(4);

                        // Store the song line
                        SongLine line = new SongLine(currentLine, song);
                        songLines.Add(line);
                    }
                }
            }

            song.LoadLines(songLines);
            return song;
        }

        /// <summary>
        /// Checks if the given line is a verse heading
        /// </summary>
        /// <param name="line">The line to check</param>
        /// <returns>Whether the line is a verse heading</returns>
        private bool IsVerseHeading(string line)
        {
            string[] splitLine = line.Split(' ');
            if (2 < splitLine.Length) return false;

            // Split the actual hading and a possibly following number or letter
            string verseHeading = splitLine[0];
            string headingNumber = 2 == splitLine.Length ? splitLine[1] : "";

            if ((SupportedVerseHeadingList.Contains(verseHeading) && ("" == headingNumber || Regex.IsMatch(headingNumber, "^[0-9][0-9]?[a-z]?$")))
                ||
                (SupportedAlphaVerseHeadingList.Contains(verseHeading) && Regex.IsMatch(headingNumber, "^[A-Z]$")))
            {
                return true;
            }

            // No objections were raised, so this isn't a verse heading
            return false;
        }

        protected void FilterSongInfo(string currentLine)
        {
            //throw new NotImplementedException();
        }

        protected enum State
        {
            SongHeading,
            VerseEnded,
            VerseHeading,
        }

        /// <summary>
        /// All accepted verse headings that can be followed by [00-99] or [a-z]
        /// </summary>
        protected static string[] SupportedVerseHeadingList = new string[25]
        {
            "Unbekannt", "Unbenannt", "Unknown", "Intro", "Vers", "Verse", "Strophe",
            "Pre-Bridge", "Bridge", "Misc", "Pre-Refrain", "Refrain", "Pre-Chorus",
            "Chorus", "Pre-Coda", "Zwischenspiel", "Instrumental", "Interlude", "Coda",
            "Ending", "Outro", "Teil", "Part", "Chor", "Solo"
        };

        /// <summary>
        /// All accepted verse headings that have to be followed by [A-Z]
        /// </summary>
        protected static string[] SupportedAlphaVerseHeadingList = new string[2]
        {
            "Part", "Teil"
        };
    }
}
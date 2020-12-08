using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Threading.Tasks;

namespace SongSimilarityFinder
{
    /// <summary>
    /// Finds similarities between a list of songs
    /// </summary>
    public class SimilarityFinder
    {
        /// <summary>
        /// Manager for tracking running tasks
        /// </summary>
        protected readonly TaskTrackerManager TaskTrackerManager;

        /// <summary>
        /// Whether or not a comparison task is currently running
        /// </summary>
        protected bool ComparisonIsRunning = false;

        /// <summary>
        /// Indicates if the song list has been updated while the comparison task was running
        /// </summary>
        protected bool SongListUpdated = false;

        /// <summary>
        /// The tracker for tracking the comparison tasks progress
        /// </summary>
        protected TaskTracker ComparisonTaskTracker = new EmptyTaskTracker();

        /// <summary>
        /// A list of all available songs
        /// </summary>
        protected readonly HashSet<Song> AllSongs = new HashSet<Song>();

        /// <summary>
        /// Finds similarities between a list of songs
        /// </summary>
        /// <param name="taskTrackerManager">Manager for tracking running tasks</param>
        public SimilarityFinder(TaskTrackerManager taskTrackerManager)
        {
            TaskTrackerManager = taskTrackerManager;
        }

        /// <summary>
        /// Add new songs to compare
        /// </summary>
        /// <param name="songList">The song list to load</param>
        internal void LoadSongList(IEnumerable<Song> songList)
        {
            HashSet<Song> newSongSet = new HashSet<Song>(songList);
            AllSongs.UnionWith(newSongSet);
            if (ComparisonIsRunning) SongListUpdated = true;
        }

        /// <summary>
        /// Start looking for similarities
        /// </summary>
        internal void Start()
        {
            // Only one task should be running
            if (ComparisonIsRunning) return;
            else
            {
                ComparisonIsRunning = true;
                SongListUpdated = false;
            }

            // Start a tracker if none is running
            if (ComparisonTaskTracker is EmptyTaskTracker) ComparisonTaskTracker = TaskTrackerManager.NewTask("Finding Song Similarities");

            Task.Factory.StartNew(() =>
            {
                Stopwatch stopwatch = new Stopwatch();
                stopwatch.Start();

                // Get a snapshot of all currently loaded songs
                Song[] songList = new Song[AllSongs.Count];
                AllSongs.CopyTo(songList);
                int length = songList.Length * songList.Length;
                ComparisonTaskTracker.SetMaxSteps(length);

                // Loop all songs with themselves
                foreach (Song songA in songList)
                {
                    foreach (Song songB in songList)
                    {
                        ComparisonTaskTracker.DoStep();
                        if (songA == songB) continue;

                        SongDiff diff = new SongDiff(songA, songB);
                        float score = diff.GetDiffRelativeScore();
                    }
                }

                // Cleanup
                ComparisonIsRunning = false;
                if (SongListUpdated) Start();
                else
                {
                    ComparisonTaskTracker.TaskDone();
                    ComparisonTaskTracker = new EmptyTaskTracker();
                }

                stopwatch.Stop();
                long elapsedMsc = stopwatch.ElapsedMilliseconds;
            });
        }
    }
}

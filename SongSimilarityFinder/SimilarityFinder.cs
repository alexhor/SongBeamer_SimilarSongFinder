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
        /// All already calculated song differences
        /// </summary>
        private readonly IDictionary<Song, IDictionary<Song, float>> CalculatedDiffs = new Dictionary<Song, IDictionary<Song, float>>();

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
                // Get a snapshot of all currently loaded songs
                Song[] songList = new Song[AllSongs.Count];
                AllSongs.CopyTo(songList);
                ComparisonTaskTracker.SetMaxSteps(songList.Length);

                // Loop all songs with themselves
                Parallel.ForEach(songList, songA =>
                {
                    foreach (Song songB in songList)
                    {
                        if (songA == songB) continue;

                        // Check if this was already calculated
                        if (HasDiff(songA, songB)) continue;

                        SongDiff diff = new SongDiff(songA, songB);
                        float score = diff.GetDiffRelativeScore();
                        SetDiff(songA, songB, score);
                    }
                    ComparisonTaskTracker.DoStep();
                });

                // Cleanup
                ComparisonIsRunning = false;
                if (SongListUpdated) Start();
                else
                {
                    ComparisonTaskTracker.TaskDone();
                    ComparisonTaskTracker = new EmptyTaskTracker();
                }
            });
        }

        /// <summary>
        /// Save the calcualted diff between two songs
        /// </summary>
        /// <param name="songA">First song</param>
        /// <param name="songB">Second song</param>
        /// <param name="diff">Diff score between the two songs</param>
        private void SetDiff(Song songA, Song songB, float diff)
        {
            Song[] songList = new Song[2] { songA, songB };

            lock (CalculatedDiffs)
            {
                for (int i = 0; i <= 1; i++)
                {
                    if (!CalculatedDiffs.ContainsKey(songList[i])) CalculatedDiffs[songList[i]] = new Dictionary<Song, float>();
                    CalculatedDiffs[songList[i]][songList[1 - i]] = diff;
                }
            }
        }

        /// <summary>
        /// Checks if a diff between these two songs has already been calculated
        /// </summary>
        /// <param name="songA">First song</param>
        /// <param name="songB">Second song</param>
        /// <returns>Whether or not this difference has been calculated before</returns>
        private bool HasDiff(Song songA, Song songB)
        {
            lock (CalculatedDiffs)
            {
                return CalculatedDiffs.ContainsKey(songA) && CalculatedDiffs[songA].ContainsKey(songB) && CalculatedDiffs.ContainsKey(songB) && CalculatedDiffs[songB].ContainsKey(songA);
            }
        }
    }
}

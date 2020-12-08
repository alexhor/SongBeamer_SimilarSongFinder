using System;
using System.Collections.Generic;
using Eto.Forms;
using Eto.Drawing;
using System.Text;
using System.Diagnostics;

namespace SongSimilarityFinder
{
    public class MainForm : Form
    {
        /// <summary>
        /// Tracker for all running tasks
        /// </summary>
        public TaskTrackerManager TaskTrackerManager { get; protected set; }

        /// <summary>
        /// Song file loading handler
        /// </summary>
        public readonly SongLoader SongLoader;

        /// <summary>
        /// The object in charge of finding similarities between songs
        /// </summary>
        public readonly SimilarityFinder SimilarityFinder;

        /// <summary>
        /// All gui elements
        /// </summary>
        protected DynamicLayout mainLayout;
        protected Control runningTasksWrapper;

        /// <summary>
        /// The programs main and starting window
        /// </summary>
        public MainForm()
        {
            // Init all objects
            TaskTrackerManager = new TaskTrackerManager();
            runningTasksWrapper = TaskTrackerManager.GetWrapper();
            SongLoader = new SongLoader(this, TaskTrackerManager);
            SimilarityFinder = new SimilarityFinder(TaskTrackerManager);

            // Init the gui
            Title = "Song Similarity Finder";
            ClientSize = new Size(600, 400);
            Padding = new Padding(10);
            BuildBaseGui();
            BuildMenuBar();
        }

        /// <summary>
        /// Build the forms basic gui elements
        /// </summary>
        protected void BuildBaseGui()
        {
            Content = mainLayout = new DynamicLayout();
            mainLayout.BeginVertical();
            mainLayout.BeginHorizontal();
            mainLayout.Add(runningTasksWrapper);
            mainLayout.EndHorizontal();
            mainLayout.EndVertical();
        }

        /// <summary>
        /// Build this forms menu bar
        /// </summary>
        protected void BuildMenuBar()
        {
            Menu = new MenuBar
            {
                Items =
                {
                    new ButtonMenuItem
                    {
                        Text = "Songs",
                        Items =
                        {
                            new ButtonMenuItem(HandleLoadSongs) { Text = "Load" },
                            new ButtonMenuItem(HandleFindSimilarities) { Text = "Find Similarities" },
                        }
                    }
                },
                AboutItem = new ButtonMenuItem(HandleAbout) { Text = "About" },
            };
        }

        /// <summary>
        /// Trigger actions to find similarities between all currently loaded songs
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        protected void HandleFindSimilarities(object sender, EventArgs e)
        {
            SimilarityFinder.Start();
        }

        /// <summary>
        /// Trigger actions to let the user load song files
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        protected void HandleLoadSongs(object sender, EventArgs e)
        {
            TaskTracker tracker = SongLoader.LoadSongs();
            // Push the new songs to the similarity finder
            if (tracker is EmptyTaskTracker) return;
            tracker.RegisterCallback(TaskTracker.CallbackType.OnDone, () =>
            {
                IEnumerable<Song> songList = SongLoader.GetSongList();
                SimilarityFinder.LoadSongList(songList);
            });
        }

        /// <summary>
        /// Show the about dialog
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        protected void HandleAbout(object sender, EventArgs e)
        {
            new AboutDialog().ShowDialog(this);
        }
    }
}

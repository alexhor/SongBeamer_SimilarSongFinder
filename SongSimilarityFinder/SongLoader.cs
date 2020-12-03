using Eto.Forms;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text;
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
                    LoadSong(fileLocation);
                    // Update the task tracker
                    tracker.DoStep();
                }

                // Terminate the task tracker
                tracker.TaskDone();
                Debug.WriteLine("{0:D} songs loaded", fileDialog.Filenames.Count());
            });
        }

        /// <summary>
        /// Load a song class from the given file location
        /// </summary>
        /// <param name="fileLocation">Location to load a song class from</param>
        protected void LoadSong(string fileLocation)
        {
            System.Threading.Thread.Sleep(1000);
            // TODO: load the song
            Debug.WriteLine(fileLocation);
        }
    }
}

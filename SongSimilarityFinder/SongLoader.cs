using Eto.Forms;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text;

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
        protected readonly Control parentControl;

        /// <summary>
        /// A handler class to load song files into song classes
        /// </summary>
        /// <param name="parentControl">A parent control for a the file dialog</param>
        public SongLoader(Control parentControl)
        {
            this.parentControl = parentControl;

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
            DialogResult result = fileDialog.ShowDialog(parentControl);

            // Only continue if files were selected
            if (DialogResult.Ok != result && DialogResult.Yes != result || 0 == fileDialog.Filenames.Count())
            {
                return;
            }

            // Load all selected filenames
            foreach (string fileLocation in fileDialog.Filenames)
            {
                LoadSong(fileLocation);
            }
        }

        /// <summary>
        /// Load a song class from the given file location
        /// </summary>
        /// <param name="fileLocation">Location to load a song class from</param>
        protected void LoadSong(string fileLocation)
        {
            throw new NotImplementedException();
        }
    }
}

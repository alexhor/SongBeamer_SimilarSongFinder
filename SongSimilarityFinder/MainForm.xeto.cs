using System;
using System.Collections.Generic;
using Eto.Forms;
using Eto.Drawing;
using Eto.Serialization.Xaml;

namespace SongSimilarityFinder
{
    public class MainForm : Form
    {
        /// <summary>
        /// Song file loading handler
        /// </summary>
        public readonly SongLoader songLoader;

        /// <summary>
        /// The programs main and starting window
        /// </summary>
        public MainForm()
        {
            XamlReader.Load(this);
            songLoader = new SongLoader(this);
        }

        /// <summary>
        /// Trigger actions to find similarities between all currently loaded songs
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        protected void HandleFindSimilarities(object sender, EventArgs e)
        {
            MessageBox.Show("Findig Similarities");
        }

        /// <summary>
        /// Trigger actions to let the user load song files
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        protected void HandleLoadSongs(object sender, EventArgs e)
        {
            songLoader.LoadSongs();
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

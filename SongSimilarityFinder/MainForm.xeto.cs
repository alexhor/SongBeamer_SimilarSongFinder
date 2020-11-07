using System;
using System.Collections.Generic;
using Eto.Forms;
using Eto.Drawing;
using Eto.Serialization.Xaml;

namespace SongSimilarityFinder
{
    public class MainForm : Form
    {
        public MainForm()
        {
            XamlReader.Load(this);
        }

        protected void HandleFindSimilarities(object sender, EventArgs e)
        {
            MessageBox.Show("Findig Similarities");
        }

        protected void HandleLoadSongs(object sender, EventArgs e)
        {
            MessageBox.Show("Load Songs");
        }

        protected void HandleAbout(object sender, EventArgs e)
        {
            new AboutDialog().ShowDialog(this);
        }
    }
}

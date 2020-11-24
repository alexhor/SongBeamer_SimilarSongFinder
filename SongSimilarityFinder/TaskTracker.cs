using Eto.Forms;
using System;
using System.Collections.Generic;
using System.Text;

namespace SongSimilarityFinder
{
    public class TaskTracker
    {
        /// <summary>
        /// The gui control the tasks should be tracked in
        /// </summary>
        protected Control GuiWrapper;

        /// <summary>
        /// Track active tasks and their progress in a gui
        /// </summary>
        /// <param name="guiWrapper">The gui control the tasks should be tracked in</param>
        public TaskTracker(Control guiWrapper)
        {
            GuiWrapper = guiWrapper;
        }
    }
}

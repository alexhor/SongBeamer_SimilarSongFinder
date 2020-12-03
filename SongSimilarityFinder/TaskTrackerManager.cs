using Eto.Forms;
using System;
using System.Collections.Generic;
using System.Text;

namespace SongSimilarityFinder
{
    public class TaskTrackerManager
    {
        /// <summary>
        /// The gui control the tasks should be tracked in
        /// </summary>
        protected StackLayout GuiWrapper = new StackLayout();

        /// <summary>
        /// Returns the wrapper all tasks are displayed in
        /// </summary>
        public Control GetWrapper() => GuiWrapper;

        /// <summary>
        /// All currently running tracker
        /// </summary>
        protected IList<TaskTracker> ActiveTracker = new List<TaskTracker>();

        /// <summary>
        /// Track active tasks and their progress in a gui
        /// </summary>
        public TaskTrackerManager()
        {

        }

        /// <summary>
        /// Creates a new task tracker
        /// </summary>
        /// <param name="label">Description for this task</param>
        /// <param name="Indeterminate">Whether the tasks progress is currently unknown</param>
        /// <returns>The newly created task tracker</returns>
        public TaskTracker NewTask(string label, bool Indeterminate = true)
        {
            TaskTracker tracker = new TaskTracker(this, label, Indeterminate);
            ActiveTracker.Add(tracker);
            Application.Instance.Invoke(() =>
            {
                GuiWrapper.Items.Add(tracker.GuiControl);
            });
            return tracker;
        }

        /// <summary>
        /// Remove a task tracker
        /// </summary>
        /// <param name="tracker">The task tracker to remvoe</param>
        public void RemoveTracker(TaskTracker tracker)
        {
            // Remove from gui (normal Items.Remove doesn't work)
            int i = 0;
            foreach (StackLayoutItem item in GuiWrapper.Items)
            {
                if (item.Control == tracker.GuiControl)
                {
                Application.Instance.Invoke(() =>
                {
                    GuiWrapper.Items.RemoveAt(i);
                });
                    break;
                }
                i++;
            }

            // Remove from the managers internal list
            ActiveTracker.Remove(tracker);
        }
    }
}

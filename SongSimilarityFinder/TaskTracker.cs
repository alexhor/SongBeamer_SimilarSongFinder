using Eto.Forms;
using System;
using System.Threading.Tasks;

namespace SongSimilarityFinder
{
    /// <summary>
    /// Track a tasks progress
    /// </summary>
    public class TaskTracker
    {
        /// <summary>
        /// The gui element displaying the tasks progress
        /// </summary>
        protected ProgressBar ProgressBar;

        /// <summary>
        /// The trackers gui representation
        /// </summary>
        public Control GuiControl;

        /// <summary>
        /// The trackers descriptive label
        /// </summary>
        protected Label LabelControl;

        /// <summary>
        /// How many steps it takes to complete this task
        /// </summary>
        protected int MaxSteps = 100;

        /// <summary>
        /// How many steps have been completed so far
        /// </summary>
        protected int CurrentStep = 0;

        protected readonly TaskTrackerManager Manager;

        /// <summary>
        /// Create the task trackers gui representation
        /// </summary>
        /// <param name="manager">The manager for this tracker</param>
        /// <param name="label">Description for this task</param>
        /// <param name="Indeterminate">Whether the tasks progress is currently unknown</param>
        public TaskTracker(TaskTrackerManager manager, string label, bool Indeterminate = true)
        {
            Manager = manager;
            Application.Instance.Invoke(() => {
                // Layout wrapper
                StackLayout wrapper = new StackLayout()
                {
                    Orientation = Orientation.Horizontal,
                };

                // Tasks label
                LabelControl = new Label()
                {
                    Text = label,
                };
                wrapper.Items.Add(LabelControl);

                // Progress bar
                ProgressBar = new ProgressBar()
                {
                    Indeterminate = Indeterminate,
                    Value = CurrentStep,
                };
                wrapper.Items.Add(ProgressBar);

                // Add finished wrapper
                GuiControl = wrapper;
            });
        }

        /// <summary>
        /// Set the total amount of steps this task requires
        /// </summary>
        /// <param name="maxSteps">The total amount of steps this task requries</param>
        public void SetMaxSteps(int maxSteps)
        {
            MaxSteps = maxSteps;
            Application.Instance.Invoke(() =>
            {
                ProgressBar.Indeterminate = false;
            });
                UpdateProgress();
        }

        /// <summary>
        /// Indicate that a step has been completed
        /// </summary>
        /// <param name="stepCount">State how many steps have been completed</param>
        public void DoStep(int stepCount = 1)
        {
            CurrentStep += stepCount;
            UpdateProgress();
        }

        /// <summary>
        /// Recalculate the tasks current progress and update the gui accordingly
        /// </summary>
        protected void UpdateProgress()
        {
            double exactProgress = (double)CurrentStep / MaxSteps * 100;
            int ceiledProgress = (int) Math.Ceiling(exactProgress);
            Application.Instance.Invoke(() =>
            {
                ProgressBar.Value = ceiledProgress;
            });
        }

        /// <summary>
        /// Tell the tracker that a task is done
        /// </summary>
        public void TaskDone()
        {
            Application.Instance.Invoke(() =>
            {
                LabelControl.Text += " - done";
            });
            Task.Factory.StartNew(() =>
            {
                // Give the user a few seconds to realize that the task is done
                System.Threading.Thread.Sleep(2000);
                Manager.RemoveTracker(this);
            });
        }
    }
}

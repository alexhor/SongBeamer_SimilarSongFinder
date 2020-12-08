using Eto.Forms;
using System;
using System.Collections.Generic;
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
        /// A constructor for the empty task
        /// </summary>
        protected TaskTracker()
        {
            Application.Instance.Invoke(() =>
            {
                ProgressBar = new ProgressBar();
                GuiControl = LabelControl = new Label();
            });
        }

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
                };
                UpdateProgress();
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
            DoCallbacks(CallbackType.OnSetMaxStep);
        }

        /// <summary>
        /// Indicate that a step has been completed
        /// </summary>
        /// <param name="stepCount">State how many steps have been completed</param>
        public void DoStep(int stepCount = 1)
        {
            CurrentStep += stepCount;
            UpdateProgress();
            DoCallbacks(CallbackType.OnStep);
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
            DoCallbacks(CallbackType.OnDone);
        }

        /// <summary>
        /// All currently registered callbacks
        /// </summary>
        protected IDictionary<CallbackType, IList<Action>> RegisteredCallbacks = new Dictionary<CallbackType, IList<Action>>();

        /// <summary>
        /// Register a callback function at the given hook position
        /// </summary>
        /// <param name="type">At what type of event this callback should be called</param>
        /// <param name="callback">The function to call</param>
        public void RegisterCallback(CallbackType type, Action callback)
        {
            if (!RegisteredCallbacks.ContainsKey(type)) RegisteredCallbacks[type] = new List<Action>();
            RegisteredCallbacks[type].Add(callback);
        }

        /// <summary>
        /// Run all registered callbacks of the given type
        /// </summary>
        /// <param name="typeToRun">What type of callback to run</param>
        protected void DoCallbacks(CallbackType typeToRun)
        {
            if (!RegisteredCallbacks.ContainsKey(typeToRun)) return;
            foreach (Action callback in RegisteredCallbacks[typeToRun])
            {
                callback();
            }
        }

        /// <summary>
        /// Different callback types that can be hooked into
        /// </summary>
        public enum CallbackType
        {
            OnStep,
            OnDone,
            OnSetMaxStep,
        }
    }

    /// <summary>
    /// Indicating a not existing task tracker
    /// </summary>
    public class EmptyTaskTracker : TaskTracker
    {
        /// <summary>
        /// Dummy constructor to avoid exceptions
        /// </summary>
        public EmptyTaskTracker() :base() { }

        /// <summary>
        /// No function, just here to avoid exceptions
        /// </summary>
        public new void TaskDone() { }
    }
}

using System;
using System.Collections.Generic;
using System.Text;

namespace SongSimilarityFinder
{
    /// <summary>
    /// Compare two songs lyrics
    /// </summary>
    class SongDiff
    {
        /// <summary>
        /// First song to compare
        /// </summary>
        protected readonly Song SongA;

        /// <summary>
        /// Second song to compare
        /// </summary>
        protected readonly Song SongB;

        private int AbsoluteDiffScore = -1;
        private float RelativeDiffScore = -1;

        /// <summary>
        /// Load the two songs
        /// </summary>
        /// <param name="songA">First song to compare</param>
        /// <param name="songB">Second song to compare</param>
        public SongDiff(Song songA, Song songB)
        {
            SongA = songA;
            SongB = songB;
        }

        /// <summary>
        /// Calculate a score determining the distance between the two songs
        /// </summary>
        private void CalcDiffScore()
        {
            AbsoluteDiffScore = 0;
            RelativeDiffScore = 0;
            int diffCount = 0;

            // Loop all lines in song A
            foreach (SongLine lineA in SongA)
            {
                // Loop all lines in song A
                foreach (SongLine lineB in SongB)
                {
                    // Get the two diff scores
                    SongLineDiff diff = new SongLineDiff(lineA, lineB);
                    AbsoluteDiffScore += diff.GetDiffAbsoluteScore();
                    RelativeDiffScore += diff.GetDiffRelativeScore();
                    diffCount++;
                }
            }

            // Normalize the scores
            if (0 == diffCount) return;
            AbsoluteDiffScore /= diffCount;
            RelativeDiffScore /= diffCount;
        }

        /// <summary>
        /// Get a score that tells how far these two songs are apart
        /// </summary>
        /// <returns>The diff score</returns>
        public int GetDiffAbsoluteScore()
        {
            if (-1 == AbsoluteDiffScore) CalcDiffScore();
            return AbsoluteDiffScore;
        }

        /// <summary>
        /// Put the absolute diff score in relation to the songs length
        /// </summary>
        /// <returns>A diff score relative to the songs length</returns>
        public float GetDiffRelativeScore()
        {
            if (-1 == RelativeDiffScore) CalcDiffScore();
            return RelativeDiffScore;
        }
    }
}

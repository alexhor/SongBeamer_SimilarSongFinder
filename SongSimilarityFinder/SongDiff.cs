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

    }
}

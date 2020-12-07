using System;

namespace SongSimilarityFinder
{
    /// <summary>
    /// One line of text in a song
    /// </summary>
    public class SongLine
    {
        /// <summary>
        /// This song lines text
        /// </summary>
        public readonly string Text;

        /// <summary>
        /// Amount of characters in this line
        /// </summary>
        public int Length => Text.Length;

        /// <summary>
        /// The song this line is a part of
        /// </summary>
        public readonly Song Song;

        /// <summary>
        /// This lines hash code
        /// </summary>
        private int Hash = 0;

        /// <summary>
        /// Load this lines text
        /// </summary>
        /// <param name="text">This song lines text</param>
        /// <param name="song">The song this line is a part of</param>
        public SongLine(string text, Song song)
        {
            Text = text;
            Song = song;
        }

        /// <summary>
        /// Returns the hash code for this song line
        /// </summary>
        /// <returns>A 32-bit signed integer hash code</returns>
        public override int GetHashCode()
        {
            if (0 == Hash) CalcHash();
            return Hash;
        }

        /// <summary>
        /// Calculate this song lines hash value
        /// </summary>
        private void CalcHash()
        {
            Hash = Text.GetHashCode();
        }

        internal void LoadMetadata()
        {


            // TODO: check if more metadata is stored on the harddrive
        }

        /// <summary>
        /// Returns the song lines text
        /// </summary>
        /// <returns>The song lines text</returns>
        public override string ToString()
        {
            return Text;
        }

        /// <summary>
        /// Indexer declcaration
        /// </summary>
        /// <param name="index">Choosen index</param>
        /// <returns></returns>
        public char this[int index]
        {
            get => Text[index];
        }
    }
}

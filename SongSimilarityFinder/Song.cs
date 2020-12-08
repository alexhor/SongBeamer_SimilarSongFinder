using System;
using System.Collections.Generic;

namespace SongSimilarityFinder
{
    /// <summary>
    /// Representation of a songfile
    /// </summary>
    public class Song
    {
        /// <summary>
        /// The location where this songs file is stored
        /// </summary>
        protected readonly string FileLocation;

        /// <summary>
        /// All text lines this song has
        /// </summary>
        protected IEnumerable<SongLine> SongLines = new List<SongLine>();

        /// <summary>
        /// This songs hash code
        /// </summary>
        private int Hash = 0;

        /// <summary>
        /// The songs title
        /// </summary>
        public string Title { get; private set; } = "";

        /// <summary>
        /// Create a new empty song
        /// </summary>
        /// <param name="fileLocation">What file this song is representing</param>
        public Song(string fileLocation)
        {
            FileLocation = fileLocation;
        }

        /// <summary>
        /// Load all text lines this song has
        /// </summary>
        /// <param name="lineList">A list of all text lines</param>
        internal void LoadLines(IEnumerable<SongLine> lineList)
        {
            SongLines = lineList;

            foreach (SongLine line in SongLines)
            {
                line.LoadMetadata();
            }
        }

        /// <summary>
        /// Returns the hash code for this song
        /// </summary>
        /// <returns>A 32-bit signed integer hash code</returns>
        public override int GetHashCode()
        {
            if (0 == Hash) CalcHash();
            return Hash;
        }

        /// <summary>
        /// Calculate this songs hash value
        /// </summary>
        private void CalcHash()
        {
            string songLineHashes = FileLocation;
            foreach (SongLine line in SongLines)
            {
                int lineHash = line.GetHashCode();
                songLineHashes += lineHash.ToString();
            }
            Hash = songLineHashes.GetHashCode();
        }

        /// <summary>
        /// Check if the given object matches with this song
        /// </summary>
        /// <param name="objectToCompare">Object to compare to</param>
        /// <returns>Whether the two objects match</returns>
        public override bool Equals(object objectToCompare)
        {
            return objectToCompare.GetHashCode() == GetHashCode();
        }

        /// <summary>
        /// Set the songs title
        /// </summary>
        /// <param name="title">The songs title</param>
        internal void SetTitle(string title)
        {
            Title = title;
        }

        /// <summary>
        /// Make a song usable in a foreach loop
        /// </summary>
        /// <returns>An Enumerator over all the songs lines</returns>
        public IEnumerator<SongLine> GetEnumerator()
        {
            return SongLines.GetEnumerator();
        }
    }
}

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
        protected IList<SongLine> SongLines = new List<SongLine>();

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
        /// Add a new line at the end of this song
        /// </summary>
        /// <param name="line"></param>
        internal void LoadLines(IList<SongLine> lineList)
        {
            SongLines = lineList;
        }

        /// <summary>
        /// Set the songs title
        /// </summary>
        /// <param name="title">The songs title</param>
        internal void SetTitle(string title)
        {
            Title = title;
        }
    }
}

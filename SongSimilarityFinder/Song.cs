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

        protected IList<SongLine> SongLines = new List<SongLine>();

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
    }
}

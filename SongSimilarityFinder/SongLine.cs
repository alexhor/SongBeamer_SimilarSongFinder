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
        /// The song this line is a part of
        /// </summary>
        public readonly Song Song;

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
    }
}

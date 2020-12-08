using System;
using System.Linq;
using System.Collections.Generic;
using System.Text;

namespace SongSimilarityFinder
{
    /// <summary>
    /// Compare two song lines
    /// </summary>
    class SongLineDiff
    {
        /// <summary>
        /// First song line to compare
        /// </summary>
        protected readonly SongLine LineA;

        /// <summary>
        /// Second song line to compare
        /// </summary>
        protected readonly SongLine LineB;

        /// <summary>
        /// Load the two song lines
        /// </summary>
        /// <param name="lineA">First song line to compare</param>
        /// <param name="lineB">Second song line to compare</param>
        public SongLineDiff(SongLine lineA, SongLine lineB)
        {
            LineA = lineA;
            LineB = lineB;
        }

        /// <summary>
        /// Longest common subsequence matrix of the two lines
        /// </summary>
        private int[,] LcsMatrix;

        private string LongestCommonSubsequence;

        /// <summary>
        /// 
        /// </summary>
        private void CalcLongestCommonSubsequenceMatrix()
        {
            LcsMatrix = new int[LineA.Length + 1, LineB.Length + 1];

            // Fill the first col and row
            for (int i = 0; i < LineA.Length; i++) LcsMatrix[i, 0] = 0;
            for (int i = 0; i < LineB.Length; i++) LcsMatrix[0, i] = 0;

            // Loop every character in line A
            for (int IndexLineA = 1; IndexLineA <= LineA.Length; IndexLineA++)
            {
                // Loop every character in line B
                for (int IndexLineB = 1; IndexLineB <= LineB.Length; IndexLineB++)
                {
                    // If characters are equal, increase their matrix value
                    if (LineA[IndexLineA - 1] == LineB[IndexLineB - 1])
                    {
                        LcsMatrix[IndexLineA, IndexLineB] = LcsMatrix[IndexLineA - 1, IndexLineB - 1] + 1;
                    }
                    // If the characters don't match, copy the previous matrix value
                    else
                    {
                        LcsMatrix[IndexLineA, IndexLineB] = Math.Max(LcsMatrix[IndexLineA - 1, IndexLineB], LcsMatrix[IndexLineA, IndexLineB - 1]);
                    }
                }
            }
        }

        private void CalcLongestCommonSubsequence()
        {
            if (null == LcsMatrix) CalcLongestCommonSubsequenceMatrix();
            if (null == LongestCommonSubsequence) LongestCommonSubsequence = BacktrackLongestCommonSubsequence(LineA.Length, LineB.Length);
        }

        private string BacktrackLongestCommonSubsequence(int IndexLineA, int IndexLineB)
        {
            // Skip the initial col and row
            if (0 == IndexLineA || 0 == IndexLineB)
            {
                return "";
            }
            // If the two characters match, add them to the current subsequence
            else if (LineA[IndexLineA - 1] == LineB[IndexLineB - 1])
            {
                return BacktrackLongestCommonSubsequence(IndexLineA - 1, IndexLineB - 1) + LineA[IndexLineA - 1];
            }
            // If the two characters don't match, continue with the character with a higher LCS score
            else if (LcsMatrix[IndexLineA, IndexLineB - 1] > LcsMatrix[IndexLineA - 1, IndexLineB])
            {
                return BacktrackLongestCommonSubsequence(IndexLineA, IndexLineB - 1);
            }
            else
            {
                return BacktrackLongestCommonSubsequence(IndexLineA - 1, IndexLineB);
            }
        }

        public string GetLongestCommonSubsequence()
        {
            CalcLongestCommonSubsequence();
            return LongestCommonSubsequence;
        }

        /// <summary>
        /// Determines how much an insert operation costs in the diff
        /// </summary>
        /// <returns>How much an insert operation costs</returns>
        private static int InsertCost()
        {
            return 1;
        }

        /// <summary>
        /// Determines how much a delete operation costs in the diff
        /// </summary>
        /// <returns>How much a delete operation costs</returns>
        private static int DeleteCost()
        {
            return 1;
        }

        /// <summary>
        /// Determines how much a replace operation costs in the diff
        /// </summary>
        /// <param name="a">Character to be replace</param>
        /// <param name="b">Character to replace with</param>
        /// <returns>How much a replace operation costs</returns>
        private static int ReplaceCost(char a, char b)
        {
            return a == b ? 0 : 1;
        }

        /// <summary>
        /// Calculates the two song lines levenshtein distace
        /// In squared time and linear space
        /// </summary>
        /// <returns>Calculated levenshtein distance</returns>
        private int CalcLevenshteinDistance()
        {
            // Init starting scores
            int[] scores = new int[LineB.Length + 1];
            scores[0] = 0;
            for (int i = 1; i <= LineB.Length; i++)
            {
                scores[i] = scores[i - 1] + InsertCost();
            }

            // Loop all characters from line A
            for (int IndexLineA = 1; IndexLineA <= LineA.Length; IndexLineA++)
            {
                char charA = LineA[IndexLineA - 1];
                int secondToLastCharacterScore = scores[0];
                scores[0] += DeleteCost();
                int lastCharacterScore = scores[0];

                // Loop all characters from line B
                for (int IndexLineB = 1; IndexLineB <= LineB.Length; IndexLineB++)
                {
                    char charB = LineB[IndexLineB - 1];
                    // Calculate the three different scores
                    int insertScore = lastCharacterScore + InsertCost();
                    int deleteScore = scores[IndexLineB] + DeleteCost();
                    int replaceScore = secondToLastCharacterScore + ReplaceCost(charA, charB);

                    // Prepare scores for the next character
                    lastCharacterScore = Math.Min(Math.Min(insertScore, deleteScore), replaceScore);
                    secondToLastCharacterScore = scores[IndexLineB];
                    scores[IndexLineB] = lastCharacterScore;
                }
            }

            // Return the strings distance
            return scores.Last();
        }

        /// <summary>
        /// The two song lines levenshtein distace
        /// </summary>
        private int LevenshteinDistance = -1;

        /// <summary>
        /// Get a score that tells how far these two song lines are apart
        /// </summary>
        /// <returns>The diff score</returns>
        public int GetDiffAbsoluteScore()
        {
            if (-1 == LevenshteinDistance) LevenshteinDistance = CalcLevenshteinDistance();
            return LevenshteinDistance;
        }

        /// <summary>
        /// Put the absolute diff score in relation to the song lines length
        /// </summary>
        /// <returns>A diff score relative to the song line length</returns>
        public float GetDiffRelativeScore()
        {
            float absScore = GetDiffAbsoluteScore();
            float length = Math.Max(LineA.Length, LineB.Length);
            return absScore / length;
        }
    }
}

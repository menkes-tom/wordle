from Analysis_functions import *
from CSV_handler import *
import time


# read the dictionary data from Wordle
word_list = readData()
# score the English letters by their frequency in the Wordle dictionary
letter_scores = getFrequency(word_list)
# average the frequency of each letter by the number of letters used in the dictionary
letter_scores = averageFrequency(letter_scores)
# score the English letters by their frequency for each letter position in the words of the Wordle dictionary
letter_positions = letterPositionFrequency(word_list)
# average the frequency of each letter by the number of letters in each position used in the dictionary
letter_positions = averagePositionalFrequency(letter_positions)
# export the results to a CSV files for future or further analysis
print("After analysis, the following frequency and positional average was received:")
print("------------------------------------------------------------")
documentLetterScores(letter_scores)
documentLetterPositions(letter_positions)
# generate all the possible feedback to a given word played
combinations = possibleCombinations()
# calculate all the data for each word and feedback combination and for ease of display
print("Starting to match 242 combinations with ~2,300 words in the Wordle dictionary, hang tight:")
start = time.time()
words_starting_ranks=rankStartingScore(combinations, word_list, letter_scores, letter_positions)
end = time.time()
# export the results to a CSV file for future or further analysis
print("Operation took %f seconds." %(end - start))
print("After analysis, the following starting letter score was received:")
print("------------------------------------------------------------")
documentWordScores(words_starting_ranks)

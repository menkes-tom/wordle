from Analysis_functions import *
from CSV_handler import *


def getNewGuess(_word_list):
    # read the dictionary data from Wordle
    word_list = _word_list
    # score the English letters by their frequency in the Wordle dictionary
    letter_scores = getFrequency(word_list)
    # average the frequency of each letter by the number of letters used in the dictionary
    letter_scores = averageFrequency(letter_scores)
    # score the English letters by their frequency for each letter position in the words of the Wordle dictionary
    letter_positions = letterPositionFrequency(word_list)
    # average the frequency of each letter by the number of letters in each position used in the dictionary
    letter_positions = averagePositionalFrequency(letter_positions)
    # generate all the possible feedback to a given word played
    combinations = possibleCombinations()
    # calculate all the data for each word and feedback combination and for ease of display
    words_starting_ranks = rankStartingScore(combinations, word_list, letter_scores, letter_positions)
    # return only the top ranked word to use as a next guess in a game of Wordle
    return words_starting_ranks[0][0]

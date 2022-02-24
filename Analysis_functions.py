# importing modules
import itertools
from collections import Counter
from Progress_bar import *


# create a counter dictionary of letter frequencies
def getFrequency(_words):
    concatenation= ''.join(map(str, _words))
    return Counter(concatenation)


# average the letter frequency across the numbers of letters in the counter dictionary keys
def averageFrequency(_letter_scores):
    for key in _letter_scores.keys():
        _letter_scores[key] = _letter_scores[key]/len(_letter_scores.keys())
    return _letter_scores


# create a counter dictionary for letter frequencies per location in word:
def letterPositionFrequency(_words):
    concatenation = ["", "", "", "", ""]
    for _word in _words:
        for _letter, index in zip(_word, range(5)):
            concatenation[index]+=_letter
    return [Counter(concatenation[0]), Counter(concatenation[1]), Counter(concatenation[2]), Counter(concatenation[3]), Counter(concatenation[4])]


# average the letter positional frequency across the numbers of letters in the counter dictionary keys
def averagePositionalFrequency(_letter_positions):
    for position in _letter_positions:
        for key in position.keys():
            position[key] = position[key] / len(position.keys())
    return _letter_positions


# get the score of a word using the letter scores (by frequency) found earlier
def getFrequencyScore(_word, _letter_scores):
    score = 0
    for letter in _word:
        score += _letter_scores[letter]
    return score


# get the score of a word using the letter positional scores (by frequency) found earlier
def getPositionalScore(_word, _letter_positions):
    score = 0
    for letter, index in zip(_word, range(5)):
        score += _letter_positions[index][letter]
    return score


# creating a list of all possible permutations of received feedback for a guessed word
def possibleCombinations():
    N = 5  # number of objects (e.g. slots)
    possible_values = [-1, 0, 1]  # -1 wrong letter, 0 right letter wrong place, 1 right letter right place
    # using itertools to create the permutations in question
    result = list(itertools.product(possible_values, repeat=N))
    # removing the option to guess the word on the first try, not statistically significant or interesting
    result.remove((1, 1, 1, 1, 1))
    return result


# check the remaining words after playing the first word and comparing it with a combination of a given answer (received feedback for a guessed word)
def checkWordAndCombo(_combination, _word, _words):
    # -1 wrong letter, 0 right letter wrong place, 1 right letter right place
    words_to_check = _words.copy()
    misplaced_letters = []
    refreshed_list = []
    for slot, index in zip(_combination, range(5)):
        if slot == -1:
            # if the letter is not in the target word at all, clear the words with that letter at that location
            words_to_check = [x for x in words_to_check if x[index] != _word[index]]
        if slot == 0:
            # if the letter is not in the target word at a specific location, clear the words with that letter at that location
            words_to_check = [x for x in words_to_check if x[index] != _word[index]]
            # add the letter to a collection of misplaced letters
            misplaced_letters.append(_word[index])
        if slot == 1:
            # if the letter is in the target word at the correct location, clear the words with that don't have that letter at that location
            words_to_check = [x for x in words_to_check if x[index] == _word[index]]
    if misplaced_letters:
        # if there were misplaced letters, create a new list of words that contain all the misplaced letters
        for a_word in words_to_check:
            test_condition = all(letter in a_word for letter in misplaced_letters)
            if test_condition:
                refreshed_list.append(a_word)
        return refreshed_list
    return words_to_check


# check all the words against all the combinations of possible outcomes (242 possible outcomes against ~2300 words in the Wordle answer bank)
def rankStartingScore(_combinations, _words, _letter_scores, _letter_positions, showProgress=False):
    starting_rank = []
    # Initial call to print 0% progress
    if showProgress:
        printProgressBarPyCharm(0, len(_words), prefix='Progress:', suffix='Complete', length=50)
    # iterate over all the words in the word bank
    for a_word, progress in zip(_words, range(len(_words))):
        current_word = ["", 0]  # word and score combo
        current_word[0] = a_word
        NonZero = 0
        # for each word, iterate over all the possible received feedback
        for combination in _combinations:
            # add all possible next turns given the data (all remaining words given the answer received)
            current_word[1] += len(checkWordAndCombo(combination, a_word, _words))
            # count the number of times there was any possible future data - 0 options left means the word is either very unique,
            # therefore not providing a lot of data, or we were right on the first guess - low possibility with low statistical significance
            if len(checkWordAndCombo(combination, a_word, _words)) != 0:
                NonZero += 1
        # average the score of all possible next-turn words divided by iterations that provided data
        if NonZero > 0:
            current_word[1] = current_word[1]/NonZero
        else:
            current_word[1] = 1
        starting_rank.append([current_word[0], current_word[1], len(set(a_word)), getFrequencyScore(current_word[0], _letter_scores), getPositionalScore(current_word[0], _letter_positions)])
        # calculate the final score
        starting_rank[-1].append((1/starting_rank[-1][1])*starting_rank[-1][2]*starting_rank[-1][3]*starting_rank[-1][4])
        # Update Progress Bar
        if showProgress:
            printProgressBarPyCharm(progress, len(_words), prefix='Progress:', suffix='Complete', length=50)
    if showProgress:
        printProgressBarPyCharm(100, 100, prefix='Progress:', suffix='Complete', length=50)
    starting_rank.sort(key=lambda x: x[5], reverse=True)
    return starting_rank

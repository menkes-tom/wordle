# importing modules
from pandas import *


# reading CSV files
def readResult():
    try:
        word_bank = read_csv('data/Starting_Ranks.csv', index_col=False)
        result = word_bank.values.tolist()
        for line in result:
            line.pop(0)
        new_dataframe = DataFrame(result, columns=['Word', 'Rank_by_remaining words', 'Unique_letters', 'Score_by_frequency', 'Calculated_Score'])
        return new_dataframe
    except FileNotFoundError:
        return -1


def readData():
    word_bank = read_csv("data/Word_Bank.csv")
    # convert column data to list
    _word_list = word_bank['Words'].tolist()
    return _word_list


# export the letter scores to a CSV, sorted, file for future usage or analysis
def documentLetterScores(_letter_scores):
    combination = []
    for letter, score in zip(_letter_scores.keys(), _letter_scores.values()):
        combination.append((letter, score))
    combination.sort(key=lambda x: x[1], reverse=True)
    letter_scores_data_frame = DataFrame(combination, columns=['Letter', 'Frequency'])
    letter_scores_data_frame.to_csv('data/Letter_Frequency.csv')
    print(letter_scores_data_frame.head())
    print("...")
    print(letter_scores_data_frame.tail())
    print(letter_scores_data_frame.shape)


# export the word scores to a CSV file, sorted, for future usage or analysis
def documentWordScores(_words_starting_ranks):
    for _word in _words_starting_ranks:
        _word.append((1/_word[1])*_word[2]*_word[3])
    _words_starting_ranks.sort(key=lambda x: x[4], reverse=True)
    words_data_frame = DataFrame(_words_starting_ranks, columns=['Word', 'Rank_by_remaining words', 'Unique_letters', 'Score_by_frequency', 'Calculated_Score'])
    words_data_frame.to_csv('data/Starting_Ranks.csv')
    print(words_data_frame)


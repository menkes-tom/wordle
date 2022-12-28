from Analysis_functions import *
from Game_objects import *
from Score_Dictionary import getNewGuess


# a function to check the feedback from a given word against the goal word
def checkWord(_word, _game):
    feedback = [0, 0, 0, 0, 0]
    goal = _game.goal_word
    # check the letters of the goal word and the guessed word index by index to create a feedback vector
    for played_letter, goal_letter, index in zip(_word, goal, range(5)):
        if played_letter == goal_letter:
            feedback[index] = 1
        elif played_letter in goal:
            feedback[index] = 0
        else:
            feedback[index] = -1
    return feedback


# simulation of playing a turn of Wordle, and using the analysis function to get the next guess accordingly
def playTurn(_game, _word_list, _word):
    # create a new turn object, give it a name and a number
    turn_number = len(_game.turn_list)
    turn_number += 1
    new_turn = Turn(turn_number, _word)
    new_turn.previous_dictionary = _word_list.copy()
    # add the turn to the list of turns in the current game
    _game.addTurn(new_turn)
    # calculate the feedback from the current played word and check if the game is won
    feedback = checkWord(_word, _game)
    new_turn.turn_feedback = feedback
    _game.checkGameOver()
    if _game.game_over:
        return "Game Over"
    # if the game wasn't won, get the next best word to use, using the analysis functions used to rank the words in Wordle
    new_turn.next_dictionary = checkWordAndCombo(feedback, _word, _word_list)
    find_next_guess = getNewGuess(new_turn.next_dictionary)
    return find_next_guess


# a debug function to print a whole "game" of Wordle, using its objects
def printResults(_game: Game):
    print("Playing Wordle with the goal word: ", _game.goal_word)
    for turn in _game:
        print("At turn %d the guessed word was %s and the feedback was %s" %(_game.turn_list.index(turn)+1, turn.played_word, turn.turn_feedback))
    if _game.game_won:
        print("The game was won at %d turns." %len(_game.turn_list))
    else:
        print("The game was lost at %d turns." %len(_game.turn_list))


# simulate a full game of Wordle
def playWordle(_goal_word, _first_guess, _word_list):
    # create a new game object
    wordle_game = Game(_goal_word)
    # print("Starting a new game, the goal word is: ", wordle_game.goal_word)
    # playing the game until 6 turns have passed or the game was won (or both)
    next_guess = playTurn(wordle_game, _word_list, _first_guess)
    wordle_game.checkGameOver()
    while not wordle_game.game_over:
        next_guess = playTurn(wordle_game, wordle_game.turn_list[-1].next_dictionary, next_guess)
        wordle_game.checkGameOver()
    return wordle_game

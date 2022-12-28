from Game_objects import *
from Score_Dictionary import *




def playTurn(_game, _word, _word_list, previous_feedback):
    turn_number = len(_game.turn_list)
    turn_number += 1
    new_turn = Turn(turn_number, _word)
    new_turn.previous_dictionary = _word_list.copy()
    _game.addTurn(new_turn)
    new_turn.next_dictionary = checkWordAndCombo(previous_feedback, _word, _word_list)
    find_next_guess = getNewGuess(new_turn.next_dictionary)
    return find_next_guess, new_turn.next_dictionary


word_list = readData()
game = Game()

while not game.game_won or not game.game_over:
    feedback = [0, 0, 0, 0, 0]
    played_word = input("Enter your last played word: ")
    for letter in list(enumerate(played_word)):
        _str = "Enter feedback for the letter: " + str(letter[1]) +  ", in position: " + str(letter[0]+1) + " = "
        feedback[letter[0]] = int(input(_str))
    print(feedback)
    new_guess, word_list = playTurn(game, played_word, word_list, feedback)
    print(new_guess)
    print(word_list)


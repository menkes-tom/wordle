from typing import List, Union
from src.analysis_functions import check_word_and_combo
from src.game_objects import Game, Turn
from src.score_dictionary import get_new_guess


def check_word(word: str, game: Game) -> List[int]:
    """
    Checks the feedback from a given word against the goal word.
    
    Args:
        word: The word guessed by the player or script.
        game: The current Game object containing the goal word.
        
    Returns:
        A feedback vector representing the match (-1 for wrong, 0 for wrong place, 1 for correct place).
    """
    feedback = [0, 0, 0, 0, 0]
    goal = game.goal_word
    
    if not goal:
        return feedback
        
    # check the letters of the goal word and the guessed word index by index
    for index, (played_letter, goal_letter) in enumerate(zip(word, goal)):
        if played_letter == goal_letter:
            feedback[index] = 1
        elif played_letter in goal:
            feedback[index] = 0
        else:
            feedback[index] = -1
            
    return feedback


def play_turn(game: Game, word_list: List[str], word: str) -> Union[str, str]:
    """
    Simulates playing a turn of Wordle, checking feedback and retrieving the next best guess.
    
    Args:
        game: The current Game object.
        word_list: The list of remaining possible words.
        word: The current word to guess.
        
    Returns:
        The next best word to guess, or 'Game Over' if the game ended.
    """
    turn_number = len(game.turn_list) + 1
    new_turn = Turn(turn_number, word)
    new_turn.previous_dictionary = word_list.copy()
    
    game.add_turn(new_turn)
    
    feedback = check_word(word, game)
    new_turn.turn_feedback = feedback
    
    game.check_game_over()
    if game.game_over:
        return "Game Over"
        
    # get the next best word to use based on analysis
    new_turn.next_dictionary = check_word_and_combo(feedback, word, word_list)
    next_guess = get_new_guess(new_turn.next_dictionary)
    
    return next_guess


def print_results(game: Game) -> None:
    """
    Prints the results of a simulated Wordle game.
    """
    print(f"Playing Wordle with the goal word: {game.goal_word}")
    
    for index, turn in enumerate(game.turn_list):
        print(f"At turn {index + 1} the guessed word was {turn.played_word} and the feedback was {turn.turn_feedback}")
        
    if game.game_won:
        print(f"The game was won at {len(game.turn_list)} turns.")
    else:
        print(f"The game was lost at {len(game.turn_list)} turns.")


def play_wordle(goal_word: str, first_guess: str, word_list: List[str]) -> Game:
    """
    Simulates a full game of Wordle using the automated strategy.
    
    Args:
        goal_word: The target word to guess.
        first_guess: The optimal first word.
        word_list: The complete dictionary of possible words.
        
    Returns:
        The completed Game object.
    """
    wordle_game = Game(goal_word)
    
    next_guess = play_turn(wordle_game, word_list, first_guess)
    wordle_game.check_game_over()
    
    while not wordle_game.game_over:
        # Pass the reduced dictionary from the previous turn's calculation
        next_guess = play_turn(wordle_game, wordle_game.turn_list[-1].next_dictionary, next_guess)
        wordle_game.check_game_over()
        
    return wordle_game

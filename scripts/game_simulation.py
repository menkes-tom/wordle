from typing import Tuple, List
from src.game_objects import Game, Turn
from src.score_dictionary import get_new_guess
from src.analysis_functions import check_word_and_combo
from src.csv_handler import read_data


def play_interactive_turn(game: Game, word: str, word_list: List[str], previous_feedback: List[int]) -> Tuple[str, List[str]]:
    """
    Plays a turn interactively based on manual user input of feedback.
    
    Args:
        game: The current Game object.
        word: The played word.
        word_list: The remaining valid dictionary words.
        previous_feedback: The feedback vector provided by the user.
        
    Returns:
        A tuple of the next recommended guess and the updated list of remaining words.
    """
    turn_number = len(game.turn_list) + 1
    new_turn = Turn(turn_number, word)
    new_turn.previous_dictionary = word_list.copy()
    
    game.add_turn(new_turn)
    
    new_turn.next_dictionary = check_word_and_combo(tuple(previous_feedback), word, word_list)
    find_next_guess = get_new_guess(new_turn.next_dictionary)
    
    return find_next_guess, new_turn.next_dictionary


def main() -> None:
    """
    Main entry point for interactive game simulation.
    """
    word_list = read_data()
    game = Game(max_turns=1000)
    
    while not game.game_won and not game.game_over:
        feedback = [0, 0, 0, 0, 0]
        played_word = input("Enter your last played word (or type 'win'/'re'): ").strip().lower()
        
        if played_word == "win":
            print("Congratulations!")
            break
        if played_word == "re":
            print("Restarting with full dictionary...")
            word_list = read_data()
            continue
            
        if len(played_word) != 5:
            print("Invalid word length. Please try again.")
            continue
            
        for index, letter in enumerate(played_word):
            prompt_str = f"Enter feedback for the letter '{letter}', in position {index + 1} (-1=wrong, 0=misplaced, 1=correct): "
            try:
                feedback[index] = int(input(prompt_str))
            except ValueError:
                print("Invalid input, defaulting to -1.")
                feedback[index] = -1
                
        print(f"Feedback vector received: {feedback}")
        
        new_guess, word_list = play_interactive_turn(game, played_word, word_list, feedback)
        
        print(f"Recommended next guess: {new_guess}")
        print(f"Remaining possible words count: {len(word_list)}")
        # print(word_list) # uncomment to see all remaining words


if __name__ == "__main__":
    main()

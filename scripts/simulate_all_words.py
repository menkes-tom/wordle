import time
from src.csv_handler import read_data, document_game_records
from src.progress_bar import print_progress_bar
from src.play_wordle_auto import play_wordle, print_results


def main() -> None:
    """
    Main entry point to simulate all words in the Wordle dictionary to evaluate performance.
    """
    # load the dictionary from a CSV file and maintain a list of game results
    word_list = read_data()
    game_results = []
    
    total_words = len(word_list)
    
    # print a progress bar
    print_progress_bar(0, total_words, prefix='Progress:', suffix='Complete', length=50)
    
    # document the initial time of the test
    start_time = time.time()
    
    # iterate over all the words in the dictionary
    for index, word in enumerate(word_list):
        # play the game Wordle with each word using "slate" as the starting guess
        game_result = play_wordle(goal_word=word, first_guess="slate", word_list=word_list)
        game_results.append(game_result)
        
        # update the progress bar
        print_progress_bar(
            index + 1, 
            total_words, 
            prefix='Progress:', 
            suffix=f'Complete {index + 1} words analyzed of {total_words}', 
            length=50
        )
        
    end_time = time.time()
    print(f"Operation took {end_time - start_time:.4f} seconds.")
    
    # histogram dictionary that counts game wins or losses and number of turns
    game_records = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, -1: 0}
    
    for game in game_results:
        if game.game_won:
            num_turns = len(game.turn_list)
            # cap at 6 turns for histogram or record over-6 turn wins if tracking
            if num_turns in game_records:
                game_records[num_turns] += 1
            else:
                game_records[num_turns] = 1 # create new record entry if won in > 6 turns
        else:
            game_records[-1] += 1
            
    document_game_records(game_records)


if __name__ == "__main__":
    main()

import time
from src.analysis_functions import (
    get_frequency,
    average_frequency,
    letter_position_frequency,
    average_positional_frequency,
    possible_combinations,
    rank_starting_score
)
from src.csv_handler import (
    read_data,
    document_letter_scores,
    document_letter_positions,
    document_word_scores
)


def main() -> None:
    """
    Main entry point for analyzing the Wordle dictionary to find the best starting word.
    """
    # read the dictionary data from Wordle
    word_list = read_data()
    
    # score the English letters by their frequency in the Wordle dictionary
    letter_scores = get_frequency(word_list)
    # average the frequency of each letter by the number of letters used in the dictionary
    letter_scores = average_frequency(letter_scores)
    
    # score the English letters by their frequency for each letter position in the words of the Wordle dictionary
    letter_positions = letter_position_frequency(word_list)
    # average the frequency of each letter by the number of letters in each position used in the dictionary
    letter_positions = average_positional_frequency(letter_positions)
    
    # export the results to a CSV files for future or further analysis
    print("After analysis, the following frequency and positional average was received:")
    print("-" * 60)
    document_letter_scores(letter_scores)
    document_letter_positions(letter_positions)
    
    # generate all the possible feedback to a given word played
    combinations = possible_combinations()
    
    # calculate all the data for each word and feedback combination
    print("Starting to match 242 combinations with ~2,300 words in the Wordle dictionary, hang tight:")
    start_time = time.time()
    
    words_starting_ranks = rank_starting_score(
        combinations, 
        word_list, 
        letter_scores, 
        letter_positions, 
        show_progress=True
    )
    
    end_time = time.time()
    
    # export the results to a CSV file for future or further analysis
    print(f"Operation took {end_time - start_time:.4f} seconds.")
    print("After analysis, the following starting letter score was received:")
    print("-" * 60)
    document_word_scores(words_starting_ranks)


if __name__ == "__main__":
    main()

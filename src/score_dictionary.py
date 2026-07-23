from typing import List
from src.analysis_functions import (
    get_frequency,
    average_frequency,
    letter_position_frequency,
    average_positional_frequency,
    possible_combinations,
    rank_starting_score
)


def get_new_guess(word_list: List[str]) -> str:
    """
    Determines the best next guess for Wordle using entropy-based ranking algorithms.
    
    Args:
        word_list: A list of remaining valid words.
        
    Returns:
        The highest-ranked word to guess next.
    """
    # Create a local copy to avoid mutation
    current_list = word_list.copy()
    
    if not current_list:
        return ""
        
    # Score the English letters by their frequency in the dictionary
    letter_scores = get_frequency(current_list)
    letter_scores = average_frequency(letter_scores)
    
    # Score the English letters by their frequency for each letter position
    letter_positions = letter_position_frequency(current_list)
    letter_positions = average_positional_frequency(letter_positions)
    
    # Generate all the possible feedback to a given word played
    combinations = possible_combinations()
    
    # Calculate all the data for each word and feedback combination
    words_starting_ranks = rank_starting_score(
        combinations, 
        current_list, 
        letter_scores, 
        letter_positions
    )
    
    # Return only the top ranked word to use as the next guess
    return words_starting_ranks[0][0]

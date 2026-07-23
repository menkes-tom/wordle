import itertools
from collections import Counter
from typing import List, Dict, Tuple, Any
from src.progress_bar import print_progress_bar


def get_frequency(words: List[str]) -> Counter:
    """
    Creates a counter dictionary of letter frequencies across a list of words.
    """
    concatenation = ''.join(words)
    return Counter(concatenation)


def average_frequency(letter_scores: Counter) -> Dict[str, float]:
    """
    Averages the letter frequency across the number of unique letters in the counter.
    """
    averaged = dict(letter_scores)
    num_keys = len(averaged.keys())
    for key in averaged.keys():
        averaged[key] = averaged[key] / num_keys
    return averaged


def letter_position_frequency(words: List[str]) -> List[Counter]:
    """
    Creates a list of counter dictionaries for letter frequencies per location (0-4) in word.
    """
    concatenation = ["", "", "", "", ""]
    for word in words:
        for letter, index in zip(word, range(5)):
            concatenation[index] += letter
    return [
        Counter(concatenation[0]),
        Counter(concatenation[1]),
        Counter(concatenation[2]),
        Counter(concatenation[3]),
        Counter(concatenation[4])
    ]


def average_positional_frequency(letter_positions: List[Counter]) -> List[Dict[str, float]]:
    """
    Averages the letter positional frequency across the number of letters in each position.
    """
    averaged_positions = []
    for position in letter_positions:
        averaged_pos = dict(position)
        num_keys = len(averaged_pos.keys())
        for key in averaged_pos.keys():
            averaged_pos[key] = averaged_pos[key] / num_keys
        averaged_positions.append(averaged_pos)
    return averaged_positions


def get_frequency_score(word: str, letter_scores: Dict[str, float]) -> float:
    """
    Calculates the score of a word using the letter scores (by overall frequency).
    """
    score = 0.0
    for letter in word:
        score += letter_scores.get(letter, 0.0)
    return score


def get_positional_score(word: str, letter_positions: List[Dict[str, float]]) -> float:
    """
    Calculates the score of a word using the letter positional scores.
    """
    score = 0.0
    for letter, index in zip(word, range(5)):
        score += letter_positions[index].get(letter, 0.0)
    return score


def possible_combinations() -> List[Tuple[int, ...]]:
    """
    Creates a list of all possible permutations of received feedback for a guessed word.
    -1: wrong letter, 0: right letter wrong place, 1: right letter right place
    """
    n_slots = 5
    possible_values = [-1, 0, 1]
    result = list(itertools.product(possible_values, repeat=n_slots))
    # removing the option to guess the word on the first try
    if (1, 1, 1, 1, 1) in result:
        result.remove((1, 1, 1, 1, 1))
    return result


def check_word_and_combo(combination: Tuple[int, ...], word: str, words: List[str]) -> List[str]:
    """
    Filters the remaining words after playing the first word and comparing it with a feedback combination.
    """
    vowels = ['a', 'e', 'i', 'o', 'u']
    words_to_check = words.copy()
    misplaced_letters = []
    refreshed_list = []
    
    for slot, index in zip(combination, range(5)):
        if slot == -1:
            if word[index] == "_":
                continue
            # if the letter is not in the target word at all, clear the words with that letter at that location
            words_to_check = [x for x in words_to_check if ((word[index] not in x or word[index] in vowels) and word[index] != x[index])]
        elif slot == 0:
            # if the letter is not in the target word at a specific location, clear the words with that letter at that location
            words_to_check = [x for x in words_to_check if x[index] != word[index]]
            misplaced_letters.append(word[index])
        elif slot == 1:
            # if the letter is in the target word at the correct location, clear the words that don't have that letter at that location
            words_to_check = [x for x in words_to_check if x[index] == word[index]]
        else:
            continue
            
    if misplaced_letters:
        for a_word in words_to_check:
            test_condition = all(letter in a_word for letter in misplaced_letters)
            if test_condition:
                refreshed_list.append(a_word)
        return refreshed_list
        
    return words_to_check


def rank_starting_score(combinations: List[Tuple[int, ...]], words: List[str], letter_scores: Dict[str, float], letter_positions: List[Dict[str, float]], show_progress: bool = False) -> List[Any]:
    """
    Ranks the words against all combinations of possible outcomes.
    """
    starting_rank = []
    total_words = len(words)
    
    if show_progress:
        print_progress_bar(0, total_words, prefix='Progress:', suffix='Complete', length=50)
        
    for index, a_word in enumerate(words):
        current_word_data = [a_word, 0.0]
        non_zero = 0
        
        for combination in combinations:
            remaining_words = check_word_and_combo(combination, a_word, words)
            current_word_data[1] += len(remaining_words)
            if remaining_words:
                non_zero += 1
                
        if non_zero > 0:
            current_word_data[1] = current_word_data[1] / non_zero
        else:
            current_word_data[1] = 1.0
            
        unique_letters_count = len(set(a_word))
        freq_score = get_frequency_score(a_word, letter_scores)
        pos_score = get_positional_score(a_word, letter_positions)
        
        word_record = [
            current_word_data[0], 
            current_word_data[1], 
            unique_letters_count, 
            freq_score, 
            pos_score
        ]
        
        # calculate the final score
        calculated_score = (1 / word_record[1]) * word_record[2] * word_record[3] * word_record[4]
        word_record.append(calculated_score)
        
        starting_rank.append(word_record)
        
        if show_progress:
            print_progress_bar(index + 1, total_words, prefix='Progress:', suffix='Complete', length=50)
            
    starting_rank.sort(key=lambda x: x[5], reverse=True)
    return starting_rank

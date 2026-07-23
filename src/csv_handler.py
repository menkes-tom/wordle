import pandas as pd
from typing import Optional, List, Dict, Any


def read_result() -> Optional[pd.DataFrame]:
    """
    Reads the starting ranks result from CSV if it exists.
    """
    try:
        word_bank = pd.read_csv('data/Starting_Ranks.csv', index_col=False)
        result = word_bank.values.tolist()
        new_dataframe = pd.DataFrame(result, columns=['Word', 'Rank_by_remaining words', 'Unique_letters', 'Score_by_frequency', 'Calculated_Score'])
        return new_dataframe
    except FileNotFoundError:
        return None


def read_data() -> List[str]:
    """
    Reads the dictionary data from the Word_Bank.csv file.
    """
    word_bank = pd.read_csv("data/Word_Bank.csv")
    word_list = word_bank['Words'].tolist()
    return word_list


def document_letter_scores(letter_scores: Dict[str, float]) -> None:
    """
    Exports the letter scores to a sorted CSV file.
    """
    combination = [(letter, score) for letter, score in letter_scores.items()]
    combination.sort(key=lambda x: x[1], reverse=True)
    
    letter_scores_df = pd.DataFrame(combination, columns=['Letter_total_frequency', 'Frequency'])
    letter_scores_df.to_csv('data/Letter_Frequency.csv', index=False)
    
    print(letter_scores_df.head())
    print("...")
    print(letter_scores_df.tail())
    print(letter_scores_df.shape)


def document_letter_positions(letter_positions: List[Dict[str, float]]) -> None:
    """
    Exports the letter positional frequency to a combined CSV file.
    """
    combination: List[List[tuple]] = [[], [], [], [], []]
    for index, position in enumerate(letter_positions):
        for letter, score in position.items():
            combination[index].append((letter, score))
        combination[index].sort(key=lambda x: x[1], reverse=True)
        
    first_letter_df = pd.DataFrame(combination[0], columns=['First_Letter_Frequency', 'Frequency'])
    second_letter_df = pd.DataFrame(combination[1], columns=['Second_Letter_Frequency', 'Frequency'])
    third_letter_df = pd.DataFrame(combination[2], columns=['Third_Letter_Frequency', 'Frequency'])
    fourth_letter_df = pd.DataFrame(combination[3], columns=['Fourth_Letter_Frequency', 'Frequency'])
    fifth_letter_df = pd.DataFrame(combination[4], columns=['Fifth_Letter_Frequency', 'Frequency'])
    
    combined_df = pd.concat([first_letter_df, second_letter_df, third_letter_df, fourth_letter_df, fifth_letter_df], axis=1)
    combined_df.to_csv('data/Combined_Letter_Frequency.csv', index=False)
    print(combined_df.head())


def document_word_scores(words_starting_ranks: List[Any]) -> None:
    """
    Exports the calculated word scores to a CSV file.
    """
    words_df = pd.DataFrame(words_starting_ranks, columns=[
        'Word', 'Rank_by_remaining words', 'Unique_letters', 'Score_by_frequency', 'Score_by_position', 'Calculated_Score'
    ])
    words_df.to_csv('data/Starting_Ranks.csv', index=False)
    print(words_df)


def document_game_records(game_records: Dict[int, int]) -> None:
    """
    Exports the game records to a CSV file.
    """
    game_records_df = pd.DataFrame(list(game_records.items()), columns=['Number_of_turns', 'Games_won'])
    game_records_df.to_csv('data/Game_Records.csv', index=False)
    print(game_records_df)

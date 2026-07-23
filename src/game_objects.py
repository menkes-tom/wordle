from typing import Optional, Dict, Any, List

class Turn(object):
    """
    Represents a single turn in a game of Wordle.
    """
    def __init__(self, turn_num: int, played_word: str):
        self.turn_num: int = turn_num
        self.played_word: str = played_word
        # a dictionary of possible words that were able to be guesses
        self.previous_dictionary: Dict[str, Any] = {}
        # a dictionary of the next possible words according to the turn feedback, in order to pass to the next turn
        self.next_dictionary: Dict[str, Any] = {}
        self.turn_feedback: Any = -1

    def __repr__(self) -> str:
        return f"<Turn {self.turn_num}: '{self.played_word}' (Feedback: {self.turn_feedback})>"


class Game(object):
    """
    Represents a game of Wordle, tracking turns, max turns, and whether the game was won.
    """
    def __init__(self, goal_word: Optional[str] = None, max_turns: int = 6):
        self.goal_word: Optional[str] = goal_word
        self.max_turns: int = max_turns
        self.turn_list: List[Turn] = []
        self.game_over: bool = False
        self.game_won: bool = False

    # declare a way to iterate over a game using its turns
    def __getitem__(self, index: int) -> Turn:
        return self.turn_list[index]

    # a way to add turns without physically touching the turn list
    def add_turn(self, turn: Turn) -> None:
        """
        Adds a new turn to the game's turn list.
        """
        self.turn_list.append(turn)

    # check all the conditions in which a game ends in
    def check_game_over(self) -> None:
        """
        Evaluates the current turn list against the max turns and goal word to determine
        if the game is over and whether it was won.
        """
        if not self.turn_list:
            return

        last_turn = self.turn_list[-1]
        
        # if max turns were played and the last played word is not the goal word, game over and not won
        if len(self.turn_list) >= self.max_turns and last_turn.played_word != self.goal_word:
            self.game_over = True
            self.game_won = False
        # if the last played word is the goal word, game over and won
        elif last_turn.played_word == self.goal_word:
            self.game_over = True
            self.game_won = True
        # else, game is not over and not won
        else:
            self.game_over = False
            self.game_won = False

    def __repr__(self) -> str:
        status = "Won" if self.game_won else ("Over" if self.game_over else "In Progress")
        return f"<Game (Goal: {self.goal_word}, Turns: {len(self.turn_list)}/{self.max_turns}, Status: {status})>"

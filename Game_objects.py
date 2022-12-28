# create a new class to store Game data
class Game(object):
    def __init__(self, _goal_word=None, _max_turns=6):
        self.goal_word = _goal_word
        self.max_turns = _max_turns
        self.turn_list = []
        self.game_over = False
        self.game_won = False

    # declare a way to iterate over a game using its turns
    def __getitem__(self, index):
        return self.turn_list[index]

    # a way to add turns without physically touching the turn list
    def addTurn(self, _turn):
        self.turn_list.append(_turn)

    # check all the conditions in which a game ends in
    def checkGameOver(self):
        # if 6 turns were played and the last played word is not the goal word, game over and not won
        if len(self.turn_list) == self.max_turns and self.turn_list[-1].played_word != self.goal_word:
            self.game_over = True
        # if the last played word is the goal word, game over and won
        elif self.turn_list[-1].played_word == self.goal_word:
            self.game_over = True
            self.game_won = True
        # else, game is not over and not won
        else:
            self.game_over = False
            self.game_won = False


# create a new class to store Turn data
class Turn(object):
    def __init__(self, _turn_num, _played_word):
        self.turn_num = _turn_num
        self.played_word = _played_word
        # a list of possible words that were able to be guesses
        self.previous_dictionary = {}
        # a list of the next possible words according to the turn feedback, in order to pass to the next turn
        self.next_dictionary = {}
        self.turn_feedback = -1

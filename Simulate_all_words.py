# importing modules
from CSV_handler import *
import time
from Progress_bar import *
from Play_wordle_auto import playWordle, printResults

# load the dictionary from a CSV file and maintain a list of game results
word_list = readData()
game_results = []

# print a progress bar
printProgressBarPyCharm(0, len(word_list), prefix='Progress:', suffix='Complete', length=50)
# document the initial time of the test
start = time.time()
# iterate over all the words in the dictionary, use a counter called progress to count the iterations in order to draw a progress bar
for word, progress in zip(word_list, range(len(word_list))):
    # play the game Wordle with each word using "slate" as the starting guess as previously calculated
    game_result = playWordle(word, "slate", word_list)
    game_results.append(game_result)
    # update the progress bar with each iteration
    printProgressBarPyCharm(progress, len(word_list), prefix='Progress:', suffix='Complete ' + str(progress) + ' words analyzed of ' + str(len(word_list)), length=50)
printProgressBarPyCharm(100, 100, prefix='Progress:', suffix='Complete', length=50)
end = time.time()
print("Operation took %f seconds." % (end - start))

# histogram dictionary that counts game wins or losses and number of turns
game_records = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, -1: 0}
for game in game_results:
    if game.game_won:
        game_records[len(game.turn_list)]+=1
    else:
        game_records[-1]+=1

documentGameRecords(game_records)

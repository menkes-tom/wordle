Playing with Data Science to crack the "Wordle" starting word - Using Pandas with Python
--------------------------------------------------------------------------------------------------

* [Wordle original](https://www.powerlanguage.co.uk/wordle/) - Play the classic 1 word per day game
* [Wordle spin-off](https://wordlegame.org/) - Play an unlimited game


Wordle is a daily, turn based guess-the-word internet sensation recently bought by the New York Times.
The rules are simple, you try and guess a 5 letter word and recieve feedback based on your guessed word, letter by letter, slowly providing you with more data for further guesses. You have up to six attempts to reach the daily goal-word.

For example: if the daily word is "stale", and we guessed the word "steps" we will get the following feedback:
(S - correct, T - correct, E - misplaced, P - not in the word, S - misplaced)
And we now know we better proceed with our next guess in the following format:
S,T,_,_,_ - where one of the blanks should be the letter 'E', but not the third letter.

So what is the best way to use this feedback to our advantage?

The goal of this project, is to use data science tools, in order to determine the best word to use as your first guess, with as little spoilers as possible so we can continue to enjoy the game. This means the data collection and analysis was done without taking into account previous goal-words or checking letter positioning frequency.

So how do we approach this?
--------------------------------------------------------------------------------------------------

### - Step 1
My first step was to determine how to match a score to each word, in order to have some information about its probability to be used. I started by mapping the words using Python and Pandas and checking the frequencies of appearance for each letter in the Wordle dictionary. I then averaged the amount of times the letter appeared in the dictionary by the amount of unique letters in the dictionary. I will also take into account the position of each letter. This means I need to check the average frequency of each letter in the first location, second location and so forth..

```
After analysis, the following frequency average was received:
------------------------------------------------------------
   Letter  Frequency
0       e  47.423077
1       a  37.653846
2       r  34.576923
3       o  29.000000
4       t  28.038462
...   ...        ...
21      v   5.884615
22      z   1.538462
23      x   1.423077
24      q   1.115385
25      j   1.038462

[26 rows x 2 columns]

  First_Letter_Frequency  Frequency  ... Fifth_Letter_Frequency  Frequency
0                      s      14.64  ...                      e  18.434783
1                      c       7.92  ...                      y  15.826087
2                      b       6.92  ...                      t  11.000000
3                      t       5.96  ...                      r   9.217391
4                      p       5.68  ...                      l   6.782609


```
We can see that its most likely that a word will start with an 'S' and end with an 'E'

The second step was to encode and generate all the possible feedback outcomes. I used a vector of 5 slots (1 per letter) that recives the values (-1,0,1).
```
-1: The letter does not exist in the daily word
 0: The letter exists but is misplaced
 1: The letter is correct and in the right location
 ```
 
For example: (1,1,1,1,1) - represents guessing the correct word in a given turn.
Using "itertools" in Python, I generated all the possible 242 combinations of the feedback vectors.
 
Step three. Now that I have my encoding, I would like to check every word in the dictionary against all the possible feedback data each vector represents and check according to that vector, what are my remaining options for my next turns. Using the average number of next possible words as a metric to determine which played word will ensure I will be on the best track on my next guesses. This is the most complex stage of the algorithm as it requires crossing ~2300 words from thr Wordle dictionary against each and every one of the 242 possible feedbacks.

In step four, I will add more metrics to my generated dictionary data. Each word now has the average possible next words after its played. In order to have more data for the words, I was also interested in the amount of unique letters in each word. The word "Bobby" only gives me data on 3 letters, B,O and Y, while the word "Steal" gives me data on 5 different letters. Since our goal is playing a game of elimination, unique number of letters in the word would play a crucial part in the decision making. Using the previously generated frequency score for each letter, I added another metric that sums up all the frequencies of all the letters in any given word to play a part in the final scoring of each word.

Step five was coming up with a formula to calculate the score of each word, derived from the three previously generated metrics.
The variables in the equation are:
```
X - Average Remaining Words: The less, the better.
Y - Amount of Unique letter: The more, the better.
Z - Sum of Letter Average Frequency: The larger the better.
M - Sum of Letter Average Positional Frequency: The larger the better
```

And finally the equation to calculate the final score will be: X^(-1)*Y*Z*M. The word with the highest score, will corelate to the best possible starting guess.

```
After analysis, the following starting letter score was received:
------------------------------------------------------------
       Word  Rank_by_remaining words  ...  Score_by_position  Calculated_Score
0     slate                38.716129  ...          58.173244       1250.879852
1     shale                39.941176  ...          56.900936       1092.846721
2     stale                42.380952  ...          54.324013       1067.100634
3     crane                41.854167  ...          55.711706       1065.640759
4     crate                42.586667  ...          53.991706       1052.524235
...     ...                      ...  ...                ...               ...
2310  inbox                67.657143  ...          12.526288         82.531324
2311  nymph                62.828571  ...          12.754247         80.887994
2312  unzip                76.344828  ...          13.844013         73.929013
2313  jumbo                70.245614  ...          13.781739         69.610995
2314  affix                67.176471  ...          13.577057         66.758588

[2315 rows x 6 columns]
```
From that we can derive that playing the words "Slate","Stale","Crate","" or "Cane" as our first guess, will yeild the maximum amount of data (feedback) for our future guesses. Lets put the theory to the test: if we chose to play the word "Affix", we will only get data for 4 words instead of 5, 1 of which is the letter "x" which is in the bottom 5 of the average appearance possibility list.

So how do we verify these results? Since the data set is complete, we can start playing wordle using the word "slate" and check to see how it goes. but where is the fun in that? 
"Why do something by hand for 6 minutes when you can spend 6 hours automating it?"

Step six. I wrote a script that plays the game "Wordle". The script simulates a game of wordle by getting a goal-word and a first word - in our case, the first played word will always be "slate" in order to verify our results from the previous step. After checking the initial guess, the game script goes through the proccess of using the algorithm to get the second word with the highest score, and continues to play until the game was either won or lost and exports the data.

Step seven. Now that we can simulate a full game of "Wordle", I used this script to iterate over all the words in the "Wordle" dictionary and document the results of each game against the starting word "slate" and saved them into a histogram (-1 turns means the game was lost, the goal word was not acheieved by my script; 0 turns, the trivial solution, is when the goal-word was "slate", same as the first played word):

```
Progress: |██████████████████████████████████████████████████| 100.0% Complete
   Number_of_turns  Games_won
0                1          1
1                2         92
2                3        515
3                4        775
4                5        560
5                6        238
6               -1        134

Process finished with exit code 0
```

A quick calculation of the winnning frequency will show that the algorithm wins a game of wordle 94.21% of the time in 6 turns or less, where most games were won in 4 games or less. I was satisfied (for now) with an inaccuracy rate of around 5%.


Notes:
---------------------------------------------------------------------------------------------------
1) Since this analysis does not take into account previously used daily goal words, the results are unbiased and are true for even a fresh game of Wordle, as if today was the first ever day Wordle is up and running.
2) Words with a relative close "distance" were not filtered out, meaning "Slate" and "Stale" do appeare in the top 5 list even though they are composed of the same letters since positional data of a letter plays a critical role in Wordle.
3) Words with similate structure such as "Amuse", "Pause" or Abuse" all using the _,_,U,S,E structure, were not filtered out since grouping words with the same structure would require a level of analysis that would spoil the game and leave less room for enjoyment in the future.

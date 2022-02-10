# wordle (original: https://www.powerlanguage.co.uk/wordle/, spin-off: https://wordlegame.org/)

Playing with Data Science to crack the "Wordle" starting word - Using Pandas with Python
--------------------------------------------------------------------------------------------------

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

My first step was to determine how to match a score to each word, in order to have some information about its probability to be used. I started by mapping the words using Python and Pandas and checking the frequencies of appearance for each letter in the Wordle dictionary. I then averaged the amount of times the letter appeared in the dictionary by the amount of unique letters in the dictionary.

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

The second step was to encode and generate all the possible feedback outcomes. I used a vector of 5 slots (1 per letter) that recives the values (-1,0,1).
-1: The letter does not exist in the daily word
 0: The letter exists but is misplaced
 1: The letter is correct and in the right location
 
For example: (1,1,1,1,1) - represents guessing the correct word in a given turn.
Using "itertools" in Python, I generated all the possible 242 combinations of the feedback vectors.
 
Step three. Now that I have my encoding, I would like to check every word in the dictionary against all the possible feedback data each vector represents and check according to that vector, what are my remaining options for my next turns. Using the average number of next possible words as a metric to determine which played word will ensure I will be on the best track on my next guesses. This is the most complex stage of the algorithm as it requires crossing ~2300 words from thr Wordle dictionary against each and every one of the 242 possible feedbacks.

In step four, I will add more metrics to my generated dictionary data. Each word now has the average possible next words after its played. In order to have more data for the words, I was also interested in the amount of unique letters in each word. The word "Bobby" only gives me data on 3 letters, B,O and Y, while the word "Steal" gives me data on 5 different letters. Since our goal is playing a game of elimination, unique number of letters in the word would play a crucial part in the decision making. Using the previously generated frequency score for each letter, I added another metric that sums up all the frequencies of all the letters in any given word to play a part in the final scoring of each word.

Step five was coming up with a formula to calculate the score of each word, derived from the three previously generated metrics.
The variables in the equation are:
X - Average Remaining Words: The less, the better.
Y - Amount of Unique letter: The more, the better.
Z - Sum of Letter Average Frequency: The larger the better.

And finally the equation to calculate the final score will be: X^(-1)*Y*Z. The word with the highest score, will corelate to the best possible starting guess.


After analysis, the following starting letter score was received:
------------------------------------------------------------
       Word  Rank_by_remaining words  ...  Score_by_frequency  Calculated_Score
0     slate                38.716129  ...          166.500000         21.502666
1     trace                41.974026  ...          166.038462         19.778715
2     stale                42.380952  ...          166.500000         19.643258
3     crate                42.586667  ...          166.038462         19.494184
4     plate                40.250000  ...          154.884615         19.240325
...     ...                      ...  ...                 ...               ...
2310  jiffy                57.483333  ...           60.884615          4.236680
2311  fizzy                56.113208  ...           54.076923          3.854845
2312  dizzy                64.080000  ...           60.346154          3.766926
2313  jazzy                66.391304  ...           58.115385          3.501385
2314  fuzzy                59.042553  ...           46.230769          3.132030

[2315 rows x 5 columns]

From that we can derive that playing the words "Slate","Trace","Crate","" or "Plate" as our first guess, will yeild the maximum amount of data (feedback) for our future guesses. Lets put the theory to the test: if we chose to play the word "Fuzzy", we will only get data for 4 words instead of 5, 1 of which is the letter "Z" which is in the bottom 5 of the average appearance possibility list.

Notes:
---------------------------------------------------------------------------------------------------
1) Since this analysis does not take into account previously used daily goal words, the results are unbiased and are true for even a fresh game of Wordle, as if today was the first every day Wordle is up and running.
2) Words with a relative close "distance" were not filtered out, meaning "Slate" and "Stale" do appeare in the top 5 list even though they are composed of the same letters since positional data of a letter plays a critical role in Wordle.
3) Words with similate structure such as "Amuse", "Pause" or Abuse" all using the _,_,U,S,E structure, were not filtered out since grouping words with the same structure would require a level of analysis that would spoil the game and leave less room for enjoyment in the future.

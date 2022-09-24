
# Scrabble Cheat 

## Overwiev

A simple program written in Python which helps with Scrabble game. <br>
It uses framework CherryPy so it is easy to use it on a mobile phone with a browser. <br>

It works with Polish dictionary but it should be easy to switch the language. <br>

![Screenshot](Screenshot.png)

Blanks are written with italics.<br>
Preview of the new word is written with bold. <br>
In edit mode it is possible mark blanks with a checkbox. <br>
Searching needs player's letters and number of its blanks. <br>
Points are calculating with respecting player's blanks and with blanks on the board. <br>

## How to create own language

You need a file with words which looks like <i>PolishWords.py</i> <br>
See the file <i>PolishScrabble.py</i>. <br>
There you can see that it is needed a dictionary which looks like <i>polishWordScores</i>. <br>
Then you have to create an alphabet from the dictionary <br>
and create a <i>WordList</i> with this alphabet and the word list. <br>
At last you must replace <i>getPolishScrabbleBoard</i> in <i>ScrabbleMain.py</i> with your new function. <br>

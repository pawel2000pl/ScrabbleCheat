from ScrabbleEngine import WordList, ScrabbleBoard    
from PolishWords import wordList

polishWordScores = {"a": 1, "ą": 5, "b": 3, "c": 2, "ć": 6, "d": 2, "e": 1, "ę": 5, "f": 5, "g": 3, "h": 3, "i": 1, "j": 3, "k": 2, "l": 2, "ł": 3, "m": 2, "n": 1, "ń": 7, "o": 1, "ó": 5, "p": 2, "r": 1, "s": 1, "ś": 5, "t": 2, "u": 3, "w": 1, "y": 2, "z": 1, "ź": 9, "ż": 5, " ": 0}
polishAlphabet = set(polishWordScores.keys())

cachedWordList = None

def getPolishScrabbleBoard():
    global cachedWordList
    if cachedWordList is None:
        wl = WordList(wordList, polishAlphabet)
        wl.pointsForLetter = {ord(k): v for k, v in polishWordScores.items()}
        cachedWordList = wl
    else:
        wl = cachedWordList     
    sb = ScrabbleBoard(wl)
    return sb

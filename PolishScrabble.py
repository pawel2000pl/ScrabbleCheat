from ScrabbleEngine import WordList, ScrabbleBoard
from PolishWords import wordList

polishWordScores = {"a": 1, "ą": 5, "b": 3, "c": 2, "ć": 6, "d": 2, "e": 1, "ę": 5, "f": 5, "g": 3, "h": 3, "i": 1, "j": 3, "k": 2, "l": 2, "ł": 3, "m": 2, "n": 1, "ń": 7, "o": 1, "ó": 5, "p": 2, "r": 1, "s": 1, "ś": 5, "t": 2, "u": 3, "w": 1, "y": 2, "z": 1, "ź": 9, "ż": 5, " ": 0}
polishAlphabet = {'m', 'p', 'n', 'e', 'f', 't', 'ę', 'h', 'w', 'y', 'z', 'c', 'ź', 'ó', 'd', 'g', 'a', 'ą', 'ń', 'k', 'ć', 'o', 'i', 'j', 'u', 's', 'l', 'r', 'ż', 'b', 'ł', 'ś'}

cachedWordList = None

def getPolishScrabbleBoard():
    global cachedWordList
    if cachedWordList is None:
        wl = WordList(wordList, polishAlphabet)
        cachedWordList = wl
    else:
        wl = cachedWordList 
    wl.pointsForLetter = {ord(k): v for k, v in polishWordScores.items()}
    sb = ScrabbleBoard(wl)
    return sb
    
    
#sb = getPolishScrabbleBoard()

#sb.fields[7][7] = ord("s")
#sb.fields[7][8] = ord("ł")
#sb.fields[7][9] = ord("o")
#sb.fields[7][10] = ord("w")
#sb.fields[7][11] = ord("o")

#words = sb.getRankedWords([ord(l) for l in "werfya"], 2)
#for word in words:
    #print(str(word))

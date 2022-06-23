from ScrabbleFields import FieldType, ScrabbleBoardFields
from copy import deepcopy

class WordList:
    
    def __init__(self, rawInput: str, alphabet, maxWordLength: int = 15):
        
        #f = open(fileName, "r")
        #rawInput = f.read().lower()
        #f.close()
        self.wordList = tuple(w for w in rawInput.split("\n") if len(w) > 1 and len(w) <= maxWordLength and len(set(w).difference(alphabet)) == 0)
        self.wordSet = set(self.wordList)
        self.wordLists = tuple(tuple(ord(l) for l in w) for w in self.wordList)
        self.maxWordLength = max(len(w) for w in self.wordList)
        self.lengthIndex = tuple(tuple(j for j, word in enumerate(self.wordLists) if len(word)==i) for i in range(self.maxWordLength))
        self.alphabet = alphabet.copy()
        self.pointsForLetter = {letter: 1 for letter in self.alphabet}
        
    def wordExists(self, word: str):
        return word in self.wordSet
        
class RankedWord:
    
    def __init__(self, word: str, x: int, y: int, dx: int, score: int, blanks = []):
        self.word = word
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = 1-dx
        self.score = score           
        self.blanks = blanks        
        
    def __str__(self):
        return str(self.score) + " x:" + str(self.x) + " y:" + str(self.y) + [" H", " V"][self.dy] + "  \"" + self.word.upper() + "\"  blanks: " + str(self.blanks)
        
        
class EmptyPlaceOnBoard:
    
    def __init__(self, x: int, y: int, length: int, dx: int, board):
        dy = 1-dx
                
        if (dx==1) and (not ((x==0 or board.fields[x-1][y]==ord(" ")) and (x+length-1<board.width) and (x+length==board.width or board.fields[x+length][y]==ord(" ")))):
            self.possible = False
            return
        if (dy==1) and (not ((y==0 or board.fields[x][y-1]==ord(" ")) and (y+length-1<board.height) and (y+length==board.height or board.fields[x][y+length]==ord(" ")))):
            self.possible = False
            return
        
        self.dx = dx
        self.dy = dy
        self.length = length
        self.x = x
        self.y = y
        self.letterRequirments = []
        self.wordRequirments = []
        self.parsedWords = []
        self.board = board
        
        ix=x
        iy=y        
        center = (board.width//2, board.height//2)
        touch = False
        for i in range(length):
            field = board.fields[ix][iy] 
            if field != ord(" "):
                self.letterRequirments.append((i, field))  
            else:
                r = self.checkPerpendicularRequirment(ix, iy, i)
                if r != None:
                    self.wordRequirments.append(r)
            touch = touch or (center[0]==ix and center[1]==iy)
            ix+=dx
            iy+=dy
                
        self.possible = touch or len(self.letterRequirments) + len(self.wordRequirments) > 0
        
        if self.possible:
            self.setOfLetterRequirmentPositions = set(letterRequirment[0] for letterRequirment in self.letterRequirments)
            self.letterRequirments = tuple(requirment for requirment in self.letterRequirments)
            self.wordRequirments = tuple(requirment for requirment in self.wordRequirments)
        
    def checkPerpendicularRequirment(self, x, y, i):
        
        begin = []
        end = []
        ix = x-self.dy
        iy = y-self.dx
        while ix in range(self.board.width) and iy in range(self.board.height) and self.board.fields[ix][iy] != ord(" "):
            begin.insert(0, chr(self.board.fields[ix][iy]))
            ix-=self.dy
            iy-=self.dx
        ix = x+self.dy
        iy = y+self.dx
        while ix in range(self.board.width) and iy in range(self.board.height) and self.board.fields[ix][iy] != ord(" "):
            end.append(chr(self.board.fields[ix][iy]))
            ix+=self.dy
            iy+=self.dx
            
        if len(begin) + len(end) == 0:
            return None
        return (str().join(begin), i, str().join(end)) 
        
    def parse(self, wordAsList):
        if (not self.possible) or (len(wordAsList) != self.length):
            return False
        return self.fastParse(wordAsList)
    
    def fastParse(self, wordAsList):
        try:
            for letterRequirment in self.letterRequirments:
                if wordAsList[letterRequirment[0]] != letterRequirment[1]:
                    return False
            for wordRequirment in self.wordRequirments:
                if not self.board.wordIndex.wordExists(wordRequirment[0] + chr(wordAsList[wordRequirment[1]]) + wordRequirment[2]):
                    return False
            self.parsedWords.append(wordAsList)
            return True
        except:
            return False
        
    def checkWord(self, wordAsList, letterList, blankCount):     
        availableLetters = letterList.copy()
        for i, l in enumerate(wordAsList):
            if i not in self.setOfLetterRequirmentPositions:
                try:
                    availableLetters.remove(l)
                except:
                    blankCount -= 1
                    if blankCount < 0:
                        return False
        return True     
    
    def removeImpossibleWords(self, letterList, blankCount):
        letterList.sort()
        self.parsedWords = [word for word in self.parsedWords if self.checkWord(word, letterList, blankCount)]
        return len(self.parsedWords)
                
    def magicField(self, x, y, baseLetterScores, scores, wordMultiplication):
        ft = self.board.fieldTypes[x][y]                
        if ft == FieldType.Normal:
            scores += baseLetterScores
        elif ft == FieldType.DoubleLetter:
            scores += 2*baseLetterScores
        elif ft == FieldType.TripleLetter:
            scores += 3*baseLetterScores   
        elif ft == FieldType.DoubleWord:
            wordMultiplication *= 2  
            scores += baseLetterScores
        elif ft == FieldType.TripleWord:
            wordMultiplication *= 3
            scores += baseLetterScores
        return (scores, wordMultiplication)
                
    def createRankedWords(self, letterList):
        results = []
        
        for word in self.parsedWords:
            wordMultiplication = 1        
            ix = self.x
            iy = self.y
            dx = self.dx
            dy = self.dy
            usedLetters = 0
            availableLetters = letterList.copy()
            usedBlanks = []
            insertedBlanks = []
            scoresForLetter = []
            for letter in word:                
                baseLetterScores = self.board.wordIndex.pointsForLetter[letter]   
                if self.board.fields[ix][iy] == ord(" "):
                    usedLetters += 1
                    (scoreForLetter, wordMultiplication) = self.magicField(ix, iy, baseLetterScores, 0, wordMultiplication)
                    scoresForLetter.append(scoreForLetter)
                    try:
                        availableLetters.remove(letter)
                    except:
                        usedBlanks.append(letter)
                else:
                    if self.board.blanks[ix][iy]:
                        scoresForLetter.append(0)
                    else:
                        scoresForLetter.append(baseLetterScores)
                ix += dx
                iy += dy
                
            for blank in usedBlanks:
                minIndex = -1
                minValue = max(scoresForLetter)+1
                for i, letter in enumerate(word):
                    if blank == letter and minValue > scoresForLetter[i] and scoresForLetter[i] != 0:
                        minIndex = i
                        minValue = scoresForLetter[i]
                assert minIndex >= 0
                scoresForLetter[minIndex] = 0
                insertedBlanks.append((minIndex, chr(blank)))
            
            scores = sum(scoresForLetter) * wordMultiplication
                            
            for requrment in self.wordRequirments:
                baseScores = sum(self.board.wordIndex.pointsForLetter[l] for l in [ord(c) for c in requrment[0]+requrment[2]])
                baseLetterScores = scoresForLetter[requrment[1]] 
                ix = self.x+requrment[1]*self.dx
                iy = self.y+requrment[1]*self.dy
                if self.board.fields[ix][iy] == ord(" "):
                    (baseScores, multiplication) = self.magicField(ix, iy, baseLetterScores, baseScores, 1)
                    scores += baseScores * multiplication
                
            if usedLetters >= self.board.premiumPointTrigger:
                scores += self.board.premiumPointValue

            results.append(RankedWord(str().join([chr(c) for c in word]), self.x, self.y, self.dx, scores, insertedBlanks))
        
        return results


class ScrabbleBoard:
    
    def __init__(self, wordIndex):        
        self.fields = [[ord(" ") for col in row] for row in ScrabbleBoardFields]
        self.blanks = [[False for col in row] for row in ScrabbleBoardFields]
        self.fieldTypes = ScrabbleBoardFields
        self.width = len(self.fields)
        self.height = len(self.fields[0])
        self.wordIndex = wordIndex
        self.premiumPointTrigger = 7
        self.premiumPointValue = 50
        
    def getPossiblePlaces(self):
        results = []
        for x in range(self.width):
            for y in range(self.height):
                for dx in [1, 0]:
                    for i in range(self.wordIndex.maxWordLength):
                        results.append(EmptyPlaceOnBoard(x, y, i, dx, self))
        return [place for place in results if place.possible]
    
    def placeWord(self, wordAsList):
        places = self.getPossiblePlaces()
        results = []
        for place in places:
            if place.parse(wordAsList):
                result.extend(place.createRankedWords(wordAsList))
        return results
        
    def getPossibleWorlds(self, letterList, blankCount, progress: dict = None):
        places = self.getPossiblePlaces()
        count = 0
        placesLen = len(places)
        for i, place in enumerate(places):
            for j in self.wordIndex.lengthIndex[place.length]:
                place.fastParse(self.wordIndex.wordLists[j])
            count+=place.removeImpossibleWords(letterList, blankCount)    
            if progress is not None:
                progress["percent"] = i/placesLen
                progress["max"] = placesLen
                progress["current"] = i       
        return places                    
    
    def getRankedWords(self, letterList, blankCount, progress: dict = None):
        places = self.getPossibleWorlds(letterList, blankCount, progress)
        result = []
        for place in places:
            result.extend(place.createRankedWords(letterList))
        result.sort(reverse=True, key=lambda w: w.score)
        return result
    
    def getFieldsAndBlanks(self):
        return (self.fields, self.blanks, [[False for col in row] for row in ScrabbleBoardFields])
                    
    def placeRankedWord(self, word, applyChanges=True):
        ix = word.x
        iy = word.y
        locations = []
        fields = deepcopy(self.fields)
        blanks = deepcopy(self.blanks)
        updated = [[False for col in row] for row in ScrabbleBoardFields]
        for l in word.word:
            fields[ix][iy] = ord(l)
            updated[ix][iy] = fields[ix][iy] != self.fields[ix][iy]
            locations.append((ix, iy))
            ix += word.dx
            iy += word.dy
        for b in word.blanks:
            pos = locations[b[0]]
            blanks[pos[0]][pos[1]] = True     
        if applyChanges:
            self.fields = fields
            self.blanks = blanks
        return (fields, blanks, updated)
        

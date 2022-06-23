from enum import Enum

class FieldType(Enum):
    Normal = 0
    DoubleLetter = 1
    TripleLetter = 2
    DoubleWord = 3
    TripleWord = 4
    
    def createEmptyDictionary(emptyField = 0):
        return {FieldType.Normal: emptyField, FieldType.DoubleLetter: emptyField, FieldType.TripleLetter: emptyField, FieldType.DoubleWord: emptyField, FieldType.TripleWord: emptyField}
    

ScrabbleBoardFields = (
    (FieldType.TripleWord, FieldType.Normal, FieldType.Normal, FieldType.DoubleLetter, FieldType.Normal, FieldType.Normal, FieldType.Normal,
    FieldType.TripleWord, FieldType.Normal, FieldType.Normal, FieldType.Normal, FieldType.DoubleLetter, FieldType.Normal, FieldType.Normal, FieldType.TripleWord),
    (FieldType.Normal, FieldType.DoubleWord, FieldType.Normal, FieldType.Normal, FieldType.Normal, FieldType.TripleLetter, FieldType.Normal,
    FieldType.Normal, FieldType.Normal, FieldType.TripleLetter, FieldType.Normal, FieldType.Normal, FieldType.Normal, FieldType.DoubleWord, FieldType.Normal),
    (FieldType.Normal, FieldType.Normal, FieldType.DoubleWord, FieldType.Normal, FieldType.Normal, FieldType.Normal, FieldType.DoubleLetter,
    FieldType.Normal, FieldType.DoubleLetter, FieldType.Normal, FieldType.Normal, FieldType.Normal, FieldType.DoubleWord, FieldType.Normal, FieldType.Normal),
    (FieldType.DoubleLetter, FieldType.Normal, FieldType.Normal, FieldType.DoubleWord, FieldType.Normal, FieldType.Normal, FieldType.Normal,
    FieldType.DoubleLetter, FieldType.Normal, FieldType.Normal, FieldType.Normal, FieldType.DoubleWord, FieldType.Normal, FieldType.Normal, FieldType.DoubleLetter),
    (FieldType.Normal, FieldType.Normal, FieldType.Normal, FieldType.Normal, FieldType.DoubleWord, FieldType.Normal, FieldType.Normal, FieldType.Normal,
    FieldType.Normal, FieldType.Normal, FieldType.DoubleWord, FieldType.Normal, FieldType.Normal, FieldType.Normal, FieldType.Normal),
    (FieldType.Normal, FieldType.TripleLetter, FieldType.Normal, FieldType.Normal, FieldType.Normal, FieldType.TripleLetter, FieldType.Normal,
    FieldType.Normal, FieldType.Normal, FieldType.TripleLetter, FieldType.Normal, FieldType.Normal, FieldType.Normal, FieldType.TripleLetter, FieldType.Normal),
    (FieldType.Normal, FieldType.Normal, FieldType.DoubleLetter, FieldType.Normal, FieldType.Normal, FieldType.Normal, FieldType.DoubleLetter,
    FieldType.Normal, FieldType.DoubleLetter, FieldType.Normal, FieldType.Normal, FieldType.Normal, FieldType.DoubleLetter, FieldType.Normal, FieldType.Normal),
    (FieldType.TripleWord, FieldType.Normal, FieldType.Normal, FieldType.DoubleLetter, FieldType.Normal, FieldType.Normal, FieldType.Normal,
    FieldType.Normal, FieldType.Normal, FieldType.Normal, FieldType.Normal, FieldType.DoubleLetter, FieldType.Normal, FieldType.Normal, FieldType.TripleWord),
    (FieldType.Normal, FieldType.Normal, FieldType.DoubleLetter, FieldType.Normal, FieldType.Normal, FieldType.Normal, FieldType.DoubleLetter,
    FieldType.Normal, FieldType.DoubleLetter, FieldType.Normal, FieldType.Normal, FieldType.Normal, FieldType.DoubleLetter, FieldType.Normal, FieldType.Normal),
    (FieldType.Normal, FieldType.TripleLetter, FieldType.Normal, FieldType.Normal, FieldType.Normal, FieldType.TripleLetter, FieldType.Normal,
    FieldType.Normal, FieldType.Normal, FieldType.TripleLetter, FieldType.Normal, FieldType.Normal, FieldType.Normal, FieldType.TripleLetter, FieldType.Normal),
    (FieldType.Normal, FieldType.Normal, FieldType.Normal, FieldType.Normal, FieldType.DoubleWord, FieldType.Normal, FieldType.Normal, FieldType.Normal,
    FieldType.Normal, FieldType.Normal, FieldType.DoubleWord, FieldType.Normal, FieldType.Normal, FieldType.Normal, FieldType.Normal),
    (FieldType.DoubleLetter, FieldType.Normal, FieldType.Normal, FieldType.DoubleWord, FieldType.Normal, FieldType.Normal, FieldType.Normal,
    FieldType.DoubleLetter, FieldType.Normal, FieldType.Normal, FieldType.Normal, FieldType.DoubleWord, FieldType.Normal, FieldType.Normal, FieldType.DoubleLetter),
    (FieldType.Normal, FieldType.Normal, FieldType.DoubleWord, FieldType.Normal, FieldType.Normal, FieldType.Normal, FieldType.DoubleLetter,
    FieldType.Normal, FieldType.DoubleLetter, FieldType.Normal, FieldType.Normal, FieldType.Normal, FieldType.DoubleWord, FieldType.Normal, FieldType.Normal),
    (FieldType.Normal, FieldType.DoubleWord, FieldType.Normal, FieldType.Normal, FieldType.Normal, FieldType.TripleLetter, FieldType.Normal,
    FieldType.Normal, FieldType.Normal, FieldType.TripleLetter, FieldType.Normal, FieldType.Normal, FieldType.Normal, FieldType.DoubleWord, FieldType.Normal),
    (FieldType.TripleWord, FieldType.Normal, FieldType.Normal, FieldType.DoubleLetter, FieldType.Normal, FieldType.Normal, FieldType.Normal,
    FieldType.TripleWord, FieldType.Normal, FieldType.Normal, FieldType.Normal, FieldType.DoubleLetter, FieldType.Normal, FieldType.Normal, FieldType.TripleWord));  

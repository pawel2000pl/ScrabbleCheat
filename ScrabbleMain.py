import cherrypy
from PolishScrabble import getPolishScrabbleBoard
from threading import Thread
from ScrabbleFields import FieldType

class ScrabbleThread(Thread):
    
    def __init__(self, board, letters, blanks):
        super().__init__()
        self.letters = letters
        self.blanks = blanks
        self.results = []
        self.done = False
        self.board = board
        self.progress = {"percent": 0}
    
    def run(self):
        self.done = False
        self.results = tuple(self.board.getRankedWords([ord(l) for l in self.letters], self.blanks, self.progress))
        self.done = True
        
    def stringProgress(self):
        return str(round(self.progress["percent"]*100)) + "%"
            
def wrapInBody(code):
    return '<html><head><style>table, th, td {border: 1px solid black;}</style></head><body>' + code + '</body> </html>'
    
def mainTable(topleft="", topright="", bottomleft="", bottomright=""):
    return '<table style="background-color:MediumSeaGreen;"><tr><td>'+topleft+'</td><td>'+topright+'</td></tr><tr><td>'+bottomleft+'</td><td>'+bottomright+'</td></tr></table>'
    
def boardToHtml(board, wordToApply=None, editMode=False):    
    result = ['<form method="post" action="index"><table>']
    
    fieldColors = dict()
    fieldColors[FieldType.Normal] = "SeaGreen"
    fieldColors[FieldType.DoubleLetter] = "LightBlue"
    fieldColors[FieldType.TripleLetter] = "DarkBlue"
    fieldColors[FieldType.DoubleWord] = "Coral"
    fieldColors[FieldType.TripleWord] = "Crimson"
    
    if wordToApply is None:
        (fields, blanks, updates) = board.getFieldsAndBlanks()
    else:
        (fields, blanks, updates) = board.placeRankedWord(wordToApply, applyChanges=False)
    
    if editMode:
        result.append('<input type="hidden" name="editing" value="True">')
    else:
        result.append('<input type="hidden" name="editing" value="False">')
    
    for j in range(board.height):
        result.append("<tr>\n")
        for i in range(board.height):
            cell = fields[i][j]
            cellStr = chr(cell)
            
            if editMode:
                if cellStr == " ":
                    cellStr = ""
                cellStr = '<input type="text" style="width:20px;height:25px;" maxlength="1" name="field_x'+str(i)+'y'+str(j)+'" value="'+cellStr+'">'  
                if blanks[i][j]:
                    cellStr += '<input type="checkbox" maxlength="1" name="blank_x'+str(i)+'y'+str(j)+'" checked="True">' 
                else:
                    cellStr += '<input type="checkbox" maxlength="1" name="blank_x'+str(i)+'y'+str(j)+'">' 
            else:
                cellStr = '<center>'+cellStr+'</center>'
                
                    
            if updates[i][j]:
                cellStr = '<b>'+cellStr+'</b>'
            if blanks[i][j]:
                cellStr = '<i>'+cellStr+'</i>'
            
            if (not editMode) and (cell != ord(" ")):
                cellStr = '<table style="width:100%;height:100%;background:LemonChiffon;"><tr><td>'+cellStr+'</td></tr></table>'
                
            result.append('<td style="width:40px;height:40px;background:'+fieldColors[board.fieldTypes[i][j]]+';">'+cellStr+'</td>\n')
            
        result.append("</tr>\n")
        
    result.append('</table>\n')
    if editMode:
        result.append('<input type="submit" value="Save"><input type="reset" value="Reset">')
    result.append('</form>')
    return str().join(result)
            
def wrapButtonInLink(index, button):
    return '<a href="/index?showWord='+str(index)+'">'+button+'</a>'

class ScrabbleMain(object):
    
    def __init__(self):
        getPolishScrabbleBoard()
        
    def setDefaults(self):
        cherrypy.session.setdefault('letters', "")
        cherrypy.session.setdefault('blanks', "0")
        cherrypy.session.setdefault('page', 0)
        try:
            board = cherrypy.session['board']
        except:
            board = getPolishScrabbleBoard()
            cherrypy.session.setdefault('board', board)   
            
        try:
            thread = cherrypy.session['results']
        except:
            newThread = ScrabbleThread(board, "", 0)
            newThread.done = True
            cherrypy.session.setdefault('results', newThread)         

    def getWordForm(self):
        return '''<form method="get" action="calculate">
                    <input type="text" value="''' + cherrypy.session['letters'] + '''" name="letters" />              
                    <input type="number" min="0" max="15" step="1" style="width:64px;" value="''' + str(cherrypy.session['blanks']) + '''" name="blanks" />
                    <button type="submit">Search</button>
                  </form>'''
                  
    def showProgress(self, always=True):
        thread = cherrypy.session['results']
        return "" if thread.done else '<br><center>Please wait... <br>'+thread.stringProgress()+'<br><a href="/index">Refresh list on board</a></center><br>'
        
    @cherrypy.expose
    def calculate(self, letters=None, blanks=None):
        self.setDefaults()
        if letters is not None and blanks is not None:
            cherrypy.session['letters'] = letters
            try:
                blanks = int(blanks)
                cherrypy.session['blanks'] = int(blanks)
            except:
                cherrypy.session['blanks'] = 0
                blanks = 0
            thread = ScrabbleThread(cherrypy.session['board'], letters, blanks) 
            thread.start()
            cherrypy.session['results'] = thread
            
        result = self.showProgress()
        if cherrypy.session['results'].done:
            result += ' <meta http-equiv=\"refresh\" content=\"1; url=/index\">'
        else:
            result += ' <meta http-equiv=\"refresh\" content=\"1; url=/calculate\">'
        return wrapInBody(result)

    def applyBoard(self, dic):
        board = cherrypy.session['board']
        for j in range(board.height):
            for i in range(board.height):
                fieldName = 'field_x'+str(i)+'y'+str(j) 
                blankName = 'blank_x'+str(i)+'y'+str(j)
                if fieldName in dic:
                    c = dic[fieldName]
                    if c == "":
                        c = " "
                    board.fields[i][j] = ord(c)
                board.blanks[i][j] = blankName in dic


    @cherrypy.expose
    def index(self, **args):
        self.setDefaults()
        try:
            page = int(args["page"])
        except:
            page = int(cherrypy.session['page'])
        cherrypy.session['page'] = page
        
        try:
            editMode = bool(args["editMode"])
        except:
            editMode = False     
            
        board = cherrypy.session['board']
            
        if 'editing' in args:
            self.applyBoard(args)
            
        if 'clearBoard' in args:
            board = getPolishScrabbleBoard()
            cherrypy.session['board'] = board
            newThread = ScrabbleThread(board, "", 0)
            newThread.done = True
            cherrypy.session['results'] = newThread
            return 'Clearing... <meta http-equiv="refresh" content="1; url=/index">'        
        
        editModeLink = '<a href="/index?editMode=True">Edit board</a>   <a href="/index">Cancel editing (if any)</a> <a href="/index?clearBoard=True">Clear board</a>'
        generatePageButton = lambda number: '<a href="/index?page='+str(number)+'"> '+('[<b>'+str(number+1)+'</b>]' if page==number else '['+str(number+1)+']')+' </a>'
        resultsPerPage = 20        
        pageRange = list(range(resultsPerPage*page, resultsPerPage*(page+1)))
        thread = cherrypy.session['results']
        
        pageList = list(set(range(len(thread.results)//resultsPerPage)).intersection(set(range(page-5, page+5))).union({0, len(thread.results)//resultsPerPage-1}))
        pageList.sort()
        if len(thread.results) > 0:
            pageMenu = str().join([generatePageButton(i) for i in pageList]) + "<br><br>"
        else:
            pageMenu = ""
        
        try:
            wordsToStr = str().join([wrapButtonInLink(i, str(word)) + "<br>" for i, word in enumerate([thread.results[result] for result in pageRange])])
        except:
            wordsToStr = ""
            
        if 'applyWorld' in args:
            try:
                wordToApply = thread.results[pageRange[int(args['applyWorld'])]]
                board.placeRankedWord(wordToApply, applyChanges=True)
            except:
                pass
            
        try:
            wordToApply = thread.results[pageRange[int(args['showWord'])]]
            wordsToStr += '<br><br><a href="/index?applyWorld='+args['showWord']+'">Apply world</a>'
        except:
            wordToApply = None
            
        return wrapInBody(mainTable(topleft=boardToHtml(board, wordToApply=wordToApply, editMode=editMode), bottomleft=editModeLink, topright=pageMenu + wordsToStr + self.showProgress(), bottomright=self.getWordForm()))
    

if __name__ == '__main__':    
    conf = {'/': {'tools.sessions.on': True}}
    cherrypy.server.socket_host = "0.0.0.0" 
    cherrypy.server.socket_port = 8080
    cherrypy.quickstart(ScrabbleMain(), '/', conf)

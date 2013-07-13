# Abdelwahab Bourai + abourai + Section B
#collaborators: acrigler + ashrethr + dhaddox
  
from Tkinter import *
import random
import copy

#used to draw walls for moreSnake
#functional only when game is not
#over and game is paused
def mousePressed(event, canvas):
    if event.num == 1:
        print 'hi :D'
    if(canvas.data.game == 'moreSnake'):
        if(canvas.data.gameOver == False and canvas.data.isPaused == True):
            drawWall(canvas,event.x,event.y)
            redrawSnake(canvas)

#overall keyPressed
#calls each games keyPressed based on the number inputted
def keyPressed(event,canvas):
    if(event.char == '0'):
        canvas.data.game = ''
        initAll(canvas)
        redrawAll(canvas)
    elif(event.char == '1'):
        canvas.data.game = 'tetris'
        initTetris(canvas)
    elif(event.char == '2'):
        canvas.data.game = 'snake'
        initSnake(canvas)
    elif(event.char == '3'):
        canvas.data.game = 'moreSnake'
        initMoreSnake(canvas)
    elif(canvas.data.game == 'moreSnake' or canvas.data.game == 'snake'):
        moreSnakeKeyPressed(event,canvas)
    elif(canvas.data.game == 'tetris'):
        tetrisKeyPressed(event,canvas)

def tetrisKeyPressed(event, canvas):
    canvas = event.widget.canvas
    canvas.data.keyText = event.keysym
    #restarts game
    if(event.char == 'r'):
        initTetris(canvas)
    #these can only be invoked when the game is not over
    if(canvas.data.tetrisGameOver == False):
        if(canvas.data.keyText == 'Up'): rotateFallingPiece(canvas)
        elif(canvas.data.keyText == 'Down'): changeTetrisSpeed(canvas)
        elif(canvas.data.keyText == 'Right'): moveFallingPiece(canvas,0,1)
        elif(canvas.data.keyText == 'Left'): moveFallingPiece(canvas,0,-1)
    redrawAll(canvas)

#shared keyPressed for both snake and moreSnakes
def moreSnakeKeyPressed(event, canvas):
    canvas.data.keyText = event.keysym
    canvas.data.ignoreNextTimerEvent = True
    #restarts game based on which game is running, snake or moreSnake
    if(event.char == 'r'):
        if(canvas.data.game == 'snake'): initSnake(canvas)
        elif(canvas.data.game == 'moreSnake'): initMoreSnake(canvas)
    #pauses game only if game is moreSnake
    elif(event.char == 'p' and canvas.data.game == 'moreSnake'):
            canvas.data.isPaused = not canvas.data.isPaused
            canvas.data.ignoreNextTimerEvent = False
    #snake can be controlled only when game isn't paused or over        
    if(canvas.data.gameOver == False and canvas.data.isPaused == False):
        if(canvas.data.keyText == 'Up'): moveSnake(canvas,-1,0)
        elif(canvas.data.keyText == 'Down'): moveSnake(canvas,1,0)
        elif(canvas.data.keyText == 'Right'): moveSnake(canvas,0,1)
        elif(canvas.data.keyText == 'Left'): moveSnake(canvas,0,-1)
        #ends game
        elif(event.char == 'q'): gameOver(canvas)
        #used to see numbers in cell
        elif(event.char == 'd'):
            canvas.data.debugMode = not canvas.data.debugMode
        redrawSnake(canvas)

#timerFired used for all games
def timerFired(canvas):
    ignore = canvas.data.ignoreNextTimerEvent
    canvas.data.ignoreNextTimerEvent = False
    #runs only when game isnt paused or over
    #runs only when game is either snake or moreSnake
    if(canvas.data.isPaused == False and canvas.data.gameOver == False and
       ignore == False and (canvas.data.game == 'moreSnake' or
                            canvas.data.game == 'snake')):
            #moves snake in a given direction after each delay
            moveSnake(canvas, canvas.data.snakeDrow, canvas.data.snakeDcol)
    #moves pieces for tetris
    elif(canvas.data.tetrisGameOver == False and canvas.data.game == 'tetris'):
        redrawAll(canvas)
        if(moveFallingPiece(canvas,1,0) == False):
            placeFallingPiece(canvas), newFallingPiece(canvas)
            if(fallingPieceIsLegal(canvas) == False):canvas.data.tetrisGameOver = True
        removeFullRows(canvas), redrawAll(canvas)
    elif(canvas.data.gameOver == False and canvas.data.game == 'moreSnake'):
        redrawAll(canvas)
    #checks when food eaten is 3, then speeds up game
    if(canvas.data.game == 'moreSnake'): checkLevel(canvas)
    #prevents speed from snake affected speed for tetris
    if(canvas.data.game == 'tetris'):
       delay = canvas.data.tetrisSpeed # milliseconds
    else: delay = canvas.data.speed # milliseconds        
    def f(): timerFired(canvas)
    canvas.after(delay, f) # pause, then call timerFired again

#overall redraw
#calls specific redraws based on game currently being played
def redrawAll(canvas):
    #clears canvas
    canvas.delete(ALL)
    #used for launch screen
    if(canvas.data.game == ''):
        canvas.create_text(canvas.data.width/2,canvas.data.width/6
                           , text = 'Press 1 for Tetris')
        canvas.create_text(canvas.data.width/2,2 * canvas.data.width/6,
                           text = 'Press 2 for Snake')
        canvas.create_text(canvas.data.width/2,3 * canvas.data.width/6,
                           text = 'Press 3 for More Snake')
        canvas.create_text(canvas.data.width/2,4 * canvas.data.width/6,
                           text = 'Press 0 to return to launch screen')
    #redraw for snake and more snake
    elif(canvas.data.game == 'moreSnake' or canvas.data.game == 'snake'):
        redrawSnake(canvas)
    #redraw for tetris
    elif(canvas.data.game == 'tetris'):
        redrawTetris(canvas)

def changeTetrisSpeed(canvas):
    canvas.data.tetrisSpeed = 5

#redraws tetris board and pieces
def redrawTetris(canvas):
    canvas.delete(ALL)
    drawGame(canvas)
    #places score on top left
    drawScore(canvas)

#redraws snake board and snake, food, poison
def redrawSnake(canvas):
    canvas.delete(ALL)
    #if game is lost, prints mean message
    if(canvas.data.gameOver == True):
        canvas.create_text(canvas.data.width/2,canvas.data.height/4,text =
                           'YOU LOSE! GOOD DAY SIR!',font ='Helvetica 40 bold')
        #if game is moreSnake, prints a list of all high scores in this session
        if(canvas.data.game == 'moreSnake'):
            canvas.create_text(canvas.data.width/2,canvas.data.height/3,
                               text = 'High Scores:', font = 'Helvetica 20')
            canvas.data.highScoreList.append(canvas.data.moreSnakeScore)
            hs = sorted(canvas.data.highScoreList)
            hs.reverse()
            if len(hs) >= 3 : a =3
            else: a = len(hs)
            for i in xrange(a):
                canvas.create_text(canvas.data.width/2,
                                   canvas.data.height/2 + i * canvas.data.height/24,text = str(hs[i]))
    else:
        #if game is not lost, continues redrawing board
        drawSnakeBoard(canvas)

#initializes all necessary values for snake
def initSnake(canvas):
    canvas.data.game = 'snake'
    canvas.data.rows = 15
    canvas.data.cols = 15
    canvas.data.margin = (canvas.data.width/2) / canvas.data.rows
    canvas.data.snakeDrow,canvas.data.snakeDcol = 0,0
    canvas.data.quit,canvas.data.gameOver = False, False
    canvas.data.headRow, canvas.data.headCol = 0, 0
    canvas.data.snakeScore, canvas.data.speed  = 0,150
    canvas.data.ignoreNextTimerEvent = False
    canvas.data.debugMode = False
    canvas.data.snakeBoard = []
    loadSnakeBoard(canvas)

#initializes all values needed for moreSnake
def initMoreSnake(canvas):
    canvas.data.game = 'moreSnake'
    canvas.data.isPaused = False
    canvas.data.rows = 15
    canvas.data.cols = 15
    canvas.data.margin = (canvas.data.width/2) / canvas.data.rows
    canvas.data.snakeDrow,canvas.data.snakeDcol = 0,0
    canvas.data.quit,canvas.data.gameOver = False, False
    canvas.data.headRow, canvas.data.headCol = 0, 0
    canvas.data.moreSnakeScore, canvas.data.speed  = 0,150
    canvas.data.ignoreNextTimerEvent = False
    canvas.data.debugMode = False
    canvas.data.snakeBoard = []
    loadSnakeBoard(canvas)

#initializes all values needed for Tetris
def initTetris(canvas):
    canvas.data.tetrisGameOver = False
    canvas.data.rows = 20
    canvas.data.cols = 15
    canvas.data.margin = (canvas.data.width/4 *3) / canvas.data.rows
    canvas.data.tetrisScore = 0
    canvas.data.fallingPiece = []
    canvas.data.fallingPieceColor = ''
    canvas.data.fallingPieceRows = 0
    canvas.data.fallingPieceCols = 0
    canvas.data.tetrisSpeed  = 200
    canvas.data.emptyColor = 'blue'
    canvas.data.gridSize = 3
    canvas.data.board = [[canvas.data.emptyColor for col in xrange(canvas.data.cols)]
                        for row in xrange(canvas.data.rows)]
    canvas.data.tetrisPieces = [iPiece(), jPiece(), lPiece(), oPiece(),
                                sPiece(), tPiece(), zPiece()]
    canvas.data.tetrisPiecesColors = ['red', 'yellow', 'magenta', 'pink',
                                     'cyan', 'green', 'orange']
    newFallingPiece(canvas)
    drawGame(canvas)

#initializes general values
def initAll(canvas):
    canvas.data.game = ''
    canvas.data.isPaused = False
    canvas.data.snakeDrow,canvas.data.snakeDcol = 0,0
    canvas.data.quit,canvas.data.gameOver = False, False
    canvas.data.tetrisGameOver = False
    canvas.data.headRow, canvas.data.headCol = 0, 0
    canvas.data.snakeScore, canvas.data.speed  = 0,150
    canvas.data.tetrisSpeed  = 200
    canvas.data.moreSnakeScore = 0
    canvas.data.ignoreNextTimerEvent = False
    canvas.data.debugMode = False
    canvas.data.snakeBoard = []

#draws tetris game
def drawGame(canvas):
    #draws orange background
    canvas.create_rectangle(0,0,canvas.data.width,canvas.data.height,
                            fill = 'orange', width = 0)
    #draws full board
    drawTetrisBoard(canvas)
    #draws random falling tetris piece
    drawFallingPiece(canvas)
    #if game is lost, game prints lose screen
    if(canvas.data.tetrisGameOver == True):
        canvas.create_text(canvas.data.width/3,canvas.data.height/4,
                           text ='Game Over!',fill = 'white', font ='Helvetica 40')

#loops through every location on game and prints individual cell
def drawTetrisBoard(canvas):
    for row in xrange(canvas.data.rows):
        for col in xrange(canvas.data.cols):
            drawTetrisCell(canvas,row,col,canvas.data.board[row][col])

#draws blue cell with thick black borders
def drawTetrisCell(canvas,r,c,color):
    m = canvas.data.margin
    gs = canvas.data.gridSize
    cs = canvas.data.cellSize
    canvas.create_rectangle(m + c*cs, m + r*cs, m + c*cs + cs,
                            m + r*cs + cs, fill = 'black', width = 0)
    canvas.create_rectangle(m + c*cs+ gs, m + r*cs + gs, m + c*cs + cs - gs,
                            m + r*cs + cs - gs, fill = color, width = 0)

#the following functions draw the different tetris piece labeled
#zPiece, tPiece, sPiece, oPiece, lPiece, jPiece, and iPiece
def zPiece():
    return [
        [ True,  True, False ],
        [ False, True, True]
    ]

def tPiece():
    return [
        [ False, True, False ],
        [ True,  True, True]
    ]

def sPiece():
    return [
        [ False, True, True],
        [ True,  True, False ]
    ]

def oPiece():
    return [
        [ True, True],
        [ True, True]
    ]

def lPiece():
    return [
        [ False, False, True],
        [ True,  True,  True]
    ]

def jPiece():
    return [
        [ True, False, False ],
        [ True, True,  True]
    ]

def iPiece():
    return [
        [ True,  True,  True,  True]
    ]        

#initializes a random falling piece at the top of the tetris board
def newFallingPiece(canvas):
    canvas.data.fallingPieceRow = 0
    canvas.data.fallingPieceCol = 0
    i = random.randint(0, len(canvas.data.tetrisPieces) - 1)
    canvas.data.fallingPiece = canvas.data.tetrisPieces[i]
    p = canvas.data.fallingPiece
    canvas.data.fallingPieceColor = canvas.data.tetrisPiecesColors[i]
    canvas.data.fallingPieceCols = len(p[0])
    canvas.data.fallingPieceRows = len(p)
    canvas.data.fallingPieceCol = canvas.data.cols/2 - canvas.data.fallingPieceCols/2

#draws tetris piece on its way down
def drawFallingPiece(canvas):
    r = canvas.data.fallingPieceRow
    c = canvas.data.fallingPieceCol
    for row in xrange(canvas.data.fallingPieceRows):
        for col in xrange(canvas.data.fallingPieceCols):
            if(canvas.data.fallingPiece[row][col] == True):
                drawTetrisCell(canvas,row + r,col + c,canvas.data.fallingPieceColor)

#ensures that each tetris move is legal
def fallingPieceIsLegal(canvas):
    r = canvas.data.fallingPieceRow
    c = canvas.data.fallingPieceCol
    for row in xrange(canvas.data.fallingPieceRows):
        for col in xrange(canvas.data.fallingPieceCols):
            if(canvas.data.fallingPiece[row][col] == True):
                if(row + r < 0 or col + c < 0
                   or row + r >= canvas.data.rows
                   or col + c >= canvas.data.cols):
                    return False
                elif(canvas.data.board[row + r][col + c] != canvas.data.emptyColor):
                    return False
    return True

#moves piece in direction specified if legal
#if not legal, returns back to original position
def moveFallingPiece(canvas,drow,dcol):
    canvas.data.fallingPieceRow += drow
    canvas.data.fallingPieceCol += dcol
    newCol = canvas.data.fallingPieceCol + dcol
    newRow = canvas.data.fallingPieceRow + drow
    #returns piece back to original position
    if(fallingPieceIsLegal(canvas) == False):
        canvas.data.fallingPieceRow -= drow
        canvas.data.fallingPieceCol -= dcol
        return False
    return True

#used to center the falling piece as it rotates
def fallingPieceCenter(canvas):
    r = canvas.data.fallingPieceRow
    r2 = canvas.data.fallingPieceRows
    c = canvas.data.fallingPieceCol
    c2 = canvas.data.fallingPieceCols
    return (r + r2/2, c + c2/2)

#when piece hits bottom of board this functions places it permanently on board
def placeFallingPiece(canvas):
    canvas.data.tetrisSpeed = 100
    c = canvas.data.fallingPieceColor
    col = canvas.data.fallingPieceCol
    row = canvas.data.fallingPieceRow
    cols = canvas.data.fallingPieceCols
    rows = canvas.data.fallingPieceRows
    for i in xrange(row,row + rows):
        for j in xrange(col, col + cols):
            if(canvas.data.fallingPiece[i- row][j - col] == True):
                canvas.data.board[i][j] = c

#rotates piece 
def rotateFallingPiece(canvas):
    #stores old piece and location
    p = copy.deepcopy(canvas.data.fallingPiece)
    r = canvas.data.fallingPieceRow
    c = canvas.data.fallingPieceCol
    r2 = canvas.data.fallingPieceRows
    c2 = canvas.data.fallingPieceCols
    oldCenterRow,oldCenterCol = fallingPieceCenter(canvas)
    oldRows = canvas.data.fallingPieceRows
    oldCols = canvas.data.fallingPieceCols
    newList = [[False for row in xrange(oldRows)]
                for col in xrange(oldCols)]
    #creates list for rotated piece
    for row in xrange(oldRows):
        for col in xrange(oldCols):
            newList[oldCols - 1 - col][row] = canvas.data.fallingPiece[row][col]
    canvas.data.fallingPiece = newList
    canvas.data.fallingPieceCols = oldRows
    canvas.data.fallingPieceRows = oldCols
    newCenterRow,newCenterCol = fallingPieceCenter(canvas)
    canvas.data.fallingPieceRow += oldCenterRow - newCenterRow
    canvas.data.fallingPieceCol += oldCenterCol - newCenterCol
    #if rotation is not legal, the piece is reset to its old form
    if(fallingPieceIsLegal(canvas) == False):
        canvas.data.fallingPiece = p
        canvas.data.fallingPieceRow = r
        canvas.data.fallingPieceCol = c
        canvas.data.fallingPieceRows = r2
        canvas.data.fallingPieceCols = c2

#removes row when no empty cells in row
def removeFullRows(canvas):
    #starts new row at bottom
    newRow = canvas.data.rows - 1
    isFull = True
    #starts old row at bottom
    oldRow = canvas.data.rows - 1
    fullRows = 0
    #creates a new board for the row clearing
    newBoard = [[canvas.data.emptyColor for i in xrange(canvas.data.cols)]
            for j in xrange(canvas.data.rows)]
    #iterates from bottom to top
    while(oldRow > 0):
        for col in xrange(canvas.data.cols):
            #checks if row has any empty cells
            try:
                if(canvas.data.board[oldRow][col] == canvas.data.emptyColor):
                    isFull = False
            except: print oldRow, col
        #if rows aren't full, redraws row    
        if(isFull == False):
            for col in xrange(canvas.data.cols):
                newBoard[newRow] = copy.deepcopy(canvas.data.board[oldRow])
                canvas.data.board[newRow] = newBoard[oldRow]
            newRow -= 1
        #if row are full increments fullRows, which is used in scoring
        else:
            fullRows += 1
        oldRow -= 1
    canvas.data.tetrisScore += fullRows ** 2
    canvas.data.board = newBoard

#draws tetris score in upper left hand corner
def drawScore(canvas):
    canvas.create_text(canvas.data.margin * 2, canvas.data.margin/2,
                       text = 'Score: ' + str(canvas.data.tetrisScore))

#loads board for snake and moreSnake
#for moreSnake, loads poison as well as food
def loadSnakeBoard(canvas):
    canvas.data.snakeBoard = [[0 for col in xrange(canvas.data.cols)]
                             for row in xrange(canvas.data.rows)]
    canvas.data.snakeBoard[canvas.data.rows/2][canvas.data.cols/2] = 1
    findSnakeHead(canvas)
    placeFood(canvas)
    if(canvas.data.game == 'moreSnake'):
        placePoison(canvas)
    canvas.data.snakeDrow = 0
    canvas.data.snakeDcol = -1
    canvas.data.ignoreNextTimerEvent = False

#used when redrawing the snake as it moves
def removeTail(canvas):
    for row in xrange(len(canvas.data.snakeBoard)):
        for col in xrange(len(canvas.data.snakeBoard[0])):
            if(canvas.data.snakeBoard[row][col] > 0):
                canvas.data.snakeBoard[row][col] -= 1

#used to store headRow and headCol values
#and when redrawing the snake
def findSnakeHead(canvas):
    maxVal = 0
    for row in xrange(len(canvas.data.snakeBoard)):
        for col in xrange(len(canvas.data.snakeBoard[0])):
            if(canvas.data.snakeBoard[row][col] > maxVal):
                maxVal = canvas.data.snakeBoard[row][col]
                canvas.data.headRow = row
                canvas.data.headCol = col

#moves snake in the direction specified
def moveSnake(canvas, drow, dcol):
    b = canvas.data.snakeBoard
    newHR = canvas.data.headRow + drow
    newHC = canvas.data.headCol + dcol
    #if snake hits wall, game over
    if(newHR < 0 or newHR >= len(b) or newHC < 0 or newHC >= len(b[0])):
       gameOver(canvas)
    elif(b[newHR][newHC] > 0): gameOver(canvas)
    #if snake eats food, score + 1
    #moves poison to a new random location
    elif(b[newHR][newHC] == -1):
        b[newHR][newHC] = b[canvas.data.headRow][canvas.data.headCol] + 1
        canvas.data.headRow,canvas.data.headCol = newHR,newHC
        if(canvas.data.game == 'snake'): canvas.data.snakeScore += 1
        if(canvas.data.game == 'moreSnake'): canvas.data.moreSnakeScore += 1
        placeFood(canvas), removePoison(canvas)
        if(canvas.data.game == 'moreSnake'): placePoison(canvas)
    #if snake eats poison, dies
    elif(b[newHR][newHC] == -2):
        gameOver(canvas)
    #if snake eats wall, score - 1, if score dips below 0, game over
    elif(b[newHR][newHC] == -3):
        b[newHR][newHC] = 0
        canvas.data.moreSnakeScore -= 1
        if(canvas.data.moreSnakeScore < 0): gameOver(canvas)
    #if nothing exciting happens, snake continues boring trek by moving one cell
    else:
        b[newHR][newHC] = b[canvas.data.headRow][canvas.data.headCol] + 1
        canvas.data.headRow,canvas.data.headCol = newHR,newHC
        removeTail(canvas)
    canvas.data.snakeDrow, canvas.data.snakeDcol = drow, dcol
    redrawSnake(canvas)    

#used to remove poison when snake eats food
def removePoison(canvas):
    b = canvas.data.snakeBoard
    for row in xrange(canvas.data.rows):
        for col in xrange(canvas.data.cols):
            if(b[row][col] == -2):
                b[row][col] = 0

#places food at a random point on the canvas
def placeFood(canvas):
    isFood = False
    while(isFood == False):
        row = random.randint(0,len(canvas.data.snakeBoard) - 1)
        col = random.randint(0,len(canvas.data.snakeBoard[0]) - 1)
        #ensures location for food will be empty
        if(canvas.data.snakeBoard[row][col] == 0):
            canvas.data.snakeBoard[row][col] = -1
            isFood = True

#places a poison at random point on the canvas
def placePoison(canvas):
    r = canvas.data.rows
    c = canvas.data.cols
    hr = canvas.data.headRow
    hc = canvas.data.headCol
    isPoison = False
    while(isPoison == False):
        row = random.randint(0,len(canvas.data.snakeBoard) - 1)
        col = random.randint(0,len(canvas.data.snakeBoard[0]) - 1)
        #ensures location for poison will be empty
        #also ensures that poison isn't one cell away form snake head
        if(canvas.data.snakeBoard[row][col] == 0 and
           abs(row - hr) >= 2 and abs(col - hc) >= 2):
            canvas.data.snakeBoard[row][col] = -2
            isPoison = True

#when mouse is pressed, draws wall when the game is paused for moreSnake
def drawWall(canvas, x,y):
    cs = canvas.data.cellSize
    m = canvas.data.margin 
    row = (y - 3 * m)/cs
    col = (x - m)/cs
    #if wall is already at the point, removes wall
    #if no wall, draw wall
    if(canvas.data.isPaused == True):
        if(canvas.data.snakeBoard[row][col] == -3):
            canvas.data.snakeBoard[row][col] = 0
        else:
            if(canvas.data.snakeBoard[row][col] == 0):
                canvas.data.snakeBoard[row][col] = -3

#draws individual snake cells and its contents
def drawSnakeCell(canvas, row, col):
    m, cs, s = canvas.data.margin, canvas.data.cellSize, canvas.data.scoreBox
    left,top = m + col * cs,m + row * cs + s
    #dims colors when game is paused
    if(canvas.data.isPaused == True):
        color1,color2,color3,color4,lineColor='light blue','light green','pink','tan','gray'
        canvas.create_text(canvas.data.width/3, canvas.data.height/4,
                           text = 'PAUSED', font = 'Helvetica 40 bold')
    else:
        color1,color2,color3,color4,lineColor = 'blue', 'green', 'red','brown','black'       
    #draws white cells
    canvas.create_rectangle(left, top, left + cs, top + cs,
                            fill = 'white', outline = lineColor)
    #draws snake,food, poison, and walls
    if(canvas.data.snakeBoard[row][col] > 0):
        canvas.create_oval(left, top,left + cs,top + cs,fill=color1,width=0)
    elif(canvas.data.snakeBoard[row][col] == -1):
        canvas.create_oval(left, top,left + cs,top + cs,fill=color2,width=0)
    elif(canvas.data.snakeBoard[row][col] == -2):
        canvas.create_oval(left, top, left + cs,top +cs,fill=color3,width = 0)
    elif(canvas.data.snakeBoard[row][col] == -3):
        canvas.create_rectangle(left, top, left +cs,top+cs,fill=color4,width=0)
    if(canvas.data.debugMode == True):
        canvas.create_text(left + cs/2, top + cs/2, text = str(canvas.data.snakeBoard[row][col]))

#draws full snakeBoard
def drawSnakeBoard(canvas):
    w = canvas.data.width/3
    h = canvas.data.height/3
    #draws background
    canvas.create_rectangle(0,0,canvas.data.width,canvas.data.height,
                            fill = "Gray",width = 0)
    #draws scorebox
    canvas.create_rectangle(canvas.data.width/6, 5, 2 * canvas.data.width/3 ,
                            35, fill = 'white',width = 0)
    #displays score in scoreBox
    if(canvas.data.game == 'snake'): score = canvas.data.snakeScore
    elif(canvas.data.game == 'moreSnake'): score = canvas.data.moreSnakeScore
    canvas.create_text(canvas.data.width/3, 20,
                       text = "Score: " + str(score))
    #draws all the cells in the snake board and their contents
    for row in xrange(len(canvas.data.snakeBoard)):
        for col in xrange(len(canvas.data.snakeBoard[0])):
            drawSnakeCell(canvas,row,col)

#ends the game
def gameOver(canvas):
    canvas.data.gameOver = True

#looks through board looking for walls
#used to give bonus point
def checkWalls(canvas):
    for row in xrange(canvas.data.rows):
        for col in xrange(canvas.data.cols):
            if(canvas.data.snakeBoard[row][col] == -3):
                return True
    return False

#when snake eats 3 pieces of food speed increases
#each time snake eats 20 pieces of food and  a wall is still existing
#bonus point is added
def checkLevel(canvas):
    if(canvas.data.moreSnakeScore == 3):
        canvas.data.speed = 100
    if(canvas.data.moreSnakeScore%20 == 0):
        if(checkWalls(canvas) == True):
            canvas.data.moreSnakeScore += 1

def run():
    # create the root and the canvas
    root = Tk()
    scoreBox,cellSize,canvasWidth,canvasHeight = 40,30,700,1000
    canvas = Canvas(root, width=canvasWidth, height=canvasHeight)
    canvas.pack()
    # Store canvas in root and in canvas itself for callbacks
    root.canvas = canvas.canvas = canvas
    # Set up canvas data and call init
    class Struct: pass
    canvas.data = Struct()
    canvas.data.highScoreList = []
    canvas.data.width,canvas.data.height = canvasWidth,canvasHeight
    canvas.data.scoreBox,canvas.data.highScoreList = scoreBox,[]
    canvas.data.cellSize = cellSize
    canvas.create_text(canvas.data.width/2, canvas.data.height/2, text =
                       'WELCOME! Press 0 for options!')
    initAll(canvas)
    # set up events
    def mousePressedFn(event): mousePressed(event,canvas)
    root.bind("<Button-1>", mousePressedFn)
    def keyPressedFn(event): keyPressed(event,canvas)
    root.bind("<Key>", keyPressedFn)
    timerFired(canvas)
    # and launch the app
    root.mainloop()  # This call BLOCKS (so your program waits until you close the window!)

run()


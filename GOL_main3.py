from Tkinter import *
import math
import random

def init(data):
    data.startText = "3D Game of Life"
    data.startText2 = "inspired by Conway"
    data.chooseText = "Choose the Game Mode:"
    data.myName = "Created By JJ Cheng"
    data.chooseFont = ('Consolas', 25)
    data.smallFont = ('Consolas', 10)
    data.titleFont = ('Consolas', 40)
    data.subtitleFont = ('Consolas', 15)
    data.gameModes = ['Explorer', 'Multiplayer']

    #possible locations of the selector
    data.arrowX, data.arrowY = 160, 315
    data.altArrowX, data.altArrowY = 160, 345

    #vertices of graphics part
    data.lastCube = [
    [(35, 430),(0, 410),(35, 390),(70, 410)],
    [(35, 465),(0, 445),(0,410),(35,430)],
    [(35, 465),(70,445),(70,410),(35,430)]
    ]

    data.lastCubeX = 35
    data.lastCubeY = 430

    data.cubeColors = ['blue', 'yellow', 'pink', 'red', 'purple', 'orange']

    data.cubes = [
    [[(35, 430),(0, 410),(35, 390),(70, 410)],
    [(35, 465),(0, 445),(0,410),(35,430)],
    [(35, 465),(70,445),(70,410),(35,430)]]
    ]

    data.enter = False
    data.choice = 0
    data.timePassed = 0

def initializeCube(data):
    optionsX = [-35, 35]
    optionsY = [-55, 55]
    if data.lastCubeY + 55 > data.width:
        dx, dy = optionsX[1], optionsY[0]
        valid = True
    else:
        valid = False
    while valid == False:
        randomX, randomY = random.randint(0,1), random.randint(0,1)
        dx,dy = optionsX[randomX], optionsY[randomY]
        if dx >= 0 or dy >= 0: valid = True
    newX = data.lastCubeX + dx
    newY = data.lastCubeY + dy
    data.lastCubeX += dx
    data.lastCubeY += dy
    return newX, newY

def positionCube(x,y,data):
    cube = [ #set coordinates difference, just change center
    [(x, y),(x-35, y-20),(x, y-40),(x+35, y-20)],
    [(x, y+35),(x-35, y+15),(x-35,y-20),(x,y)],
    [(x, y+35),(x+35,y+15),(x+35,y-20),(x,y)]
    ]
    data.lastCube = cube
    return cube


def keyPressed(event, data, root):
    if event.keysym == "Up" or event.keysym == "Down":
        tempX, tempY = data.altArrowX, data.altArrowY
        data.altArrowX, data.altArrowY = data.arrowX, data.arrowY
        data.arrowX, data.arrowY = tempX, tempY
        if data.choice == 0:
            data.choice = 1
        else:
            data.choice = 0
    if event.keysym == "Return":
        if data.choice == 0: #runs seed stage
            import GOL_seedStage3
            root.destroy()
            GOL_seedStage3.run(500,500)
        elif data.choice == 1: #runs preset game stage
            import GOL_seedStageMulti3
            root.destroy()
            GOL_seedStageMulti3.run(500,500)

def mousePressed(event, data):
    print(event.x, event.y)

def timerFired(data):
    data.timePassed += data.timerDelay
    if data.timePassed % 1000 == 0:
        x,y = initializeCube(data)
        newCube = positionCube(x,y,data)
        data.cubes.append(newCube)


def redrawAll(canvas, data): #calls the necessary draw functions
    drawCubes(canvas, data)
    canvas.create_rectangle(data.width/2-75, data.height-15,
                            data.width/2+75, data.height,
                            fill='white', outline = 'white')
    drawStart(canvas, data)
    drawArrow(canvas, data)

def drawStart(canvas, data): #draws all text and labels for start screen
    canvas.create_text(data.width/2, data.height/4,
                        text = data.startText,
                        font = data.titleFont)
    canvas.create_text(data.width/2, data.height/3,
                        text = data.startText2,
                        font = data.subtitleFont)
    canvas.create_text(data.width/2, data.height/2,
                        text = data.chooseText,
                        font = data.chooseFont)
    canvas.create_text(data.width/2, data.height*10/16,
                        text = data.gameModes[0],
                        font = data.subtitleFont)
    canvas.create_text(data.width/2, data.height*11/16,
                        text = data.gameModes[1],
                        font = data.subtitleFont)
    canvas.create_text(data.width/2, data.height,
                        text = data.myName,
                        font = data.smallFont,
                        anchor = S)

def drawArrow(canvas, data):
    pointerX = data.arrowX
    pointerY = data.arrowY
    #pointer is at x,y; arrow is pointing right
    vdata = [pointerX-10,pointerY-10,
            pointerX,pointerY,
            pointerX-10,pointerY+10]
    canvas.create_polygon(vdata)

def drawCubes(canvas, data):
    for i in range(len(data.cubes)):
        if i == len(data.cubes)-1:
            default = data.cubeColors[random.randint(0,len(data.cubeColors)-1)]
        else:
            default = 'grey'
        for face in data.cubes[i]:
            canvas.create_polygon(face, fill = 'White', outline = default)


####################################
# use the run function as-is
####################################

"""
Start of Citation...
NOT ORIGINAL CODE:
Taken from CMU 15112 Animation Starter Code
"""

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data, root)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

"""
End of Citation...
Taken from CMU 15112 Animation Starter Code
"""

run(500,500)

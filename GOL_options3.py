# Basic Animation Framework

#File by jcheng3
#Options page or Game Of Life
# Basic Animation Framework

#File by jcheng3
#Seed stage for 3D Game Of Life

from Tkinter import *

import copy

####################################
# customize these functions
####################################

inSeeds = []

def init(data):
    data.liveOption = 2
    data.spawnOption = 3
    data.gridSize = 5
    data.itrDelay = 250
    data.box1X = 345
    data.box1Y = 212
    data.box2X = 365
    data.box2Y = 241
    data.box3X = 220
    data.box3Y = 265
    data.box4X = 335
    data.box4Y = 290
    data.boxSize = 25
    data.highlight = 0
    data.infoFont = ("Consolas", 10)
    data.titleFont = ("Helvetica", 20)
    data.fin = False
    data.error = False
    pass

def mousePressed(event, data):
    print(event.x, event.y)
    if event.x >= data.box1X and event.y >= data.box1Y and \
    event.x <= data.box1X + data.boxSize and \
    event.y <= data.box1Y + data.boxSize:
        data.highlight = 1
    elif event.x >= data.box2X and event.y >= data.box2Y and \
    event.x <= data.box2X + data.boxSize and \
    event.y <= data.box2Y + data.boxSize:
        data.highlight = 2
    elif event.x >= data.box3X and event.y >= data.box3Y and \
    event.x <= data.box3X + data.boxSize and \
    event.y <= data.box3Y + data.boxSize:
        data.highlight = 3
    elif event.x >= data.box4X and event.y >= data.box4Y and \
    event.x <= data.box4X + data.boxSize and \
    event.y <= data.box4Y + data.boxSize:
        data.highlight = 4
    else: data.highlight = 0


def keyPressed(event, data):
    if data.highlight == 1:
        if event.keysym == "BackSpace":
            data.liveOption = data.liveOption // 10
        else:
            try:
                data.liveOption = (data.liveOption*10) + int(event.keysym)
                data.error = False
            except:
                data.error = True
    elif data.highlight == 2:
        if event.keysym == "BackSpace":
            data.spawnOption = data.spawnOption // 10
        else:
            try:
                data.spawnOption = (data.spawnOption*10) + int(event.keysym)
                data.error = False
            except:
                data.error = True
    elif data.highlight == 3:
        if event.keysym == "BackSpace":
            data.gridSize = data.gridSize // 10
        else:
            try:
                data.gridSize = (data.gridSize*10) + int(event.keysym)
                data.error = False
            except:
                data.error = True
    elif data.highlight == 4:
        if event.keysym == "BackSpace":
            data.itrDelay = data.itrDelay // 10
        else:
            try:
                data.itrDelay = (data.itrDelay*10) + int(event.keysym)
                data.error = False
            except:
                data.error = True
    if event.keysym == "Return" and data.fin == False:
        data.fin = True
    if event.keysym == "Return" and data.fin:
        if len(inSeeds) == 1:
            import GOL_playStage3
            root.destroy()
            GOL_playStage3.runStage(inSeeds[0], data.liveOption, data.spawnOption,
                                        data.gridSize, data.itrDelay/1000.0)
        elif len(inSeeds) == 2:
            import GOL_playStageMulti3

            root.destroy()

            GOL_playStageMulti3.runStage(inSeeds[0], inSeeds[1], data.liveOption, data.spawnOption,
                                        data.gridSize, data.itrDelay/1000.0)
    elif event.keysym == "BackSpace" and data.fin:
        data.fin = False

def drawText(canvas, data):
    center = data.width/2
    centerLeft = data.width/8
    row = data.height/5
    rowCount = 1
    canvas.create_text(center, rowCount * row,
                        text = "Game Of Life Options:",
                        font = data.titleFont)
    rowCount += 0.5
    canvas.create_text(center, rowCount * row,
                        text = "Changing these parameters will change\nthe behavior of the game. Experiment!",
                        font = data.infoFont)
    rowCount += 0.5
    canvas.create_text(center, rowCount * row,
                        text = "Press \'Enter\' to Continue",
                        font = data.infoFont)
    rowCount += 0.25
    canvas.create_text(centerLeft, rowCount * row,
                        text = "# live neighbors to survive (default 2):",
                        font = data.infoFont,
                        anchor = W)
    rowCount += 0.25
    canvas.create_text(centerLeft, rowCount * row,
                        text = "# live neighbors to spawn cell (default 3):",
                        font = data.infoFont,
                        anchor = W)
    rowCount += 0.25
    canvas.create_text(centerLeft, rowCount * row,
                        text = "Grid Size (default 5):",
                        font = data.infoFont,
                        anchor = W)
    rowCount += 0.25
    canvas.create_text(centerLeft, rowCount * row,
                        text = "Time per iteration (default 250 ms):",
                        font = data.infoFont,
                        anchor = W)
    rowCount += 0.5
    canvas.create_text(center, rowCount * row,
                        text = "(If # live neighbors != either option, cell dies)",
                        font = data.infoFont)
    rowCount += 0.5
    canvas.create_text(center, rowCount*row,
                        text = "A cool one to try is 27 and 2. \n (27 neighbors will never happen)")
    rowCount += 0.5
    canvas.create_text(center, rowCount*row,
                        text = "27/2 is called the Exploding character")
    rowCount += 0.25
    canvas.create_text(center, rowCount*row,
                        text = "(http://psoup.math.wisc.edu/mcell/rullex_life.html)")
    if data.error:
        rowCount += 0.25
        canvas.create_text(center, rowCount * row,
                            text = "PLEASE ENTER VALID INTEGER",
                            font = data.infoFont,
                            anchor = S)

def drawBoxes(canvas, data):
    if data.highlight == 0:
        color1, color2, color3, color4 = 'White', 'White','White','White'
    elif data.highlight == 1:
        color1, color2, color3, color4 = 'Yellow', 'White','White','White'
    elif data.highlight == 2:
        color1, color2, color3, color4 = 'White', 'Yellow','White','White'
    elif data.highlight == 3:
        color1, color2, color3, color4 = 'White', 'White','Yellow','White'
    elif data.highlight == 4:
        color1, color2, color3, color4 = 'White', 'White','White','Yellow'

    canvas.create_rectangle(data.box1X, data.box1Y,
                            data.box1X + data.boxSize,
                            data.box1Y + data.boxSize,
                            fill = color1)
    canvas.create_rectangle(data.box2X, data.box2Y,
                            data.box2X + data.boxSize,
                            data.box2Y + data.boxSize,
                            fill = color2)
    canvas.create_rectangle(data.box3X, data.box3Y,
                            data.box3X + data.boxSize,
                            data.box3Y + data.boxSize,
                            fill = color3)
    canvas.create_rectangle(data.box4X, data.box4Y,
                            data.box4X + data.boxSize,
                            data.box4Y + data.boxSize,
                            fill = color4)
    canvas.create_text(data.box1X + 0.5*data.boxSize,
                        data.box1Y + 0.5*data.boxSize,
                        text=str(data.liveOption))
    canvas.create_text(data.box2X + 0.5*data.boxSize,
                        data.box2Y + 0.5*data.boxSize,
                        text=str(data.spawnOption))
    canvas.create_text(data.box3X + 0.5*data.boxSize,
                        data.box3Y + 0.5*data.boxSize,
                        text=str(data.gridSize))
    canvas.create_text(data.box4X + 0.5*data.boxSize,
                        data.box4Y + 0.5*data.boxSize,
                        text=str(data.itrDelay))

def redrawAll(canvas, data): #draws two 5x5 grids
    # draw in canvas
    drawText(canvas, data)
    drawBoxes(canvas, data)
    if data.fin:
        canvas.create_rectangle(data.width/4,data.height/3,
                                data.width*3/4,data.height*2/3,
                                fill = 'white')
        canvas.create_text(data.width/2, data.height/2,
            text = "\'Enter\' to confirm, \n\'Delete\' to abort")
    pass

####################################
# use the run function as-is
####################################

"""
Start of Citation...
NOT ORIGINAL CODE:
Taken from CMU 15112 Animation Starter Code
"""

root = Tk()

def run(width=500, height=500):
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
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height

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
    redrawAll(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

"""
End of Citation...
Taken from CMU 15112 Animation Starter Code
"""

#run(500,500)

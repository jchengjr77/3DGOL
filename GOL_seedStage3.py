# Basic Animation Framework

#File by jcheng3
#Seed stage for 3D Game Of Life

from Tkinter import *

####################################
# customize these functions
####################################

def init(data):
    data.instructions = True
    # load data.xyz as appropriate
    data.seeds = [] #stores lists of x,y,z coords
    data.deletedSeeds = []
    data.maxSeeds = 5
    data.margin = 30
    data.textMargin = 15
    data.gridSize = 5
    data.currSeed = ['x','y','z']
    data.cellSize = ((data.width/2)-2*data.margin)/data.gridSize
    data.fillColor = "Grey"
    data.emptyColor = "White"
    data.xColor = 'Red'
    data.yColor = 'Blue'
    data.zColor = 'Green'
    data.axisWidth = 3
    data.infoFont = ("Consolas", 10)
    data.titleFont = ("Helvetica", 20)
    data.controlPressed = False
    data.finished = False
    pass

def mousePressed(event, data):
    if data.instructions == False:
        if data.finished == False: #cannot seed if more than max seed
            # use event.x and event.y
            if event.x < data.width/2:
                if event.y < data.height/2:
                    scanXYQuad(event, data)
                else:
                    scanYZQuad(event, data)
            else:
                scanXZQuad(event, data)

            intFlag = True
            for i in range(len(data.currSeed)):
                if type(data.currSeed[i]) != int:
                    intFlag = False
            if intFlag:
                data.seeds.append(data.currSeed)
                data.currSeed = ['x','y','z']
                if len(data.seeds) == data.maxSeeds:
                    data.finished = True



def scanXYQuad(event, data): #checks XY graph
    #check if the click is within the bounds
    if event.x < data.margin or event.x > (data.width/2)-data.margin:
        return None
    elif event.y < data.margin or event.y > (data.height/2)-data.margin:
        return None
    row = (event.y - data.margin)//data.cellSize
    col = (event.x - data.margin)//data.cellSize
    if type(data.currSeed[1]) != int: #only add them if they are just strings
        data.currSeed[1] = data.gridSize-row-1 #seeded y-coord
    if type(data.currSeed[0]) != int:
        data.currSeed[0] = col #seeded x-coord

def scanYZQuad(event, data): #checks YZ graph
    #check if the click is within the bounds
    if event.x < data.margin or event.x > (data.width/2)-data.margin:
        return None
    elif event.y < (data.height/2)+data.margin or \
        event.y > data.height-data.margin:
        return None
    row = (event.y - (data.margin+(data.height/2)))//data.cellSize
    col = (event.x - data.margin)//data.cellSize
    if type(data.currSeed[2]) != int:
        data.currSeed[2] = data.gridSize-row-1 #seeded z-coord
    if type(data.currSeed[1]) != int:
        data.currSeed[1] = col #seeded y-coord

def scanXZQuad(event, data): #checks XZ graph
    #check if the click is within the bounds
    if event.x < (data.width/2)+data.margin or event.x > data.width-data.margin:
        return None
    elif event.y < (data.height/2)+data.margin or \
        event.y > data.height-data.margin:
        return None
    row = (event.y - (data.margin+(data.height/2)))//data.cellSize
    col = (event.x - (data.margin+(data.width/2)))//data.cellSize
    if type(data.currSeed[2]) != int:
        data.currSeed[2] = data.gridSize-row-1 #seeded z-coord
    if type(data.currSeed[0]) != int:
        data.currSeed[0] = col #seeded y-coord


def keyPressed(event, data):
    # use event.char and event.keysym
    if data.instructions:
        if event.keysym == "Return":
            data.instructions = False
    elif data.instructions == False:
        if data.controlPressed == True:
            if event.keysym == "z" and data.deletedSeeds != []:
                data.seeds.append(data.deletedSeeds.pop())
            else:
                data.controlPressed = False
        elif event.keysym == "BackSpace":
            data.deletedSeeds.append(data.seeds.pop())
            if data.finished:
                data.finished = False
        elif event.keysym == "Escape" and data.finished == False:
            data.instructions = True
        elif event.keysym == "Control_L" or event.keysym == "Control_R":
            data.controlPressed = True
        elif event.keysym == "Return" and data.finished == True:
            #import GOL_playStage_2
            #root.destroy()
            #GOL_playStage_2.runStage(data.seeds)
            import GOL_options3
            root.destroy()
            GOL_options3.inSeeds.append(data.seeds)
            GOL_options3.run()

            if event.keysym == "Escape" or event.keysym == "BackSpace":
                data.deletedSeeds.append(data.seeds.pop())
                data.finished = False
        elif event.keysym == "Return" and data.finished == False:
            data.finished = True


def checkCellColor(data, coord1, coord2, graphLabel):
    for elem in data.seeds:
        if graphLabel == 'xy':
            if elem[0] == coord1 and elem[1] == coord2:
                return data.fillColor
        elif graphLabel == 'yz':
            if elem[1] == coord1 and elem[2] == coord2:
                return data.fillColor
        elif graphLabel == 'xz':
            if elem[0] == coord1 and elem[2] == coord2:
                return data.fillColor
    return data.emptyColor

def drawGridXY(canvas, data):
    canvas.create_text(0,0,text = 'Top View', anchor = NW)
    canvas.create_rectangle(0,0,data.width/2, data.height/2, ) #border outline
    canvas.create_rectangle(data.margin, data.margin,
                            data.width/2-data.margin,
                            data.height/2-data.margin) #inner outline
    canvas.create_text(data.margin/2, (data.height/4),
                        text = "Y")
    canvas.create_text(data.width/4, data.height/2-data.margin/2,
                        text = 'X')
    canvas.create_text(data.margin/2, data.height/2-data.margin/2, text="(0,0)")
    for i in range(5):
        newY = (data.height/2 - data.margin) - (i*(data.cellSize))
        for j in range(5):
            newX = j*(data.cellSize) + data.margin
            color = checkCellColor(data, j, i, 'xy')
            canvas.create_rectangle(newX, newY,
                                    newX+data.cellSize, newY-data.cellSize,
                                    fill = color)
    #x-axis line
    canvas.create_line(data.margin, data.height/2-data.margin,
                    data.width/2 - data.margin, data.height/2 - data.margin,
                    fill=data.xColor, width = data.axisWidth)
    #y-axis line
    canvas.create_line(data.margin, data.margin,
                        data.margin, data.height/2 - data.margin,
                        fill=data.yColor, width = data.axisWidth)



def drawGridYZ(canvas, data):
    canvas.create_text(0,data.height/2,text = 'Side View', anchor = NW)
    canvas.create_rectangle(0,data.height/2,data.width/2, data.height)
    canvas.create_rectangle(data.margin, data.height/2 + data.margin,
                            data.width/2-data.margin,
                            data.height-data.margin) #inner outline

    canvas.create_text(data.margin/2, (data.height/4)*3,
                        text = "Z")
    canvas.create_text(data.width/4, data.height - (data.margin/2),
                        text = 'Y')
    canvas.create_text(data.margin/2, data.height-data.margin/2, text="(0,0)")
    for i in range(5):
        newZ = (data.height - data.margin) - (i*(data.cellSize))
        for j in range(5):
            newY = j*(data.cellSize) + data.margin
            color = checkCellColor(data, j, i, 'yz')
            canvas.create_rectangle(newY, newZ,
                                    newY+data.cellSize, newZ-data.cellSize,
                                    fill = color)
    #y-axis line
    canvas.create_line(data.margin, data.height - data.margin,
                    data.width/2 - data.margin, data.height - data.margin,
                    fill=data.yColor, width = data.axisWidth)
    #z-axis line
    canvas.create_line(data.margin, data.height - data.margin,
                        data.margin, data.height/2 + data.margin,
                        fill=data.zColor, width = data.axisWidth)

def drawGridXZ(canvas, data):
    canvas.create_text(data.width/2,data.height/2,text = 'Front View',
                        anchor = NW)
    canvas.create_rectangle(data.width/2,data.height/2,data.width, data.height)
    canvas.create_rectangle(data.width/2 + data.margin,
                            data.height/2 + data.margin,
                            data.width-data.margin,
                            data.height-data.margin) #inner outline
    canvas.create_text(data.width/2 + data.margin/2, (data.height/4)*3,
                        text = "Z")
    canvas.create_text((data.width/4)*3, data.height - (data.margin/2),
                        text = 'X')
    canvas.create_text(data.width/2 + data.margin/2,
                    data.height-data.margin/2, text="(0,0)")
    for i in range(5):
        newZ = (data.height - data.margin) - (i*(data.cellSize))
        for j in range(5):
            newX = j*(data.cellSize) + (data.width/2 + data.margin)
            color = checkCellColor(data, j, i, 'xz')
            canvas.create_rectangle(newX, newZ,
                                    newX+data.cellSize, newZ-data.cellSize,
                                    fill = color)
    #x-axis line
    canvas.create_line(data.width/2 + data.margin, data.height-data.margin,
                        data.width - data.margin, data.height-data.margin,
                        fill=data.xColor, width = data.axisWidth)
    #z-axis line
    canvas.create_line(data.width/2 + data.margin, data.height - data.margin,
                        data.width/2 + data.margin, data.height/2 + data.margin,
                        fill=data.zColor, width = data.axisWidth)

def drawInfo(canvas, data): #displays all the info of the seed stage
    fontGap = 20
    displayCurr = [] #convert to non-list counting
    for i in range(len(data.currSeed)):
        if type(data.currSeed[i]) == int:
            displayCurr.append(data.currSeed[i]+1)
        else:
            displayCurr.append(data.currSeed[i])
    canvas.create_text(data.width/2 + data.textMargin, data.textMargin,
                        text = "Current Seed:" + str(displayCurr),
                        font = data.infoFont, anchor = W)
    canvas.create_text(data.width/2+data.textMargin,
                        data.textMargin + fontGap,
                        text = "Amount Seeded:" + str(len(data.seeds)),
                        font = data.infoFont, anchor = W)
    canvas.create_text(data.width/2+data.textMargin,
                        data.textMargin + 2*fontGap,
                        text = "Seed Limit:" + str(data.maxSeeds),
                        font = data.infoFont, anchor = W)
    canvas.create_text(data.width/2+data.textMargin,
                        data.textMargin + 3*fontGap,
                        text = "SeedList:",
                        font = data.infoFont, anchor = W)
    canvas.create_text(data.width/2+data.textMargin,
                        data.height/2-data.textMargin,
                        text = "Press \'Esc\' for controls",
                        font = data.infoFont, anchor = W)

    #gotta wrap the seed text. There is a max seed limit so they won't overflow
    lineLength = 3
    display = ''
    for i in range(len(data.seeds)):
        displaySeed = convertSeed(data.seeds[i])
        display += str(displaySeed)
        if i != len(data.seeds)-1:
            display += ','
        if i > 0 and i % (lineLength-1) == 0:
            display += '\n'
    canvas.create_text(data.width/2+data.textMargin,
                        data.textMargin + (4)*fontGap,
                        text = display,
                        font = data.infoFont, anchor = NW)
    if len(data.seeds) == data.maxSeeds:
        canvas.create_text(data.width/2+data.textMargin,
                            data.height/2 - 2*data.textMargin,
                            text = "MAX LIMIT REACHED",
                            font = data.infoFont, anchor = W)
    if data.finished:
        canvas.create_rectangle(data.width/4,data.height/3,
                                data.width*3/4,data.height*2/3,
                                fill = 'white')
        canvas.create_text(data.width/2, data.height/2,
                            text = "\'Enter\' to continue, \n\'Delete\' or \'Esc\' to abort")


def convertSeed(seed):
    newSeed = []
    for i in range(len(seed)):
        newSeed.append(seed[i]+1)
    return newSeed

def drawInstructions(canvas, data): #simply displays all basic instructions
    center = data.width/2
    row = data.height/10
    rowCount = 2
    canvas.create_text(center, rowCount * row,
                        text = "Seed Stage Instructions:",
                        font = data.titleFont)
    rowCount += 1
    canvas.create_text(center, rowCount * row,
                        text = "Select seed coordinates with mouse click",
                        font = data.infoFont)
    rowCount += 1
    canvas.create_text(center, rowCount * row,
                text = "First select on xy-plane, then on yz- or xz-plane",
                        font = data.infoFont)
    rowCount += 1
    canvas.create_text(center, rowCount * row,
                        text = "\"Delete\" will delete most recent seed",
                        font = data.infoFont)
    rowCount += 1
    canvas.create_text(center, rowCount * row,
                        text = "\"Ctrl+Z\" will undo your deleted seed",
                        font = data.infoFont)
    rowCount += 1
    canvas.create_text(center, rowCount * row,
                        text = "\"Esc\" will bring you back here",
                        font = data.infoFont)
    rowCount += 1
    canvas.create_text(center, rowCount * row,
                        text = "\"Enter\" to Continue to next stage",
                        font = data.infoFont)




def redrawAll(canvas, data): #draws two 5x5 grids
    # draw in canvas
    if data.instructions:
        drawInstructions(canvas, data)
    elif data.instructions == False:
        drawGridXY(canvas, data)
        drawGridYZ(canvas, data)
        drawGridXZ(canvas, data)
        drawInfo(canvas, data)
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

from direct.showbase.ShowBase import ShowBase
#import direct.directbase.DirectStart

import math #for angles and stuff
import random
import copy
from direct.task import Task #basically the update function
from direct.actor.Actor import Actor #animated models
from direct.interval.IntervalGlobal import Sequence #background processes
from panda3d.core import *
from direct.gui.DirectGui import * #buttons and such

#global variables
seedState = False
playState = True

class PlayStage(ShowBase):
    def __init__(self, cubeList, live, spawn, gridSize, itrDelay):
        ShowBase.__init__(self)

        self.showEnv = False #choose whether to show env or not

        self.gridSize = gridSize #size of play space
        self.camDist = 20 #distance of camera away from playspace
        self.camRot = 10.0 #rotation speed in angles per second

        self.itrDelay = itrDelay #time it takes to show one iteration

        #Create list of cubes
        #THIS IS NOW BASED ON SEEDS
        self.cubeList = cubeList
        self.prevCubeList = []
        self.origCopy = copy.deepcopy(cubeList)
        self.live = live #number of neighbors for cell to sustain
        self.spawn = spawn #number of neighbors for cell to spawn

        #Creates new list of cubes for next iteration
        self.newCubeList = []

        #List of all cubes already rendered
        self.renderList = []

        #Create water box
        self.latestX, self.latestY, self.latestZ = 0,0,0
        waterTexture = loader.loadTexture("models/textures/waterTexture.png")
        self.cubeTexture = waterTexture

        #timer stuff
        self.prevIncrement = 0
        self.length = float(len(self.cubeList))
        self.percent = (self.length/(self.gridSize**3))*100
        self.p1 = OnscreenText(text = 'Status: ' + str(self.percent) + '%',
                            pos = (-0.75,0.75), scale = 0.10)

        self.iterated = False
        self.finished = False

        #creates spacial outline for game
        self.taskMgr.add(self.createSpace, "CreateSpace")

        #shows environment if set to True
        if self.showEnv == True:
            self.taskMgr.add(self.createEnv, "ShowEnv")

        #Manage camera position
        self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")

        #generating boxes at random locations next to the previous box
        #self.taskMgr.add(self.generateCube, "GenerateCube")


        #The initial render
        self.taskMgr.add(self.kickOff, "KickOff")

        #finds next iteration inside a 5X5X5 grid
        self.taskMgr.add(self.nextIteration, "NextIteration")

        self.taskMgr.add(self.updateGUI, "UpdateGUI")


    def restartGame(self):
        self.cubeList = copy.deepcopy(self.origCopy)
        self.percent = (float(self.length)/float(self.gridSize**3))*100
        #Creates new list of cubes for next iteration
        self.newCubeList = []
        #List of all cubes already rendered
        self.renderList = []
        self.iterated = False
        self.finished = False

    def updateGUI(self, task):
        self.p1.destroy()
        self.p1 = OnscreenText(text = 'Status: ' + str(self.percent) + '%',
                            pos = (-0.75,0.75), scale = 0.10)
        if self.finished == True:
            if self.prevCubeList == self.cubeList:
                self.message = OnscreenText(text ='Stable State',
                                            pos = (0,0.80), scale = 0.20)
            else:
                self.message = OnscreenText(text ='Life ended',
                                        pos = (0,0.80), scale = 0.20)

            self.restart = OnscreenText(text ='Press \'r\' to restart',
                    pos = (0,-0.85), scale = 0.20)
            self.accept('r', self.restartGame)
        return Task.cont

    def createEnv(self, task):
        #Create environment
        self.scene = loader.loadModel("models/environment")
        # Reparent the model to render.
        self.scene.reparentTo(self.render)
        # Apply scale and position transforms on the model.
        self.scene.setScale(0.25,0.25,0.25)
        self.scene.setPos(-8,42,0)

    def createSpace(self, task): #creates cube outline for play space
        print(self.itrDelay)
        spaceFormat = GeomVertexFormat.getV3() #setting format of Geom object
        vtexs = GeomVertexData('vertex', spaceFormat, Geom.UHStatic)
        vtexs.setNumRows(8) #cube has 8 points
        vertexAdd = GeomVertexWriter(vtexs, "vertex") #writing in vertices
        vertexAdd.addData3f(0,0,0)
        vertexAdd.addData3f(self.gridSize, 0, 0)
        vertexAdd.addData3f(self.gridSize, self.gridSize, 0)
        vertexAdd.addData3f(0, self.gridSize,0)
        vertexAdd.addData3f(0,0,self.gridSize)
        vertexAdd.addData3f(self.gridSize, 0, self.gridSize)
        vertexAdd.addData3f(self.gridSize, self.gridSize, self.gridSize)
        vertexAdd.addData3f(0, self.gridSize,self.gridSize)

        lines = GeomLines(Geom.UHStatic) #creating my lines

        for i in range(4): #range 4 b/c vertices in square
            if i == 3: #close off the square
                lines.addVertex(i)
                lines.addVertex(0)
                lines.closePrimitive()
            else:
                lines.addVertex(i)
                lines.addVertex(i+1)
                lines.closePrimitive()

        for j in range(4,8): #range 4-8 b/c vertices in top square
            if j == 7: #close off the square
                lines.addVertex(j)
                lines.addVertex(4)
                lines.closePrimitive()
            else:
                lines.addVertex(j)
                lines.addVertex(j+1)
                lines.closePrimitive()

        for k in range(4): #connect the top and bottom squares
            lines.addVertex(k)
            lines.addVertex(k+4)
            lines.closePrimitive()

        spaceHolder = Geom(vtexs) #Geom object to store the primitives
        spaceHolder.addPrimitive(lines)

        space = GeomNode('spaceOutline')
        space.addGeom(spaceHolder)
        self.render.attachNewNode(space) #GeomNodes do not reparent, they attach

    def spinCameraTask(self, task):
        camOffset = self.gridSize/2.0
        if playState:
            #rotate camera 6 degrees every second
            angleDegrees = task.time * self.camRot
            #Convert to radians for math
            angleRadians = angleDegrees * (math.pi / 180)
            #set camera's position (which is orbiting it, NOT rotating)
            camX = self.camDist * math.sin(angleRadians)
            camX += camOffset #start at 0, goes anti-clkwise
            camY = -self.camDist * math.cos(angleRadians)
            camY += camOffset #start at -20, same direction
            self.camera.setPos(camX, camY, self.camDist + camOffset)
            #Actually rotates camera so it looks at the middle while orbiting
            self.camera.setHpr(angleDegrees, -45, 0) #always will be 45deg angle
        return Task.cont


    def kickOff(self, task): #renders all starting cubes
        for crd in self.cubeList:
            newCube = loader.loadModel("models/box")
            newCube.reparentTo(self.render)
            newCube.setScale(1,1,1)
            newCube.setPos(crd[0], crd[1], crd[2])
            newCube.setTexture(self.cubeTexture, 1)
            self.renderList.append(newCube)

    def nextIteration(self, task):
        newIncrement = task.time // self.itrDelay
        if playState and newIncrement > self.prevIncrement and \
        self.finished == False:
            self.prevIncrement = newIncrement
            self.iterated = True
            for i in range(self.gridSize): #check next iteration
                for j in range(self.gridSize):
                    for k in range(self.gridSize): #only carries alive cubes
                        nbors = self.checkNeighbors(i,j,k)
                        if nbors == self.spawn:
                            self.newCubeList.append([i,j,k])
                        elif nbors == self.live and \
                        [i,j,k] in self.cubeList:
                            self.newCubeList.append([i,j,k])
            for cube in self.renderList: #remove all old rendered cubes
                cube.removeNode()
            self.renderList = []
            self.prevCubeList = self.cubeList
            self.cubeList = self.newCubeList #transfer current cubes to old list
            self.newCubeList = []
            for crd in self.cubeList: #render all current cubes
                newCube = loader.loadModel("models/box")
                newCube.reparentTo(self.render)
                newCube.setScale(1,1,1)
                newCube.setPos(crd[0], crd[1], crd[2])
                newCube.setTexture(self.cubeTexture, 1)
                self.renderList.append(newCube)
            #by this point, we got the future iteration

            self.percent=(float(len(self.cubeList))/float(self.gridSize**3))*100

            if len(self.cubeList) == 0 and self.iterated:
                self.finished = True
                self.iterated = False
            elif self.prevCubeList == self.cubeList:
                self.finished = True

        return Task.cont

    def checkNeighbors(self, x, y, z):
        nBors = 0
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                for k in [-1,0,1]:
                    if (i != 0 or j != 0 or k != 0) and \
                    [i+x,j+y,k+z] in self.cubeList:
                        nBors += 1
        return nBors


if seedState:
    #Need to connect Seedstage tkinter thing to this file
    #seedDemo = SeedStage()
    #seedDemo.run()
    pass

defaultSeeds = [[2,2,2],
                [2,2,1],
                [2,1,2],
                [1,2,2],
                ]

def runStage(seeds, live, spawn, gridSize, itrDelay):
    playStage = PlayStage(seeds, live, spawn, gridSize, itrDelay)
    playStage.run()

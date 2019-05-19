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
from direct.gui.OnscreenText import OnscreenText

#global variables
seedState = False
playState = True

class PlayStage(ShowBase):
    def __init__(self, cubeList1, cubeList2, live, spawn, gridSize, itrDelay):
        ShowBase.__init__(self)

        self.showEnv = False #choose whether to show env or not

        self.gridSize = gridSize #size of play space
        self.camDist = 20 #distance of camera away from playspace
        self.camRot = 10.0 #rotation speed in angles per second

        self.itrDelay = itrDelay #time it takes to show one iteration

        self.currIter = 0 #current iteration
        self.maxIter = 20 #after 20 iterations, game ends
        self.hasFinished = False

        #Create list of cubes
        #THIS IS NOW BASED ON SEEDS
        self.cubeList1 = cubeList1
        self.origCopy1 = copy.deepcopy(cubeList1)
        self.length1 = float(len(self.cubeList1))
        self.cubeList2 = cubeList2
        self.origCopy2 = copy.deepcopy(cubeList2)
        self.length2 = float(len(self.cubeList2))

        self.live = live
        self.spawn = spawn

        self.p1Percent = (self.length1/(self.gridSize**3))*100
        self.p2Percent = (self.length2/(self.gridSize**3))*100
        self.p1 = OnscreenText(text = 'P1:' + str(self.p1Percent) + '%',
                            pos = (-0.75,0.75), scale = 0.25)
        self.p2 = OnscreenText(text = 'P2:' + str(self.p2Percent) + '%',
                            pos = (0.75,0.75), scale = 0.25)

        #Creates new list of cubes for next iteration
        self.newCubeList1 = []
        self.newCubeList2 = []

        #List of all cubes already rendered
        self.renderList = []

        #Create water box
        self.latestX, self.latestY, self.latestZ = 0,0,0

        #texture stuff
        waterTexture = loader.loadTexture("models/textures/waterTexture.png")
        self.cubeTexture2 = waterTexture
        fireTexture = loader.loadTexture("models/textures/fire.png")
        self.cubeTexture1 = fireTexture

        #timer stuff
        self.prevIncrement = 0

        self.message = ""
        self.restart = None

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

        #updates GUI for players to see
        self.taskMgr.add(self.updateGUI, "UpdateGUI")


    def restartGame(self):
        print('restart')
        self.cubeList1 = copy.deepcopy(self.origCopy1)
        self.cubeList2 = copy.deepcopy(self.origCopy2)
        self.p1percent = (float(self.length1)/float(self.gridSize**3))*100
        self.p2percent = (float(self.length2)/float(self.gridSize**3))*100
        #Creates new list of cubes for next iteration
        self.newCubeList1 = []
        self.newCubeList2 = []

        #List of all cubes already rendered
        for cube in self.renderList: #remove all old rendered cubes
            cube.removeNode()
        self.renderList = []

        self.currIter = 0
        self.hasFinished = False

    def updateGUI(self, task):
        self.p1.destroy()
        self.p1 = OnscreenText(text = 'P1: ' + str(self.p1Percent) + '%',
                            pos = (-0.75,0.75), scale = 0.10)
        self.p2.destroy()
        self.p2 = OnscreenText(text = 'P2: ' + str(self.p2Percent) + '%',
                            pos = (0.75,0.75), scale = 0.10)
        if self.hasFinished == True:
            if self.p1Percent > self.p2Percent:
                self.message = OnscreenText(text ='P1 Wins',
                                        pos = (0,0.80), scale = 0.20)
            elif self.p2Percent > self.p1Percent:
                self.message = OnscreenText(text ='P2 Wins',
                                        pos = (0,0.80), scale = 0.20)
            else:
                self.message = OnscreenText(text ='Tie',
                                        pos = (0,0.80), scale = 0.20)

            self.restart = OnscreenText(text ='Press \'r\' to review',
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


    def kickOff(self, task): #renders all starting cubes, both player 1 and 2
        for crd in self.cubeList1:
            newCube = loader.loadModel("models/box")
            newCube.reparentTo(self.render)
            newCube.setScale(1,1,1)
            newCube.setPos(crd[0], crd[1], crd[2])
            newCube.setTexture(self.cubeTexture1, 1)
            self.renderList.append(newCube)
        for crd in self.cubeList2:
            newCube = loader.loadModel("models/box")
            newCube.reparentTo(self.render)
            newCube.setScale(1,1,1)
            newCube.setPos(crd[0], crd[1], crd[2])
            newCube.setTexture(self.cubeTexture2, 1)
            self.renderList.append(newCube)

    def nextIteration(self, task):
        newIncrement = task.time // self.itrDelay
        if playState and newIncrement > self.prevIncrement and \
        self.hasFinished == False:
            self.currIter += 1
            self.prevIncrement = newIncrement
            for i in range(self.gridSize): #check next iteration
                for j in range(self.gridSize):
                    for k in range(self.gridSize): #only carries alive cubes
                        nbors = self.checkNeighbors(i,j,k)
                        nbors1 = nbors[0]
                        nbors2 = nbors[1]
                        if nbors1 == self.spawn:
                            self.newCubeList1.append([i,j,k])
                        elif nbors1 == self.live and \
                        [i,j,k] in self.cubeList1:
                            self.newCubeList1.append([i,j,k])
                        elif nbors2 == 3:
                            self.newCubeList2.append([i,j,k])
                        elif nbors2 == 2 and \
                        [i,j,k] in self.cubeList2:
                            self.newCubeList2.append([i,j,k])
            for cube in self.renderList: #remove all old rendered cubes
                cube.removeNode()
            self.renderList = []
            self.cubeList1 = self.newCubeList1
            self.cubeList2 = self.newCubeList2 #transfer current cubes to old list
            self.newCubeList1 = []
            self.newCubeList2 = []
            for crd in self.cubeList1: #render all current cubes
                newCube = loader.loadModel("models/box")
                newCube.reparentTo(self.render)
                newCube.setScale(1,1,1)
                newCube.setPos(crd[0], crd[1], crd[2])
                newCube.setTexture(self.cubeTexture1, 1)
                self.renderList.append(newCube)
            for crd in self.cubeList2: #render all current cubes
                newCube = loader.loadModel("models/box")
                newCube.reparentTo(self.render)
                newCube.setScale(1,1,1)
                newCube.setPos(crd[0], crd[1], crd[2])
                newCube.setTexture(self.cubeTexture2, 1)
                self.renderList.append(newCube)
            #by this point, we got the future iteration
        #Gotta update the percents
        self.p1Percent = (float(len(self.cubeList1))/float(self.gridSize**3))*100
        self.p2Percent = (float(len(self.cubeList2))/float(self.gridSize**3))*100

        if self.currIter >= self.maxIter: #checks if game is over
            self.hasFinished = True

        return Task.cont

    def checkNeighbors(self, x, y, z):
        nBors = [0,0]
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                for k in [-1,0,1]:
                    if (i != 0 or j != 0 or k != 0):
                        if [i+x,j+y,k+z] in self.cubeList1:
                            nBors[0] += 1
                        if [i+x,j+y,k+z] in self.cubeList2:
                            nBors[1] += 1
        return nBors


defaultSeeds1 = [[2,2,2],
                [2,2,1],
                [2,1,2],
                [1,2,2],
                ]
defaultSeeds2 = [[5,5,5],
                [5,5,4],
                [5,4,5],
                [4,5,5],
                ]


def runStage(seeds1, seeds2, live, spawn, gridSize, itrDelay):
    playStage = PlayStage(seeds1, seeds2, live, spawn, gridSize, itrDelay)
    playStage.run()

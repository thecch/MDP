import Astar
from Car import Car
#from Node import Node
from HamiltonAlgorithm import findHamiltonPath
import time

class Map:
    #nMap = []
    gridMap=[]
    car = Car(0,0,'N')
    obsList = []
    obsPosList = []
    barrierList = []
    PTPPath = []
    movement = []
    size = 0
    clearCount=0
    iteration = 0
    startTime = 0
    elapsedTime = 0
    timeLimit = 6*60 #6 minutes
    def __init__(self,size,x,y,direction):
        self.size = size
        self.initMap(size,x,y,direction)
        self.startTime = time.time()
        for i in range(size):
            self.barrierList.append([0,i])
            self.barrierList.append([19, i])
            self.barrierList.append([i,0])
            self.barrierList.append([i,19])
            
        
    
    def printMap(self):
        # print("\n=====Iteration: "+str(self.iteration)+", Images Cleared: "+str(self.clearCount)+"=====")
        # print(end="  ")
        # for i in range(0,self.size):
        #     print(str(i%10),end=" ")
        # print()
        # for i in range(0,self.size):
        #     print(str(i%10),end=" ")
        #     for j in range(0,self.size):
        #         print(self.gridMap[j][i], end=" ")
        #     print()
        self.iteration+=1
                    

    def initMap(self,size,x,y,direction):
        self.car.pos=[x,y]
        self.car.direction = direction
        for i in range(0,size):
            newRow=[]
            g_newRow = []
            for j in range(0,size):
                #n = Node(i,j)
                #newRow.append(n)
                g_newRow.append('-')
            #self.nMap.append(newRow)
            self.gridMap.append(g_newRow)
        self.drawCar()

    def getCarFace(self):
        pos = self.car.pos.copy()
        if self.car.direction == 0:
            pos[1]-=1
        elif self.car.direction ==1:
            pos[0]+=1
            pos[1]-=1
        elif self.car.direction ==2:
            pos[0]+=1
        elif self.car.direction ==3:
            pos[0]+=1
            pos[1]+=1
        elif self.car.direction ==4:
            pos[1]+=1
        elif self.car.direction ==5:
            pos[0]-=1
            pos[1]+=1
        elif self.car.direction ==6:
            pos[0]-=1
        elif self.car.direction ==7:
            pos[0]-=1
            pos[1]-=1
        return pos
    
    
    def drawCar(self):
        pos = self.car.pos.copy()
        face = self.getCarFace()
        #print("pos: "+str(pos[0])+","+str(pos[1]))
        #print("face: "+str(face[0])+","+str(face[1]))
        extrusion = int((self.car.size-1)/2)
        for i in range(-extrusion,extrusion+1):
            for j in range(-extrusion,extrusion+1):
                if pos[0]+i>=0 and pos[0]+i<20 and pos[1]+j>=0 and pos[1]+j<20:
                    if i==0 and j ==0:
                        self.gridMap[pos[0]][pos[1]] = '@' #draw centre
                    elif (pos[0]+i) == face[0] and (pos[1]+j)==face[1]:
                        self.gridMap[pos[0]+i][pos[1]+j] = '*' #draw face
                    else:
                        self.gridMap[pos[0]+i][pos[1]+j] = '#'
                        
    def eraseCar(self):
        pos = self.car.pos
        #print("hello")
        carsize = 3
        extrusion = int((carsize-1)/2)
        for i in range(-extrusion,extrusion+1):
            for j in range(-extrusion,extrusion+1):
                if pos[0]+i>=0 and pos[0]+i<20 and pos[1]+j>=0 and pos[1]+j<20:
                    self.gridMap[pos[0]+i][pos[1]+j] = '-'

        

    def drawAStarPath(self):
        for i in self.PTPPath:
            pos = i.pos
            self.gridMap[pos[0]][pos[1]] = '+'
            
    def addBlock(self,x,y,direction):

        for i in range(-2,3):
            for j in range(-2,3):  
                if x+i>=0 and x+i<20 and y+j>=0 and y+j<20:
                        #self.nMap[x+i][y+j].nodeType=1
                        self.barrierList.append([x+i,y+j])
       # self.nMap[x][y].nodeType = 1
        self.obsPosList.append([x,y,direction])
       # self.nMap[x][y].obsDir = direction
        self.gridMap[x][y] = direction
       # self.obsList.append(self.nMap[x][y])
        
        
    def findHamiltonPath(self):
        targetList=[]
        #find path based on actual position the car needs to be in
        for i in range(0,len(self.obsPosList)):
            pos = self.getTarget(i)
            targetList.append(pos)
            self.gridMap[pos[0]][pos[1]] = 'X'
            #self.nMap[pos[0]][pos[1]].printNode()

        hPath = findHamiltonPath(targetList,self.car.pos)
        for i in hPath:
            print(i,end="->")
        print()

        return hPath
        
    def getTarget(self,target):
        targetNode = self.obsPosList[target]
        tarPos = self.obsPosList[target][0:2].copy()
        if targetNode[2]=='N':
            tarPos[1] -=4
        elif targetNode[2]=='E':
            tarPos[0] +=4
        elif targetNode[2]=='S':
            tarPos[1]+=4
        elif targetNode[2]=='W':
            tarPos[0]-=4
        
        return tarPos
        
    def moveToTarget(self,target, useTimer): #useTimer is a bool integer if the sim should run with a timer
        #tarPos = self.calibTarget(target)
        tarPos = self.getTarget(target)
        self.movement.clear()
        nextDif = [0,0]
        i=face = diff=0
        tarBlock = self.obsPosList[target]
        direction = tarBlock[2]
        
        #self.insertMoveOffObs()
        path = list(Astar.Astar(self.car.pos, tarPos,self.barrierList,self.size))
        #self.deleteMoveOffObs()
        
        self.printMap()
        
        if tarPos[0]!= self.getTarget(target)[0] or tarPos[1]!= self.getTarget(target)[1]:
            #self.insertArrivalObs(tarPos, tarBlock.obsDir)
            path.extend(list(Astar.Astar(tarPos, self.getTarget(target), self.barrierList, self.size)))
            #self.deleteArrivalObs(tarPos, tarBlock.obsDir)
        for j in path:
            self.gridMap[j[0]][j[1]] = '+'
            
        while i<len(path):
            nextDif = list(path[i]).copy()
            if nextDif[0]==self.car.pos[0] and nextDif[1]==self.car.pos[1]:
                i+=1
            else:
                nextDif[0] -= self.car.pos[0];
                nextDif[1] -= self.car.pos[1];
                if(self.moveCarXY(nextDif)==1):
                    i+=1

                if useTimer == 1:
                    time.sleep(0.5)
                    self.printMap()
                    self.elapsedTime = time.time() - self.startTime
                    print("Elasped Time: "+str(self.elapsedTime))
                    if(self.isTimeLimit() == 1):
                        print("Time is up!!")
                        return None
                else:
                    self.printMap()
                    
            
        #reached
        if direction == 'N':
            face=4
        elif direction == 'E':
            face=6
        elif direction == 'S':
            face=0
        elif direction == 'W':
            face=2
            
        while(self.car.direction!=face):
            diff = face - self.car.direction
            if diff<0:
                diff+=8
                
            if diff>4:
                self.turnCar(-1)
            else:
                self.turnCar(1)
            self.printMap()
        
        # self.moveCarFB(1)
        self.printMap()
        self.clearCount+=1
        #print(self.movement)
        if(useTimer == 1):
            print("Scanning Image...")
            time.sleep(10)
            self.elapsedTime = time.time() - self.startTime
            print("Elasped Time: "+str(self.elapsedTime))
        # self.moveCarFB(-1)
        return self.movement
        
    
    def isTimeLimit(self):
        if self.elapsedTime>=self.timeLimit:
            return 1
        else:
            return 0
        
    def moveCarXY(self,position):
        face = 0
        if(position[0] == 0 and position[1] < 0):
            face = 0;
        elif(position[0] > 0 and position[1] < 0):
            face = 1;
        elif(position[0] > 0 and position[1] == 0):
            face = 2;
        elif(position[0] > 0 and position[1] > 0):
            face = 3;
        elif(position[0] == 0 and position[1] > 0):
            face = 4;
        elif(position[0] < 0 and position[1] > 0):
            face = 5;
        elif(position[0] < 0 and position[1] == 0):
            face = 6;
        elif(position[0] < 0 and position[1] < 0):
            face = 7;
        
        if self.car.direction == face:
            self.moveCarFB(1)
            return 1
        else:
            if face-self.car.direction<0:
                face+=8
            
            if face-self.car.direction>4:
                self.turnCar(-1)
            else:
                self.turnCar(1)
                
        return 0
    
    def moveCarTP(self, direction):
        if direction > 0:
            self.moveCarFB(-1)
        
    def moveCarFB(self,steps):
        #self.gridMap[self.car.pos[0]][self.car.pos[1]] = '-'
        self.eraseCar()
        self.car.moveFB(steps)
        self.movement.append("Move:"+str(steps)+":<"+str(self.car.pos[0])+">,<"+str(self.car.pos[1])+">,<"+str(self.car.direction)+">")
        self.drawCar()
        print("Move car forward by "+str(steps)+" steps")
        
        
    def turnCar(self,direction):
        self.eraseCar()
        self.car.turn(direction)
        self.movement.append("Turn:"+str(direction)+":<"+str(self.car.pos[0])+">,<"+str(self.car.pos[1])+">,<"+str(self.car.direction)+">")
        self.drawCar()
        print("Turning car towards "+str(direction))
        
        
    def calibTarget(self,target):
        tarBlock = self.obsPosList[target]
        calibPos = tarBlock[0:2].copy()
        posDif = tarBlock[0:2].copy()
        posDif[0] -= self.car.pos[0]
        posDif[1]-=self.car.pos[1]
        
        if tarBlock[2] == 'N':
            calibPos[1] -= 3;
            if(posDif[1] <= 0):
                if(posDif[0] > 0 and calibPos[0]-3 >= 0):
                    calibPos[0] -= 3;
                else:
                    calibPos[0] += 3;
            
        elif tarBlock[2]== 'S':
            calibPos[1] += 3;
            if(posDif[1] >= 0):
                if(posDif[0] > 0 and calibPos[0]-3 >= 0):
                    calibPos[0] -= 3;
                else:
                    calibPos[0] += 3;
             
        elif tarBlock[2] == 'E':
            calibPos[0] += 3;
            if(posDif[0] >= 0):
                if(posDif[1] > 0 and calibPos[1]-3 >= 0):
                    calibPos[1] -= 3;
                else:
                    calibPos[1] += 3;
            
        
        elif tarBlock[2] == 'W':
            calibPos[0] -= 3;
            if(posDif[0] <= 0):
                if(posDif[1] > 0 and calibPos[1]-3 >= 0):
                    calibPos[1] -= 3;
                else:
                    calibPos[1] += 3;
        
        return calibPos
    
    def removeBarrier(self,x,y):
        for i in range(0,len(self.barrierList)):
            if self.barrierList[i][0] == x and self.barrierList[i][1] == y:
                del self.barrierList[i]
                return 1
        return 0
        
    #add obs for moving off from target
    def insertMoveOffObs(self):
        pos = self.car.pos
        faceDif = self.getCarFace().copy()
        
        #print("Difference: (" + str(faceDif[0]) + "," + str(faceDif[1]) + ")")
        """if self.clearCount > 0:
            self.barrierList.append(faceDif.copy())"""
            
        faceDif[0]-=pos[0]
        faceDif[1]-=pos[1]
        
        extrusion = int((self.car.size-1)/2)
        for i in range(-extrusion,extrusion+1):
            for j in range(-extrusion,extrusion+1):
                if pos[0]+i>=0 and pos[0]+i<20 and pos[1]+j>=0 and pos[1]+j<20:
                    if i != faceDif[0] and faceDif[1] == 0 and i != 0:
                        #self.nMap[pos[0]+i][pos[1]+j].setObstacle()
                        self.barrierList.append([pos[0]+i,pos[1]+j])
                    elif j != faceDif[1] and faceDif[0] == 0 and j != 0:
                        #self.nMap[pos[0]+i][pos[1]+j].setObstacle()
                        self.barrierList.append([pos[0]+i,pos[1]+j])
        """
        for i in range(-extrusion,extrusion+1):
            for j in range(-extrusion,extrusion+1):
                if pos[0]+i>=0 and pos[0]+i<20 and pos[1]+j>=0 and pos[1]+j<20:
                    if (i==0 and j==0) or (i==faceDif[0]and j==0) or (i==0 and j==faceDif[1]): #avoid face and centre of car
                        pass
                    elif(faceDif[0]==0 and j==faceDif[1]and (i==faceDif[0]+1 or i==faceDif[0]-1)): #avoid side of face of car
                        pass
                    elif(faceDif[1]==0 and i==faceDif[0] and (j==faceDif[1]+1 or j==faceDif[1]-1)): #avoid side of face of car
                        pass
                    else:
                        self.nMap[pos[0]+i][pos[1]+j].setObstacle()"""
    
    
    
    #delete obs for moving off
    def deleteMoveOffObs(self):
        pos = self.car.pos
        faceDif = self.getCarFace().copy()
        
        """if self.clearCount > 0:
            self.barrierList.append(faceDif.copy())"""
            
        faceDif[0]-=pos[0]
        faceDif[1]-=pos[1]
        
        #print("Difference: (" + str(faceDif[0]) + "," + str(faceDif[1]) + ")")
        
        extrusion = int((self.car.size-1)/2)
        for i in range(-extrusion,extrusion+1):
            for j in range(-extrusion,extrusion+1):
                if pos[0]+i>=0 and pos[0]+i<20 and pos[1]+j>=0 and pos[1]+j<20:
                    if i != faceDif[0] and faceDif[1] == 0 and i != 0:
                        self.removeBarrier(pos[0]+i, pos[1]+j)
                    elif j != faceDif[1] and faceDif[0] == 0 and j != 0:
                        #self.nMap[pos[0]+i][pos[1]+j].removeObstacle()
                        self.removeBarrier(pos[0]+i, pos[1]+j)
        """
        for i in range(-extrusion,extrusion+1):
            for j in range(-extrusion,extrusion+1):
                if pos[0]+i>=0 and pos[0]+i<20 and pos[1]+j>=0 and pos[1]+j<20:
                    if (i==0 and j==0) or (i==faceDif[0]and j==0) or (i==0 and j==faceDif[1]): #avoid face and centre of car
                        pass
                    elif(faceDif[0]==0 and j==faceDif[1]and (i==faceDif[0]+1 or i==faceDif[0]-1)): #avoid side of face of car
                        pass
                    elif(faceDif[1]==0 and i==faceDif[0] and (j==faceDif[1]+1 or j==faceDif[1]-1)): #avoid side of face of car
                        pass
                    else:
                        self.nMap[pos[0]+i][pos[1]+j].removeObstacle()"""
    
    

    
    
    
    
    


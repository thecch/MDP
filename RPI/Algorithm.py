from Map import *

class Algorithm:

   # m = Map(20,1,18,0)
    m = 0
    pathLeft = []
    
    def __init__(self,startPos, startDir): #init with car pos
        self.m = Map(20,startPos[0], startPos[1], startDir)
        print("init")
        
    def findPath(self,obstaclesStr):
        
        obs = obstaclesStr.split(',')
        del obs[len(obs)-1]

        for i in range(0,len(obs),3):
            self.m.addBlock(int(obs[i]),int(obs[i+1]),str(obs[i+2]))
        hPath = self.m.findHamiltonPath()
        self.pathLeft = hPath.copy()
        self.pathLeft.pop(0)
        return hPath
        

    def getMvmtList(self):
        mvmtList = []
        coordList = []
        
        if(len(self.pathLeft)>0):
            mvmtCmd = self.m.moveToTarget(self.pathLeft[0]-1,0)
            self.pathLeft.pop(0)
            if mvmtCmd !=None:
                for mvmt in mvmtCmd:
                    instr = mvmt.split(':')
                    #print(mvmt)
                    if instr[0] == "Turn":
                        if int(instr[1]) > 0:
                            mvmtList.append('D')
                        else:
                            mvmtList.append('A')
                    else:
                        if int(instr[1]) > 0:
                            mvmtList.append('W')
                        else:
                            mvmtList.append('X')
                    coordList.append(instr[2])
                mvmtList, coordList = self.cleanMvmtList(mvmtList, coordList)
                return mvmtList, coordList
        else:
            return None, None

    def cleanMvmtList(self, mvmtList, coordList):
        newMvmtList = []
        newCoordList = []
        i = 0
        while (i<len(mvmtList)):
            if((i+1)<len(mvmtList) and mvmtList[i] != "W" and mvmtList[i+1] != "W" and mvmtList[i] != "S" and mvmtList[i+1] != "S"):
                newMvmtList.append(mvmtList[i+1])
                newCoordList.append("ROBOT,"+coordList[i+1])
                i += 1
            else:
                newMvmtList.append(mvmtList[i])
                newCoordList.append("ROBOT,"+coordList[i])
            i += 1
        return newMvmtList, newCoordList

    #m.addBlock(4,5,'N');
    #m.addBlock(9,9,'E');
    #m.addBlock(10,5,'W');
    #m.addBlock(19,16,'W');
    #m.addBlock(18,0,'S');
    #hPath = m.findHamiltonPath()
    #pathLeft = hPath.copy()
    #pathLeft.pop(0)

    #AstarPath = m.findAstarPath([15,0])
    #print(len(AstarPath))
    #m.printMap()

    #while len(pathLeft)>0:
    #    print("Current Target: "+str(pathLeft[0]))
    #    if(m.moveToTarget(pathLeft[0]-1)==1):
    #        pathLeft.pop(0)
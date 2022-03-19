import math
from Node import Node

size = 0

def findPath(nodeMap,startPos,destPos):
    start = nodeMap[startPos[0]][startPos[1]]
    dest = nodeMap[destPos[0]][destPos[1]]
    #start.printNode()
    #dest.printNode()
    openList = []
    closedList = []
    size = len(nodeMap)
    openList.append(start)
    while(len(openList)>0):
        cur = getCheapestNode(openList)
        #cur.printNode();
        openList.remove(cur)
        closedList.append(cur)
        if cur == dest:
            return retracePath(start,dest)
        
        pList = getNeighbour(nodeMap, cur, dest,size)
        for i in range(0,len(pList)):
            n = pList[i]
            #n.printNode()
            if n.nodeType != 1 and n not in closedList:
                #print("cond1")
                distToN = cur.g + calcDistance(cur,n)
                if n not in openList or distToN<n.g:
                    initNode(n,cur,dest)
                    if n not in openList:
                        openList.append(n)
        
    return closedList
        
        
def getCheapestNode(nl):
    minCost = 9999
    cheapest = 0
    if len(nl)>0:
        for i in range(0,len(nl)):
            if nl[i].f<minCost:
                minCost = nl[i].f
                cheapest = i
        return nl[cheapest]
    else:
        print("empty")
        return null
        
        
def initNode(targetNode, parent, dest):
    targetNode.parent = parent
    g=h=0
    if targetNode.h == 0:
        h = calcDistance(targetNode, dest)
    else:
        h = targetNode.h
    g = parent.g+calcDistance(targetNode, parent)
    targetNode.g = g
    targetNode.h=h
    

def calcDistance(fromNode, to):
    x1=fromNode.pos[0]
    y1=fromNode.pos[1]
    x2=to.pos[0]
    y2=to.pos[1]
    return math.sqrt((x2-x1)*(x2-x1) + (y2-y1)*(y2-y1))
    
def getNeighbour(nodeMap, n, dest,size):
    pList = []
    pos = n.pos
    for i in range(-1,2):
        for j in range(-1,2):
            #print(str(pos[0]+i))
            #print(str(pos[1]+j))
            if pos[0]+i<0 or pos[1]+j<0:
                #print("cond1")
                pass
            elif pos[0]+i>=size or pos[1]+j>=size:
                #print("cond2")
                pass
            elif i==0 and j==0:
               # print("cond3")
                pass
            elif i==0 or j == 0:
                pList.append(nodeMap[pos[0]+i][pos[1]+j])
    #print(str(len(pList)))
    return pList
    
def retracePath(start,dest):
    path = []
    cur = dest
    path.append(cur)
    while cur!=start:
        cur = cur.parent
        path.insert(0,cur)
    
    return path


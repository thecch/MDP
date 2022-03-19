import math
import Node

def tspdp(c, tour, start, n):
    mintour = [0]*(n+1)
    temp = [0]*(n+1)
    mincost = 999
    ccost = 0
    if start == (n-1):
        return c[tour[n-1]][tour[n]]
        
    for i in range(start+1,n+1):
        for j in range(1,n+1):
            temp[j] = tour[j]
        temp[start+1]=tour[i]
        temp[i] = tour[start+1]
        ccost = tspdp(c, temp, start + 1, n)
        if (c[tour[start]][tour[i]] + ccost)< mincost:
            mincost = c[tour[start]][tour[i]] + ccost
            for k in range(0,n+1):
                mintour[k] = temp[k]
                
    for i in range(0,n+1):
        tour[i] = mintour[i]
        
    return mincost


def calculateDistance(x1,y1,x2,y2):
    return math.sqrt((x2-x1)*(x2-x1) + (y2-y1)*(y2-y1))
    

def generateGraphMatrix(nodes, n):
    mat =  [[0 for x in range(n)] for y in range(n)] 
    for i in range(0,n):
        mat[i][i] = 0
    for i in range(0,n-1):
        for j in range(i,n):
            dist = calculateDistance(nodes[i][0],nodes[i][1],nodes[j][0], nodes[j][1])
            mat[i][j] = dist
            mat[j][i] = dist
    
    return mat


def printMatrix(mat):
    for row in mat:
        for col in row:
            print(str(col)+" ",end=" ")
        print("")


def findHamiltonPath(nl,startPos):
    nodes = [[startPos[0],startPos[1]]]
    tour = [0]*(len(nl)+1)
    for i in nl:
        nodes.append(i)
        print(i)
    for i in range(0,len(nl)+1):
        tour[i] = i
    mat = generateGraphMatrix(nodes,len(nl)+1)
    cost = tspdp(mat,tour,0,len(nl))
    print("Optimal path with cost: "+str(cost))

    return tour
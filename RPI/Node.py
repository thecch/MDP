class Node:
    g=h=f=0
    nodeType = 0
    pos = [0,0]
    parent = 0
    obsDir = ''
    def __init__(self,x,y):
        self.pos = [x,y]
        
    def setObstacle(self):
        self.nodeType = 1
        
    def removeObstacle(self):
        self.nodeType = 0
    
    def printNode(self):
        print("Node Pos:["+str(self.pos[0])+","+str(self.pos[1])+"]" )
        print("G="+str(self.g)+"H="+str(self.h))
    
if __name__ == "__main__":
    n = Node(3,4)
    p = Node(2,5)
    n.parent = p
    #print(str(n.parent.pos[1]))
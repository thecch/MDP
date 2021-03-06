# -*- coding: utf-8 -*-
"""Algorithm Test.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1YlrT7l1olcswaX7ppj8180wpzzUrMBbs
"""

import queue

def reconstructPath(explored, start, goal):
  currentNode = goal                      # Start at goal node
  path = []                               # Initialize blank path

  while currentNode != start:             # Stop when backtrack reaches start node
    path.append(currentNode)              # Grow path backwards
    currentNode = explored[currentNode]   # Backtrack path

  path.append(start)                      # Append start node to path
  path.reverse()                          # Reverse path

  return path

def calcDist(nodeA, nodeB):
  return abs(nodeA[0]-nodeB[0]) + abs(nodeA[1]-nodeB[1])    #Manhattan distance between 2 nodes

def getNeighbour(node, obs, size):
  neighbour = []

  for x in range(-1, 2):
    for y in range(-1, 2):
      if (x == 0 and y == 0):                               # Not neighbour of itself
        pass
      elif (x == 0 or y == 0) and (node[0]+x, node[1]+y) not in obs and node[0]+x < size and node[1]+y < size:          
        neighbour.append((node[0]+x, node[1]+y))            # Add neighbour only if directly above or beside and is not obstacle or out of map

  return neighbour

def dirCost(nodeA, nodeB, explored):
  cost = 0
  newDir = [element1 - element2 for (element1, element2) in zip(nodeB, nodeA)] # Get new direction
  oldDir = [0,0]

  if explored[nodeA] != None:
    oldDir = [element1 - element2 for (element1, element2) in zip(nodeA, explored[nodeA])]  # Get old direction
  
  if oldDir!=newDir:
    cost = 1    # Get cost
  
  return cost

def Astar(start, goal, obs, size):
  frontier = queue.PriorityQueue()    # Priority Queue
  start = tuple(start)
  goal = tuple(goal)
  for i in range(0,len(obs)):
    obs[i] = tuple(obs[i])
  #initialization
  frontier.put((0, start))              # Add start node to Priority Queue with priority 0
  explored = {}                         # Dict of explored nodes {node : parentNode}
  explored[start] = None                # Start node has no parent node
  pathCost = {}                         # Dict of distance cost from start to node
  pathCost[start] = 0                   # Start distance cost set to 0

  while not frontier.empty():
    currentNode = frontier.get()[1]     # Get cheapest node

    if currentNode == goal:           
      return reconstructPath(explored, start, goal)   # Return path

    neighbour = getNeighbour(currentNode, obs, size)  # Get current node neighbours
    for nextNode in neighbour:                                                            # For every neighbouring node                
      newDistCost = pathCost[currentNode] + 1 + dirCost(currentNode, nextNode, explored)  # Calculate current path cost with directional change cost                
      if ((nextNode not in explored) or (newDistCost < pathCost[nextNode])):              # If next node has not been explored or new cost lesser than old cost
        frontier.put((newDistCost+calcDist(nextNode,goal), nextNode))                     # Add to priority queue with new path cost as priority
        explored[nextNode] = currentNode                                                  # Add next node to explored with parent node                     
        pathCost[nextNode] = newDistCost+dirCost(currentNode, nextNode, explored)         # Add next node with new path cost                

  return None

'''start = (1,18)
goal = (3,4)
obs = [(3,1)]
size = 20

G = [["-" for x in range(size)] for y in range(size)]
path = Astar(start, goal, obs, size)

for node in obs:
  G[node[0]][node[1]] = "0"

for node in path:
  G[node[0]][node[1]] = "X"

G[start[0]][start[1]] = "S"
G[goal[0]][goal[1]] = "E"

for y in range(len(G)):
  for x in range(len(G[y])):
    print(G[x][y], end=" ")
  print()

start = (3,4)
goal = (12,7)
obs = [(9,7)]
size = 20

G = [["-" for x in range(size)] for y in range(size)]
path = Astar(start, goal, obs, size)

for node in obs:
  G[node[0]][node[1]] = "0"

for node in path:
  G[node[0]][node[1]] = "X"

G[start[0]][start[1]] = "S"
G[goal[0]][goal[1]] = "E"

for y in range(len(G)):
  for x in range(len(G[y])):
    print(G[x][y], end=" ")
  print()

dirCost((0,1), (0,2), {(0,1): (0,0)})'''


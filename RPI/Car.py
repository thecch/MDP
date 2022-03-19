import math

class Car:
    pos = [0,0]
    direction = 0
    size = 3
    def __init__(self,x,y,direction):
        self.pos = [x,y]
        self.direction = direction
        
    def moveFB(self, steps):
        #0=N, 2=E, 4=S, 6=W
        if self.direction==0:
            self.pos[1]-=steps
        elif self.direction ==1:
            self.pos[0]+=steps
            self.pos[1]-=steps
        elif self.direction ==2:
            self.pos[0]+=steps
        elif self.direction ==3:
            self.pos[0]+=steps
            self.pos[1]+=steps
        elif self.direction ==4:
            self.pos[1]+=steps
        elif self.direction ==5:
            self.pos[0]-=steps
            self.pos[1]+=steps
        elif self.direction ==6:
            self.pos[0]-=steps
        elif self.direction ==7:
            self.pos[0]-=steps
            self.pos[1]-=steps
            
    def turn(self, direction):
        self.direction = (self.direction+direction)%8
        if self.direction<0:
            self.direction = 8+self.direction
        #print(str(self.direction))

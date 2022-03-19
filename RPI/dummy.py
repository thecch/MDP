import Algorithm
import time

elapsedTime = 0
timeLimit = 6*60 #time limit of 6 minutes
startTime = time.time()

#function to update elapsed time and check if time limit is met
def updateTime():
    elapsedTime = time.time() - startTime
    #print(str(elapsedTime))
    if elapsedTime>=timeLimit:
        return 1
    else:
        return 0


a = Algorithm.Algorithm([1,18],0) #starting car position and facing direction 0 = up, 2 = right, 4 = down, 6 = left
path = a.findPath('4,5,N,9,9,E,10,5,W,19,16,W,18,0,S') #get hamiltonian path, the only reason to use the return value path is for looping based on length

#main loop 
def main_loop():
    for j in path: #path is technically 1 size larger than what we need since it includes start pos, but it doesn't really matter
        instr, coord = a.getMvmtList() 
        if instr!=None:
            for i in range(len(instr)):
                print(instr[i])
                print(coord[i])
                if(updateTime() == 1): #update and check if times up, if times up:
                    return
                #send movement instruction to stm here
        
        #send signal for image recognition here, once image task is done, continue
        
        
main_loop()
        

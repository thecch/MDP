#1. Carpark to obstacle
#forward sensor keep checking if there is obstacle ahead, move car forward until obstacle detected
while (fsensor.readData() == 0):
    car.moveForward(1)

#turn car to the right 90 degrees
car.turn(right)

#2. Centrepoint to right edge
forwardCount = 0
#travel length/2 of obstacle
#left sensor keep checking if obstacle is still on the left, move car until obstacle disappears
while (lsensor.readData() == 1):
    forwardCount+=1
    car.moveForward(1)

#turn car to the left 90 degrees without reverse
car.turn(left)


#3. Right edge front to right edge back
#travel breadth of obstacle
while (lsensor.readData() == 1):
    car.moveForward(1)
    
#turn car to the left 90 degrees without reverse
car.turn(left)

#4. Right edge back to left edge back
#travel full length of obstacle
while (lsensor.readData() == 1):
    car.moveForward(1)

#turn car to the left 90 degrees without reverse
car.turn(left)

#5. Left edge back to left edge front
#Travel breadth of obstacle
while (lsensor.readData() == 1):
    car.moveForward(1)
    
#turn car to the left 90 degrees without reverse
car.turn(left)

#6. left edge front to centrepoint
#travel length/2 to reach centrepoint
#for i in range(0,forwardCount):
car.moveForward(forwardCount)

car.turn(right)

#7. return to car park: forward sensor keep checking if there is obstacle ahead, move car forward until obstacle detected
while (fsensor.readData() == 0):
    car.moveForward(1)
    
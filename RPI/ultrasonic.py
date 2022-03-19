import time
import RPi.GPIO as GPIO

class Ultrasonic():
    def __init__(self):
        GPIO.setmode(GPIO.BCM)  # GPIO Mode (BOARD / BCM)
        self.GPIO_ECHO = 2
        self.GPIO_TRIG = 3

        # Set GPIO pins HC-SR04
        GPIO.setup(self.GPIO_TRIG, GPIO.OUT)
        GPIO.setup(self.GPIO_ECHO, GPIO.IN)

    def find_distance(self):
            
            GPIO.setwarnings(False)
            GPIO.cleanup()

            # pin ON/OFF LED
            STATUS = 4
            
            #set GPIO direction (IN / OUT)
            GPIO.setup(STATUS, GPIO.OUT)
            GPIO.output(STATUS, True)
            time.sleep(0.1)
            GPIO.output(STATUS, False)

            # Number of Iterations For Average
            iterations = 5

            GPIO.output(STATUS, 1)

            # Find Average from all Iterations
            avg_distance = 0
            while iterations > 0:
                distance = 0
                print("Distance measurement in progress")
                GPIO.output(self.GPIO_TRIG, 0)
                print("Waiting for sensor to settle")
                time.sleep(1)

                GPIO.output(self.GPIO_TRIG, 1)
                time.sleep(0.00001)
                GPIO.output(self.GPIO_TRIG, 0)

                while GPIO.input(self.GPIO_ECHO) == 0:
                    pulse_start = time.time()
                while GPIO.input(self.GPIO_ECHO) == 1:
                    pulse_end = time.time()

                time_elapsed = pulse_end - pulse_start
                
                # multiply by supersonic speed = 34300cm/s
                # divide by 2 because there and back
                distance = (time_elapsed * 34300)/2
                distance = round(distance, 3)

                if distance >= 200:
                    distance = 200
                if distance < 50:
                    distance = 50

                print("Distance: ", distance, "cm")
                avg_distance = avg_distance + distance
                iterations -= 1
            
            # Obtain Average Distance (tbC)
            avg_distance = avg_distance / iterations
            avg_distance= round(avg_distance)
            if avg_distance < 100:
                return_distance = "b0" + str(avg_distance)
            else:
                return_distance = "b" + str(avg_distance)
            print("Average Distance = " + str(avg_distance))
            
            GPIO.output(STATUS, 0)

            print("End of measurements")

            return return_distance
    
    def cleanup(self):
        GPIO.cleanup()


# test ultrasonic code
if __name__ == "__main__":
    try:
        while True:
            ultrasonic = Ultrasonic()
            avg_dist = ultrasonic.find_distance()

    except KeyboardInterrupt:
        print("Stopped by user")
        GPIO.cleanup()
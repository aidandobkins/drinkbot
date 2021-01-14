#FILE HOLDING THE DRINKBOT FUNCTIONS
import RPi.GPIO as GPIO
from time import sleep

TIME = 24 #amount of time it takes for one shot to dispense in seconds
PURGETIME = 10 #amount of time to run the pumps when purging in seconds
PUMP1 = 17
PUMP2 = 0
PUMP3 = 0
PUMP4 = 0
PUMP5 = 0
PUMP6 = 0

class makeDrink:
    time = 0
    gpio = 0

    def __init__(self, time, gpio):
        self.time = time
        self.gpio = gpio

    def setGpio(self, gpio):
        self.gpio = gpio

def queueDrink(mix):

    pumplist = []

    for i in range(6):
        if int(mix[i]) > 0:
            temptime = int(mix[i]) * TIME
        else:
            temptime = 0

        pumplist.append(makeDrink(temptime, 0))

    pumplist[0].setGpio(PUMP1)
    pumplist[1].setGpio(PUMP2)
    pumplist[2].setGpio(PUMP3)
    pumplist[3].setGpio(PUMP4)
    pumplist[4].setGpio(PUMP5)
    pumplist[5].setGpio(PUMP6)

    storeDrink(pumplist)

    sleeper = 0

    for j in range(6): #finds the biggest amount of shots entered
        if pumplist[j].time > sleeper:
            sleeper = pumplist[j].time

    sleepit = sleeper / TIME

    for k in range(int(sleepit)):
        for j in range(6):
            if pumplist[j].time > 0:
                GPIO.setmode(GPIO.BCM) # GPIO Numbers instead of board numbers
                GPIO.setup(int(pumplist[j].gpio), GPIO.OUT) # GPIO Assign mode
                GPIO.output(int(pumplist[j].gpio), GPIO.LOW) #3.3V to pump
                print("Pumping pump " + str(pumplist[j].gpio) + " for " + str(TIME) + " seconds\n")
                pumplist[j].time = pumplist[j].time - TIME
            else:
                GPIO.output(int(pumplist[j].gpio), GPIO.HIGH) #0V to pump
        
        sleep(TIME)

        for m in range(6):
            GPIO.output(int(pumplist[m].gpio), GPIO.HIGH) #0V to pump


def purgePumps():
    GPIO.setmode(GPIO.BCM )# GPIO Numbers instead of board numbers

    GPIO.setup(PUMP1, GPIO.OUT) # GPIO Assign mode
    GPIO.setup(PUMP2, GPIO.OUT) # GPIO Assign mode
    GPIO.setup(PUMP3, GPIO.OUT) # GPIO Assign mode
    GPIO.setup(PUMP4, GPIO.OUT) # GPIO Assign mode
    GPIO.setup(PUMP5, GPIO.OUT) # GPIO Assign mode
    GPIO.setup(PUMP6, GPIO.OUT) # GPIO Assign mode

    GPIO.output(PUMP1, GPIO.LOW) # 3.3V to pump
    GPIO.output(PUMP2, GPIO.LOW) # 3.3V to pump
    GPIO.output(PUMP3, GPIO.LOW) # 3.3V to pump
    GPIO.output(PUMP4, GPIO.LOW) # 3.3V to pump
    GPIO.output(PUMP5, GPIO.LOW) # 3.3V to pump
    GPIO.output(PUMP6, GPIO.LOW) # 3.3V to pump

    sleep(PURGETIME)

    GPIO.output(PUMP1, GPIO.HIGH) # 3.3V to pump
    GPIO.output(PUMP2, GPIO.HIGH) # 3.3V to pump
    GPIO.output(PUMP3, GPIO.HIGH) # 3.3V to pump
    GPIO.output(PUMP4, GPIO.HIGH) # 3.3V to pump
    GPIO.output(PUMP5, GPIO.HIGH) # 3.3V to pump
    GPIO.output(PUMP6, GPIO.HIGH) # 3.3V to pump

def storeDrink(drink):
    for i in range(6):
        #store drink[i].time 
        #store drink[i].gpio
import RPi.GPIO as GPIO
import os
import time
import atexit
import sys
from subprocess import call
import configure


def setup():
    for i in range(3):
        GPIO.setup(TRIG[i],GPIO.OUT)
        GPIO.setup(ECHO[i],GPIO.IN)
        GPIO.output(TRIG[i], False)

        print "Waiting For Sensor To Settle"

#if ('LTRIG' in os.environ):
#	TRIG = [int(os.environ['LTRIG']),
#			int(os.environ['CTRIG']),
#			int(os.environ['RTRIG'])]
#	ECHO = [int(os.environ['LECHO']),
#			int(os.environ['CECHO']),
#			int(os.environ['RECHO'])]


if ('LTRIG' in configure.data):
    TRIG = [int(configure.data['LTRIG']),
            int(configure.data['CTRIG']),
            int(configure.data['RTRIG'])]
    ECHO = [int(configure.data['LECHO']),
            int(configure.data['CECHO']),
            int(configure.data['RECHO'])]

    GPIO.setmode(GPIO.BCM)
    setup()

def turnOffGPIO():
	GPIO.cleanup()

atexit.register(turnOffGPIO)
		

def raw_distance(TRIG, ECHO):
    #check a sonar with trigger argv1 and echo argv2
    #example usage
    #python sonar.py 22 27

    # recommended for auto-disabling motors on shutdown!
    GPIO.setmode(GPIO.BCM)
    
        
    print "Distance Measurement In Progress"
    
    GPIO.setup(TRIG,GPIO.OUT)
    
    GPIO.setup(ECHO,GPIO.IN)
    
    GPIO.output(TRIG, False)

    print "Waiting For Sensor To Settle"
    
    time.sleep(2)
    
    GPIO.output(TRIG, True)
    
    time.sleep(0.00001)
    
    GPIO.output(TRIG, False)
    
    while GPIO.input(ECHO)==0:
        pulse_start = time.time()
        
    while GPIO.input(ECHO)==1:
        pulse_end = time.time()
            
    pulse_duration = pulse_end - pulse_start
            
    distance = pulse_duration * 17150
            
    distance = round(distance, 2)
    
    print "Distance:",distance,"cm"
                                            

def distance(i):
    #print "Distance Measurement In Progress"

    GPIO.output(TRIG[i], True)

    time.sleep(0.00001)

    GPIO.output(TRIG[i], False)

    pulse_end = 0;
    pulse_start = 0;
    #print "ping"
    if GPIO.input(ECHO[i])==1:
        print "stuck in high state"
        return 0
    #else:
    #    print "not stuck in high state"
    #print "waiting for echo to go to 0"
    pulse_pre = time.time()
    while GPIO.input(ECHO[i])==0:
        pulse_start = time.time()
        if (pulse_start - pulse_pre > 0.1):
           print "would not level"
           return 666 
        
    #print "sent"
    while GPIO.input(ECHO[i])==1:
        pulse_end = time.time()
        if (pulse_end - pulse_start > 1):
           print "no reply"
           return 667 
    #print "pong"    
    if (pulse_end == 0 or pulse_start==0):
        return 1000
        
    pulse_duration = pulse_end - pulse_start

    distance = pulse_duration * 17150

    distance = round(distance, 2)

    #print "Distance:",distance,"cm"

    return distance

def ldist():
	return distance(0)

def rdist():
	return distance(2)

def cdist():
	return distance(1)


if __name__ == "__main__":
   print "Cent:",cdist(),"cm"
   print "Left:",ldist(),"cm" 
   print "Cent:",cdist(),"cm"
   print "Right:",rdist(),"cm"

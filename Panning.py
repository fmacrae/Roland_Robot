#!/usr/bin/python

from Adafruit_PWM_Servo_Driver import PWM
import time

# ===========================================================================
# Example Code
# ===========================================================================

# Initialise the PWM device using the default address
pwm = PWM(0x41)
# Note if you'd like more debug output you can instead run:
#pwm = PWM(0x40, debug=True)

servoMin = 250  # Min pulse length out of 4096
servoMax = 500  # Max pulse length out of 4096
servoMid = 375  # Max pulse length out of 4096

def setServoPulse(channel, pulse):
  pulseLength = 1000000                   # 1,000,000 us per second
  pulseLength /= 60                       # 60 Hz
  print "%d us per period" % pulseLength
  pulseLength /= 4096                     # 12 bits of resolution
  print "%d us per bit" % pulseLength
  pulse *= 1000
  pulse /= pulseLength
  pwm.setPWM(channel, 0, pulse)

def scanLeftToRight():
  pwm.setPWMFreq(60)                        # Set frequency to 60 Hz
  while (True):
    # Change speed of continuous servo on channel O
    pwm.setPWM(0, 0, servoMin)
    time.sleep(2)
    pwm.setPWM(0, 0, servoMid)
    time.sleep(2)
    pwm.setPWM(0, 0, servoMax)
    time.sleep(2)
    pwm.setPWM(0, 0, servoMid)
    time.sleep(2)

def Look():
  degree = 250/120
  pwm.setPWMFreq(60)
  while(True):
    f = open('viewAngle.txt', 'r')
    angle  = f.readline()
    #print "%s Angle Read" % angle
    servoSetting = servoMid+(degree*int(angle))
    f.close()
    #print "%d servoSetting" % servoSetting
    pwm.setPWM(0, 0, servoSetting)
    time.sleep(1)

if  __name__ == "__main__":
  #scanLeftToRight()
  Look()

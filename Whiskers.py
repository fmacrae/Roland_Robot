import time
import RPi.GPIO as GPIO
import speaker
GPIO.setmode(GPIO.BCM)
GPIO.setup(20,GPIO.IN)
GPIO.setup(21,GPIO.IN)


class Whiskers(object):
  def __init__(self):
    self.prev_left = 0
    self.prev_right = 0
  def checkBumpLeft(self):
    input_left = GPIO.input(20)
    if ((not self.prev_left) and input_left):
      print("ouch on left")
      speaker.say("oof bumped the left")
    self.prev_left = input_left
    return input_left
  def checkBumpRight(self):
    input_right = GPIO.input(21)
    if ((not self.prev_right) and input_right):
      print("ouch on right")
      speaker.say("ouch mind the right side")
    self.prev_right = input_right
    return input_right

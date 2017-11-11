
import wheels
import sonar
import time
from Whiskers import Whiskers

FORWARD=1
LEFT=2
RIGHT=3
BACKWARD=4

def autodrive(dur):
	start_time = time.time()
	end_time = time.time() + dur
	objWhiskers = Whiskers()

	mode = FORWARD

	wheels.forward(150)

	
	while(time.time() < end_time):
		time.sleep(0.1)
		cdist = sonar.cdist()
		ldist = sonar.ldist()
		rdist= sonar.rdist()
		lbump = objWhiskers.checkBumpLeft()
		rbump = objWhiskers.checkBumpRight()

		print ("%d %d %d" % (ldist, cdist, rdist))
		print ("bumpers %d %d" % (lbump, rbump))
		
		if (mode == FORWARD):
			if (cdist < 35 or ldist <6 or rdist < 6 or lbump or rbump):
                                print ("turning")
                                wheels.stop()
				if (ldist < rdist):
					mode=RIGHT
					wheels.backward(150, .5)
					time.sleep(1)
					wheels.right(150, .5)
					time.sleep(1)
				else:
					mode=LEFT
					wheels.backward(150, .5)
					time.sleep(1)
					wheels.left(150, .5)
					time.sleep(1)
					
		if (mode==LEFT or mode==RIGHT):
			if (cdist > 50):
				mode=FORWARD
				wheels.forward(150)
				
			
			
	wheels.stop()


	
if (__name__ == '__main__'):
	autodrive(600)


import wheels
import sonar
import time
from Whiskers import Whiskers
import os

FORWARD=1
LEFT=2
RIGHT=3
BACKWARD=4






def autodrive(dur):
	start_time = time.time()
	end_time = time.time() + dur
	objWhiskers = Whiskers()
	timestr = time.strftime("%Y%m%d-%H%M%S")
	#grab the unique id for the run from a file then increment it by 1 and store back into the file
	iRunNum = 0	
	with open('data/current_run.txt') as f:
		sRunNum=f.read()
		print ("Run number is %s", str(sRunNum))
		iRunNum=int(sRunNum)
		iRunNum+=1
	outf = open('data/current_run.txt', 'w')
	outf.write(str(iRunNum))
	
	#now build the run data directory and store its location in a flat file
	sRunDataDirectory='data/'+str(iRunNum)+'-run-'+timestr+'/'
	os.makedirs(sRunDataDirectory)

	#write the directory to a file
	outf = open('run_data_directory.txt', 'w')
	outf.write(str(sRunDataDirectory))
	print ('Logging to %s', sRunDataDirectory)
	
	#Start driving!
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

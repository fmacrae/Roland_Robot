
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
	f.close()
	os.remove('data/current_run.txt')
	#write out the new number for the run
	outf = open('data/current_run.txt', 'w')
	outf.write(str(iRunNum))
	outf.close()
	
	#now build the run data directory and store its location in a flat file
	sRunDataDirectory='data/'+str(iRunNum)+'-run-'+timestr+'/'
	os.makedirs(sRunDataDirectory)
	print('Created data Directory')
	print(sRunDataDirectory)
	#write the directory to a file
	outf = open('run_data_directory.txt', 'w')
	outf.write(str(sRunDataDirectory))
	print ('Logging to %s', sRunDataDirectory)
	outf.close()
	#Start driving!
	mode = FORWARD

	wheels.forward(150)
	
	while(time.time() < end_time):
		print ("starting autonomous loop")
		time.sleep(0.1)

		#print ("getting cdist")
		cdist = sonar.cdist()
		#print ("getting ldist")
		ldist = sonar.ldist()
		#print ("getting rdist")
		rdist= sonar.rdist()
		print ("left %d centre %d right %d" % (ldist, cdist, rdist))
		lbump = objWhiskers.checkBumpLeft()
		rbump = objWhiskers.checkBumpRight()
		print ("bumpers %d %d" % (lbump, rbump))
		
		if (mode == FORWARD):
			if (cdist < 35 or ldist <6 or rdist < 6 or lbump or rbump):
                                print ("turning")
                                wheels.stop()
				if (ldist < rdist):
					print ("turning RIGHT")
					#mode=RIGHT
					wheels.backward(150, .5)
					time.sleep(1)
					print ("turning RIGHT finshed reverse")
					wheels.right(150, .5)
					time.sleep(1)
					print ("turning RIGHT done")
				else:
					#mode=LEFT
					print ("turning LEFT")
					wheels.backward(150, .5)
					time.sleep(1)
					print ("turning LEFT finished reverse")
					wheels.left(150, .5)
					time.sleep(1)
					print ("turning LEFT finished")
                        else:
                                wheels.forward(150)



			if (mode==LEFT or mode==RIGHT):
				if (cdist > 50):
					mode=FORWARD
					print ("keep on cruisin' forward")
					wheels.forward(150)
					print ("Finished driving forward")
			
	print ("finished autonomous driving, time to relax")
	wheels.stop()


	
if (__name__ == '__main__'):
	autodrive(6000)

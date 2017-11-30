# Roland_Robot

This will run a simple robot with a webserver on a raspberry PI with the Adafruit Motor Hat.  This is a development off of Lukas' great work on his robot.  Core things we are adding is mapping capability, notification APIs and imporved self driving.

## Hardware

- Raspberry PI 3
- Voltage dividers 5V to 3.3V for the echo channels for the sonars, ebay has lots of options for this or build your own from two resistors.
- If you want the Robot to speak get either a small self powered speaker system that uses 3.5mm jacks or something like a PAM8403 Amplifier Board which can run off your 5V outputs
- Servo to rotate the camera SG90 or MG90 Mini Servos work fine
- Get mini breadboards, lots of dupont wires and make sure to order sufficient header pins, including stackable ones for the adafruit hats.
- nice to haves - camera mount and sonar mounts.  Ebay again is a good source.
- 16GB (or larger) SIM Card
- Adafruit Motor Hat (for wheels)
- Any chassis with DC motors - for example: https://www.amazon.com/Emgreat-Chassis-Encoder-wheels-Battery/dp/B00GLO5SMY/ref=sr_1_2?ie=UTF8&qid=1486959207&sr=8-2&keywords=robot+chassis
- Adafruit Servo Hat (for arms)
- HC-SR04 sonars
- Any stepper motor arm - for example: SainSmart DIY Control Palletizing Robot Arm for the arm (https://www.amazon.com/dp/B0179BTLZ2/ref=twister_B00YTW763Y?_encoding=UTF8&psc=1)
- Raspberry PI compatible camera - for example: https://www.amazon.com/Raspberry-Pi-Camera-Module-Megapixel/dp/B01ER2SKFS/ref=sr_1_1?s=electronics&ie=UTF8&qid=1486960149&sr=1-1&keywords=raspberry+pi+camera
- for Whiskers to work you have to connect two bump sensors like this guy made http://www.instructables.com/id/Cheap%2C-Durable%2C-Very-Effective-Robot-Bump-Sensor/#ampshare=http://www.instructables.com/id/Cheap%252C-Durable%252C-Very-Effective-Robot-Bump-Sensor/ and connect via a safe circuit from your 3.3V outputs like this guy shows.  http://www.cl.cam.ac.uk/projects/raspberrypi/tutorials/robot/buttons_and_switches/ Do not miss out the resistors or you may fry your pi.
Order the stuff well ahead of time, that way you can use the cheaper and slower vendors.  Adafruit is hard to get in the UK quickly at a reasonable price but you can find it.

To get started, you should be able to make the robot work without the arm, whiskers, sonar and servo hat.

## Programs

- robot.py program will run commands from the commandline
- sonar.py tests sonar wired into GPIO ports
- wheels.py tests simple DC motor wheels
- arm.py tests a servo controlled robot arm
- autonomous.py implements a simple driving algorithm using the wheels and sonal
- inception_server.py runs an image classifying microservice
- Notification_Test.py tests the Twitter and Gmail integration.

## Example Robots

Here is the robot I made that uses this software

![Robots](https://s3.amazonaws.com/websofttechnology/roland.png)

## Wiring The Robot
### Sonar

If you want to use the default sonar configuation, wire like this:

- Left sonar trigger GPIO pin 23 echo 24
- Center sonar trigger GPIO pin 17 echo 18
- Right sonar trigger GPIO pin 22 echo 27
- Right whisker GPIO pin 21
- Left whisker GPIO pin 20

You can modify the pins by making a robot.conf file.

### Wheels

You can easily change this but this is what wheels.py expects

- M1 - Front Left
- M2 - Back Left (optional - leave unwired for 2wd chassis)
- M3 - Back Right (optional - leave unwired for 2wd chassis)
- M4 - Front Right 


## Installation

### basic setup

There are a ton of articles on how to do basic setup of a Raspberry PI - one good one is here https://www.howtoforge.com/tutorial/howto-install-raspbian-on-raspberry-pi/
Boot it with a screen, keyboard and mouse, connect to your wifi and note your IP address.  Best to log into your hub and assign it a static IP address so you know what to ssh to.


You will need to turn on i2c and optionally the camera

```
sudo raspi-config
```
1. Change your password as you need one for SSH
2. Change your hostname to something meaningful like Robot or Roland
5. Interfacing options, enable: P1 Camera, P2 SSH, P5 I2C
8. Update - always update :)
Finish

Now upgrade your Pi - takes a while....then do a restart
```
sudo apt-get update
sudo apt-get upgrade
pip install --upgrade pip
sudo shutdown now
```
Now you can unplug and SSH into it from a real computer.

Next you will need to download i2c tools and smbus

```
sudo apt-get install i2c-tools python-smbus python3-smbus
```

Test that your hat is attached and visible with

```
i2cdetect -y 1
```

Install this code

```
sudo apt-get install git
git clone https://github.com/fmacrae/Roland_Robot.git
cd Roland_Robot
```

Install dependencies = adafruit pip install fails at moment so install manually

```
cd ~
git clone https://github.com/adafruit/Adafruit-Motor-HAT-Python-Library.git
cd Adafruit-Motor-HAT-Python-Library
sudo apt-get install python-dev
sudo python setup.py install
cd ~/Roland_Robot
easy_install pykalman
sudo pip install -r requirements.txt
sudo apt-get install flite
sudo apt-get install python-paramiko
```

At this point you should be able to drive your robot locally, try:

```
./robot.py forward
```

### server

To run a webserver in the background with a camera you need to setup gunicorn and nginx

#### nginx

Nginx is a lightway fast reverse proxy - we store the camera image in RAM and serve it up directly.  This was the only way I was able to get any kind of decent fps from the raspberry pi camera.  We also need to proxy to gunicorn so that the user can control the robot from a webpage.

copy the configuration file from nginx/nginx.conf to /etc/nginx/nginx.conf

```
sudo apt-get install nginx
sudo cp nginx/nginx.conf /etc/nginx/nginx.conf
```

restart nginx

```
sudo nginx -s reload
```

#### gunicorn

install gunicorn


copy configuration file from services/web.service /etc/systemd/system/web.service

```
sudo cp services/web.service /etc/systemd/system/web.service
```

start gunicorn web app service

```
sudo systemctl daemon-reload
sudo systemctl enable web
sudo systemctl start web
```

Your webservice should be started now.


#### camera

In order to stream from the camera you can use RPi-cam.  It's documented at http://elinux.org/RPi-Cam-Web-Interface but you can also just run the following

```
git clone https://github.com/silvanmelchior/RPi_Cam_Web_Interface.git
cd RPi_Cam_Web_Interface
chmod u+x *.sh
./install.sh
```
Popup giving you choices will appear, accept defaults.  You'll get a few errors like:
```
Failed to start The Apache HTTP Server.
```

But just ignore them.
Now a stream of images from the camera should be constantly updating the file at /dev/shm/mjpeg.  Nginx will serve up the image directly if you request localhost/cam.jpg.  Be aware that SD cards only have a limited write capacity so if you leave this running 24 7 then over a few months you will burn out a consumer level card.  Make sure you clone your card at least every other month as it will either lock in read only state or start to have write errors.  It is a good practice to get into.  Either plug the Pi into a monitor and use the SD Card clone function or put the sd card into your main machine and use disks to take an image of it.  Another warning, use the same SD Card type as there is a minor variation in total size between the 16Gb manufacturers.

#### tensorflow

There is a great project at https://github.com/samjabrahams/tensorflow-on-raspberry-pi that gives instructions on installing tensorflow on the Raspberry PI.  Recently it's gotten much easier, just do

```
wget https://github.com/samjabrahams/tensorflow-on-raspberry-pi/releases/download/v0.11.0/tensorflow-0.11.0-cp27-none-linux_armv7l.whl
sudo pip install tensorflow-0.11.0-cp27-none-linux_armv7l.whl
```

Last command took an age... run it and go out or run it just before bed so it can go overnight
 
It also doesn’t install tensorflow, just the python interfaces or at least didn’t get a proper tensorflow directory with any of the stuff we need….

``` 
cd ~
git clone https://github.com/tensorflow/tensorflow.git
cd tensorflow
tensorflow/contrib/makefile/download_dependencies.sh
sudo apt-get install -y autoconf automake libtool gcc-4.8 g++-4.8
cd tensorflow/contrib/makefile/downloads/protobuf/
./autogen.sh
./configure
make
sudo make install
sudo ldconfig  # refresh shared library cache
cd ../../../../..
export HOST_NSYNC_LIB=`tensorflow/contrib/makefile/compile_nsync.sh`
export TARGET_NSYNC_LIB="$HOST_NSYNC_LIB"
make -f tensorflow/contrib/makefile/Makefile HOST_OS=PI TARGET=PI \
 OPTFLAGS="-Os -mfpu=neon-vfpv4 -funsafe-math-optimizations -ftree-vectorize" CXX=g++-4.8

```

I found running the steps from:
- https://github.com/tensorflow/tensorflow/tree/master/tensorflow/contrib/makefile#raspberry-pi
- https://github.com/tensorflow/tensorflow/tree/master/tensorflow/contrib/pi_examples

Install and compile tensorflow correctly for the Pi.  Takes around 3-8hrs to do so kick off the make commands and find something else to do for a few hours.  The final make command is best run overnight.
 

Now create a symbolic link for the labels in your tensorflow directory to the pi_examples label_image directory

```
pi@raspberrypi:~/tensorflow $ ln -s tensorflow/contrib/pi_examples/label_image/gen/bin/label_image label_image
```


Next start a tensorflow service that loads up an inception model and does object recognition the the inception model

```
sudo cp services/inception.service /etc/systemd/system/inception.service
sudo systemctl daemon-reload
sudo systemctl enable inception
sudo systemctl start inception
```


Once everything is installed and ready you can get the robot running using:
```
sh startRobot.sh
```

If you want to control it via the web interface then do this:

```
sudo sh server.sh &
python inception_server.py &
```

 
Then on localhost:
- port 9999 for inception  http://localhost:9999
- port 8000 for drive http://localhost:8000
- /cam.jpg to see what it sees  http://localhost/cam.jpg
 
I have an issue with drive as it tries to show the picture and fails as its appending ?T=1242341…
 
Not sure how to resolve and lukas has an issue open for it.
 
https://github.com/lukas/robot/issues/6
 
 

#### notification

- Update Notification_Settings.csv with your Twitter API OAuth settings, 
Siraj has a good guide on how to set it up here https://www.youtube.com/watch?v=o_OZdbCzHUA 
- Also create a Gmail API OAuth token called client_secret.json using instructions here https://developers.google.com/gmail/api/quickstart/python
- Run the Notification_Test.py which will hopefully Tweet then ask for your permission via a browser to send email.
- If you cannot do this due to running via SSH or similar then install the dependancies and run the Notification_Test.py on your desktop which creates a special json file in your home directory in a hidden subfolder called .credentials
- sftp the file to your Pi 
```
sftp pi@yourpisaddress
lcd ~/.credentials
cd /home/pi/.credentials
put gmail-python-email-send.json
```



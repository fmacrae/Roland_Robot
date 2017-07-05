# Roland_Robot

This will run a simple robot with a webserver on a raspberry PI with the Adafruit Motor Hat.  This is a development off of Lukas' great work on his robot.  Core things we are adding is mapping capability, notification APIs and imporved self driving.

## Hardware

- Raspberry PI 3
- 16GB (or larger) SIM Card
- Adafruit Motor Hat (for wheels)
- Any chassis with DC motors - for example: https://www.amazon.com/Emgreat-Chassis-Encoder-wheels-Battery/dp/B00GLO5SMY/ref=sr_1_2?ie=UTF8&qid=1486959207&sr=8-2&keywords=robot+chassis
- Adafruit Servo Hat (for arms)
- HC-SR04 sonars
- Any stepper motor arm - for example: SainSmart DIY Control Palletizing Robot Arm for the arm (https://www.amazon.com/dp/B0179BTLZ2/ref=twister_B00YTW763Y?_encoding=UTF8&psc=1)
- Raspberry PI compatible camera - for example: https://www.amazon.com/Raspberry-Pi-Camera-Module-Megapixel/dp/B01ER2SKFS/ref=sr_1_1?s=electronics&ie=UTF8&qid=1486960149&sr=1-1&keywords=raspberry+pi+camera

To get started, you should be able to make the robot work without the arm, sonar and servo hat.

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

![Robots](https://s3.amazonaws.com/websofttechnology/roland.jpg)

## Wiring The Robot
### Sonar

If you want to use the default sonar configuation, wire like this:

- Left sonar trigger GPIO pin 23 echo 24
- Center sonar trigger GPIO pin 17 echo 18
- Right sonar trigger GPIO pin 22 echo 27

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

You will need to turn on i2c and optionally the camera

```
raspi-config
```

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

Install dependencies

```
sudo pip install -r requirements.txt
sudo apt-get install flite

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

Your webservice should be started now.  You can try driving your robot with buttons or arrow keys

#### camera

In order to stream from the camera you can use RPi-cam.  It's documented at http://elinux.org/RPi-Cam-Web-Interface but you can also just run the following

```
git clone https://github.com/silvanmelchior/RPi_Cam_Web_Interface.git
cd RPi_Cam_Web_Interface
chmod u+x *.sh
./install.sh
```

Now a stream of images from the camera should be constantly updating the file at /dev/shm/mjpeg.  Nginx will serve up the image directly if you request localhost/cam.jpg.

#### tensorflow

There is a great project at https://github.com/samjabrahams/tensorflow-on-raspberry-pi that gives instructions on installing tensorflow on the Raspberry PI.  Recently it's gotten much easier, just do

```
wget https://github.com/samjabrahams/tensorflow-on-raspberry-pi/releases/download/v0.11.0/tensorflow-0.11.0-cp27-none-linux_armv7l.whl
sudo pip install tensorflow-0.11.0-cp27-none-linux_armv7l.whl
```

Last command took an age... run it and go out or run it just before bed so it can go overnight
 
It also doesn’t install tensorflow, just the python interfaces or at least didn’t get a proper tensorflow directory with any of the stuff we need….
 
I found running the steps from:
- https://github.com/tensorflow/tensorflow/tree/master/tensorflow/contrib/makefile#raspberry-pi
- https://github.com/tensorflow/tensorflow/tree/master/tensorflow/contrib/pi_examples

Install and compile tensorflow correctly for the Pi.  Takes around 3hrs to do
 

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
sudo sh server.sh &
python inception_server.py &
```
think second one is to d/l the files needed to tmp
 
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
- Drop the file into your Roland_Robot directory.




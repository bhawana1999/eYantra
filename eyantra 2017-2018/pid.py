# import the necessary packages
from imutils.video import VideoStream
import datetime
import argparse
import imutils
import time
import cv2
import os
import sys
from picamera import PiCamera
import RPi.GPIO as GPIO
#from picamera.exc import PiCameravalueerror
from time import sleep
 
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--picamera", type=int, default=-1,
	help="whether or not the Raspberry Pi camera should be used")
args = vars(ap.parse_args())
 
# initialize the video stream and allow the cammera sensor to warmup
vs = VideoStream(usePiCamera=args["picamera"] > 0).start()
time.sleep(2.0)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
 
Motor1A = 33
Motor1B = 35
Motor1E = 37
Motor2A = 36
Motor2B = 38
Motor2E = 40

GPIO.setup(Motor1A,GPIO.OUT)
GPIO.setup(Motor1B,GPIO.OUT)
GPIO.setup(Motor1E,GPIO.OUT)
GPIO.setup(Motor2A,GPIO.OUT)
GPIO.setup(Motor2B,GPIO.OUT)
GPIO.setup(Motor2E,GPIO.OUT)

left = GPIO.PWM(Motor1E, 100)
right = GPIO.PWM(Motor2E, 100)
left.start(50)
right.start(50)

frame_cnt = 0
last_error=0
error=0

## PID constants
kp = 0.8
kd = 1
error=0
base_speed=40

while True:
    frame=vs.read()
    frame = imutils.resize(frame, width=640, height=480)
    blur_CM = cv2.medianBlur(crop_img,5)
        filt_CM = cv2.bilateralFilter(blur_CM,5,1000,1000)
        gray = cv2.cvtColor(filt_CM, cv2.COLOR_BGRA2GRAY)
        blur = cv2.GaussianBlur(gray,(5,5),0)
        ret,thresh = cv2.threshold(blur,100,255,cv2.THRESH_BINARY_INV)
        _,contours,hierarchy = cv2.findContours(thresh.copy(), 1, cv2.CHAIN_APPROX_NONE)
        if len(contours) > 0:

                c = max(contours, key=cv2.contourArea)

                M = cv2.moments(c)
                if M['m00']==0:
                    continue

                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])
                
                cv2.drawContours(crop_img, contours, -1, (0,255,0), 1)
                cv2.putText(crop_img,str(320-cx),(cx,cy), cv2.FONT_HERSHEY_SIMPLEX, .5,(255,0,0),2,cv2.LINE_AA)
                
                dist=320-cx
                error=dist

                derivative=last_error-error
                print "derivative=",derivative
                pwm= (kp*error)+(kd*derivative)
                print "pwm=",pwm
                last_error=error
                if dist>0:
                    right_fin = pwm - base_speed
                    left_fin = pwm + base_speed

                if dist<0:
                    right_fin = pwm + base_speed
                    left_fin = pwm - base_speed

                
                
                if right_fin > 100:
                    right_fin = 100
                if right_fin < 0:
                    right_fin = 0
                if left_fin > 100:
                    left_fin = 100
                if left_fin < 0:
                    left_fin = 0
                GPIO.output(Motor1A,GPIO.LOW)
                GPIO.output(Motor1B,GPIO.HIGH)
                left.ChangeDutyCycle(left_fin)
                GPIO.output(Motor2A,GPIO.LOW)
                GPIO.output(Motor2B,GPIO.HIGH)
                right.ChangeDutyCycle(right_fin)
                
                

                cv2.imshow("Video",crop_img)
                cv2.waitKey(1)
                key = cv2.waitKey(1) & 0xFF
                if key == ord("Q"):
                    sys.exit()




    
        
                

    

    

    


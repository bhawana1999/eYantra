import cv2
import os
from picamera import PiCamera
from picamera.array import PiRGBArray
import numpy as np
import time
import RPi.GPIO as GPIO
from time import sleep

try:
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
    left.start(25)
    right.start(25)

    cam = PiCamera()
    cam.resolution = (640,480)
    cam.framerate = 5

    raw_cap = PiRGBArray(cam,(640,480))

    frame_cnt = 0

    for frame in cam.capture_continuous(raw_cap,format="bgr",use_video_port=True,splitter_port=2,resize=(640,480)):
        list=[]
        color_image = frame.array
        crop_img4 = color_image[0:120, :]
        crop_img3 = color_image[120:240,:]
        crop_img2 = color_image[240:360,:]
        crop_img1 = color_image[360:480,:]
        image_array=[crop_img1,crop_img2,crop_img3,crop_img4]
        
        for i in image_array:
            gray = cv2.cvtColor(i, cv2.COLOR_BGR2GRAY)
        
            blur = cv2.GaussianBlur(gray,(5,5),0)
            ret,thresh = cv2.threshold(blur,60,255,cv2.THRESH_BINARY_INV)
            _,contours,hierarchy = cv2.findContours(thresh.copy(), 1, cv2.CHAIN_APPROX_NONE)
            if len(contours) > 0:

                c = max(contours, key=cv2.contourArea)

                M = cv2.moments(c)
                if M['m00']==0:
                    continue

                cx = int(M['m10']/M['m00'])

                cy = int(M['m01']/M['m00'])
                list.append(cx-320)
                cv2.putText(i,str(cx),(cx,cy), cv2.FONT_HERSHEY_SIMPLEX, .5,(255,0,0),2,cv2.LINE_AA)
                #cv2.drawContours(color_image, contours, -1, (0,255,0), 1)
                cv2.drawContours(i, contours, -1, (0,255,0), 1)

        sum=0
        for l in list:
            sum=sum+l
        print sum           
        if sum < -20:
            print "Turn Left!"
            GPIO.output(Motor1A,GPIO.LOW)
            GPIO.output(Motor1B,GPIO.LOW)
            left.ChangeDutyCycle(100)
            GPIO.output(Motor2A,GPIO.LOW)
            GPIO.output(Motor2B,GPIO.HIGH)
            right.ChangeDutyCycle(100)
        if sum>=-20 and sum <=20 :

            print "On Track!"
            GPIO.output(Motor1A,GPIO.LOW)
            GPIO.output(Motor1B,GPIO.HIGH)
            left.ChangeDutyCycle(100)
            GPIO.output(Motor2A,GPIO.LOW)
            GPIO.output(Motor2B,GPIO.HIGH)
            right.ChangeDutyCycle(100)

         
        if sum >20:

            print "Turn Right"
            GPIO.output(Motor1A,GPIO.LOW)
            GPIO.output(Motor1B,GPIO.HIGH)
            left.ChangeDutyCycle(100)
            GPIO.output(Motor2A,GPIO.LOW)
            GPIO.output(Motor2B,GPIO.LOW)
            right.ChangeDutyCycle(100)

         

        else:
            print "I don't see the line"
        cv2.line(color_image,(320,0),(320,480),(0,0,255),3)
        cv2.imshow("Video",color_image)
        cv2.waitKey(1)
        #clear the data of the previous frame
        raw_cap.truncate(0)
        #raw_cap.seek(0)
        #increment the frame count
        frame_cnt = frame_cnt + 1
        #if the picam has captured 10 seconds of video leave the loop and stop recording
        #except KeyboardInterrupt:
         #   GPIO.cleanup()
        
        #if frame_cnt>200:
    #	    break
except KeyboardInterrupt:
        GPIO.cleanup()
           



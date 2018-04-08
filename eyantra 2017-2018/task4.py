'''
* Team Id : 931
* Author List : Abhaysheel Anand, Aditya Arora, Bhawana Chhaglani, Milap Sharma
* Filename: <Filename>
* Theme: Planter Bot (PB)
* Functions: blink_led, turnoff_led, shed_blink, blend_transparent, file_handling, overlayCM
* Global Variables: Red, Green, Blue, Listof_colors, Listof_shapes, Colorlist, Colorlist_element, plantation 
'''

from imutils.video import VideoStream
import datetime
import argparse
import imutils
import time
import cv2
import numpy as np
import os
import sys
from picamera import PiCamera
import RPi.GPIO as GPIO
from time import sleep

try:
    global Red
    global Green
    global Blue
    global Listof_colors
    global Listof_shapes
    global Colorlist
    global Colorlist_element
    global plantation
    
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--picamera", type=int, default=-1,
            help="whether or not the Raspberry Pi camera should be used")
    args = vars(ap.parse_args())

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    
    Red=29
    Green=31
    Blue=32

    Listof_colors=["Red", "Green", "Blue"]
    Listof_shapes=["Triangle","Square","Circle"]
    Colorlist = []
    Colorlist_element = 0

    plantation=cv2.imread("Plantation.png", -1)
    
    GPIO.setup(Red,GPIO.OUT)
    GPIO.setup(Green,GPIO.OUT)
    GPIO.setup(Blue,GPIO.OUT)
    GPIO.output(Blue,GPIO.LOW)
    GPIO.output(Red,GPIO.LOW)
    GPIO.output(Green,GPIO.LOW)

    rightled=11
    leftled=13
    topled=7

    GPIO.setup(rightled,GPIO.OUT)
    GPIO.setup(leftled,GPIO.OUT)
    GPIO.setup(topled,GPIO.OUT)
    leftled_pwm = GPIO.PWM(leftled, 100)
    rightled_pwm = GPIO.PWM(rightled, 100)
    topled_pwm = GPIO.PWM(topled, 100)
    rightled_pwm.start(50)
    leftled_pwm.start(50)
    topled_pwm.start(0)
    
    Motor1A = 5
    Motor1B = 3
    Motor1E = 21
    Motor2A = 8
    Motor2B = 10
    Motor2E = 23
    
    GPIO.setup(Motor1A,GPIO.OUT)
    GPIO.setup(Motor1B,GPIO.OUT)
    GPIO.setup(Motor1E,GPIO.OUT)
    GPIO.setup(Motor2A,GPIO.OUT)
    GPIO.setup(Motor2B,GPIO.OUT)
    GPIO.setup(Motor2E,GPIO.OUT)

    left = GPIO.PWM(Motor1E, 100)
    right = GPIO.PWM(Motor2E, 100)
    left.start(0)
    right.start(0)

    plantation=cv2.imread("Plantation.png")

    ZI = 0

    last_error = 0
    rightmotor_basespeed = 13
    leftmotor_basespeed = 13
    kp = 0.15
    kd = 1.1

    vs = VideoStream(usePiCamera=args["picamera"] > 0).start()
    time.sleep(1)
    
##* Function Name: blink_led
##* Input: color (color of the Color Markers), CM (number of Color Markers)
##* Output: -
##* Logic: Accepts color and number of Color Markers, and blinks the RGB-LED according to the color passed, in a loop which runs as many times as the value of CM
##* Example Call: blink_led(Red, 4), where Red is the color and 4 is the number of Color Markers


    def blink_led(color, CM):
        global Red
        global Green
        global Blue
        global Colorlist
        global Colorlist_element
        if color not in Listof_colors:
            pass
        else:
            if color=="Red":
                color=Red
            elif color=="Green":
                color=Green
            elif color=="Blue":
                color=Blue
            while CM>0:
                GPIO.output(color, GPIO.HIGH)
                sleep(1)
                GPIO.output(color, GPIO.LOW)
                sleep(0.25)
                CM=CM-1
            Colorlist.insert(Colorlist_element,color)
            Colorlist_element = Colorlist_element + 1


##* Function Name: turnoff_led
##* Input: color ( color of the Color Markers )
##* Output: -
##* Logic: Takes the color as input and turns off the RGB-LED.
##* Example Call: turnoff_led(Red), where Red is the color.


    def turnoff_led(color):
        global Red
        global Green
        global Blue

        if color not in Listof_colors:
           pass
        else:
            if color=="Red":
                color=Red
            elif color=="Green":
                color=Green
            elif color=="Blue":
                color=Blue
            GPIO.output(color, GPIO.LOW)


##* Function Name: shed_blink
##* Input: -
##* Output: -
##* Logic: Blinks the RGB-LED for 1 second according to the elements of the Colorlist ( used to store the value of color detected at each ZI )
##* Example Call: shed_blink()


    def shed_blink():
        global Colorlist
        global Colorlist_element
        loop_element = 0
        while(loop_element < Colorlist_element):
            GPIO.output(Colorlist[loop_element], GPIO.HIGH)
            sleep(1)
            GPIO.output(Colorlist[loop_element], GPIO.LOW)
##            turnoff_LED(Colorlist[loop_element])
            sleep(0.25)
            loop_element = loop_element +1
    

##* Function Name: blend_transparent
##* Input: face_img ( background image ), overlay_t_img ( image to be overlayed )
##* Output: overlay ( overlayed image )
##* Logic: Returns an overlayed image, converts the background image and overlay image into numpy array and add them to create an overlayed image.
##* Example Call: blend_transparent(background, overlay), where background and overlay are two images

    
    def blend_transparent(face_img, overlay_t_img):
    # Split out the transparency mask from the colour info
        overlay_img = overlay_t_img[:,:,:3] # Grab the BRG planes
        overlay_mask = overlay_t_img[:,:,3]  # And the alpha plane

    # Again calculate the inverse mask
        background_mask = 255 - overlay_mask

    # Turn the masks into three channel, so we can use them as weights
        overlay_mask = cv2.cvtColor(overlay_mask, cv2.COLOR_GRAY2BGR)
        background_mask = cv2.cvtColor(background_mask, cv2.COLOR_GRAY2BGR)

    # Create a masked out face image, and masked out overlay
    # We convert the images to floating point in range 0.0 - 1.0
        face_part = (face_img * (1 / 255.0)) * (background_mask * (1 / 255.0))
        overlay_part = (overlay_img * (1 / 255.0)) * (overlay_mask * (1 / 255.0))

    # And finally just add them together, and rescale it back to an 8bit integer image    
        overlay = np.uint8(cv2.addWeighted(face_part, 255.0, overlay_part, 255.0, 0.0))
        return overlay


##* Function Name: file_handling
##* Input: color ( color of the Color Markers ), shape ( shape of the Color Markers )
##* Output: seedling ( name of the seedling image ) 
##* Logic: Takes shape and color of the Color Marker as the input and by traversing line by line in the csv file ( open mode ), it replaces the character and returns the name of the corresponding seedling. 
##* Example Call: file_handling(Red, Square), where Red is the color and Square is the shape of the Color Markers.


    def file_handling(color,shape):
        if color not in Listof_colors or shape not in Listof_shapes:
            pass
        
        else:
            with open("Input Table.csv") as f:
             for line in f:
                
                if color in line and shape in line:
                     line=line.replace(color,"")
                     line=line.replace(",","")
                     line=line.replace("\n","")
                     line=line.replace(" ","")
                     seedling=line.replace(shape,"")
            return seedling


##* Function Name: overlayCM
##* Input: overlay_image_name ( name of the seedling image ), CM ( number of Color Markers ), ZI ( Number of the planting zone )
##* Output: - 
##* Logic: Takes name of seedling image, reads the image from the folder and overlays it based on static coordinates for a particular Planting Zone on the "Plantation.png" image. 
##* Example Call: overlayCM("carnation.png", 4, 1), where "carnation.png" is the name of the seedling image, 4 is number of CMs, 1 is the count of Zone Indicator


    def overlayCM(overlay_image_name,CM,ZI):
        global plantation
        global overlay
        if overlay_image_name==None:
            pass
        else:
            path = 'Seedlings/'+overlay_image_name
            
            overlay=cv2.imread(path,-1)
            if CM>0:   
                if ZI==1:
                    
                    i=343
                    j=240
                    for k in range(CM):
                        x, y, w, h = i,j,30,30
                        overlay_image = cv2.resize(overlay, (h, w))
                        plantation[y:y + w, x:x + h, :] = blend_transparent(plantation[y:y + w, x:x + h, :], overlay_image)
                        i=i+35    

                if ZI==2:
                    
                    i=115
                    j=209
                    for k in range(CM):
                        if k==2:
                            j=240
                            i=90
                        x, y, w, h = i,j,30,30
                        overlay_image = cv2.resize(overlay, (h, w))
                        plantation[y:y + w, x:x + h, :] = blend_transparent(plantation[y:y + w, x:x + h, :], overlay_image)
                        i=i+35
                        
                if ZI==3:
                    
                    i=238
                    j=179
                    for k in range(CM):
                        if k==2:
                            j=165
                        x, y, w, h = i,j,30,30
                        overlay_image = cv2.resize(overlay, (h, w))
                        plantation[y:y + w, x:x + h, :] = blend_transparent(plantation[y:y + w, x:x + h, :], overlay_image)
                        i=i+35
                        
                if ZI==4:
                    
                    i=499
                    j=187
                    for k in range(CM):
                        x, y, w, h = i,j,30,30
                        overlay_image = cv2.resize(overlay, (h, w))
                        plantation[y:y + w, x:x + h, :] = blend_transparent(plantation[y:y + w, x:x + h, :], overlay_image)
                        i=i+35

            else:
                pass

    while True:
##        print "innn"
        Traversal_feed = vs.read()
        Traversal_feed_resize = imutils.resize(Traversal_feed, width=240, height=180)
        Traversal_feed_crop = Traversal_feed_resize[30:150,20:220]
        Traversal_feed_medianblur = cv2.medianBlur(Traversal_feed_crop,5)
        Traversal_feed_bilateralfilter = cv2.bilateralFilter(Traversal_feed_medianblur,5,1000,1000)
        Traversal_feed_gray = cv2.cvtColor(Traversal_feed_bilateralfilter, cv2.COLOR_BGRA2GRAY)

        InvertedPlane_leftcrop=Traversal_feed_gray[:,120:]
        InvertedPlane_rightcrop=Traversal_feed_gray[:,120:]
        ret, InvertedPlane_leftcrop_thresh = cv2.threshold(InvertedPlane_leftcrop,10,255,cv2.THRESH_BINARY_INV)
        ret, InvertedPlane_rightcrop_thresh = cv2.threshold(InvertedPlane_rightcrop,10,255,cv2.THRESH_BINARY_INV)
        _,InvertedPlane_leftcrop_contours,hierarchy = cv2.findContours(InvertedPlane_leftcrop_thresh, 1, cv2.CHAIN_APPROX_NONE)
        _,InvertedPlane_rightcrop_contours,hierarchy = cv2.findContours(InvertedPlane_rightcrop_thresh, 1, cv2.CHAIN_APPROX_NONE)

        if len(InvertedPlane_leftcrop_contours)>0:
            InvertedPlane_maxcontour_left=max(InvertedPlane_leftcrop_contours, key=cv2.contourArea)
            InvertedPlane_maxcontour_left_area=cv2.contourArea(InvertedPlane_maxcontour_left)
        else:
            InvertedPlane_maxcontour_left_area=0
            
        if len(InvertedPlane_rightcrop_contours)>0:
            InvertedPlane_maxcontour_right=max(InvertedPlane_rightcrop_contours, key=cv2.contourArea)
            InvertedPlane_maxcontour_right_area=cv2.contourArea(InvertedPlane_maxcontour_right)
        else:
            InvertedPlane_maxcontour_right_area=0
        
        if ZI==5:
            Traversal_complete_frame = Traversal_feed_bilateralfilter[30:90,:]
            Traversal_complete_gray = cv2.cvtColor(Traversal_complete_frame, cv2.COLOR_BGRA2GRAY)
            ret, Traversal_complete_thresh = cv2.threshold(Traversal_complete_gray,10,255,cv2.THRESH_BINARY_INV)
            _ ,Traversal_complete_contours ,hierarchy = cv2.findContours(Traversal_complete_thresh, 1, cv2.CHAIN_APPROX_NONE)
            print len(Traversal_complete_contours)
            if len(Traversal_complete_contours)>0:
                Traversal_complete_maxcontour = max(Traversal_complete_contours, key=cv2.contourArea)
            else:
                print "end"
                GPIO.output(Motor1A,GPIO.HIGH)
                GPIO.output(Motor1B,GPIO.LOW)
                left.ChangeDutyCycle(0)
                GPIO.output(Motor2A,GPIO.HIGH)
                GPIO.output(Motor2B,GPIO.LOW)
                right.ChangeDutyCycle(0)
                sleep(0.03)
                GPIO.output(Motor1A,GPIO.HIGH)
                GPIO.output(Motor1B,GPIO.HIGH)
                left.ChangeDutyCycle(0)
                GPIO.output(Motor2A,GPIO.HIGH)
                GPIO.output(Motor2B,GPIO.HIGH)
                right.ChangeDutyCycle(0)
                sleep(0.25)
                shed_blink()
                cv2.imwrite("Plantation.png", plantation)
                break
            
            if cv2.contourArea(Traversal_complete_maxcontour)<100:
                print "end"
                GPIO.output(Motor1A,GPIO.HIGH)
                GPIO.output(Motor1B,GPIO.LOW)
                left.ChangeDutyCycle(0)
                GPIO.output(Motor2A,GPIO.HIGH)
                GPIO.output(Motor2B,GPIO.LOW)
                right.ChangeDutyCycle(0)
                sleep(0.03)
                GPIO.output(Motor1A,GPIO.HIGH)
                GPIO.output(Motor1B,GPIO.HIGH)
                left.ChangeDutyCycle(0)
                GPIO.output(Motor2A,GPIO.HIGH)
                GPIO.output(Motor2B,GPIO.HIGH)
                right.ChangeDutyCycle(0)
                sleep(0.25)
                shed_blink()
                cv2.imwrite("Plantation.png", plantation)
                break
            
            else:
                print "traversalip"
                    
                if cv2.contourArea(InvertedPlane_maxcontour_left)>6000 and cv2.contourArea(InvertedPlane_maxcontour_right)>6000:
                    ret, Traversal_feed_thresh = cv2.threshold(Traversal_feed_gray,10,255,cv2.THRESH_BINARY)
                else:
                    ret, Traversal_feed_thresh = cv2.threshold(Traversal_feed_gray,10,255,cv2.THRESH_BINARY_INV)
                    
                _,Traversal_feed_contours,hierarchy = cv2.findContours(Traversal_feed_thresh, 1, cv2.CHAIN_APPROX_NONE)
                if len(Traversal_feed_contours)>0:
                    print "inverted"
                    Traversal_feed_maxcontour = max(Traversal_feed_contours, key=cv2.contourArea)
                    M=cv2.moments(Traversal_feed_maxcontour)
                    if M['m00']==0:
                        continue
                    cx = int(M['m10']/M['m00'])
                    error = 120-cx
                    derivative = error-last_error
                    pwm = (kp*error)+(kd*derivative)

                    last_error=error
                    
                    if error<0 or error==0:
                        left_fin = -pwm + rightmotor_basespeed
                        right_fin = pwm + leftmotor_basespeed
                        

                    if error>0:
                        right_fin = pwm + rightmotor_basespeed
                        left_fin = -pwm + leftmotor_basespeed
                        
                    if right_fin < 0:
                        right_fin = abs(right_fin)
                        
                    if left_fin < 0:
                        left_fin = abs(left_fin)
                    
                    
                    if right_fin > 40:
                        right_fin = 40
                    
                    if left_fin > 40:
                        left_fin = 40

                    GPIO.output(Motor1A,GPIO.LOW)
                    GPIO.output(Motor1B,GPIO.HIGH)
                    left.ChangeDutyCycle(left_fin+4.6)
                    GPIO.output(Motor2A,GPIO.LOW)
                    GPIO.output(Motor2B,GPIO.HIGH)
                    right.ChangeDutyCycle(right_fin+3.2)
            

            
        else:
            ret, Traversal_feed_thresh = cv2.threshold(Traversal_feed_gray,10,255,cv2.THRESH_BINARY_INV)
            _,Traversal_feed_contours,hierarchy = cv2.findContours(Traversal_feed_thresh, 1, cv2.CHAIN_APPROX_NONE)
            if len(Traversal_feed_contours)>0:
                Traversal_feed_maxcontour = max(Traversal_feed_contours, key=cv2.contourArea)
                
                if cv2.contourArea(Traversal_feed_maxcontour)>7000:

                    print "zi"

                    ZI=ZI+1
                    
                    GPIO.output(Motor1A,GPIO.HIGH)
                    GPIO.output(Motor1B,GPIO.LOW)
                    left.ChangeDutyCycle(0)
                    GPIO.output(Motor2A,GPIO.HIGH)
                    GPIO.output(Motor2B,GPIO.LOW)
                    right.ChangeDutyCycle(0)
                    sleep(0.03)
                    GPIO.output(Motor1A,GPIO.HIGH)
                    GPIO.output(Motor1B,GPIO.HIGH)
                    left.ChangeDutyCycle(0)
                    GPIO.output(Motor2A,GPIO.HIGH)
                    GPIO.output(Motor2B,GPIO.HIGH)
                    right.ChangeDutyCycle(0)
                    sleep(0.25)

                    Correction_frame = vs.read()
                    Correction_frame_resize = imutils.resize(Correction_frame, width=240, height=180)
                    Correction_frame_crop = Correction_frame_resize[150:180,:]
                    Correction_frame_medianblur = cv2.medianBlur(Correction_frame_crop,5)
                    Correction_frame_bilateralfilter = cv2.bilateralFilter(Correction_frame_medianblur,5,1000,1000)
                    Correction_frame_gray = cv2.cvtColor(Correction_frame_bilateralfilter, cv2.COLOR_BGRA2GRAY)
                    ret,Correction_frame_thresh = cv2.threshold(Correction_frame_gray,10,255,cv2.THRESH_BINARY_INV)
                    _,Correction_frame_contours,hierarchy = cv2.findContours(Correction_frame_thresh, 1, cv2.CHAIN_APPROX_NONE)
                    
                    if len(Correction_frame_contours)>0:
                        print "correction"
                        Correction_frame_maxContour=max(Correction_frame_contours, key=cv2.contourArea)
                        M = cv2.moments(Correction_frame_maxContour)
                        if M['m00']==0:
                            continue

                        cx = int(M['m10']/M['m00'])
                        
                        if cx>160:
                            if cx>210:
                                GPIO.output(Motor1A,GPIO.LOW)
                                GPIO.output(Motor1B,GPIO.HIGH)
                                left.ChangeDutyCycle(15)
                                GPIO.output(Motor2A,GPIO.LOW)
                                GPIO.output(Motor2B,GPIO.LOW)
                                right.ChangeDutyCycle(15)
                                sleep(0.4)
                                GPIO.output(Motor1A,GPIO.HIGH)
                                GPIO.output(Motor1B,GPIO.LOW)
                                left.ChangeDutyCycle(0)
                                GPIO.output(Motor2A,GPIO.HIGH)
                                GPIO.output(Motor2B,GPIO.LOW)
                                right.ChangeDutyCycle(0)
                                sleep(0.03)
                                GPIO.output(Motor1A,GPIO.HIGH)
                                GPIO.output(Motor1B,GPIO.HIGH)
                                left.ChangeDutyCycle(0)
                                GPIO.output(Motor2A,GPIO.HIGH)
                                GPIO.output(Motor2B,GPIO.HIGH)
                                right.ChangeDutyCycle(0)
                                sleep(0.25)
                            else:
                                GPIO.output(Motor1A,GPIO.LOW)
                                GPIO.output(Motor1B,GPIO.HIGH)
                                left.ChangeDutyCycle(15)
                                GPIO.output(Motor2A,GPIO.LOW)
                                GPIO.output(Motor2B,GPIO.LOW)
                                right.ChangeDutyCycle(15)
                                sleep(0.2)
                                GPIO.output(Motor1A,GPIO.HIGH)
                                GPIO.output(Motor1B,GPIO.LOW)
                                left.ChangeDutyCycle(0)
                                GPIO.output(Motor2A,GPIO.HIGH)
                                GPIO.output(Motor2B,GPIO.LOW)
                                right.ChangeDutyCycle(0)
                                sleep(0.03)
                                GPIO.output(Motor1A,GPIO.HIGH)
                                GPIO.output(Motor1B,GPIO.HIGH)
                                left.ChangeDutyCycle(0)
                                GPIO.output(Motor2A,GPIO.HIGH)
                                GPIO.output(Motor2B,GPIO.HIGH)
                                right.ChangeDutyCycle(0)
                                sleep(0.25)
                        elif cx<80:
                            if cx<30:
                                GPIO.output(Motor1A,GPIO.LOW)
                                GPIO.output(Motor1B,GPIO.LOW)
                                left.ChangeDutyCycle(15)
                                GPIO.output(Motor2A,GPIO.LOW)
                                GPIO.output(Motor2B,GPIO.HIGH)
                                right.ChangeDutyCycle(15)
                                sleep(0.4)
                                GPIO.output(Motor1A,GPIO.HIGH)
                                GPIO.output(Motor1B,GPIO.LOW)
                                left.ChangeDutyCycle(0)
                                GPIO.output(Motor2A,GPIO.HIGH)
                                GPIO.output(Motor2B,GPIO.LOW)
                                right.ChangeDutyCycle(0)
                                sleep(0.03)
                                GPIO.output(Motor1A,GPIO.HIGH)
                                GPIO.output(Motor1B,GPIO.HIGH)
                                left.ChangeDutyCycle(0)
                                GPIO.output(Motor2A,GPIO.HIGH)
                                GPIO.output(Motor2B,GPIO.HIGH)
                                right.ChangeDutyCycle(0)
                                sleep(0.25)
                            else:
                                GPIO.output(Motor1A,GPIO.LOW)
                                GPIO.output(Motor1B,GPIO.LOW)
                                left.ChangeDutyCycle(15)
                                GPIO.output(Motor2A,GPIO.LOW)
                                GPIO.output(Motor2B,GPIO.HIGH)
                                right.ChangeDutyCycle(15)
                                sleep(0.2)
                                GPIO.output(Motor1A,GPIO.HIGH)
                                GPIO.output(Motor1B,GPIO.LOW)
                                left.ChangeDutyCycle(0)
                                GPIO.output(Motor2A,GPIO.HIGH)
                                GPIO.output(Motor2B,GPIO.LOW)
                                right.ChangeDutyCycle(0)
                                sleep(0.03)
                                GPIO.output(Motor1A,GPIO.HIGH)
                                GPIO.output(Motor1B,GPIO.HIGH)
                                left.ChangeDutyCycle(0)
                                GPIO.output(Motor2A,GPIO.HIGH)
                                GPIO.output(Motor2B,GPIO.HIGH)
                                right.ChangeDutyCycle(0)
                                sleep(0.25)
                                
                    topled_pwm.ChangeDutyCycle(50)

                    ColorMarker_frame = vs.read()
                    ColorMarker_frame_resize = imutils.resize(ColorMarker_frame, width=1280, height=720)
                    ColorMarker_frame_crop = ColorMarker_frame_resize[:,120:1160]
                    ColorMarker_frame_hsv = cv2.cvtColor(ColorMarker_frame_crop,cv2.COLOR_BGR2HSV)
                    ColorMarker_frame_medianblur = cv2.medianBlur(ColorMarker_frame_hsv,5)
                    ColorMarker_frame_bilateralfilter = cv2.bilateralFilter(ColorMarker_frame_medianblur,5,1000,1000)
                    ColorMarker_frame_gray = cv2.cvtColor(ColorMarker_frame_bilateralfilter, cv2.COLOR_BGRA2GRAY)
                    ret,ColorMarker_frame_thresh = cv2.threshold(ColorMarker_frame_gray,125,255,cv2.THRESH_BINARY_INV)
                    _,ColorMarker_frame_contours,hierarchy = cv2.findContours(ColorMarker_frame_thresh, 1, cv2.CHAIN_APPROX_NONE)

                    loop_variable=0
                    colorof_CM=None
                    shapeof_CM=None
                    CM=0
                    
                    for cnt in ColorMarker_frame_contours:
                        if cv2.contourArea(cnt)>20000 or cv2.contourArea(cnt)<1000:
                            pass
                        else:
                            print "cm"
                            loop_variable=loop_variable+1
                            (x,y),radius = cv2.minEnclosingCircle(cnt)
                            center = (int(x), int(y))
                            radius = int(radius)
                            if (radius < 70) and (radius > 40):
                                shapeof_CM = "Circle"
                                approx = cv2.approxPolyDP(cnt, 0.1 * cv2.arcLength(cnt, True), True)
                                M = cv2.moments(cnt)
                                if M['m00']==0:
                                            continue

                                cx = int(M['m10']/M['m00'])

                                cy = int(M['m01']/M['m00'])
                                
                                color=ColorMarker_frame_hsv[cy,cx]
                                
                                if color[0]>55 and color[0]<90:
                                    if color[1]>20 and color[1]<50:
                                        if color[2]>125 and color[2]<140:
                                            colorof_CM="Red"
                                            
                                        elif color[2]>116 and color[2]<123:
                                            colorof_CM="Green"

                                        else:
                                            colorof_CM="Blue"
                                sides = len(approx)
                                if (sides == 3):
                                    shapeof_CM = "Triangle"
                                else:
                                    if(radius > 49):
                                        shapeof_CM = "Square"

                    CM = loop_variable
                    ######################################################################
                    CM=4
                    colorof_CM="Green"
                    shapeof_CM="Square"
                    ######################################################################
                    print CM, shapeof_CM, colorof_CM
                    
                    nameof_seedling = file_handling(colorof_CM, shapeof_CM)
                    
                    nameof_seedling=nameof_seedling[:len(nameof_seedling)-1]
                    print nameof_seedling
                    if nameof_seedling=="tulipblue.png":
                        print "huraaah"
                    overlayCM(nameof_seedling, CM, ZI)
                    blink_led(colorof_CM, CM)

                    topled_pwm.ChangeDutyCycle(0)

                    while True:
                        print "skip"
                        SkipZI_frame = vs.read()
                        SkipZI_frame_resize = imutils.resize(SkipZI_frame, width=240, height=180)
                        SkipZI_frame_crop = SkipZI_frame_resize[30:150,20:220]
                        SkipZI_frame_medianBlur = cv2.medianBlur(SkipZI_frame_crop,5)
                        SkipZI_frame_bilateralfilter = cv2.bilateralFilter(SkipZI_frame_medianBlur,5,1000,1000)
                        SkipZI_frame_gray = cv2.cvtColor(SkipZI_frame_bilateralfilter, cv2.COLOR_BGRA2GRAY)
                        ret,SkipZI_frame_thresh = cv2.threshold(SkipZI_frame_gray,5,255,cv2.THRESH_BINARY_INV)
                        _,SkipZI_frame_contours,hierarchy = cv2.findContours(SkipZI_frame_thresh, 1, cv2.CHAIN_APPROX_NONE)
                        
                        if len(SkipZI_frame_contours)>0:
                            SkipZI_frame_maxContour=max(SkipZI_frame_contours, key=cv2.contourArea)
                            SkipZI_frame_maxContour=cv2.contourArea(SkipZI_frame_maxContour)
                        else:
                            SkipZI_frame_maxContour=6000
                            
                        if SkipZI_frame_maxContour>5999:
                            GPIO.output(Motor1A,GPIO.LOW)
                            GPIO.output(Motor1B,GPIO.HIGH)
                            left.ChangeDutyCycle(20)
                            GPIO.output(Motor2A,GPIO.LOW)
                            GPIO.output(Motor2B,GPIO.HIGH)
                            right.ChangeDutyCycle(20)
                        else:
                            break

                else:
                    print "traversal"
                    M=cv2.moments(Traversal_feed_maxcontour)
                    if M['m00']==0:
                        continue
                    cx = int(M['m10']/M['m00'])
                    error = 120-cx
                    derivative = error-last_error
                    pwm = (kp*error)+(kd*derivative)

                    last_error=error
                    
                    if error<0 or error==0:
                        left_fin = -pwm + rightmotor_basespeed
                        right_fin = pwm + leftmotor_basespeed

                    if error>0:
                        right_fin = pwm + rightmotor_basespeed
                        left_fin = -pwm + leftmotor_basespeed
                        
                    if right_fin < 0:
                        right_fin = abs(right_fin)
                        
                    if left_fin < 0:
                        left_fin = abs(left_fin)
                    
                    
                    if right_fin > 40:
                        right_fin = 40
                    
                    if left_fin > 40:
                        left_fin = 40

                    GPIO.output(Motor1A,GPIO.LOW)
                    GPIO.output(Motor1B,GPIO.HIGH)
                    left.ChangeDutyCycle(left_fin+4.6)
                    GPIO.output(Motor2A,GPIO.LOW)
                    GPIO.output(Motor2B,GPIO.HIGH)
                    right.ChangeDutyCycle(right_fin+3.2)
            else:
                continue

        cv2.imshow("Plantation", plantation)
        cv2.waitKey(1)
    
except KeyboardInterrupt:

    cv2.destroyAllWindows()
    vs.stop()
    sys.exit()

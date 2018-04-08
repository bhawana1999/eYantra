############################################################################
#									   #
#	    Overlaying of images and video processing	   #
#									   #
############################################################################

########################################################################################
#                                                                                      #
# Team Id           eYRC_931                                                           #
# Author List       Abhaysheel Anand, Aditya Arora, Bhawana Chhaglani, Milap Sharma    #
# Filename          Task-1B_main.py                                                    #
# Theme             Planter Bot                                                        #
# Fuctions          writecsv, main                                                     #
#                                                                                      #
########################################################################################

#classes and subclasses to import
import cv2
import numpy as np
import os
import time
import datetime

filename = 'results1B_teamid.csv'
#################################################################################################
# DO NOT EDIT!!!
#################################################################################################
#subroutine to write results to a csv
def writecsv(color,shape,(cx,cy)):
    global filename
    #open csv file in append mode
    filep = open(filename,'a')
    # create string data to write per image
    datastr = "," + color + "-" + shape + "-" + str(cx) + "-" + str(cy)
    #write to csv
    filep.write(datastr)

#################################################################################################
# DO NOT EDIT!!!
#################################################################################################
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
    return np.uint8(cv2.addWeighted(face_part, 255.0, overlay_part, 255.0, 0.0))


def main(video_file_with_path):
    list=[]
    cap = cv2.VideoCapture(video_file_with_path) #capturing video
    print cap.isOpened()
    print cap.get(cv2.CAP_PROP_FPS)

    image_red = cv2.imread("yellow_flower.png",-1)                                                                                          #reading the image
    image_blue = cv2.imread("pink_flower.png",-1)                                                                                           #reading the image
    image_green = cv2.imread("red_flower.png",-1)                                                                                           #reading the image
    rval, frame=cap.read()                                                                                                                  #capturing frames
    count = 0
    start_time = datetime.datetime.now()


    while rval:
        rval, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray, 127, 255, 1)
        _, contours, hierarchy = cv2.findContours(thresh, 1, 2)
        print len(contours)
        i=0
        for cnt in contours:
            i=i+1

            approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)                                                            # finding the vertices
            if len(approx) == 5:                                                                                                             # logic for pentagon
                shape = "pentagon"                                                                                                           # #
                                                                                                                                            #
                                                                                                                                           #
            elif len(approx) == 3:                                                                                                          # logic for triangle
                shape = "triangle"                                                                                                          #
                                                                                                                                            #
            elif len(approx) == 4:                                                                                                              # logic for shape with 4 edges
                slope1 = (approx[1][0][1] - approx[0][0][1]) / (approx[1][0][0] - approx[0][0][0])  #
                slope2 = (approx[2][0][1] - approx[1][0][1]) / (approx[2][0][0] - approx[1][0][0])  #
                slope3 = (approx[3][0][1] - approx[2][0][1]) / (approx[3][0][0] - approx[2][0][0])  #
                slope4 = (approx[3][0][1] - approx[0][0][1]) / (approx[3][0][0] - approx[0][0][0])  #
                slope = []
                c = 0
                slope.append(slope1)
                slope.append(slope2)
                slope.append(slope3)
                slope.append(slope4)

                for s in slope:
                    if s < 0:
                        c = c + 1
                if c == 1:                                                                              # for trapezium
                    shape = "trapezium"
                else:                                                                                    # for square
                    shape = "rhombus"                                                                        #
                                                                                                                          #
            elif len(approx) == 6:                                                                          #
                shape = "hexagon"                                                                        # logic for hexagon
                                                                                                                        #
            elif len(approx) > 15:                                                                          # logic for circle
                shape = "circle"
            M = cv2.moments(cnt)
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            # print "Centroid = ", cx, ", ", cy
            color = frame[cy, cx]                                                                   # finding color of the object buy detecting the color at its centroid
            if (color[0] >= 0 and color[0] <= 10 and color[1] >= 0 and color[1] <= 10 and color[2] >= 250 and color[2] <= 255):  # logic for red
                colour = "red"  #
            elif (color[0] >= 250 and color[0] <= 255 and color[1] >= 0 and color[1] <= 10 and color[2] >= 0 and color[2] <= 10):  # logic for blue
                colour = "blue"  #
            elif (color[0] >= 0 and color[0] <= 10 and color[1] >= 120 and color[1] <= 130 and color[2] >= 0 and color[2] <= 10):  # logic for green
                colour = "green"
            a=len(list)
            if cx not in list and cx+2 not in list and cx+1 not in list and cx-1 not in list and cx-2 not in list:
                list.append(i)
                list.append(colour)
                list.append(cx)


                writecsv(colour, shape, (cx, cy))
        if len(contours)>0:
            if (list[3 * (len(contours) - 1) + 1] == "red"):

                x, y, w, h = cv2.boundingRect(contours[list[3 * (len(contours) - 1) ]-1])
                overlay_image = cv2.resize(image_red, (h, w))

                frame[y:y + w, x:x + h, :] = blend_transparent(frame[y:y + w, x:x + h, :], overlay_image)


            elif (list[3 * (len(contours) - 1) + 1] == "blue"):

                x, y, w, h = cv2.boundingRect(contours[list[3 * (len(contours) - 1) ]-1])
                overlay_image = cv2.resize(image_blue, (h, w))

                frame[y:y + w, x:x + h, :] = blend_transparent(frame[y:y + w, x:x + h, :], overlay_image)


            elif (list[3 * (len(contours) - 1) + 1] == "green"):

                x, y, w, h = cv2.boundingRect(contours[list[3 * (len(contours) - 1) ]-1])
                overlay_image = cv2.resize(image_green, (h, w))

                frame[y:y + w, x:x + h, :] = blend_transparent(frame[y:y + w, x:x + h, :], overlay_image)
        cv2.imshow("output_video", frame)
        cv2.waitKey(40)

    cap.release()
    end_time = datetime.datetime.now()
    tp = end_time - start_time
    print tp
    cv2.destroyAllWindows()




                #####################################################################################################
    #Write your code here!!!
#####################################################################################################

#####################################################################################################
    #sample of overlay code for each frame
    #x,y,w,h = cv2.boundingRect(current_contour)
    #overlay_image = cv2.resize(image_red,(h,w))
    #frame[y:y+w,x:x+h,:] = blend_transparent(frame[y:y+w,x:x+h,:], overlay_image)
#######################################################################################################

#################################################################################################
# DO NOT EDIT!!!
#################################################################################################
#main where the path is set for the directory containing the test images
if __name__ == "__main__":
    main('./Video.mp4')

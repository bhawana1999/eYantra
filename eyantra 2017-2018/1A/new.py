import numpy as np
import cv2
list=[]
red = [0, 0, 255]
blue = [255, 0, 0]
green = [0, 128, 0]
img_name="test5.png"
list.append(img_name)
img = cv2.imread(img_name, cv2.IMREAD_COLOR)
h, w, c = img.shape
area = (h - 3) * (w - 3)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(gray, 127, 255, 1)
_, contours, hierarchy = cv2.findContours(thresh, 1, 2)
print len(contours)
for cnt in contours:
    approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
    if len(approx) == 5:
        shape="pentagon"


    elif len(approx) == 3:
        shape="triangle"

    elif len(approx) == 4:
        slope1 = (approx[1][0][1] - approx[0][0][1]) / (approx[1][0][0] - approx[0][0][0])
        slope2 = (approx[2][0][1] - approx[1][0][1]) / (approx[2][0][0] - approx[1][0][0])
        slope3 = (approx[3][0][1] - approx[2][0][1]) / (approx[3][0][0] - approx[2][0][0])
        slope4 = (approx[3][0][1] - approx[0][0][1]) / (approx[3][0][0] - approx[0][0][0])
        # print slope1, slope2, slope3, slope4
        slope = []
        c = 0
        slope.append(slope1)
        slope.append(slope2)
        slope.append(slope3)
        slope.append(slope4)

        for s in slope:
            if s < 0:
                c = c + 1
        if c == 1:
            shape="trapezium"
        else:
            shape="rhombus"


    elif len(approx) == 6:
        shape="hexagon"

    elif len(approx) > 15:
        shape="circle"


    M = cv2.moments(cnt)
    cx = int(M['m10'] / M['m00'])
    cy = int(M['m01'] / M['m00'])
    #print "Centroid = ", cx, ", ", cy
    color = img[cy, cx]
    if (color[0] == 0 and color[1] == 0 and color[2] == 255):
        color="red"
    elif (color[0] == 255 and color[1] == 0 and color[2] == 0):
        color="blue"
    elif (color[0] == 0 and color[1] == 128 and color[2] == 0):
        color="green"
    font = cv2.FONT_HERSHEY_SIMPLEX

    cv2.putText(img, color, (cx-40,cy-40), font, 0.5, (0, 0,0), 1, cv2.LINE_AA)
    cv2.putText(img, shape, (cx - 20, cy - 20), font, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
    cv2.putText(img, "("+str(cx)+","+str(cy)+")", (cx , cy ), font, 0.5, (0, 0, 0), 1, cv2.LINE_AA)

    element=color+"-"+shape+"-"+str(cx)+"-"+str(cy)
   # print element
    list.append(element)

print list
cv2.imshow("image", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
filep=open('result.csv', 'a')
filep.write(str(list))
filep.close()
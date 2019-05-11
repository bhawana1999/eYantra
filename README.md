# eYantra

A bot that follows black line on a white surface using video analytics and image processing. A raspberry pi and camera is placed on the bot for this purpose. Multi-threading concept was used  to increase the frame rate from pi-cam.

![alt text](https://github.com/sona-19/eYantra/blob/master/Selection_007.png)

The robot will traverse the field represented by the arena using image processing. Raspberry Pi and PiCamera are used to serve the purpose. The frame captured by the PiCam is divided into four equal parts horizontally. The four parts are stored in the array. Then each element of the array is processed by the image processing algorithm.
● First of all, contour with maximum area is identified in the element and its centroid is detected.
● Then the shift between the midpoint of element and the centroid of the contour with maximum area helps us to identify the direction and the intensity of the turn. For this a vertical line in the middle of the frame is drawn. The distances between the centroid of all the 4 contours of the image-parts and the middle line is calculated. If the centroid is in the left, then its distance is taken to be negative and if the centroid lies to the right of the middle line, then its distance is taken to be positive. The sum of all the four distances is calculated. The sign of the sum gives us the direction and the magnitude of the sum gives the intensity of the turn .


<img src="https://github.com/sona-19/eYantra/blob/master/eyantra%202017-2018/pic.PNG" width = 300>
<img src = "https://github.com/sona-19/eYantra/blob/master/Selection_009.png" width = 300>
The bot also detects the coloured markers in the run :- their shape, color and number and overlays the corresponding image on the overlay image as shown:

![alt text](https://github.com/sona-19/eYantra/blob/master/eyantra%202017-2018/overlay.PNG)

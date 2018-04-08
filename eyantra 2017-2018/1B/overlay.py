import cv2
import numpy as np

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
img=cv2.imread("rhombus.png",-1)
img2=cv2.imread("yellow_flower.png",-1)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)                                                                                      #converting from BGR to GRAY
ret, thresh = cv2.threshold(gray, 127, 255, 1)                                                                                      #setting threshold for finding contours
_, contours, hierarchy = cv2.findContours(thresh, 1, 2)
for cnt in contours:
    x, y, w, h = cv2.boundingRect(cnt)
    overlay_image = cv2.resize(img2,(h,w))
    img[y:y+w,x:x+h,:] = blend_transparent(img[y:y+w,x:x+h,:], overlay_image)
cv2.imshow("image",img)
cv2.waitKey(0)
cv2.destroyAllWindows()



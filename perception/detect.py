import cv2
import numpy as np
import os 

# ------------------------------------------------------------------------

# This is just boring stuff like reading the image and getting the height
# and width. We also convert it to the HSV color format to help with the mask

# just a bit of directory work to make this more reliable 
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

img = cv2.imread(os.path.join(__location__, 'red.png'))
dimensions = img.shape
height =  int(img.shape[0])
width =  int(img.shape[1])

# convert img to correct color type for masking
hsvImg = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# ------------------------------------------------------------------------

# The next section of code masks out everything that is not an orange color
# This is so we can detect where the cones are based upon their color
# I think that they are too small to detect by shape 

#   HSV cheatsheet       hue, sat, value
lower_bound = np.array([100.0, 90, 90])   
upper_bound = np.array([300.0, 255, 255])

#pass hsv image to a masking function
mask = cv2.inRange(hsvImg, lower_bound, upper_bound)

#noise removal (not sure how this works?)
kernel = np.ones((7,7),np.uint8)
mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel) #removes black noise
mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel) #removes white noise

# ------------------------------------------------------------------------


# This next segment of code gives the program a FOV, I added this to focus the 
# vision on the middle of the image, instead of detecting things far away
# that might not be relevent to the navigation tasks. It also does a bit of blur

#create temp mask filled with nothing
temp_mask = np.zeros(mask.shape[:2], dtype="uint8")

#make that mask a circle
cv2.circle(temp_mask, (int((width/2)), int((height/2))), int((width - width/2)), 255, -1)

#apply that circle mask to our orginal mask with an and operation
mask = cv2.bitwise_and(mask, mask, mask=temp_mask)
mask = cv2.GaussianBlur(mask,(5,5),0)


# ------------------------------------------------------------------------


# Countours are found from the previous mask... 

contours, hierarchy = cv2.findContours(image=mask, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)


# -----------------------------------------------------------------------

# Create an array of the centers of each countour, to find the center of
# each cone on screen. Then, order that list based on the x value so that
# we can draw the lines from bottom to top, and not randomly

arrayOfCenters = []

for c in contours:
    # compute the center of the contour... this is math magic to me!
    M = cv2.moments(c)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    arrayOfCenters.append((cX, cY))

arrayOfCenters = sorted(arrayOfCenters, key=lambda tup: tup[0])


# ------------------------------------------------------------------------

# Loop through the array of centers and draw a line connecting each one.
# Unless they are too far apart, in which was, just skip over it. This is
# done in order to not connect the bottom and top points, so we avoid
# creating a rectangle, and instead have two lines. Then the output is drawn
# to the final image, in order to be displayed !

currentpoint = 0
length = len(arrayOfCenters)

while currentpoint < length - 1:
    # 300 is kind of arbitrarily defined here... not so good...
    if (abs(arrayOfCenters[currentpoint + 1][0] - arrayOfCenters[currentpoint][0])) > 300:
        pass 
    else:
        #draw the line here
        cv2.line(img, arrayOfCenters[currentpoint], arrayOfCenters[currentpoint + 1], (52,52,225), thickness=9)
    currentpoint += 1  

# saving the output

cv2.imwrite(os.path.join(__location__, 'answer.png'), img)



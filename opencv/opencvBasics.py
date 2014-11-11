# Here we will go over the basics of using OpenCV and Python

# 'import' imports libraries
# 'as' gives the library an alias so you don't have to type the entire name
import cv2 # base opencv libraries
import cv2.cv as cv # other cv libraries that are sometimes needed
import numpy as np # python library for matlab like functions

# set the image path here so it is easier to modify
img_dir = 'Images\\'
img_base = 'irRemote'
img_ext = '.jpg'

####
# Here we will read an image as rgb
# Note that OpenCV stores rgb files in bgr order
# So the channels are: [:,:,0] is blue, [:,:,1] is green, [:,:,2] is red
####

# cv2.imread('image_file_path',image_type)
# Options: IMREAD_COLOR for RGB, IMREAD_UNCHANGED for RGBA, IMREAD_GRAYSCALE
# Or: 1, -1, 0
# Note: + is used for string concatenation
img = cv2.imread(img_dir+img_base+img_ext,cv2.IMREAD_GRAYSCALE)

####
# Now let's look at a few stats about the image
####

print img.dtype # image data type, good for debugging
print img.size # number of pixels
print img.shape # rows, columns, channels

####
# Now let's open the image in a window
####

# cv2.imshow('window_name',image_file)
cv2.imshow('image',img)
# how long the window should stay open
# 0 means it will wait until a key is pressed
cv2.waitKey(0)
# closes all windows
cv2.destroyAllWindows()

####
# Now let's write the image to a file
####

cv2.imwrite(img_dir+'\\output'+img_base+'_grascale'+img_ext,img)

###
# Let's try some video capture
# We'll just use the camera on your computer
# Note: Close the image window before doing the following section
###

# 0 means the first available camera that is attached
# Others would follow 1,2,3,...
cap = cv2.VideoCapture(0)
cap.open(0)

# if you want to use a file, just put the file name in instead of a number:
# vid_file = 'videos\\IR_DARK_FILTERED.mp4'
# cap = cv2.VideoCapture(vid_file)
# cap.open(vid_file)

# infinite loop, basically: open until you press q
while(cap.isOpened()):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    # cvt2.cvtColor() is to convert the image from one color format to another
    # Here we convert the color image to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    cv2.imshow('frame',gray)
    # Exit condition
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

# Still need to close the window to move forward, so press 'q'
# If you get an error such as the following:
#   OpenCV Error: Assertion failed (scn == 3 || scn == 4) blah blah
# Then you need to add this underneath cap = cv2.VideoCapture(0):
#   cap.open(0)
# Also, Note: Built-in Webcams are glitchy, so this may not work at all
#   better to use another camera or video source

####
# Now let's do some more interesting image manipulation with some IR images
# Goal is to read an image of IR LEDs
# And identify the number of LEDs seen
####

# read the image (there are 4)
img_directory = 'Images\\'
img_base = 'irImg'
img_extension = '.jpg'

# list to hold our images
images = []
# add images to array
# Note: They have numerical indexed file names

for i in range(1,5):
  images.append(cv2.imread(img_directory+img_base+str(i)+
                img_extension,cv2.IMREAD_GRAYSCALE))

# create result image base
dst = images[0]
# blend each image in list into dst
# cv2.addWeighted(firstImage,alpha,secondImage,beta,gamma)
for i in range(1,4):
  dst = cv2.addWeighted(dst,1,images[i],1,0)

# get the number of rows and columns, might be helpful to know how
rows,cols = dst.shape

# use Hough Circles algorithm to find the IR lights, which are circular
# see http://docs.opencv.org/modules/imgproc/doc/feature_detection.html for
#   documentation on Hough Circle Transform
# finds circles and returns a vector with 3 values for each circle (x,y,radius)
circles = cv2.HoughCircles(dst,cv.CV_HOUGH_GRADIENT,1,rows/8,
                            param1=100,param2=15,minRadius=0,maxRadius=0)

# number of circles, wont' actually use but good to see
print circles.size/3

# draw the circles on the image
circles = np.uint16(np.around(circles))
for i in circles[0,:]:
    # draw the outer circle
    cv2.circle(dst,(i[0],i[1]),i[2],(0,255,0),2)
    # draw the center of the circle
    cv2.circle(dst,(i[0],i[1]),2,(0,0,255),3)

# write to file
cv2.imwrite(img_directory+'\\output'+img_base+'_circles'+img_extension,dst)

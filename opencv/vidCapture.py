import numpy as np
import cv2
import cv2.cv as cv

def findCircles(img):
    """Find circles in an image"""
    # blur the image first to reduce noise
    blur = cv2.GaussianBlur(img, (9,9), 0)
    # calculate threshold
    ret,thresh = cv2.threshold(blur, 127, 255, cv2.THRESH_BINARY)
    # find circles
    rows,cols = thresh.shape
    circles = cv2.HoughCircles(thresh, cv.CV_HOUGH_GRADIENT, 1, rows/8,
                               param1=200, param2=100, minRadius=0,
                               maxRadius=0)
    return circles

def drawCircles(img, circles):
    """Draw the circles on an image after circle detection"""
    for i in circles[0,:]:
        # draw the outer circle
        cv2.circle(img, (i[0],i[1]), i[2], (0,255,0), 2)
        # draw the center of the circle
        cv2.circle(img, (i[0],i[1]), 2, (0,0,255), 3)
    return img

vid_file = 'Videos\\IR_DARK_FILTERED.mp4'
cap = cv2.VideoCapture(vid_file)    # the capture
cap.open(vid_file)  # doesn't always open automatically

# fourcc = cv.CV_FOURCC(*'XVID')
# out = cv2.VideoWriter('Videos\\output.avi',fourcc, 20.0, (1920,1080))

while(cap.isOpened()):
    # ret is a boolean that lets us know if anything was returned
    ret, frame = cap.read()
    if ret==True:
        # if a frame was returned; make frame grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        circles = findCircles(gray)
        # draw circles
        if type(circles) is np.ndarray:
            # if any LEDs detected, they will be of data type numpy.ndarray
            circles = np.uint16(np.around(circles))
            gray = drawCircles(gray, circles)
        # Show when a circle was detected and where so that we can adjust the
        # param1 and param2 of HoughCircles as needed.
        cv2.imshow('frames', gray)
        # slow down the video playback
        cv2.waitKey(10)
        # lets us quit the video early
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        # out.write(gray)
    else:
        break

# When everything done, release the capture
cap.release()
# out.release()
cv2.destroyAllWindows()




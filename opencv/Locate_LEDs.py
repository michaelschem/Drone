import numpy as np
import cv2
import cv2.cv as cv

vid_file = 'Videos\\IR_DARK_FILTERED.mp4'
cap = cv2.VideoCapture(vid_file)    # the capture
cap.open(vid_file)  # doesn't always open automatically
frame_count = 0
frames_total = int(cap.get(cv.CV_CAP_PROP_FRAME_COUNT))
fps = int(cap.get(cv.CV_CAP_PROP_FPS))
frame_width = cap.get(cv.CV_CAP_PROP_FRAME_WIDTH)
lefty = [0] * frames_total # keep track of when the left light is seen
righty = [0] * frames_total # keep track of when the right light is seen
led_centers = []
one = two = zero = 0
print 'FPS: '+str(fps)+'\n'
print 'Total Frames: '+str(frames_total)+'\n\n'

"""Find LEDs"""

while(cap.isOpened()):
    # success is a boolean that lets us know if anything was returned
    success, frame = cap.read()
    if success is True:
        frame_count += 1
        # if a frame was returned; make frame grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # blur the image first to reduce noise
        blur = cv2.GaussianBlur(gray, (3,3), 0)
        # calculate threshold (make it a pure black and white image)
        ret_,thresh = cv2.threshold(blur, 60, 255, cv2.THRESH_BINARY)
        # find contours (LEDs)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE,
                                               cv2.CHAIN_APPROX_SIMPLE)
        centers = []
        radii = []
        num_contours = len(contours)
        for cntr in contours:
            (x,y),radius = cv2.minEnclosingCircle(cntr)
            centers.append((int(x),int(y)))
            led_centers.append((int(x),int(y),num_contours))
            radii.append(int(radius))
        if num_contours == 1:
            one += 1
        elif num_contours == 2:
            two += 1
        else:
            zero += 1
        # draw circles around LEDs in image
        size = len(centers)
        for i in range(0,size):
            cv2.circle(frame,centers[i],radii[i],(255,255,255),2)
        cv2.imshow('frames', frame)
        # # slow down the video playback
        # cv2.waitKey(10)
        # lets us quit the video early
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# When everything done, release the capture
cap.release()
# out.release()
cv2.destroyAllWindows()

"""Determine how often each LED was seen"""

# num_centers = len(led_centers)
# for center in range(0,num_centers):
#     if led_centers[center][2] == 1:

lefty_freq = 0
righty_freq = 0

for i in range(0,frames_total):
    if lefty[i] == 1:
        lefty_freq += 1
    if righty[i] == 1:
        righty_freq += 1

print "Two frequency: "+str(two)+"\n"
print "One frequency: "+str(one)+"\n"
print "Zero frequency: "+str(zero)+"\n"

# lefty_freq = (float(lefty_freq)/float(frames_total)) * 100.0
# righty_freq = (float(righty_freq)/float(frames_total)) * 100.0

two = (float(two)/float(frames_total)) * 100.0
one = (float(one)/float(frames_total)) * 100.0
zero = (float(zero)/float(frames_total)) * 100.0

# lefty_freq = float(lefty_freq/frames_total) * 100.0
# righty_freq = float(righty_freq/frames_total) * 100.0

print "Two frequency: "+str(two)+"\n"
print "One frequency: "+str(one)+"\n"
print "Zero frequency: "+str(zero)+"\n"

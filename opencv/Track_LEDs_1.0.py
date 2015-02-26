import numpy as np
import cv2
import cv2.cv as cv

vid_file = 'Videos\\IR_DARK_FILTERED.mp4'
cap = cv2.VideoCapture(vid_file)    # the capture
cap.open(vid_file)  # use because vid doesn't always open automatically
LED_both_locations = []
# We know that there are only x number of LEDs
LED_1_locations = []
LED_2_locations = []

frames_total = int(cap.get(cv.CV_CAP_PROP_FRAME_COUNT))
frame_num = 0
frame_width = cap.get(cv.CV_CAP_PROP_FRAME_WIDTH)
frame_height = cap.get(cv.CV_CAP_PROP_FRAME_HEIGHT)
# print "total frames" + str(frames_total)

"""Track LEDs in Frame"""

while(cap.isOpened()):
    # success is a boolean that lets us know if anything was returned
    success, frame = cap.read()
    if success is True:
        frame_num+=1
        # if a frame was returned; make frame grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # blur the image first to reduce noise
        blur = cv2.GaussianBlur(gray, (3,3), 0)
        # calculate threshold (make it a pure black and white image)
        ret_,thresh = cv2.threshold(blur, 60, 255, cv2.THRESH_BINARY)
        # find contours (LEDs)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE,
                                               cv2.CHAIN_APPROX_SIMPLE)
        # store (x,y) of the center of the led
        centers = []
        for cntr in contours:
            (x,y),radius = cv2.minEnclosingCircle(cntr)
            centers.append((int(x),int(y)))
        # draw circles around LEDs in image, set radius to a fixed size: 10
        size = len(centers)
        for i in range(0,size):
            # cv2.circle(frame,centers[i],radii[i],(255,255,255),2)
            cv2.circle(frame,centers[i],10,(255,255,255),2)
            # Storing:
            #   (center coords of LED, which frame,
            #       which LED in frame, num LEDs seen in frame)
            LED_both_locations.append((centers[i],frame_num,i+1,size))
        cv2.imshow('frames', frame)
        # # slow down the video playback
        # cv2.waitKey(1)
        # lets us quit the video early
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

cv2.destroyAllWindows()
cap.release()

size = len(LED_both_locations)
# print "size" + str(size)

for i in range(0,size):
    # if LEDs[i][1] is LEDs[i-1][1] or LEDs[i][1] is LEDs[i+1][1]:
    center = LED_both_locations[i][0]
    frame_num = LED_both_locations[i][1]
    LED_num = LED_both_locations[i][2]
    LED_total = LED_both_locations[i][3]
    LED_1_size = len(LED_1_locations)
    LED_2_size = len(LED_2_locations)
    # if LED found
    if LED_total > 0:
        # see at lest 1 LED
        if LED_1_size is 0:
            # if no LEDs seen so far, this is the first and will be called
            #   LED_1
            LED_1_locations.append((center,frame_num))
        elif LED_2_size is 0:
            # need to determine if this is LED_1 or LED_2,
            #   but LED_1 has been seen at least once before
            LED_1_last_arr = np.array(LED_1_locations[LED_1_size-1][0])
            dist_to_1 = np.linalg.norm(np.array(center)-LED_1_last_arr)
            if ((dist_to_1 < 10) and
                (LED_1_locations[LED_1_size-1][1] is not frame_num)):
                # if very close to LED_1, assume it is LED_1,
                #   unless one of the LEDs seen in the frame has already been
                #   attributed to LED_1
                LED_1_locations.append((center,frame_num))
            else:
                LED_2_locations.append((center,frame_num))
        else:
            LED_1_last_arr = np.array(LED_1_locations[LED_1_size-1][0])
            LED_2_last_arr = np.array(LED_2_locations[LED_2_size-1][0])
            dist_to_1 = np.linalg.norm(np.array(center)-LED_1_last_arr)
            dist_to_2 = np.linalg.norm(np.array(center)-LED_2_last_arr)
            if dist_to_1 < dist_to_2:
                # assume LED_1 if closer
                LED_1_locations.append((center,frame_num))
            elif LED_1_locations[LED_1_size-1][1] is frame_num:
                # already attributed an LED to LED_1 in this frame
                LED_2_locations.append((center,frame_num))
            elif LED_2_locations[LED_2_size-1][1] is frame_num:
                # already attributed an LED to LED_2 in this frame
                LED_1_locations.append((center,frame_num))
            else:
                LED_2_locations.append((center,frame_num))

# now for visual confirmation
# plot all of LED_1s locations
print "LED_1"
LED_1_size = len(LED_1_locations)
output_img = np.zeros((frame_height,frame_width,3), np.uint8)
for i in range(0, LED_1_size):
    cv2.circle(output_img,LED_1_locations[i][0],2,(0,255,0),2)

# plot all of LED_2s locations
print "\nLED_2"
LED_2_size = len(LED_2_locations)
for i in range(0, LED_2_size):
    cv2.circle(output_img,LED_2_locations[i][0],2,(255,0,0),2)

cv2.imshow('image',output_img)
cv2.waitKey(0)


cv2.destroyAllWindows()

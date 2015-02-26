import numpy as np
import cv2
import cv2.cv as cv

vid_file = 'Videos\\IR_DARK_FILTERED.mp4'
cap = cv2.VideoCapture(vid_file)    # the capture
cap.open(vid_file)  # use because vid doesn't always open automatically
LED_both_locations = []
# We know that there are only 2 LEDs
LED_1_locations = []
LED_2_locations = []

# get vital stats
frames_total = int(cap.get(cv.CV_CAP_PROP_FRAME_COUNT))
frame_num = 0
frame_width = cap.get(cv.CV_CAP_PROP_FRAME_WIDTH)
frame_height = cap.get(cv.CV_CAP_PROP_FRAME_HEIGHT)

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

        # display visual confirmation of LED location and identity
        number_LEDs = len(centers)
        size_LED_1 = len(LED_1_locations)
        size_LED_2 = len(LED_2_locations)
        for i in range(0,number_LEDs):

            # Identify
            if size_LED_1 is 0:
                # no baseline set
                LED_1_locations.append((centers[i],frame_num))
            elif size_LED_2 is 0:
                # LED_1 has a baseline, but LED_2 doesn't
                # Need to determine if this is LED_1 again or the first
                #   sighting of LED_2
                # convert to numpy array to use numpy's distance calculations
                LED_1_last_arr = np.array(LED_1_locations[size_LED_1-1][0])
                # distance from current LED to the last sighting of LED 1
                dist_to_1 = np.linalg.norm(np.array(centers[i])-LED_1_last_arr)
                # if its really close to LED_1's last known location
                #   and it wasn't already seen in this frame
                if ((dist_to_1 < 10) and
                    (LED_1_locations[size_LED_1-1][1] is not frame_num)):
                    LED_1_locations.append((centers[i],frame_num))
                else:
                    LED_2_locations.append((centers[i],frame_num))
            else:
                # both LEDs have a baseline
                # determine which LED's last known location is closer
                LED_1_last_arr = np.array(LED_1_locations[size_LED_1-1][0])
                LED_2_last_arr = np.array(LED_2_locations[size_LED_2-1][0])
                dist_to_1 = np.linalg.norm(np.array(centers[i])-LED_1_last_arr)
                dist_to_2 = np.linalg.norm(np.array(centers[i])-LED_2_last_arr)

                if dist_to_1 < dist_to_2:
                    # assume LED_1 if closer
                    LED_1_locations.append((centers[i],frame_num))
                elif LED_1_locations[size_LED_1-1][1] is frame_num:
                    # already attributed an LED to LED_1 in this frame
                    LED_2_locations.append((centers[i],frame_num))
                elif LED_2_locations[size_LED_2-1][1] is frame_num:
                    # already attributed an LED to LED_2 in this frame
                    LED_1_locations.append((centers[i],frame_num))
                else:
                    # assume LED_2 if closer
                    LED_2_locations.append((centers[i],frame_num))

        # Show
        size_LED_1 = len(LED_1_locations)
        size_LED_2 = len(LED_2_locations)
        # LED_1 first
        for i in range(0, size_LED_1):
            cv2.circle(frame,LED_1_locations[i][0],2,(0,255,0),2)
        # LED_2 first
        for i in range(0, size_LED_2):
            cv2.circle(frame,LED_2_locations[i][0],2,(255,0,0),2)

        cv2.imshow('frames', frame)

        # # slow down the video playback
        # cv2.waitKey(1)
        # lets us quit the video early
        if (cv2.waitKey(1) & 0xFF == ord('q')) & frames_total > frame_num:
            break
        elif 0xFF == ord('q'):
            break

    else:
        break

cv2.destroyAllWindows()
cap.release()


import numpy as np
import cv2
import cv2.cv as cv

vid_file = 'Videos\\IR_DARK_FILTERED.mp4'
cap = cv2.VideoCapture(vid_file)    # the capture
cap.open(vid_file)  # doesn't always open automatically
frame_count = 0

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
        for cnt in contours:
          (x,y),radius = cv2.minEnclosingCircle(cnt)
          centers.append((int(x),int(y)))
          radii.append(int(radius))
        # draw circles around LEDs in image
        size = len(centers)
        for i in range(0,size):
            cv2.circle(frame,centers[i],radii[i],(255,255,255),2)
        cv2.imshow('frames', frame)
        # slow down the video playback
        cv2.waitKey(10)
        # lets us quit the video early
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# When everything done, release the capture
cap.release()
# out.release()
cv2.destroyAllWindows()

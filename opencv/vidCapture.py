import numpy as np
import cv2
import cv2.cv as cv

vid_file = 'Videos\\IR_DARK_FILTERED.mp4'
cap = cv2.VideoCapture(vid_file)
cap.open(vid_file)

# fourcc = cv.CV_FOURCC(*'XVID')
# out = cv2.VideoWriter('Videos\\output.avi',fourcc, 20.0, (1920,1080))

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret==True:
        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rows,cols = gray.shape
        circles = cv2.HoughCircles(gray,cv.CV_HOUGH_GRADIENT,1,rows/8,
                                   param1=200,param2=10,minRadius=0,maxRadius=0)
        if type(circles) is np.ndarray:
            circles = np.uint16(np.around(circles))

            for i in circles[0,:]:
                # draw the outer circle
                cv2.circle(gray,(i[0],i[1]),i[2],(0,255,0),2)
                # draw the center of the circle
                cv2.circle(gray,(i[0],i[1]),2,(0,0,255),3)
        cv2.imshow('frames',gray)
        cv2.waitKey(10)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        # out.write(gray)
    else:
        break

# When everything done, release the capture
cap.release()
# out.release()
cv2.destroyAllWindows()

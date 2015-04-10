"""Python code for interfacing to VC0706 cameras and grabbing a photo and
finding LED lights in them. Pretty basic stuff
"""


# written by ladyada. MIT license (serial and camera)
# written by nathan moore, SMU license (opencv and image analysis)

import serial
import time
import numpy as np
import cv2

# DON"T CHANGE THE BAUD RATE
BAUD = 38400
# CHECK DEVICE MANAGER FOR THE COM PORT
PORT = "COM7"
TIMEOUT = 0.2

SERIALNUM = 0    # start with 0

COMMANDSEND = 0x56
COMMANDREPLY = 0x76
COMMANDEND = 0x00

CMD_GETVERSION = 0x11
CMD_RESET = 0x26
CMD_TAKEPHOTO = 0x36
CMD_READBUFF = 0x32
CMD_GETBUFFLEN = 0x34

FBUF_CURRENTFRAME = 0x00
FBUF_NEXTFRAME = 0x01
FBUF_STOPCURRENTFRAME = 0x00

getversioncommand = [COMMANDSEND, SERIALNUM, CMD_GETVERSION, COMMANDEND]
resetcommand = [COMMANDSEND, SERIALNUM, CMD_RESET, COMMANDEND]
takephotocommand = [COMMANDSEND, SERIALNUM, CMD_TAKEPHOTO, 0x01, FBUF_STOPCURRENTFRAME]
getbufflencommand = [COMMANDSEND, SERIALNUM, CMD_GETBUFFLEN, 0x01, FBUF_CURRENTFRAME]
readphotocommand = [COMMANDSEND, SERIALNUM, CMD_READBUFF, 0x0c, FBUF_CURRENTFRAME, 0x0a]
s = serial.Serial(PORT, baudrate=BAUD, timeout=TIMEOUT)
num_pics = 1


def checkreply(r, b):
    r = map (ord, r)
    #print 'checkreply: completed  map, len=', len(r)
    #print 'r =', r
    if (r[0] == 0x76 and r[1] == SERIALNUM and r[2] == b and r[3] == 0x00):
        return True
    print 'checkReply() failed'
    return False


def reset():
    cmd = ''.join (map (chr, resetcommand))
    s.write(cmd)
    reply = s.read(100)
    r = list(reply)
    if checkreply(r, CMD_RESET):
        return True
    print 'reset(): failure'
    return False


def getversion():
    cmd = ''.join (map (chr, getversioncommand))
    s.write(cmd)
    reply =  s.read(16)
    r = list(reply);
    if checkreply(r, CMD_GETVERSION):
        return True
    return False


def takephoto():
    cmd = ''.join (map (chr, takephotocommand))
    s.write(cmd)
    reply =  s.read(5)
    r = list(reply);
    if (checkreply(r, CMD_TAKEPHOTO) and r[3] == chr(0x0)):
        return True
    return False


def getbufferlength():
    cmd = ''.join (map (chr, getbufflencommand))
    s.write(cmd)
    reply =  s.read(9)
    r = list(reply);
    if (checkreply(r, CMD_GETBUFFLEN) and r[4] == chr(0x4)):
        l = ord(r[5])
        l <<= 8
        l += ord(r[6])
        l <<= 8
        l += ord(r[7])
        l <<= 8
        l += ord(r[8])
        return l
    return 0


def readbuffer(bytes2read):
    addr = 0
    photo = []
    while (addr < bytes2read + 32):
        command = readphotocommand + [(addr >> 24) & 0xFF, (addr >> 16) & 0xFF,
                                      (addr >> 8) & 0xFF, addr & 0xFF]
        command +=  [0, 0, 0, 32]   # 32 bytes at a time
        command +=  [0x10,0]         # delay of 20ms (was 10 ms)
        #print map(hex, command)
        cmd = ''.join(map (chr, command))
        s.write(cmd)
        reply = s.read(32+5)
        r = list(reply)
        if (len(r) != 37):
            continue
        #print r
        if (not checkreply(r, CMD_READBUFF)):
            print "ERROR READING PHOTO"
            return
        photo += r[5:]
        addr += 32
    return photo


def take_picture(pic_num):

    reset()
    time.sleep(2)
    if (not getversion()):
        print "Camera not found"
        exit()
    print "VC0706 Camera found"
    if takephoto():
        print "Snap!"
    bytes2read = getbufferlength()
    print bytes2read, "bytes to read"
    photo = readbuffer(bytes2read)
    photodata = ''.join(photo)
    f = open("pic_test_"+str(pic_num)+".jpg", 'wb')
    f.write(photodata)
    f.close()
    s.close()


"""Main"""


# Take Picture

take_picture(0)
s.close()

# Analyze Picture

# image file
img_file = 'pice_test_0.jpg'
# load image
img = cv2.imread(img_file, cv2.IMREAD_COLOR)
# make grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# blur (reduces noise)
blur = cv2.Gauv2.cvssianBlur(gray, (3, 3), 0)
# calculate threshold (make it a pure black and white image)
ret_,thresh = cv2.threshold(blur, 60, 255, cv2.THRESH_BINARY)
# find contours (LEDs)
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE,
                                       cv2.CHAIN_APPROX_SIMPLE)
# store (x,y) of the center of the led
centers = []
for cntr in contours:
    (x, y), radius = cv2.minEnclosingCircle(cntr)
    centers.append((int(x), int(y)))
# draw circles around LEDs in image, set radius to a fixed size: 10
size = len(centers)
for i in range(0, size):
    # cv2.circle(frame,centers[i],radii[i],(255,255,255),2)
    cv2.circle(frame, centers[i], 10, (255, 255, 255), 2)
    # Storing:
    #   (center coords of LED, which frame,
    #       which LED in frame, num LEDs seen in frame)
    LED_both_locations.append((centers[i], frame_num, i+1, size))
cv2.imshow('image', frame)
# lets us close the window
cv2.waitKey(0)
# closes all windows
cv2.destroyAllWindows()

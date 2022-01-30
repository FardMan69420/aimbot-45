import cv2
import numpy as np
from mss import mss
import time
from win32 import win32api
import win32con

sct = mss()
monX = 1920
monY = 1080
boxsize = 290

lower = np.array([139,96,129])
upper = np.array([169,255,255])

def grab():
    # change your monitor to 1 if you aren't screenlocked like me
    # TODO: capture OBS window
    mon2 = sct.monitors[2]
    box = {
        'top': mon2['top'] + int(((monY / 2) - (boxsize / 2))),
        'left': mon2['left'] + int(((monX / 2) - (boxsize / 2))),
        'width': boxsize,
        'height': boxsize,
    }
    sct_img = sct.grab(box)
    input = np.array(sct_img)
    return input


def mouse_move(x, y):
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, x, y, 0, 0)


def process():
    hsv = cv2.cvtColor(input, cv2.COLOR_BGR2HSV)
    red_mask = cv2.inRange(hsv, lower, upper)
    res_red = cv2.bitwise_and(red_mask, red_mask, 
                              mask = red_mask)
    # original method
    # contours, hierarchy = cv2.findContours(red_mask, cv2.RETR_TREE,
                                   # cv2.CHAIN_APPROX_SIMPLE)
    contours, hierarchy = cv2.findContours(red_mask, cv2.RETR_EXTERNAL,
                                   cv2.CHAIN_APPROX_SIMPLE)

    # cv2.drawContours(input, contours, -1, (0,255,0), -1)

    print(len(contours))

    if len(contours) != 0:
        maximum = max(contours, key = cv2.contourArea)

        # x,y,w,h = cv2.boundingRect(maximum)
        # cv2.rectangle(input,(x,y),(x+w,y+h),(255,0,0), 2)
        moment = cv2.moments(res_red)
        if moment["m00"] == 0:
            return
        
        mid = boxsize / 2
        cX = int(moment["m10"] / moment["m00"])
        cY = int(moment["m01"] / moment["m00"])
            
        cv2.circle(input, (cX, cY), 5, (255, 255, 255), -1)
        xf = -(mid - cX)
        yf = -(mid - cY)

        if is_activated():
            mouse_move(int(xf), int(yf))
    
    return 

def is_activated():
    return win32api.GetAsyncKeyState(0x01) != 0

while True:
    loop_time = time.time()
    input = grab()
    process()
    cv2.rectangle(input,(200,375), (900,900),(255,239,213), -1)
    cv2.imshow('input', input)
    print('TIME {}'.format(round(1 / (time.time() - loop_time), 2)))
    loop_time = time.time()

    if (cv2.waitKey(1) & 0xFF) == ord("q"):
        cv2.destroyAllWindows()
        break

# ideas:
    # threads
    # find a new method to capture screen?
    # calc velocity of 2 characters between frames, flick to a bit before
        # would need distance, iirc only from getting memory
        # can i get that, sadly i won't risk that/im not good enough



import cv2
import numpy as np
from mss import mss
from pil import Image
import imutils
import time
from win32 import win32api
import win32con
import keyboard

time.sleep(3)

sct = mss()
monX = 1920
monY = 1080
boxsize = 290
kernel = np.ones((5, 5), "uint8")

#--- red ---#
# lower = np.array([0,81,130])
# upper = np.array([4,255,188])

#--- magenta ---#
lower = np.array([139,96,129])
upper = np.array([169,255,255])

def grab():
    # change your monitor to 1 if you aren't screenlocked like me
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
    # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, x, y, 0, 0)
    # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)

def process():
    # hsv = cv2.cvtColor(input, cv2.COLOR_BGR2HSV)
    # hsv = cv2.cvtColor(input, cv2.COLOR_BGR2GRAY)
    # img_gray = cv2.cvtColor(input, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(input, cv2.COLOR_BGR2HSV)
    red_mask = cv2.inRange(hsv, lower, upper)
    # red_mask = cv2.dilate(red_mask, kernel)
    res_red = cv2.bitwise_and(red_mask, red_mask, 
                              mask = red_mask)

    contours, hierarchy = cv2.findContours(red_mask, cv2.RETR_TREE,
                                   cv2.CHAIN_APPROX_SIMPLE)

    blank = np.zeros(res_red.shape[:2],
                    dtype='uint8')
 
    final = cv2.drawContours(blank, contours, -1,
                   (255, 0, 0), 1)

    if len(contours) != 0:
        maximum = max(contours, key = cv2.contourArea)
        x,y,w,h = cv2.boundingRect(maximum)
        # draw the biggest contour (c) in green
        cv2.rectangle(input,(x,y),(x+w,y+h),(0, 255, 0), 2)
        # cv2.drawContours(final, contours, -1, (0,255,0), 3)

        testx = int(x + (1/2 * w))
        testy = int(y + (1/2 * h))

        cv2.circle(input, (testx,testy), 4, (0, 255, 0), -1)

        moment = cv2.moments(final)
        if moment["m00"] == 0:
            return
        cx = int(moment["m10"] / moment["m00"])
        cy = int(moment["m01"] / moment["m00"])

        mid = boxsize / 2
        x = -(mid - cx) if cx < mid else cx - mid
        y = -(mid - cy) if cy < mid else cy - mid

        # cx = -(mid - cx)
        # cy = -(mid - cy)

        # cv2.circle(input, (cx, cy), 5, (255, 255, 255), -1)
        # cv2.circle(input, (cx, cy), 4, (0, 0, 255), -1)
        # cv2.circle(input, (int(x), int(y)), 16, (0, 0, 255), -1)
        # mouse_move(int(x), int(y + 5))
        if is_activated():
            mouse_move(int(x), int(y))
    return res_red, final

def gettarget(target):
    # does stuff
    pass

def is_activated():
    return win32api.GetAsyncKeyState(0x05) != 0

while True:
    input = grab()
    cx = 0
    cy = 0
    # cv2.imshow('frame', input)
    res_red, final = process()
    cv2.imshow('res_red', res_red)
    cv2.imshow('final', final)
    cv2.imshow('input', input)

    if (cv2.waitKey(1) & 0xFF) == ord("q"):
        cv2.destroyAllWindows()
        break

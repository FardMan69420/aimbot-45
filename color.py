import mss
import numpy as np
import cv2
from os import system
import time
from pynput.mouse import Button, Controller

# CONFIG
fullDimensionX         = 1920 # CHANGE IF YOUR MONITOR ISN'T 1920x1080, UNTESTED
fullDimensionY         = 1080 # CHANGE IF YOUR MONITOR ISN'T 1920x1080, UNTESTED
blursize               = 10   # SIZE OF BLUR
boxsize                = int(input("DIMENSION OF BOX >  "))

# OPENCV TEXT CONFIG
font                   = cv2.FONT_HERSHEY_COMPLEX_SMALL
bottomLeftCornerOfText = (10,30)
fontScale              = 0.75
fontColor              = (0,0,255)
lineType               = 2

mouse = Controller() # STARTS MOUSE

# CALCULATES THE BOX SIZE BASED ON fullDimensionX, fullDimensionY, and boxsize
top = int(((fullDimensionY / 2) - (boxsize / 2)))
left = int(((fullDimensionX / 2) - (boxsize / 2)))
width = int(boxsize)
height = int(boxsize)

while True:
    with mss.mss() as sct:
        monitor = {'top': top, 'left': left, 'width': width, 'height': height}
        img = np.array(sct.grab(monitor))
        framespersecond = str(cv2.CAP_PROP_FPS)
        cv2.putText(img,framespersecond, 
            bottomLeftCornerOfText, 
            font, 
            fontScale,
            fontColor,
            lineType)

        cv2.imshow('img', np.array(img))

        blur = cv2.blur(src=img, ksize=(blursize, blursize))
        cv2.imshow('blur', blur)

        hsv = cv2.cvtColor(np.array(blur), cv2.COLOR_BGR2HSV)

        # RED_MIN = np.array([130, 0, 0]) # BGR ORDER
        # RED_MAX = np.array([255, 80, 80]) # BGR ORDER
        # starting colors - lower_red = np.array([0,50,50])
        # starting colors - upper_red = np.array([15,255,255])
        lower_red = np.array([7,90,35])
        upper_red = np.array([345,100,100])
        mask = cv2.inRange(hsv, lower_red, upper_red)
        res = cv2.bitwise_and(np.array(img), np.array(img), mask=mask)
        # cv2.imshow('mask', mask)
        # cv2.imshow('res', res)
        gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
        # cv2.imshow('gray', gray)
        pixels = cv2.countNonZero(gray)
        print(np.average(pixels), 'pixels found')

        if np.average(pixels) > 20:
            mouse.press(Button.left)
            mouse.release(Button.left)
            print('clicked!')

    if (cv2.waitKey(1) & 0xFF) == ord('q'):
        print("exiting...")
        time.sleep(0.5)
        system('cls')
        cv2.destroyAllWindows()
        break

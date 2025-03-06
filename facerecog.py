import numpy as np
import cv2
from cv2 import aruco
from djitellopy import Tello
import asyncio




cam = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
track = 0
def ScreenSplitLines(imag):
    global ScreenX_Half,ScreenY_Half
    size_info = imag.shape
    #print(size_info)
    #maybe Y,X? Don't know, figure out exactly what its passing
    ScreenX = int(size_info[1])
    ScreenY = int(size_info[0])
    ScreenX_Half = int(ScreenX / 2)
    ScreenY_Half = int(ScreenY / 2)
    #print(f"X End: {ScreenX} X Half: {ScreenX_Half} Y End: {ScreenY} Y Half: {ScreenY_Half}")
    cv2.line(img, (ScreenX_Half, 0), (ScreenX_Half, ScreenY), (0, 255, 0), 5)
    cv2.line(img, (0, ScreenY_Half), (ScreenX, ScreenY_Half), (255, 0, 0), 5)
    #creates thresholds for drone turning
    global thresholdRX,thresholdLX,thresholdUY,thresholdBY
    thresholdRX = ScreenX_Half + ScreenX*0.2
    thresholdLX = ScreenX_Half - ScreenX*0.2
    thresholdUY = ScreenY_Half - ScreenY*0.1

    thresholdBY = ScreenY_Half + ScreenY*0.1



def FindAruco(imag):

    global gray,x,y,w,h,xm,ym,track

    gray=cv2.cvtColor(imag,cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5,minSize=(5,5))
    edges = cv2.Canny(gray,50,200)
    contours,_ = cv2.findContours(edges,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    for (x,y,w,h) in faces:
        cv2.rectangle(imag,(x,y),(x+w,y+h),(0,255,0),2)
        try:
            if faces is not None:
                #print(x,y)
                xc = x
                yc = y
                wid = w / 2
                hei = h / 2
                xm = xc + wid
                ym = yc + hei
                distance = estimate_distance(w)
                print(f'Distance: {distance} cm')
                Controller()

            pass

        except NameError:
            pass
    track =0
def estimate_distance(perceived_width):
    real_width = 15 #average adult human face size, should work good enough \ cm
    focal_len = 670 #for the surface go school laptop \ pix WORKS FOR SCHOOL LAPTOP, NEED TO REMEASURE FOCAL FOR DRONE
    return (real_width*focal_len)/perceived_width #perceived is in pixels, focal in mm, need to make them the same
def Controller():
    global xm,ym,track
    try:
        xm = int(xm)
        ym = int(ym)
        isint = True
    except:
        isint = False
    if thresholdRX <= xm:
        print("LEFT SIDE", track)
    elif thresholdLX >= xm:
        print("RIGHT SIDE", track)
    if thresholdUY > ym:  # errors on all the y coord stuff, need to figure out which corner the y coordinate is derived from
        print("UP SIDE", track)
    elif thresholdBY < ym:
        print("DOWN SIDE", track)
    #print(xm," ", ym)



while True:
    ret, img = cam.read()
    ScreenSplitLines(img)
    FindAruco(img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    cv2.imshow("Camera", img)

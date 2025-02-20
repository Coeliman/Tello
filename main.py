from asyncio import wait_for

import numpy as np
import cv2
from djitellopy import Tello
import time
tello = Tello()
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
track = 0
last_command_time = time.time()

def wait_for_drone_ready():
    while tello.get_battery() >0:
        status = tello.get_current_state()
        if 'in_motion' not in status or not status['in_motion']:
            break
        time.sleep(0.1)
def ScreenSplitLines(imag):
    global ScreenX_Half, ScreenY_Half
    size_info = imag.shape
    # print(size_info)
    # maybe Y,X? Don't know, figure out exactly what its passing
    ScreenX = int(size_info[1])
    ScreenY = int(size_info[0])
    ScreenX_Half = int(ScreenX / 2)
    ScreenY_Half = int(ScreenY / 2)
    # print(f"X End: {ScreenX} X Half: {ScreenX_Half} Y End: {ScreenY} Y Half: {ScreenY_Half}")
    cv2.line(cam, (ScreenX_Half, 0), (ScreenX_Half, ScreenY), (0, 255, 0), 5)
    cv2.line(cam, (0, ScreenY_Half), (ScreenX, ScreenY_Half), (255, 0, 0), 5)
    # creates thresholds for drone turning
    global thresholdRX, thresholdLX, thresholdUY, thresholdBY
    thresholdRX = ScreenX_Half + ScreenX * 0.2
    thresholdLX = ScreenX_Half - ScreenX * 0.2
    thresholdUY = ScreenY_Half - ScreenY * 0.1
    thresholdBY = ScreenY_Half + ScreenY * 0.1
def CoordMath(bbox):
    global x
    global y
    x = "N"
    y = "N"
    for i in range(len(bbox)):
        x = (bbox[i - 1][0][0][0] + bbox[i - 1][0][1][0] + bbox[i - 1][0][2][0] + bbox[i - 1][0][3][0]) / 4
        y = (bbox[i - 1][0][0][1] + bbox[i - 1][0][1][1] + bbox[i - 1][0][2][1] + bbox[i - 1][0][3][1]) / 4

def DroneController():
    global xm, ym, track, last_command_time
    try:
        xm = int(xm)
        ym = int(ym)
        isint = True
    except:
        isint = False
    if isint == True:
        track += 1
       # if time.time() - last_command_time > 2:
        #    if thresholdRX <= xm:
         #       print("LEFT SIDE", track)
          #      tello.rotate_clockwise(20)
           #     last_command_time = time.time()
            #elif thresholdLX >= xm:
             #   print("RIGHT SIDE", track)
              #  tello.rotate_counter_clockwise(20)
               # last_command_time = time.time()
        if time.time() - last_command_time > 5:
            current_height = tello.get_height()
            if thresholdUY > ym:  # errors on all the y coord stuff, need to figure out which corner the y coordinate is derived from
                if current_height < 100:
                    print(f"Command: Move Up (Current height: {current_height})")
                    tello.move_up(5) #if this still doesnt work, try using tello.send_control_command('up 5')
                    wait_for_drone_ready()
                    last_command_time = time.time()
                else:
                    print("Height limit reached, can't move up.")
            elif thresholdBY < ym:
                if current_height > 5:
                    print(f"Command: Move down (Current height: {current_height})")
                    tello.move_down(5)
                    wait_for_drone_ready()
                    last_command_time = time.time()
                else:
                    print("Height limit reached, can't move down.")
    else:
        pass
def FindAruco(imag):
    global gray, x, y, w, h, xm, ym, track
    ScreenSplitLines(imag)
    gray = cv2.cvtColor(imag, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(20, 20))
    for (x, y, w, h) in faces:
        cv2.rectangle(imag, (x, y), (x + w, y + h), (0, 255, 0), 2)
        try:
            if faces is not None:
                # print(x,y)
                xc = x
                yc = y
                wid = w / 2
                hei = h / 2
                xm = xc + wid
                ym = yc + hei
                DroneController()
            pass
        except NameError:
            pass
    track = 0
tello.connect()
tello.streamon()
tello.takeoff()
while True:
    frameread = tello.get_frame_read()
    cam = cv2.cvtColor(frameread.frame,cv2.COLOR_RGB2BGR)
    FindAruco(cam)
    #prints acceleration
    cv2.imshow("Camera", cam)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
import numpy as np
import cv2
from djitellopy import Tello
import asyncio
import time
tello = Tello()
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
track = 0
last_command_time = time.time()
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("Trainer.yml")
name_list = ["", "User"]
vert_move = True
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
def estimate_distance(perceived_width):
    real_width = 15 #average adult human face size, should work good enough \ cm
    focal_len = 1000 #for the surface go school laptop \ 670 for PC, 1000 for drone
    return (real_width*focal_len)/perceived_width #perceived is in pixels, focal in mm, need to make them the same
async def move_up():
    tello.move_up(30)
async def move_down():
    tello.move_down(30)
async def move_forward():
    tello.move_forward(30)
async def move_back():
    tello.move_back(30)
async def rotate_CCW():
    tello.rotate_counter_clockwise(20)
async def rotate_CW():
    tello.rotate_clockwise(20)
def DroneController():
    global xm, ym, track, last_command_time, distance, vert_move
    try:
        xm = int(xm)
        ym = int(ym)
        isint = True
    except:
        isint = False
    if isint == True:
        if conf > 40:
            cv2.putText(cam, name_list[serial], (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
            track += 1
            if time.time() - last_command_time > 1:
                if thresholdRX <= xm:
                    print("LEFT SIDE", track)

                    last_command_time = time.time()
                    asyncio.run(rotate_CW())
                elif thresholdLX >= xm:
                    print("RIGHT SIDE", track)

                    last_command_time = time.time()
                    asyncio.run(rotate_CCW())
                elif distance > 250:

                    last_command_time = time.time()
                    asyncio.run(move_forward())
                    print("fwd 30")
                elif distance < 120:
                    last_command_time = time.time()
                    asyncio.run(move_back())

                    print("back 30")
            if time.time() - last_command_time > 10:
                current_height = tello.get_height()
                print(distance)
                if vert_move:
                    if thresholdUY > ym:  # errors on all the y coord stuff, need to figure out which corner the y coordinate is derived from
                        if current_height < 100:
                            last_command_time = time.time()
                            print(f"Command: Move Up (Current height: {current_height})")
                            asyncio.run(move_up())


                        else:
                            print("Height limit reached, can't move up.")
                    elif thresholdBY < ym:
                        if current_height > 5:
                            print(f"Command: Move down (Current height: {current_height})")
                            last_command_time = time.time()
                            asyncio.run(move_down())


                        else:
                            print("Height limit reached, can't move down.")
        else:
            cv2.putText(cam, "Unknown", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)




    else:
        pass
def FindAruco(imag):
    global gray, x, y, w, h, xm, ym, track, distance,serial,conf
    ScreenSplitLines(imag)
    gray = cv2.cvtColor(imag, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(5, 5))
    for (x, y, w, h) in faces:
        cv2.rectangle(imag, (x, y), (x + w, y + h), (0, 255, 0), 2)
        serial, conf = recognizer.predict(gray[y:y + h, x:x + w])
        try:
            if faces is not None:
                # print(x,y)
                xc = x
                yc = y
                wid = w / 2
                hei = h / 2
                xm = xc + wid
                ym = yc + hei
                distance = estimate_distance(w)
                DroneController()
            pass
        except NameError:
            pass
    track = 0
tello.connect()
tello.streamon()
tello.takeoff()
time.sleep(2)
tello.move_up(60)
time.sleep(2)
frame_interval = 1 / 20.0
last_frame_time = time.time()
print(f"Battery Level: {tello.get_battery()}%")
while True:
    current_time = time.time()
    if current_time - last_frame_time >= frame_interval:
        frameread = tello.get_frame_read()
        cam = cv2.cvtColor(frameread.frame,cv2.COLOR_RGB2BGR)
        FindAruco(cam)
        cv2.imshow("Camera", cam)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
from djitellopy import Tello
import cv2,math,time

tello = Tello()
tello.connect()

tello.streamon()
frame_read = tello.get_frame_read()

tello.takeoff()

while True:
    img = frame_read.frame
    cv2.imshow('frame',img)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("w"):
        tello.move_forward(30)
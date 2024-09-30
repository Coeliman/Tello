#imports
from djitellopy import tello
import cv2
import threading
import numpy as np


#vars
tello = tello.Tello()
imwidth = 640
imheight = 480

#tello setup
tello.connect()
tello.streamoff()
tello.streamon()
print(f"The battery is {tello.get_battery()}")
#cv2 setup

#defs
def video(drone):
    while True:
        img = drone.get_frame_read().frame
        cv2.imshow('img', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()
# main loop
def main():
    while True:
        frame = tello.get_frame_read().frame
        frame_resized = cv2.resize(frame, (imwidth, imheight))

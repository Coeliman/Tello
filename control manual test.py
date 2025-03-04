from djitellopy import Tello
import cv2,math,time

tello = Tello()
tello.connect()

tello.streamon()
frame_read = tello.get_frame_read()

tello.takeoff()


time.sleep(0.5)
tello.move_up(150)
time.sleep(1)
tello.move_down(50)
time.sleep(0.5)
tello.land()
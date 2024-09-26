
from djitellopy import tello
import cv2
import threading

def video(drone):
    while True:
        img = drone.get_frame_read().frame
        cv2.imshow('img', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()
def routine(drone):
    print("routine")
    drone.takeoff()
    drone.move_forward(20)
    drone.move_back(20)
    drone.land()
tello = tello.Tello()
tello.connect()
tello.streamoff()
tello.streamon()
video(tello)

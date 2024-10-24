import numpy as np
import cv2
from cv2 import aruco
from djitellopy import tello
import threading


# video cap cam
draw = True
#do we wanna draw aruco box
tello = tello.Tello()
tello.connect()
tello.streamoff()
tello.streamon()
#tello connection

def FindAruco(imag,markerSize=4,total_markers=1000,draw=True):
    gray=cv2.cvtColor(imag,cv2.COLOR_BGR2GRAY)
    key = getattr(cv2.aruco,f'DICT_{markerSize}X{markerSize}_{total_markers}')
    arucoDict= cv2.aruco.getPredefinedDictionary(key)
    arucoParam = cv2.aruco.DetectorParameters()
    bbox,ids,_=cv2.aruco.detectMarkers(gray,arucoDict,parameters=arucoParam)
    print(ids)
    if draw:
        aruco.drawDetectedMarkers(img,bbox,ids)

def telloCapture(drone):
    global img
    img = drone.get_frame_read().frame


while True:
    telloCapture(tello)
    FindAruco(img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    cv2.imshow("Camera", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
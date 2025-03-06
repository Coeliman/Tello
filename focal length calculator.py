import numpy as np
import cv2
from cv2 import aruco
from djitellopy import Tello
import asyncio


known_dist = 30.48
known_width = 15
cam = cv2.VideoCapture(0)

def find_obj_width(frm):
    gray = cv2.cvtColor(frm,cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray,50,200)
    contours,_ = cv2.findContours(edges,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        x,y,w,h = cv2.boundingRect(cnt)
        if w > 50:
            return w
    return None

while True:
    ret, img = cam.read()

    width_in_pixels = find_obj_width(img)

    if width_in_pixels:
        focal_length = (width_in_pixels* known_dist)/known_width
        print(f"Estimated Focal Length (pixels): {focal_length:.2f}")
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    cv2.imshow("Camera", img)
cam.release()
cv2.destroyAllWindows()
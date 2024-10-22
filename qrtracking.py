#FILE DOES NOT WORK, MERELY TEST CODE

import numpy as np
import cv2
from cv2 import aruco

aruco_type = cv2.aruco.DICT_4X4_1000
arucoDict = cv2.aruco.getPredefinedDictionary(aruco_type)
param_markers = aruco.DetectorParameters()
cam = cv2.VideoCapture(0)

while True:
    _, frame = cam.read()
    if not _:
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    marker_corners,marker_IDs,reject = aruco.detectMarkers(gray, arucoDict,parameters = param_markers)

    if marker_corners ==True:
        for ids, corners in zip(marker_IDs,marker_corners):
            cv2.polylines(frame,[corners],True,(0,255,0),3)
            corners = corners.reshape(4,2)
            corners = corners.astype(int)
            top_right = corners[0].ravel()
            top_left = corners[1].ravel()
            bottom_right = corners[2].ravel()
            bottom_left = corners[3].ravel()
            cv2.putText(frame,f"ID: {ids[0]}",top_right,cv2.FONT_HERSHEY_PLAIN,1,(0,255,0),2)
    cv2.imshow('frame',frame)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
cam.release()
cv2.destroyAllWindows()

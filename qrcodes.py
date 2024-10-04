import numpy as np
import cv2
aruco_type = cv2.aruco.DICT_4X4_1000
id = 1

arucoDict = cv2.aruco.getPredefinedDictionary(aruco_type)

tag_size  = 1000
tag = np.zeros((tag_size, tag_size,1), dtype=np.uint8)
cv2.aruco.generateImageMarker(arucoDict,id,tag_size,tag,1)

import numpy as np
import cv2
aruco_type = cv2.aruco.DICT_4X4_1000
arucoid = 1

arucoDict = cv2.aruco.getPredefinedDictionary(aruco_type)

tag_size  = 1000
tag = np.zeros((tag_size, tag_size,1), dtype=np.uint8)
cv2.aruco.generateImageMarker(arucoDict,arucoid,tag_size,tag,1)

tag_name = f"arucoMarkers/" + str(aruco_type) + f"_" + str(arucoid) + f".png"

cv2.imwrite(tag_name,tag)
cv2.imshow("Aruco",tag)

cv2.waitKey(0)
cv2.destroyAllWindows()
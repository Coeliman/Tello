import numpy as np
import cv2
from cv2 import aruco
aruco_type = cv2.aruco.DICT_4X4_1000
arucoid = 1
cam = cv2.VideoCapture(0)
var = False
# false is camera, true is arcouid
draw = True
#do we wanna draw
arucoDict = cv2.aruco.getPredefinedDictionary(aruco_type)
tag_size  = 1000
tag = np.zeros((tag_size, tag_size,1), dtype=np.uint8)
cv2.aruco.generateImageMarker(arucoDict,arucoid,tag_size,tag,1)
tag_name = f"arucoMarkers/" + str(aruco_type) + f"_" + str(arucoid) + f".png"
cv2.imwrite(tag_name,tag)
#aruco,tag is the aruco tag

def FindAruco(imag,markerSize=4,total_markers=1000,draw=True):
    gray=cv2.cvtColor(imag,cv2.COLOR_BGR2GRAY)
    key = getattr(cv2.aruco,f'DICT_{markerSize}X{markerSize}_{total_markers}')
    arucoDict= cv2.aruco.getPredefinedDictionary(key)
    arucoParam = cv2.aruco.DetectorParameters()
    bbox,ids,_=cv2.aruco.detectMarkers(gray,arucoDict,parameters=arucoParam)
    print(ids)
    if draw:
        aruco.drawDetectedMarkers(img,bbox,ids)
        print(bbox)


while True:
    if var:
      img=tag
      img = cv2.resize(img,(0,0),fx=0.7,fy=0.7)
    else:
        _,img=cam.read()
    if not var:
        FindAruco(img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    cv2.imshow("Camera",img)

cv2.waitKey(0)
cv2.destroyAllWindows()
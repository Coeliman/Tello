import numpy as np
import cv2
from cv2 import aruco
import threading


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

def ScreenSplitCords(imag):
    size_info = imag.shape
    ScreenX = int(size_info[0])
    ScreenY = int(size_info[1])
    ScreenX_Half = int(ScreenX / 2)
    ScreenY_Half = int(ScreenY / 2)
    cv2.line(img, (ScreenX_Half, 0), (ScreenX_Half, ScreenY), (0, 255, 0), 5)
    cv2.line(img, (0, ScreenY_Half), (ScreenX, ScreenY_Half), (255, 0, 0), 5)

def FindAruco(imag,markerSize=4,total_markers=1000,draw=True):
    global gray,key,arucoDict,arucoParam,corners,ids
    gray=cv2.cvtColor(imag,cv2.COLOR_BGR2GRAY)
    key = getattr(cv2.aruco,f'DICT_{markerSize}X{markerSize}_{total_markers}')
    arucoDict= cv2.aruco.getPredefinedDictionary(key)
    arucoParam = cv2.aruco.DetectorParameters()
    corners,ids,_=cv2.aruco.detectMarkers(gray,arucoDict,parameters=arucoParam)
    #print(corners)
    ScreenSplitCords(imag)
    if draw:
        aruco.drawDetectedMarkers(img,corners,ids)



   #The coord stuff with the aruco
    global x
    global y
    x = "N"
    y = "N"
    for i in range(len(corners)):
        x = (corners[i - 1][0][0][0] + corners[i - 1][0][1][0] + corners[i - 1][0][2][0] + corners[i - 1][0][3][0]) / 4
        y = (corners[i - 1][0][0][1] + corners[i - 1][0][1][1] + corners[i - 1][0][2][1] + corners[i - 1][0][3][1]) / 4







while True:
    _,img=cam.read()
    FindAruco(img)
    #thread_ScreenSplit = threading.Thread(target=ScreenSplitCords, args=(img,))
    #thread_Find = threading.Thread(target = FindAruco,args = (img,))

    #thread_Find.start()
    #thread_ScreenSplit.start()
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    cv2.imshow("Camera",img)

cv2.waitKey(0)
cv2.destroyAllWindows()
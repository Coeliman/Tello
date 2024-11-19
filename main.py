import numpy as np
import cv2
from cv2 import aruco
import djitellopy as tello


tello = tello.Tello()
tello.connect()
tello.streamoff()
tello.streamon()
aruco_type = cv2.aruco.DICT_4X4_1000
arucoid = 1
useDrone = True
if useDrone:
    pass
else:
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
def EXIT():
    tello.land()
    cv2.destroyAllWindows()
def ScreenSplitLines(imag):
    size_info = imag.shape
    #print(size_info)
    #maybe Y,X? Don't know, figure out exactly what its passing
    ScreenX = int(size_info[1])
    ScreenY = int(size_info[0])
    ScreenX_Half = int(ScreenX / 2)
    ScreenY_Half = int(ScreenY / 2)
    #print(f"X End: {ScreenX} X Half: {ScreenX_Half} Y End: {ScreenY} Y Half: {ScreenY_Half}")
    cv2.line(img, (ScreenX_Half, 0), (ScreenX_Half, ScreenY), (0, 255, 0), 5)
    cv2.line(img, (0, ScreenY_Half), (ScreenX, ScreenY_Half), (255, 0, 0), 5)
    #creates thresholds for drone turning
    global thresholdRX,thresholdLX,thresholdUY,thresholdBY
    thresholdRX = ScreenX_Half + 50
    thresholdLX = ScreenX_Half - 50
    thresholdUY = ScreenY_Half + 50
    thresholdBY = ScreenY_Half - 50
def CoordMath(bbox):
    global x
    global y
    x = "N"
    y = "N"
    for i in range(len(bbox)):
        x = (bbox[i - 1][0][0][0] + bbox[i - 1][0][1][0] + bbox[i - 1][0][2][0] + bbox[i - 1][0][3][0]) / 4
        y = (bbox[i - 1][0][0][1] + bbox[i - 1][0][1][1] + bbox[i - 1][0][2][1] + bbox[i - 1][0][3][1]) / 4

def DrawAruco(cam,crn,id):
    ScreenSplitLines(cam)
    aruco.drawDetectedMarkers(cam,crn,id)
def DroneController():
    if x and y == int:

        if thresholdRX <= x:
            tello.rotate_clockwise(10)
        elif thresholdLX >= x:
            tello.rotate_counter_clockwise(10)
    else:
        pass
def FindAruco(imag,markerSize=4,total_markers=1000,draw=True):
    global gray,key,arucoDict,arucoParam,corners,ids
    gray=cv2.cvtColor(imag,cv2.COLOR_BGR2GRAY)
    key = getattr(cv2.aruco,f'DICT_{markerSize}X{markerSize}_{total_markers}')
    arucoDict= cv2.aruco.getPredefinedDictionary(key)
    arucoParam = cv2.aruco.DetectorParameters()
    corners,ids,_=cv2.aruco.detectMarkers(gray,arucoDict,parameters=arucoParam)
    #print(corners)

    CoordMath(corners)
    if draw:
        DrawAruco(img,corners,ids)
   #The coord stuff with the aruco
tello.takeoff()
while True:
    if useDrone == False:
        _,img=cam.read()
    elif useDrone == True:
        cam = tello.get_frame_read().frame
        img = cam
    FindAruco(img)
    #thread_ScreenSplit = threading.Thread(target=ScreenSplitCords, args=(img,))
    #thread_Find = threading.Thread(target = FindAruco,args = (img,))

    #thread_Find.start()
    #thread_ScreenSplit.start()
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    cv2.imshow("Camera",img)
    DroneController()

if cv2.waitKey(0):
    EXIT()


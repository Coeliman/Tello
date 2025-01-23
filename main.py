import numpy as np
import cv2
from cv2 import aruco
import asyncio
import djitellopy as tello


tello = tello.Tello()
tello.connect()
tello.streamoff()
tello.streamon()
aruco_type = cv2.aruco.DICT_4X4_1000
arucoid = 1
useDrone = True
loopcount = 0
move = 0
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
track = 0
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
async def AntiIdle():
    global loopcount
    print('prewait')
    await asyncio.sleep(5)
    print('postwait')
    if loopcount%2 == 0:
        print("MV_FWD SEND")
        tello.move_forward(5)
        print("MV FWD CONF")
    else:
        print("MB_BWK SEND")
        tello.move_back(5)
        print("MW BWK CONF")
    loopcount+=1


def EXIT():
    tello.land()
    cv2.destroyAllWindows()
def ScreenSplitLines(imag):
    global ScreenX_Half, ScreenY_Half
    size_info = imag.shape
    # print(size_info)
    # maybe Y,X? Don't know, figure out exactly what its passing
    ScreenX = int(size_info[1])
    ScreenY = int(size_info[0])
    ScreenX_Half = int(ScreenX / 2)
    ScreenY_Half = int(ScreenY / 2)
    # print(f"X End: {ScreenX} X Half: {ScreenX_Half} Y End: {ScreenY} Y Half: {ScreenY_Half}")
    cv2.line(img, (ScreenX_Half, 0), (ScreenX_Half, ScreenY), (0, 255, 0), 5)
    cv2.line(img, (0, ScreenY_Half), (ScreenX, ScreenY_Half), (255, 0, 0), 5)
    # creates thresholds for drone turning
    global thresholdRX, thresholdLX, thresholdUY, thresholdBY
    thresholdRX = ScreenX_Half + ScreenX * 0.2
    thresholdLX = ScreenX_Half - ScreenX * 0.2
    thresholdUY = ScreenY_Half - ScreenY * 0.1

    thresholdBY = ScreenY_Half + ScreenY * 0.1
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
    global xm, ym, track
    try:
        xm = int(xm)
        ym = int(ym)
        isint = True
    except:
        isint = False
    if isint == True:
        track += 1
        if thresholdRX <= xm:
            print("LEFT SIDE", track)
        elif thresholdLX >= xm:
            print("RIGHT SIDE", track)
        if thresholdUY > ym:  # errors on all the y coord stuff, need to figure out which corner the y coordinate is derived from
            print("UP SIDE", track)
            pass
        elif thresholdBY < ym:
            print("DOWN SIDE", track)
            pass

    else:
        pass
def FindAruco(imag):
    global gray, x, y, w, h, xm, ym, track

    gray = cv2.cvtColor(imag, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(5, 5))
    for (x, y, w, h) in faces:
        cv2.rectangle(imag, (x, y), (x + w, y + h), (0, 255, 0), 2)
        try:
            if faces is not None:
                # print(x,y)
                xc = x
                yc = y
                wid = w / 2
                hei = h / 2
                xm = xc + wid
                ym = yc + hei
                DroneController()

            pass

        except NameError:
            pass
    track = 0
tello.takeoff()

while True:
    if useDrone == False:
        _,img=cam.read()
    elif useDrone == True:
        cam = tello.get_frame_read().frame
        img = cam
    FindAruco(img)
    #prints acceleration
    asyncio.run(AntiIdle())


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    cv2.imshow("Camera",img)


if cv2.waitKey(0):
    EXIT()
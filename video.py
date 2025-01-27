from djitellopy import tello
import cv2
import threading
import asyncio
def video(drone):
    while True:
        img = drone.get_frame_read().frame
        cv2.imshow('Capture', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()
async def routine(drone):
    print("routine")
    drone.takeoff()
    drone.move_forward(20)
    drone.move_back(20)
    drone.land()
tello = tello.Tello()
tello.connect()
tello.streamoff()
tello.streamon()



t1= threading.Thread(target=routine, args=(tello,))


#t2.start()
t1.start() # only call if you wish to make it fly while doing video
#join method makes it so it finished both threads before moving onto code under it
#t1.join()
#t2.join ()


from djitellopy import tello
import cv2
import threading

def video(drone):
    while True:
        img = drone.get_frame_read().frame
        cv2.imshow('img', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()
def routine(drone):
    print("routine")
    drone.takeoff()
    drone.move_forward(20)
    drone.move_back(20)
    drone.land()
tello = tello.Tello()
tello.connect()
tello.streamoff()
tello.streamon()


t2 = threading.Thread(target=video, args=(tello,))
t1= threading.Thread(target=routine, args=(tello,))


t2.start()

#join method makes it so it finished both threads before moving onto code under it
#t1.join()
#t2.join ()


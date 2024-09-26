import threading
import time
tello = "hold"
def slep(gay):
    print(gay)
    time.sleep(1)
    print("done sleep")
def yarg(aaa):
    print(aaa)
    time.sleep(1)
    print("done yarg")
t1= threading.Thread(target=slep, args=("poo",))
t2= threading.Thread(target=yarg,args=(tello,))

t1.start()
t2.start()

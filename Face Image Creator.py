# pip install opencv-python==4.5.2

import cv2,time

video = cv2.VideoCapture(0)

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

id = input("Enter Your ID (MUST BE INT): ")
# id = int(id)
count=0

while True:
    ret,frame=video.read()
    gray= cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5,minSize=(100,100))
    for (x,y,w,h) in faces:
        count=count+1
        cv2.imwrite(r"C:\Users\Elijah Goris\Documents\Tello\Datasets/User."+str(id)+"."+str(count)+".jpg", gray[y:y+h, x:x+w])
        cv2.rectangle(frame, (x,y), (x+w, y+h), (50,50,255), 1)

    cv2.imshow("Frame",frame)

    k=cv2.waitKey(1)
    print(count)
    if count>500:
        break

video.release()
cv2.destroyAllWindows()
print("Dataset Collection Done..................")
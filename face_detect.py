import cv2
import numpy as np
import face_recognition
import time
import pickle
all_face_encodings = {}
# Load the cascade
TIMER = int(5)
# To capture video from webcam. 
#cap = cv2.VideoCapture(0)
# To use a video file as input 
cap = cv2.VideoCapture('test.mp4')
framerate = int(cap.get(cv2.CAP_PROP_FPS))
print(framerate)
if framerate % 2 != 0:
    framerate = framerate-1
framecount = (framerate/2)-1
count = 0
while True:
      
    # Read and display each frame
    success, img = cap.read()
    framecount += 1
    try:
        
        imgS = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    except:
        break
    # Convert to grayscale
    
    if framecount == (framerate/2):
        framecount = 0
        cv2.imshow('image',img)
        try:
            facesCurFrame = face_recognition.face_locations(imgS)
            all_face_encodings["pari {}".format(count)] = face_recognition.face_encodings(imgS,facesCurFrame)[0]
            count = count + 1
        except:
            pass
    k = cv2.waitKey(30) & 0xff
    if k==27:
        break
    if count > 10   :
        break
# Release the VideoCapture object
cap.release()

# ... etc ...

with open('media/dataset_faces.xml', 'wb') as f:
    pickle.dump(all_face_encodings, f)

with open('dataset_faces.xml', 'rb') as f:
	all_face_encodings = pickle.load(f)

face_names = list(all_face_encodings.keys())
face_encodings = np.array(list(all_face_encodings.values()))
print(face_names,face_encodings)

result = face_recognition.compare_faces(face_encodings, face_encodings)
names_with_result = list(zip(face_names, result))
print(result)
print(names_with_result)
len(names_with_result)
res = 0
for key,val in names_with_result:
    if "pari" in key and val == True:
        res = res + 1
if res >= (len(names_with_result)/2):
    print("match")
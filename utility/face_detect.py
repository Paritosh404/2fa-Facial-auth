import cv2
import numpy as np
import face_recognition
import time
import pickle
def face_encode(path):
    all_face_encodings = {}
    # Load the cascade
    TIMER = int(5)
    # To capture video from webcam. 
    #cap = cv2.VideoCapture(0)
    # To use a video file as input 
    cap = cv2.VideoCapture('media/{}.mp4'.format(path))
    framerate = int(cap.get(cv2.CAP_PROP_FPS))
    if framerate % 2 != 0:
        framerate = framerate-1
    framecount = (framerate/2)-1
    count = 0
    while True:
        
        # Read and display each frame
        success, img = cap.read()
        framecount += 1
        try:
            imgS = cv2.resize(img,(0,0),None,0.25,0.25)
            imgS = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        except:
            break
        # Convert to grayscale
        
        if framecount == (framerate/2):
            framecount = 0
            cv2.imshow('image',img)
            try:
                facesCurFrame = face_recognition.face_locations(imgS)
                all_face_encodings["{0} {1}".format(path,count)] = face_recognition.face_encodings(imgS,facesCurFrame)[0]
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
    cv2.destroyAllWindows()
    # ... etc ...

    with open('media/{}.xml'.format(path), 'wb') as f:
        pickle.dump(all_face_encodings, f)

    return "{}.xml".format(path)

def check_face_encode(path):
    all_face_encodings = {}
    # Load the cascade
    TIMER = int(5)
    # To capture video from webcam. 
    #cap = cv2.VideoCapture(0)
    # To use a video file as input 
    cap = cv2.VideoCapture('media/{}.mp4'.format(path))
    framerate = int(cap.get(cv2.CAP_PROP_FPS))
    if framerate % 2 != 0:
        framerate = framerate-1
    framecount = (framerate/2)-1
    count = 0
    while True:
        
        # Read and display each frame
        success, img = cap.read()
        framecount += 1
        try:
            imgS = cv2.resize(img,(0,0),None,0.25,0.25)
            imgS = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        except:
            break
        # Convert to grayscale
        
        if framecount == (framerate/2):
            framecount = 0
            cv2.imshow('image',img)
            try:
                facesCurFrame = face_recognition.face_locations(imgS)
                all_face_encodings["{0} {1}".format(path,count)] = face_recognition.face_encodings(imgS,facesCurFrame)[0]
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
    cv2.destroyAllWindows()
    # ... etc ...

    with open('media/{}_check.xml'.format(path), 'wb') as f:
        pickle.dump(all_face_encodings, f)

    return "{}_check.xml".format(path)

def compair(path1,path2):
    
    with open('media/{}'.format(path1), 'rb') as f:
	    all_face_encodings = pickle.load(f)

    with open('media/{}'.format(path2), 'rb') as g:
	    all_check_face_encodings = pickle.load(g)

    face_encodings = np.array(list(all_face_encodings.values()))
    check_face_encodings = np.array(list(all_check_face_encodings.values()))
    result = face_recognition.compare_faces(face_encodings, check_face_encodings)
    res = 0
    for val in result:
        if val == True:
            res = res + 1
    print(res)
    if res >= (len(result)/2):
        print()
        return True
    else:
        return False
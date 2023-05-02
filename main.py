import cv2
import os
import pickle
import face_recognition
import numpy as np
import cvzone
from datetime import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage


cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL':"https://facerecognitionrealtime-3afbe-default-rtdb.firebaseio.com/",
    'storageBucket':"facerecognitionrealtime-3afbe.appspot.com"
})

bucket = storage.bucket()  


cap=cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

imgBackground=cv2.imread('Resources/background.png')

## Importing the mode images into list of imgModeList
ModefolderPath = 'Resources/Modes'
ModepathList=os.listdir(ModefolderPath)
#print(ModepathList)

imgModeList = []
for path in ModepathList:
    imgModeList.append(cv2.imread(os.path.join(ModefolderPath,path)))
    
# Load the encoding file
file= open('EncodeFile.p', 'rb')
encodeListKnownwithIds = pickle.load(file)
file.close()
encodeListknown, students_Ids = encodeListKnownwithIds

modeType = 0
counter = 0
id=-1
imgStudent = []

while True:
    success, img =cap.read()

    imgS= cv2.resize(img, (0,0), None, 0.25, 0.25)
    imgS= cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    imgBackground[162:162+480,55:55+640] = img
    imgBackground[44:44+633, 808:808+414] = imgModeList[modeType]
    
    if faceCurFrame:
   
        for encodeface, faceloc in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodeListknown, encodeface)
            faceDis = face_recognition.face_distance(encodeListknown, encodeface)
            # print("matches: ", matches)
            # print("faceDis: ", faceDis)
            
            matchIndex = np.argmin(faceDis)
            # print("matchIndex: ",matchIndex)
                    
            if matches[matchIndex]:
                # print("known face Detected")
                # print("student id: ",students_Ids[matchIndex])
                y1,x2,y2,x1 = faceloc                  #locating the bbox in the face
                y1,x2,y2,x1 = y1*4, x2*4, y2*4, x1*4
                bbox = 55+x1, 162+y1, x2-x1, y2-y1
                imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)
                
                id=students_Ids[matchIndex]
                if counter == 0:
                    cvzone.putTextRect(imgBackground, "Loading...", (275, 400))
                    cv2.imshow('Face Attendance', imgBackground)
                    cv2.waitKey(1)
                    counter = 1
                    modeType = 1
        
        if counter!= 0:

            if counter ==1:  
                
                # Get the Data from DB         
                studentInfo = db.reference(f"students/{id}").get()
                print(studentInfo)
                
                #Get the Image from Storage
                blob = bucket.get_blob(f"Images/{id}.png")
                array = np.frombuffer(blob.download_as_string(), np.uint8)
                imgStudent = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)
                
            #finding the diff betwn current time and time in db and mark it as timeElasped
                datetimeObject = datetime.strptime(studentInfo['last_attendance_time'], "%Y-%m-%d %H:%M:%S") 
                secondsElapsed = (datetime.now()-datetimeObject).total_seconds()
                # print(secondsElapsed)
                
                if secondsElapsed > 60:   # if time elapsed is more than 7200 seconds(2 hours), then only attendance will be marked 
                
                    #Update data of attendance and datetime in db
                    ref=db.reference(f"students/{id}")
                    studentInfo['total_attendance'] +=1
                    ref.child('total_attendance').set(studentInfo['total_attendance'])
                    ref.child('last_attendance_time').set(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                else:
                    modeType = 3
                    counter = 0
                    imgBackground[44:44+633, 808:808+414] = imgModeList[modeType]
                    
        if modeType != 3:
            
            if 10< counter <20:
                modeType= 2
            imgBackground[44:44+633, 808:808+414] = imgModeList[modeType]
                
            if counter<=10:    
                cv2.putText(imgBackground, str(studentInfo['total_attendance']), (861,125), 
                            cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255) ,1)
                cv2.putText(imgBackground, str(studentInfo['profession']), (1006, 550), 
                            cv2.FONT_HERSHEY_COMPLEX, 0.5, (255,255,255) , 1)
                cv2.putText(imgBackground, str(id), (1006, 493), 
                            cv2.FONT_HERSHEY_COMPLEX, 0.6, (255,255,255) , 1)
                cv2.putText(imgBackground, str(studentInfo['Conduct']), (910, 625), 
                            cv2.FONT_HERSHEY_COMPLEX, 0.5, (75, 75, 75) , 1)
                cv2.putText(imgBackground, str(studentInfo['year']), (1025, 625), 
                            cv2.FONT_HERSHEY_COMPLEX, 0.6, (75, 75, 75) , 1)
                cv2.putText(imgBackground, str(studentInfo['starting_year']), (1125, 625), 
                            cv2.FONT_HERSHEY_COMPLEX, 0.6, (75, 75, 75) , 1)
                
                # get the Name text size and put it in center of the imgBackground
                (w,h), _= cv2.getTextSize(studentInfo['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                offset = (414-w)//2
                cv2.putText(imgBackground, str(studentInfo['name']), (808+offset, 445), 
                            cv2.FONT_HERSHEY_COMPLEX, 1, (50,50,50) ,1)
                
                imgBackground[175:175+216, 909:909+216] = imgStudent
            
        
            counter += 1
            
            if counter >= 20:
                counter = 0
                modeType = 0
                studentInfo = []
                imgStudent = []
                imgBackground[44:44+633, 808:808+414] = imgModeList[modeType]
                                 
    else:
        modeType = 0
        counter = 0
        
    # cv2.imshow('Webcam', img)
    cv2.imshow('Face Attendance', imgBackground)
    cv2.waitKey(5)
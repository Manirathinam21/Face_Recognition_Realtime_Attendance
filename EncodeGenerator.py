import cv2
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage


cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL':"https://facerecognitionrealtime-3afbe-default-rtdb.firebaseio.com/",
    'storageBucket':"facerecognitionrealtime-3afbe.appspot.com"
})


## Importing the studen images
folderPath = 'Images'
imgPathList=os.listdir(folderPath)
students_Ids=[]
imgList = []
for path in imgPathList:
    imgList.append(cv2.imread(os.path.join(folderPath,path)))
    #path.split('.')[0]
    students_Ids.append(path.split('.')[0])
    
    #uploading the images to firebase storage bucket
    fileName = f"{folderPath}/{path}"
    bucket = storage.bucket()    
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)

def findEncodings(imagesList):
#function to generate a encoding list for each image     
    encodedList=[]
    for image in imagesList:
        img =  cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0] 
        encodedList.append(encode)
    return encodedList
 
print("Encodings started...") 
encodeListknown = findEncodings(imgList)
encodeListKnownwithIds= [encodeListknown, students_Ids]
print("Encoding complete")    

file= open("EncodeFile.p", 'wb')
pickle.dump(encodeListKnownwithIds, file)
file.close()
print('File saved')
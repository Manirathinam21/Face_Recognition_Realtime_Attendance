import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL':"https://facerecognitionrealtime-3afbe-default-rtdb.firebaseio.com/"
})

ref = db.reference('students')

data={
    "20230101":{"name": "Prabhakaran",
                "profession": "Geopolitics",
                "starting_year": 2018,
                "total_attendance": 5,
                "Conduct": "Good",
                "year": 5,
                "last_attendance_time": "2023-04-26 00:54:34"
                },
    
    "20230102":{"name": "Elon Musk",
                "profession": "Entrepreneur",
                "starting_year": 2019,
                "total_attendance": 4,
                "Conduct": "Good",
                "year": 4,
                "last_attendance_time": "2023-04-26 01:05:25"
                },
    
    "20230103":{"name": "Emly Blunt",
                "profession": "Actress",
                "starting_year": 2020,
                "total_attendance": 6,
                "Conduct": "Bad",
                "year": 3,
                "last_attendance_time": "2023-04-26 01:02:14"
                },
    
    "20230104":{"name": "Aishwarya Rai",
                "profession": "Actress",
                "starting_year": 2017,
                "total_attendance": 7,
                "Conduct": "Good",
                "year": 6,
                "last_attendance_time": "2023-04-26 00:45:08"
                },
    
    "20230105":{"name": "Bruce Lee",
                "profession": "Actor",
                "starting_year": 2015,
                "total_attendance": 9,
                "Conduct": "Good",
                "year": 8,
                "last_attendance_time": "2023-04-26 01:10:45"
                },
    
    "20230106":{"name": "Malathy",
                "profession": "Commerce",
                "starting_year": 2021,
                "total_attendance": 4,
                "Conduct": "Good",
                "year": 2,
                "last_attendance_time": "2023-04-26 00:50:28"
                },
    
    "20230108":{"name": "Manirathinam",
                "profession": "Data scientist",
                "starting_year": 2020,
                "total_attendance": 5,
                "Conduct": "Good",
                "year": 3,
                "last_attendance_time": "2023-04-26 00:55:19"
                },
    
    "20230110":{"name": "Sachin Tendulkar",
                "profession": "Cricketer",
                "starting_year": 2013,
                "total_attendance": 11,
                "Conduct": "Good",
                "year": 10,
                "last_attendance_time": "2023-04-26 00:48:11"
                }
    
    
}

for key, value in data.items():
    ref.child(key).set(value)
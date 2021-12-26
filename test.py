import face_recognition
import cv2
import pickle

# image = face_recognition.load_image_file("C:/Users/Joyel/Desktop/WIN_20211223_22_13_07_Pro.jpg")
# face_encoding = face_recognition.face_encodings(image)[0]

known_faces = []
usr_names = []

try:
    with open("saved_embeds.pt" , "rb") as f:
        known_faces = pickle.load(f)
except:
    pass

# known_faces = known_faces + [face_encoding]

# with open("saved_embeds.pt" , "wb") as f:
#     pickle.dump(known_faces, f)

# name = "Arnold"
# name2 = []

# try:
#     with open("usr_names.pt" , "rb") as f:
#         name2 = pickle.load(f)
# except:
#     pass

# usr_names = name2 + [name]

# with open("usr_names.pt", "wb") as f:
#     pickle.dump(usr_names, f)

# usr_names = []


# with open("usr_names.pt", "rb") as f:
#     usr_names = pickle.load(f)

usr_names = ["Joyel", "Arnold"]

name = None

cap = cv2.VideoCapture(0)

while True:
            ret, frame = cap.read()
            if ret:
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
                face_locations = face_recognition.face_locations(rgb_frame)
                face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

                face_names = []

                for face_encoding in face_encodings:
                    match = face_recognition.compare_faces(known_faces, face_encoding, tolerance=0.4)
                    name = None

                    for i in range(len(match)):
                        if match[i]:
                            name = usr_names[i]
                            print(name)
                            break
                            
                
                    face_names.append(name)

                for (top, right, bottom, left), name in zip(face_locations, face_names):
                    if not name:
                        continue

                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                    cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                    font = cv2.FONT_HERSHEY_DUPLEX
                    cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

                cv2.imshow("frame", frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

cap.release()
cv2.destroyAllWindows()

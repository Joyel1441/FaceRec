import face_recognition
import cv2
import pickle

cap = cv2.VideoCapture(0)

while True:
            ret, frame = cap.read()
            if ret:
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
                face_locations = face_recognition.face_locations(rgb_frame)
                if not face_locations:
                    print("No face detected")

                for (top, right, bottom, left) in face_locations:

                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                cv2.imshow("frame", frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

cap.release()
cv2.destroyAllWindows()

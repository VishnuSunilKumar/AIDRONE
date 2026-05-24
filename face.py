import cv2
import numpy as np

face_cascade = cv2.CascadeClassifier('cascades/haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    # Draw rectangles around detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    # Get face count
    face_count = len(faces)

    # Display the count on screen (top-right corner)
    text = f"Faces: {face_count}"
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.8
    color = (0, 0, 0)  # Green color
    
    thickness = 2

    # Get text size to position it neatly
    text_size, _ = cv2.getTextSize(text, font, font_scale, thickness)
    text_x = frame.shape[1] - text_size[0] - 10  # 10px from right edge
    text_y = 30  # 30px from top edge

    cv2.putText(frame, text, (text_x, text_y), font, font_scale, color, thickness)

    cv2.imshow('Face Detection', frame)

    # Quit when 'q' is pressed
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()

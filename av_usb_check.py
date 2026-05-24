import cv2

cap = cv2.VideoCapture(1)

while True:
    ret, frame = cap.read()

    if ret:
        cv2.imshow("AV Feed", frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
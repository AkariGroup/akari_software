import cv2

cap = cv2.VideoCapture(20)

while True:
    ret, frame = cap.read()
    cv2.imshow('camera' , frame)
    if cv2.waitKey(10) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
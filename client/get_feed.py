import cv2

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")

while True:
    #capture frame by frame
    ret, frame = cap.read()

    if not ret:
        print("Can't recieve frame (stream end?). Exiting...")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('frame', gray)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
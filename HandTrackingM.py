import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()  # See the default parameters by CTRL+Right click on .Hands
mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0

while True:
    success, img = cap.read()  # gives us our frame
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # convert image to RGB, because hands only uses RGB
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for handLandmarks in results.multi_hand_landmarks:
            for id, lm in enumerate(handLandmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)  # position of center
                cv2.circle(img, (cx, cy), 10, (255, 0, 0), cv2.FILLED)

            mpDraw.draw_landmarks(img, handLandmarks, mpHands.HAND_CONNECTIONS)

    # create a fps counter
    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime

    cv2.putText(img,str(int(fps)),(10,40), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255),2)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
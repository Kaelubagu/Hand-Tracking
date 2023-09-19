import cv2
import mediapipe as mp
import time
import numpy as np
import HandTrackingModule as htm
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

## parameters
widthCamera, heightCamera = 640, 480



cap = cv2.VideoCapture(0)
cap.set(3, widthCamera)
cap.set(4, heightCamera)
pTime = 0

detector = htm.handDetector(detectionCon=0.8)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
volRange = volume.GetVolumeRange()

minVolume = volRange[0]
maxVolume = volRange[1]
volumeBar = 400
vol = 0

while True:
    success, img = cap.read()
    img = detector.findHands(img)  # gives us the hand
    landmarkList = detector.findPosition(img, draw = False)
    if len(landmarkList) != 0:
        x1, y1 = landmarkList[4][1], landmarkList[4][2]
        x2, y2 = landmarkList[8][1], landmarkList[8][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        cv2.circle(img, (x1,y1), 14, (255,255,0), cv2.FILLED)
        cv2.circle(img, (x2, y2), 14, (255, 255, 0), cv2.FILLED)
        cv2.line(img, (x1,y1), (x2,y2), (255,0,0), 4)
        cv2.circle(img, (cx, cy), 10, (255, 255, 0), cv2.FILLED)

        length = math.hypot(x2 - x1, y2 - y1)

        if length < 50:
            cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)
        if length > 300:
                cv2.circle(img, (cx, cy), 10, (255, 0, 0), cv2.FILLED)

        vol = np.interp(length, [50,300], [minVolume, maxVolume])
        volumeBar = np.interp(length, [400, 150], [400, 150])
        volume.SetMasterVolumeLevel(vol, None)

        cv2.rectangle(img, (50, 150), (85,400), (0,255,0), 2)
        cv2.rectangle(img, (50, int(volumeBar)), (85, 400), (0, 255, 0), cv2.FILLED)



    #fps
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (40,70), cv2.FONT_HERSHEY_PLAIN, 4, (0,0,255), 3)


    cv2.imshow("Image", img)
    cv2.waitKey(1)
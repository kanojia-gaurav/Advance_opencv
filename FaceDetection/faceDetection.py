import mediapipe as mp
import cv2
import time

from mediapipe.python.solutions.face_detection import FaceDetection

wcam, hcam = 680, 480
cap = cv2.VideoCapture(0)
cap.set(3, wcam)
cap.set(4, hcam)
ptime = 0

mpFacedetecion = mp.solutions.face_detection
mpDraw = mp.solutions.drawing_utils
faceDetection = mpFacedetecion.FaceDetection()
#mpFace = mp.solutions.face_mesh



while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = faceDetection.process(imgRGB)
    #print(results)

    if results.detections:
        for id, detection in enumerate(results.detections):
            mpDraw.draw_detection(img, detection)

    ctime = time.time()
    fps =1/(ctime-ptime)
    ptime = ctime
    cv2.putText(img, f'FPS: {str(int(fps))}', (10,70), cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)
    cv2.imshow("image", img)
    cv2.waitKey(1)

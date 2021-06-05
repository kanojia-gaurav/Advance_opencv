import cv2
import mediapipe as mp
import time

wcam, hcam = 680, 480
cap = cv2.VideoCapture(0)
cap.set(3, wcam)
cap.set(4, hcam)
ptime = 0

mpDraw = mp.solutions.drawing_utils
mpFaceMesh = mp.solutions.face_mesh
faceMesh = mpFaceMesh.FaceMesh(max_num_faces=2)
drawspecs= mpDraw.DrawingSpec(thickness = 1, circle_radius = 2)


while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = faceMesh.process(img)
    print(results)

    if results.multi_face_landmarks:
        for landmarks in results.multi_face_landmarks:
            mpDraw.draw_landmarks(img, landmarks, mpFaceMesh.FACE_CONNECTIONS,drawspecs,drawspecs)
    

    ctime = time.time()
    fps =1/(ctime-ptime)
    ptime = ctime
    cv2.putText(img, f'FPS: {str(int(fps))}', (10,70), cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)
    cv2.imshow("image", img)
    cv2.waitKey(1)
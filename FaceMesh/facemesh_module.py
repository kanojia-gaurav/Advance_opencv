import cv2
import mediapipe as mp
import time

class facemeshDetector():
    def __init__(self, static_image_mode=False,max_num_faces=2,min_detection_confidence=0.5,min_tracking_confidence=0.5):
        self.static_image_model = static_image_mode
        self.max_num_faces = max_num_faces
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence

        self.mpDraw = mp.solutions.drawing_utils
        self.mpFaceMesh = mp.solutions.face_mesh
        self.faceMesh = self.mpFaceMesh.FaceMesh( self.static_image_model,self.max_num_faces,self.min_detection_confidence,self.min_tracking_confidence)
        self.drawspecs= self.mpDraw.DrawingSpec(thickness = 1, circle_radius = 2)

    def findfaceMesh(self, img, draw = True):
        self.imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.faceMesh.process(self.imgRGB)
        if self.results.multi_face_landmarks:
            for landmarks in self.results.multi_face_landmarks:
                self.mpDraw.draw_landmarks(img, landmarks, self.mpFaceMesh.FACE_CONNECTIONS,self.drawspecs,self.drawspecs)

        return img

wcam, hcam = 680, 480
cap = cv2.VideoCapture(0)
cap.set(3, wcam)
cap.set(4, hcam)
ptime = 0
detector = facemeshDetector()

while True:
    sucess, img = cap.read()
    img = detector.findfaceMesh(img)
        
       
    ctime = time.time()
    fps = 1/(ctime-ptime)
    ptime = ctime
    cv2.putText(img, f'FPS: {str(int(fps))}', (10,70), cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)
    cv2.imshow("Image", img)
    cv2.waitKey(1)



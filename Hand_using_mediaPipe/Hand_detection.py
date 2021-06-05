# -*- coding: utf-8 -*-
"""
Created on Sun May 30 11:19:57 2021

@author: Gaurav
"""
import cv2
import mediapipe as mp
import time
from google.protobuf.json_format import MessageToDict

cap = cv2.VideoCapture(0)

mphands = mp.solutions.hands
hands = mphands.Hands()
mpDraw =  mp.solutions.drawing_utils


ptime = 0
ctime = 0


while True:
    sucess, img = cap.read()
    
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 
    results = hands.process(imgRGB)

    #which hands is displaying
    for i,h in enumerate(results.multi_handedness):
        #print(i,h)
        print((h.classification)[0].label)
    
    #print(results.multi_hand_landmarks)
    
    
    if results.multi_hand_landmarks:
        for handles in results.multi_hand_landmarks:
            for id, lm in enumerate(handles.landmark):
                #print(id, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                #print(id, cx, cy)
            mpDraw.draw_landmarks(img, handles, mphands.HAND_CONNECTIONS)
            
    ctime = time.time()
    fps =1/(ctime-ptime)
    ptime = ctime
    cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)
    
    cv2.imshow("Image", img)
    cv2.waitKey(1)
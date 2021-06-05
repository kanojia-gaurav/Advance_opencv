# -*- coding: utf-8 -*-
"""
Created on Mon May 31 11:54:47 2021

@author: Gaurav
"""


import cv2
import mediapipe as mp
import time


class handDetector():
    def __init__(self,mode=False,maxhands = 2, detectionconfi = 0.5, trackconfi = 0.5):
        self.mode = mode
        self.maxhands = maxhands
        self.detectionconfi = detectionconfi
        self.trackconfi = trackconfi
        
        self.mphands = mp.solutions.hands
        self.hands = self.mphands.Hands(self.mode,self.maxhands,self.detectionconfi,self.trackconfi)
        self.mpDraw =  mp.solutions.drawing_utils
        
    
    def findhands(self,img, draw = True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 
        self.results = self.hands.process(imgRGB)
        #print(results.multi_hand_landmarks)
        
        if self.results.multi_hand_landmarks:
            for handles in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handles, self.mphands.HAND_CONNECTIONS)
        return img  
    
    def findposition(self,img, handno=0, draw = True):
        lmlist = []
        if self.results.multi_hand_landmarks:
            myhand = self.results.multi_hand_landmarks[handno]
            for id, lm in enumerate(myhand.landmark):
                #print(id, lm)
                
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                #print(id, cx, cy)
                lmlist.append([id, cx, cy])
            
        return lmlist

    def whichHand(self,img, handno=0, draw = True):
        if self.results.multi_handedness:
            for i,h in enumerate(self.results.multi_handedness):
                #print(i,h)
                return (h.classification)[0].label
    

def main():
    ptime = 0
    ctime = 0
    cap = cv2.VideoCapture(0)
    detector = handDetector()

    while True:
        sucess, img = cap.read()
        img = detector.findhands(img)
        lmlist = detector.findposition(img)
        whichHand = detector.whichHand(img)
        if len(lmlist)!=0:
            print(lmlist[4])
        ctime = time.time()
        fps =1/(ctime-ptime)
        ptime = ctime
        cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)
    
        cv2.imshow("Image", img)
        cv2.waitKey(1)

if __name__ == "__main__":
    main()
# -*- coding: utf-8 -*-
"""
Created on Mon May 31 12:37:02 2021

@author: Gaurav
"""


import cv2
import time
import numpy as np
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import hand_tracking_module as htm


wcam, hcam = 680, 480
cap = cv2.VideoCapture(0)
cap.set(3, wcam)
cap.set(4, hcam)
ptime = 0

detector = htm.handDetector(detectionconfi = 0.7)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volume.GetVolumeRange()
volrange = volume.GetVolumeRange()
volume.SetMasterVolumeLevel( 0, None)

minval = volrange[0]
maxval = volrange[1]

while True:
    success, img = cap.read()
    img = detector.findhands(img)   
    lmlist = detector.findposition(img, draw=False)
    if len(lmlist)!=0:
        #print(lmlist[4], lmlist[8])
        
        x1, y1 = lmlist[4][1], lmlist[4][2]
        x2, y2 = lmlist[8][1], lmlist[8][2]
        cx, cy = (x1+x2)//2, (y1+y2)//2
        
        cv2.circle(img, (x1, y1), 7, (255,0,255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 7, (255,0,255), cv2.FILLED)
        cv2.circle(img, (cx, cy), 7, (255,0,255), cv2.FILLED)
        cv2.line(img, (x1,y1), (x2, y2), (255,0,255), 3)
        
        length = math.hypot(((x2-x1)), (y2-y1))
        #print(length)
        
        #hand range 25 to 200
        #vol range -65 to 0
        
        vol = np.interp(length,[30,195],[minval, maxval])
        print(int(length),vol)
        volume.SetMasterVolumeLevel(vol, None)
        
        if length<20:
            cv2.circle(img, (cx, cy), 7, (0,255,0), cv2.FILLED)
    
    ctime = time.time()
    fps =1/(ctime-ptime)
    ptime = ctime
    cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)
    cv2.imshow("image", img)
    cv2.waitKey(1)
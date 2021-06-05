import hand_tracking_module as htm
import cv2
import time

wcam, hcam = 680, 480
cap = cv2.VideoCapture(0)
cap.set(3, wcam)
cap.set(4, hcam)
ptime = 0

detector = htm.handDetector(detectionconfi = 0.7)


fingertips = [4,8,12,16,20]

while True:
    success, img = cap.read()
    img = detector.findhands(img)   
    lmlist = detector.findposition(img, draw=False)
    whichHand = detector.whichHand(img)
    if len(lmlist)!=0:
        #print(lmlist[4], lmlist[8],)
        
        if whichHand == "Left":
            finger = []

            if lmlist[fingertips[0]][1] > lmlist[fingertips[0]-1][1]:
                    #print("index finger")
                    finger.append(1)   
            else:
                    finger.append(0)
            for id in range(1,5):
                if lmlist[fingertips[id]][2] < lmlist[fingertips[id]-2][2]:
                    #print("index finger")
                    finger.append(1)
                else:
                    finger.append(0)
            #print(finger)
            totalfinger = finger.count(1)
            #print(totalfinger)
            cv2.putText(img, str(totalfinger), (20, 255), cv2.FONT_HERSHEY_PLAIN,15,(255,0,255), 20)
        else:
            finger = []

            if lmlist[fingertips[0]][1] < lmlist[fingertips[0]-1][1]:
                    #print("index finger")
                    finger.append(1)   
            else:
                    finger.append(0)
            for id in range(1,5):
                if lmlist[fingertips[id]][2] < lmlist[fingertips[id]-2][2]:
                    #print("index finger")
                    finger.append(1)
                else:
                    finger.append(0)
            #print(finger)
            totalfinger = finger.count(1)
            #print(totalfinger)
            cv2.putText(img, str(totalfinger), (20, 255), cv2.FONT_HERSHEY_PLAIN,15,(255,0,255), 20)

    ctime = time.time()
    fps =1/(ctime-ptime)
    ptime = ctime
    cv2.putText(img, f'FPS: {str(int(fps))}', (10,70), cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)
    cv2.imshow("image", img)
    cv2.waitKey(1)
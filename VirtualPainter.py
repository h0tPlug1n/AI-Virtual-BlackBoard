import cv2
import numpy as np
import time
import os
import HandTrackingModule as htm 

brushThickness=7
eraserThickness = 50

folderPath = "header"
myList = os.listdir(folderPath)
# print(myList)
overlayList=[]
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)
# print(len(overlayList))
header = overlayList[0]
drawColor=(0,0,255)


cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)
detector = htm.handDetector(detectionCon=0.85)
xp,yp=0,0

imageCanvas = np.zeros((1080,1920,3),np.uint8)
imageCanvas.fill(255)
while True:

    #1. Import image
    success, img = cap.read()
    img = cv2.flip(img,1)

    #2. find hand landmarks
    img = detector.findHands(img)
    lmList=detector.findPosition(img, draw=False)

    if len(lmList)!=0:
        # print(lmList)

        #tip of index and middle finger
        x1,y1=lmList[8][1:]
        x2,y2=lmList[12][1:]



        #3. checking which fingers are up
        
        fingers = detector.fingersUp()
        # print(fingers)
        
        #4. if selection mode - 2 fingers are up
        
        if fingers[1] and fingers[2]:
            xp,yp = 0,0

            print("Selection mode")
            cv2.putText(img, "Selection mode", (60,225), cv2.FONT_HERSHEY_PLAIN, 5,
                    (0, 0, 255), 10)

            #checking for the click
            if y1<125:
                if 250<x1<450: #red
                    header=overlayList[0]
                    drawColor=(0,0,255) #in bgr format
                elif 450<x1<650: #green
                    header=overlayList[1]
                    drawColor=(0,255,0)
                elif 650<x1<800: #blue
                    header=overlayList[2]
                    drawColor=(255,0,0)
                elif 820<x1<900: #black
                    header=overlayList[3]
                    drawColor=(0,0,0)
                elif 920<x1<1200: #eraser=white
                    header=overlayList[4]
                    drawColor=(255,255,255)

            cv2.rectangle(img, (x1,y1-15), (x2,y2+15), drawColor, cv2.FILLED)

        #5. if drawing mode - index finger is up

        if fingers[1] and fingers[2] == False:
            cv2.circle(img, (x1,y1), 15, drawColor, cv2.FILLED)

            print("Drawing mode")
            cv2.putText(img, "Drawing mode", (60,225), cv2.FONT_HERSHEY_PLAIN, 5,
                    (0, 0, 255), 10)
            if xp==0 and yp==0:
                xp,yp=x1,y1

            if drawColor==(255,255,255):
                cv2.line(img, (xp,yp),(x1,y1), drawColor, eraserThickness)
                cv2.line(imageCanvas, (xp,yp),(x1,y1), drawColor, eraserThickness)
            else:    
                cv2.line(img, (xp,yp),(x1,y1), drawColor, brushThickness)
                cv2.line(imageCanvas, (xp,yp),(x1,y1), drawColor, brushThickness)

            xp,yp=x1,y1

    #setting the header image


    img[0:125, 0:1280] = header
    cv2.imshow("Image",img)
    cv2.imshow("Image Canvas",imageCanvas)
    cv2.waitKey(1)
import cv2
import numpy as np
import imutils

#initialize variables
cap = cv2.VideoCapture("video.avi")
firstFrame = None
count= 0
text= "empty"


while 1:
    ret, img = cap.read()
    #if no more frames break
    if not ret:
        break
    #resize de video
    img = imutils.resize(img, width=300,height=300)
    #convert to gray all the frames
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #save the first frame
    if firstFrame is None:
		firstFrame = gray
		continue

    #get the difference between the first frame and the current frame
    differenceImage = cv2.absdiff(firstFrame,gray)
    #get threhold from the difference (white: difference, black:same)
    ret,thresholdImage = cv2.threshold(differenceImage,30,255,cv2.THRESH_BINARY)
    #make a better binary image
    dilateImage = cv2.dilate(thresholdImage,None,iterations=2)
    #get the contour of the cars (white)
    image, contours,hierarchy = cv2.findContours(thresholdImage.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    #get some extra functions with moments
    moments = cv2.moments(dilateImage,True)
    area = moments['m00']

    #counter of the cars
    if area >=100:
        #get the average o the box (x,y)
        x=int(moments['m10']/moments['m00'])
        y=int (moments['m01']/moments['m00'])
        #if the center point satisfies then counter +1
        if x>150 and x<162 and y>72 and y<130:
            count+=1
            print count
            print 'a'
        elif x>102 and x<110 and y>45 and y<60:
            count+=1
            print count
            print 'b'

    #draw a green box
    for cnt in contours:
        if cv2.contourArea(cnt) > 500:
            text ="car"
            x,y,w,h = cv2.boundingRect(cnt)
            cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
        else:
            text = "empty"

    #put dynamic text
    cv2.putText(img,"status: {}".format(text), (10, 20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    #show both images
    cv2.imshow('img',img)
    cv2.imshow('diff',dilateImage)

    #press esc when you want to quit from the while bucle
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

#end the program
cap.release()
cv2.destroyAllWindows()

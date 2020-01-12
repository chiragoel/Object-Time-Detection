 -*- coding: utf-8 -*-
"""
Created on Wed Aug 21 01:11:55 2019

@author: DELL
"""

import cv2 
from datetime import datetime
import pandas as pd

video = cv2.VideoCapture(0)
a=1
first_frame = None
status_list = [None,None]
times= []
df = pd.DataFrame(columns=["Start","End"]) 
while True:
    a=a+1
    check,frame = video.read()
    status = 0
    print(frame)
    gray= cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray,(21,21),0)
    if first_frame is None:
        first_frame=gray
        continue
    delta_frame = cv2.absdiff(first_frame,gray)
    thresh_delta = cv2.threshold(delta_frame,30,255,cv2.THRESH_BINARY)[1]
    thresh_delta = cv2.dilate(thresh_delta,None,iterations=0)
    (_,cnts,_) = cv2.findContours(thresh_delta.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    #record time only if the contour area is greater than 1000
    for contour in cnts:
        if cv2.contourArea(contour)<1000:
            continue
        status=1
     #from a box around the object
        (x,y,w,h) = cv2.boundingRect(contour)
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3)
    status_list.append(status)
    status_list = status_list[-2:]
    if status_list[-1]==1 and status_list[-2]==0:
        times.append(datetime.now())
    if status_list[-1]==0 and status_list[-2]==1:
        times.append(datetime.now())
    
    cv2.imshow("Capture",gray)
    cv2.imshow("delta",delta_frame)
    cv2.imshow("thresh",thresh_delta)
    cv2.imshow("frame",frame)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
print(a)
print(status_list)
print(times)
#Saving each objects entry and exit time in a file
for i in range(0,len(times),2):
	df = df.append({"Start":times[i],"End":times[i+1]},ignore_index=True)
df.to_csv("Times.csv")
video.release()
cv2.destroyAllWindows()
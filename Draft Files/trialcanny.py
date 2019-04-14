import cv2
import numpy as np

drugShape= 'Circle'
drugColor= 'White'
drugName= 'UNDEFINED'
panLine= cv2.imread('/media/yomna/New Volume/2nd term/Project/circle.png',1)
#panLine = cv2.resize(panLine, (0, 0), None, .20, .20)
cv2.imshow('originalPanLine',panLine)

edges = cv2.Canny(panLine,100,200)

im2, contours, hierarchy = cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

#cv2.drawContours(panLine, contours, -1, (0,0,255), 3)
#for cnt in contours :
approx= cv2.approxPolyDP(contours[0], 0.01*cv2.arcLength(contours[0],True), True)
cv2.drawContours(panLine, [approx], 0,(255,0,0), 2)
x=approx.ravel()[0]
y=approx.ravel()[1]

print('nooo', len(approx))
if 6<len(approx)<15 :
	drugShape='Ellipse'


if drugShape == 'Ellipse' and drugColor== 'White':
	drugName= 'Panadol'

print(drugName)


cv2.imshow('___', panLine)





cv2.waitKey()

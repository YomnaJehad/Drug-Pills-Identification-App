import numpy as np
import cv2

panLine= cv2.imread('PanLine.jpeg',1)
panLine = cv2.resize(panLine, (0, 0), None, .20, .20)
cv2.imshow('originalPanLine',panLine)


panAE= cv2.imread('PanAE.jpeg',1)
panAE = cv2.resize(panAE, (0, 0), None, .20, .20)
#cv2.imshow('originalPanAE',panAE)



blur = cv2.GaussianBlur(panLine,(5,5),0)
mask = cv2.inRange(blur,(100, 100, 100) , (255, 255, 255) )
#mask=~mask
im2, contours, hierarchy = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
print(contours)
cv2.drawContours(panLine, contours, -1, (0,0,255), 3)
cv2.imshow('triall', panLine)           





# blur = cv2.GaussianBlur(panAE,(5,5),0)
# mask = cv2.inRange(blur,(100, 100, 100) , (255, 255, 255) )
# mask=~mask
# #im2, contours, hierarchy = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

# cv2.imshow('triallll', mask)           








cv2.waitKey()



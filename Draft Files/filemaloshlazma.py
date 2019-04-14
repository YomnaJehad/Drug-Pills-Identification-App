import cv2
import numpy as np
im = cv2.imread('/media/yomna/New Volume/2nd term/Project/PanAE.jpeg')

im = cv2.resize(im, (0, 0), None, .5, .5)

gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
im2,contours,h = cv2.findContours(gray,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)


mask = np.zeros(im.shape, np.uint8)
#for cnt in contours:

	#cv2.drawContours(mask, cnt, -1, 255, -1)

edges = cv2.Canny(im,100,200)

im2, contours, hierarchy = cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
x,y,w,h = cv2.boundingRect(contours[0]) # offsets - with this you get 'mask'
newIM = im[y:y+h,x:x+w]
yn = newIM.shape[0]
xn = newIM.shape[1]
#cv2.rectangle(im,(x,y),(x+w,y+h),(0,255,0),2)
y=y + int(yn * 15/100)
h=h - int(yn * 30/100)
x=x + int(xn * 15/100) 
w=w - int(xn * 30/100)

print(y, h, x, w, yn, xn, yn * 10/100)

cv2.imshow('cutted contour',im[y:y+h,x:x+w])

print('Average color (BGR): ',np.array(cv2.mean(im[y:y+h,x:x+w])).astype(np.uint8))
# cv2.imshow('  ' , mask)
# b,g,r,_ =np.uint8( cv2.mean(im))
#print(mean_)
# final = np.zeros(im.shape,np.uint8)
# mask = np.zeros(gray.shape,np.uint8)

# for i in range(0,len(contours)):
#     mask[...]=0
#     cv2.drawContours(mask,contours,i,255,-1)
#     cv2.drawContours(final,contours,i,cv2.mean(im,mask),-1)

#cv2.imshow('im',im)
# cv2.imshow('final',final)
cv2.waitKey()
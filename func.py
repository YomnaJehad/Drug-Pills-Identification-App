import cv2
import numpy as np
import knn_classifier

#cv2.imshow('originalPanLine',panLine)

def detectShape(path):
	img= cv2.imread(path,1)
	cv2.imshow('))', img)
	
	img = cv2.resize(img, (0, 0), None, .20, .20)

	drugShape = 'UNDEFINED'
	edges = cv2.Canny(img,100,200)
	im2, contours, hierarchy = cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	approx = cv2.approxPolyDP(contours[0], 0.01*cv2.arcLength(contours[0],True), True)	
	x,y,w,h = cv2.boundingRect(contours[0]) # offsets - with this you get 'mask'
	newIM = img[y:y+h,x:x+w]
	yn = newIM.shape[0]
	xn = newIM.shape[1]
	#cv2.rectangle(im,(x,y),(x+w,y+h),(0,255,0),2)
	y=y + int(yn * 15/100)
	h=h - int(yn * 30/100)
	x=x + int(xn * 15/100) 
	w=w - int(xn * 30/100)
	colors = np.array(cv2.mean(img[y:y+h,x:x+w])).astype(np.uint8)
	prediction = 'n.a.'
	prediction = knn_classifier.main('training.data', np.array([colors[2], colors[1], colors[0]]))
	print(colors[2], colors[1], colors[0])

	return len(approx), prediction


detectShape('/media/yomna/New Volume/2nd term/Project/cataflamketaba.png')
def detectDrug(path):
	lenn,color=detectShape(path)
	print(lenn,color)
	drugShape= 'UNDEFINED'
	drugName= 'UNDEFINED'
	if 6 < lenn < 13:
		drugShape = 'Ellipse'
	elif lenn >= 13:
		drugShape = 'Circle'
	if drugShape == 'Ellipse' and color == 'white':
		drugName = 'Panadol'
	if drugShape == 'Circle' and color =='orange':
		drugName= 'cataflam'


	return drugName


print(detectDrug('/media/yomna/New Volume/2nd term/Project/PanLine.jpeg'))

cv2.waitKey()
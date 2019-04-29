import cv2
import numpy as np
import knn_classifier
import csv



def detectShape(path):
	img= cv2.imread(path,1)
	img = cv2.resize(img, (0, 0), None, .5, .5)

	img = cv2.GaussianBlur(img, (3,3), 0)
	kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
	img = cv2.filter2D(img, -1, kernel)
	
	drugShape = 'UNDEFINED'
	edges = cv2.Canny(img,100,200)
	im2,contours, hierarchy = cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

	areas = np.array([cv2.contourArea(c) for c in contours])
	contours = np.array(contours)
	arr1inds = areas.argsort()
	contours = contours[arr1inds[::-1]]
	

	approx = cv2.approxPolyDP(contours[0], 0.01*cv2.arcLength(contours[0],True), True)	
	x,y,w,h = cv2.boundingRect(contours[0]) # offsets - with this you get 'mask'


	#cv2.drawContours(img, [contours[0]], 0,(255,0,0), 2)
	#cv2.imshow(path, img)



	newIM = img[y:y+h,x:x+w]
	yn = newIM.shape[0]
	xn = newIM.shape[1]
	#cv2.rectangle(im,(x,y),(x+w,y+h),(0,255,0),2)
	y=y + int(yn * 15/100)
	h=h - int(yn * 30/100)
	x=x + int(xn * 15/100) 
	w=w - int(xn * 30/100)
	# cv2.imshow(path, img)
	newImage = img[y:y+h,x:x+w]
	colors = np.array(cv2.mean(newImage)).astype(np.uint8)
	prediction = 'n.a.'


	#INCREASE SATURATION BEFORE WHITE DETECTION FOR LIGHT CLOLORS ELEMINATION
	# cv2.imshow('before', newImage)
	hsvImage = cv2.cvtColor(newImage, cv2.COLOR_BGR2HSV)
	
	hsvImage[:,:,1]=hsvImage[:,:,1] *2.5

	backImage = cv2.cvtColor(hsvImage, cv2.COLOR_HSV2BGR)
 	# cv2.imshow('after', backImage)


	# using rbg
	backColors = np.array(cv2.mean(backImage)).astype(np.uint8)
	prediction = knn_classifier.main('training.data', np.array([backColors[2], backColors[1], backColors[0]]))
	# print(np.array([backColors[2], backColors[1], backColors[0]]))
	if prediction =='white':
		#RED GREEN BLUE
		if backColors[2] >= 180 and backColors[1] >= 150 and backColors[0] <= 90 :
			prediction = 'other'	



	if prediction == 'other':

		# using hsv
		colors = rgb2hsv(colors[2], colors[1], colors[0])
		prediction = knn_classifier.main('newData.data', np.array([colors[0], colors[1], colors[2]]))
		# print(colors[2], colors[1], colors[0])

	return len(approx), prediction, contours[0]


def detectDrug(path):
	lenn, color, contour = detectShape(path)
	# print(lenn,color)
	drugShape= 'UNDEFINED'
	drugName= 'UNDEFINED'
	print(lenn)
	if 5 < lenn < 13:
		drugShape = 'Ellipse'
	elif lenn == 6:
		drugShape = 'Hexagon'
	elif lenn == 5:
		drugShape = 'Pentagon'
	elif lenn == 4:
		x,y,w,h = cv2.boundingRect(contour)
		ar = w / float(h)
		drugShape = "square" if ar >= 0.95 and ar <= 1.05 else "rectangle"
	elif lenn >= 13:
		drugShape = 'Circle'


	# if drugShape == 'Ellipse' and color == 'white':
	# 	drugName = 'Panadol'
	# if drugShape == 'Circle' and color =='orange':
	# 	drugName= 'cataflam'


	return drugShape, color


def getName(path):
	Name = 'UNDEFINED'
	dictt = {}
	dictt[("Circle", "lightPink")] = "Milga"
	dictt[("Ellipse", "white")] = "Panadol"
	dictt[("Circle", "pink")] = "Bruffin"
	dictt[("Ellipse", "yellow")] = "Ketofan"
	dictt[("Circle", "white")] = "Paracetamol"
	dictt[("Ellipse", "red")] = "Comtrex"
	dictt[("Circle", "lightBlue")] = "Alphintern"
	dictt[("Circle", "orange")] = "Cataflam"
	



	drugShape, color = detectDrug(path)




	Name = dictt[(drugShape, color)]
	return Name




print('panLine', detectDrug('PanLine.jpeg'))
print('panAE', detectDrug('PanAE.jpeg'))
print('brufin', detectDrug('bruf.jpg'))

print('com1', detectDrug('com1.jpg'))
print('com2', detectDrug('com2.jpg'))
print('com3	', detectDrug('com3.jpg'))

print('alpha1', detectDrug('alpha1.jpg'))
print('alpha2', detectDrug('alpha2.jpg'))
print('alpha3', detectDrug('alpha3.jpg'))


print('kito1', detectDrug('kito1.jpg'))
print('kito2', detectDrug('kito2.jpg'))
print('kito3', detectDrug('kito3.jpg'))
print('kito4', detectDrug('kito4.jpg'))


print('milga1', detectDrug('milga1.jpg'))
print('milga2', detectDrug('milga2.jpg'))
print('milga3', detectDrug('milga3.jpg'))


print('para1', detectDrug('para1.jpg'))
print('para2', detectDrug('para2.jpg'))
print('para3', detectDrug('para3.jpg'))
print('para4', detectDrug('para4.jpg'))

print('cataflam', detectDrug('cataflamsada.png'))

#print(getName('milga3.jpg'))





cv2.waitKey()





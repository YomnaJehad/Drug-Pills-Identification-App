import cv2
import numpy as np
import knn_classifier
import csv

def rgb2hsv(r, g, b):
    r = r / 255.0
    g = g / 255.0
    b = b / 255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    df = mx-mn
    if mx == mn:
        h = 0
    elif mx == r:
        h = (60 * ((g-b)/df) + 360) % 360
    elif mx == g:
        h = (60 * ((b-r)/df) + 120) % 360
    elif mx == b:
        h = (60 * ((r-g)/df) + 240) % 360
    if mx == 0:
        s = 0
    else:
        s = df/mx
    v = mx
    return h, s, v


def detectShape(path):
	img= cv2.imread(path,1)

	img = cv2.resize(img, (0, 0), None, .5, .5)
	drugShape = 'UNDEFINED'
	edges = cv2.Canny(img,100,200)
	contours, hierarchy = cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
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
	# cv2.imshow(path, img)
	newImage = img[y:y+h,x:x+w]
	colors = np.array(cv2.mean(newImage)).astype(np.uint8)
	prediction = 'n.a.'

	# using rbg
	# prediction = knn_classifier.main('training.data', np.array([colors[2], colors[1], colors[0]]))

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
	
	if 6 < lenn < 13:
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


print('circle', detectDrug('circle.png'))
print('ellipse', detectDrug('ellipse.png'))
print('hexagon', detectDrug('hexagon.png'))
print('rec', detectDrug('rec.jpg'))
print('square', detectDrug('square.jpeg'))
print('pentagon', detectDrug('pentagon.jpg'))

# print(detectDrug('/media/yomna/New Volume/2nd term/Project/PanLine.jpeg'))

cv2.waitKey()




# create hsv training data
# newData = []
# with open("training.data") as csvfile:
# 	lines = csv.reader(csvfile)
# 	dataset = list(lines)
# 	for x in range(len(dataset)):
# 		data = rgb2hsv(int(dataset[x][0]), int(dataset[x][1]), int(dataset[x][2]))
# 		newData.append([data[0], data[1], data[2], dataset[x][3]])


# with open("newData.data", 'w', newline='') as csvfile:
	# writer = csv.writer(csvfile)
	# writer.writerows(newData)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import base64
import cv2
from io import StringIO
import io
import numpy as np
import numpy as np
from . import knn_classifier
import json

# Create your views here.

def data_uri_to_cv2_img(uri):
    encoded_data = uri.split(',')[1]
    nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img

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


def detectShape(img):
	# img= cv2.imread(path,1)
	img = cv2.resize(img, (0, 0), None, .5, .5)
	img = cv2.GaussianBlur(img, (3,3), 0)
	kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
	img = cv2.filter2D(img, -1, kernel)
	
	drugShape = 'UNDEFINED'
	edges = cv2.Canny(img,100,200)
	contours, hierarchy = cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

	areas = np.array([cv2.contourArea(c) for c in contours])
	contours = np.array(contours)
	arr1inds = areas.argsort()
	contours = contours[arr1inds[::-1]]
	
	approx = cv2.approxPolyDP(contours[0], 0.01*cv2.arcLength(contours[0],True), True)	
	x,y,w,h = cv2.boundingRect(contours[0]) # offsets - with this you get 'mask'

	cv2.drawContours(img, [contours[0]], 0,(255,0,0), 2)

	newIM = img[y:y+h,x:x+w]
	yn = newIM.shape[0]
	xn = newIM.shape[1]

	y=y + int(yn * 15/100)
	h=h - int(yn * 30/100)
	x=x + int(xn * 15/100) 
	w=w - int(xn * 30/100)

	newImage = img[y:y+h,x:x+w]
	colors = np.array(cv2.mean(newImage)).astype(np.uint8)
	prediction = 'n.a.'

	hsvImage = cv2.cvtColor(newImage, cv2.COLOR_BGR2HSV)
	hsvImage[:,:,1]=hsvImage[:,:,1] *2.5
	backImage = cv2.cvtColor(hsvImage, cv2.COLOR_HSV2BGR)

	# using rbg
	backColors = np.array(cv2.mean(backImage)).astype(np.uint8)
	prediction = knn_classifier.main('training.data', np.array([backColors[2], backColors[1], backColors[0]]))
	if prediction =='white':
		#RED GREEN BLUE
		if backColors[2] >= 180 and backColors[1] >= 150 and backColors[0] <= 90 :
			prediction = 'other'	

	if prediction == 'other':
		# using hsv
		colors = rgb2hsv(colors[2], colors[1], colors[0])
		prediction = knn_classifier.main('newData.data', np.array([colors[0], colors[1], colors[2]]))
	return len(approx), prediction, contours[0]



def detectDrug(img):
	lenn, color, contour = detectShape(img)
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
	return drugShape, color

def getName(img):
	name = "UNDEFINED"
	description = "UNDEFINED"
	shape, color = detectDrug(img)

	with open("details.json", encoding='utf-8-sig') as json_file:
		json_data = json.load(json_file)
	# print(json_data)
	for element in json_data:
		print(element)
		if shape == element["shape"] and color == element["color"]:
			name = element["name"]
			description = element["description"]

	return name, description

class pill(APIView):
	def post(self, request):
		base64_string = request.data["img"]
		pillDetected = getName(data_uri_to_cv2_img(base64_string))
		return Response({"name":pillDetected[0], "description":pillDetected[1]}, status=status.HTTP_200_OK)
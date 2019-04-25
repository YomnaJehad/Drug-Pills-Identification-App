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

# Create your views here.

def data_uri_to_cv2_img(uri):
    encoded_data = uri.split(',')[1]
    nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img


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

	# using rbg
	prediction = knn_classifier.main('training.data', np.array([colors[2], colors[1], colors[0]]))

	# using hsv
	# colors = rgb2hsv(colors[2], colors[1], colors[0])
	# prediction = knn_classifier.main('newData.data', np.array([colors[0], colors[1], colors[2]]))
	# print(colors[2], colors[1], colors[0])
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


class pill(APIView):
    def post(self, request):
        base64_string = request.data["img"]
        shapeDetected = detectShape(data_uri_to_cv2_img(base64_string))
        return Response({"len":shapeDetected[0], "pred":shapeDetected[1]}, status=status.HTTP_200_OK)
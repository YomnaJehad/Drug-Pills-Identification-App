import csv
import numpy as np

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

# create hsv training data
newData = []
with open("pinkrgb.data") as csvfile:
	lines = csv.reader(csvfile)
	dataset = list(lines)
	for x in range(len(dataset)):
		data = rgb2hsv(int(dataset[x][0]), int(dataset[x][1]), int(dataset[x][2]))
		newData.append([data[0], data[1], data[2], dataset[x][3]])


with open("pinkhsv.data", 'w', newline='') as csvfile:
	writer = csv.writer(csvfile)
	writer.writerows(newData)
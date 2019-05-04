from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import

import matplotlib.pyplot as plt
import numpy as np

f=open("newData.data", "r")
if f.mode == 'r':
	contents = f.read()
	contents = contents.split("\n")

ax = ()
ay = ()
az = ()
#aw = ()
for i in contents:
	s = i.split(",")
	ax += (float(s[0]),)
	ay += (float(s[1]),)
	az += (float(s[2]),)
	#aw += (float(s[3]),)
xs = [ax]
ys = [ay]
zs = [az]

# print(type(xs))
#ax = [(0.0,1.0,0.5450980392156862)]
#ay = [(6.470588235294144,1.0,0.8)]
#az = [(352.71844660194176,1.0,0.807843137254902)]
# print(type(ax[0][0]))
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.scatter(xs[0], ys[0], zs[0])
#ax.scatter(ax[0], ay[0], az[0])

ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')



plt.show()
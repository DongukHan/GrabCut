# GrabCut
# Copyright(C) 2016 Orcuslc
# the executable script.

import sys
import os
import numpy as np
from main import GCClient
import re
import cv2

osname = os.name

nargin = len(sys.argv)

if nargin < 2:
	raise ImportError('More args needed')
elif nargin == 2:
	imgroute = sys.argv[1]
	iteration_count = 1
	component_count = 5
elif nargin == 3:
	imgroute = sys.argv[1]
	iteration_count = sys.argv[2]
	component_count = 5
else:
	imgroute = sys.argv[1]
	iteration_count = sys.argv[2]
	component_count = sys.argv[3]

img = re.findall(r'^\S+\.\S+?(?:\\|/)+?', imgroute[::-1])[0][::-1]

if osname == 'nt':
	imgname = re.findall(r'^\S+\.', img[2:])[0][:-1]
elif osname == 'posix':
	imgname = re.findall(r'^\S+\.', img[1:])[0][:-1]

if not os.path.isfile(imgroute):
	raise ImportError("Not a valid image")

try:
	img = cv2.imread(imgroute, cv2.IMREAD_COLOR)
except AttributeError:
	raise ImportError("Not a valid image")

output = np.zeros(img.shape, np.uint8)

GC = GCClient(img, component_count)
cv2.namedWindow('output')
cv2.namedWindow('input')
a = cv2.setMouseCallback('input', GC.init_mask)
cv2.moveWindow('input', img.shape[0]+10, img.shape[1]+10)

count = 0
flag = False
print("Instructions: \n")
print("Draw a rectangle around the object using right mouse button \n")

while True:
	cv2.imshow('output', output)
	cv2.imshow('input', np.asarray(GC.img, dtype=np.uint8))
	k = 0xFF & cv2.waitKey(1)

	if k == 27:
		break
	elif k == ord('s'):
		cv2.imwrite('%s_gc.jpg'%(imgname), output)
		print("Result saved as image %s_gc.jpg"%(imgname))
	elif k == ord('n'):
		if count == 0:
			GC.run()
			count += 1
		else:
			GC.iter(iteration_count)
		flag = True
	
	elif k == ord('0'):
		print('Mark background regions with left mouse button \n')
		GC._DRAW_VAL = GC._DRAW_BG
		GC.iter(1)
		flag = True
		# output = GC.show(output)

	elif k == ord('1'):
		print('Mark foreground regions with left mouse button \n')
		GC._DRAW_VAL = GC._DRAW_FG
		GC.iter(1)
		flag = True
		# output = GC.show(output)

	elif k == ord('2'):
		print('Mark prob. background regions with left mouse button \n')
		GC._DRAW_VAL = GC._DRAW_PR_BG
		GC.iter(1)
		flag = True

	elif k == ord('3'):
		print('Mark prob. foreground regions with left mouse button \n')
		GC._DRAW_VAL = GC._DRAW_PR_FG
		GC.iter(1)
		flag = True


	FGD = np.where((GC._mask == 1) + (GC._mask == 3), 255, 0).astype('uint8')
	
	if flag == True:
		output = cv2.bitwise_and(GC.img2, GC.img2, mask = FGD)
		flag = False

cv2.destroyAllWindows()
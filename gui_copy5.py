from find_fac import length
#from fine_tune import fine_tune,process_one_image
from manual import mancon
#from histogram import plotX
#from unit_selection import get_units
from merge import merge
from tkinter import *
from PIL import Image, ImageTk
from tkinter import filedialog
import os
import matplotlib.pyplot as plt
from tkSliderWidget import Slider 
import numpy as np
import numpy as np
import imutils
import cv2
import cv2 as cv
import os
from skimage import morphology, measure
import argparse
import skimage.io as io
import matplotlib.pyplot as plt
import time

from skimage import color
from functools import partial
from mpl_toolkits.mplot3d import Axes3D
from tkinter import *
from PIL import Image, ImageTk
from tkinter import filedialog
import numpy as np
import imutils
import cv2 as cv
import os
from skimage import morphology, measure
import argparse
import skimage.io as io
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')
import time

from skimage import color
from functools import partial
from mpl_toolkits.mplot3d import Axes3D
from tkinter import *
from PIL import Image, ImageTk
from tkinter import filedialog
from functools import partial
from datetime import date
import sys
import cv2
import MySQLdb
path = ''
try:
	path = str(sys.argv[1])+"\\" +str(sys.argv[2])
	buff1 = cv2.imread(path)
	buff2 = buff1.shape
except AttributeError:
	path = str(sys.argv[1])+"/" +str(sys.argv[2])
	buff1 = cv2.imread(path)
	buff2 = buff1.shape

print(path)
#--------------------------------------------------------------------------Manual Contouring/Lazzo
import cv2
import numpy as np
import random as rng
from functools import partial
pt1_x , pt1_y = None , None
drawing = False
import os
fine_cnts = []
cnts = []

def process_lazzo_image(img_path,blur_val,cann,size,dst_val,factor,scale):
	img = cv2.imread(img_path)
	#img = cv2.resize(img, (1500, 1000))
	#img= cv2.add(img,np.array([-50.0]))
	img = cv2.resize(img, (img.shape[:2][1]//scale,img.shape[:2][0]//scale))
	temp_image = img.copy()
	temp = img.copy()
	img = cv2.bilateralFilter(img,blur_val,75,75)
	
	#gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY,(0.1,0.2,0.7),1)
	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	kernel = np.ones((5,5),np.uint8)
	#gray = cv2.GaussianBlur(gray,(5,5),0)
	#gray = cv2.Canny(gray,50,100,(5,5),5,8)
	gray = cv2.Canny(gray,cann,2*cann)
	gray = cv2.dilate(gray,kernel,iterations = 1)
	ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

	# noise removal
	kernel = np.ones((5,5),np.uint8)
	#kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
	opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 1)
	closing = cv2.morphologyEx(opening,cv2.MORPH_CLOSE,kernel, iterations = 1)
	#closing = cv2.erode(closing,kernel,iterations = 2)
	#cv2.imshow('mati',closing)
	
	# sure background area
	sure_bg = cv2.dilate(thresh,kernel,iterations=1)

	# Finding sure foreground area
	dist_transform = cv2.distanceTransform(sure_bg,cv2.DIST_L2,3)

	# Threshold
	ret, sure_fg = cv2.threshold(dist_transform,dst_val*dist_transform.max(),255,0)

	# Finding unknown region
	sure_fg = np.uint8(sure_fg)
	unknown = cv2.subtract(sure_bg,sure_fg)

	# Marker labelling
	ret, markers = cv2.connectedComponents(sure_fg)

	# Add one to all labels so that sure background is not 0, but 1
	markers = markers+1

	# Now, mark the region of unknown with zero
	markers[unknown==255] = 0

	markers = cv2.watershed(img,markers)
	
	img[markers == -1] = [255,0,0]

	#------------------------------------
	import imutils
	import random as rng
	contours = []

	# loop over the unique labels, and append contours to all_cnts
	labels = markers
	for label in np.unique(labels):
			if label == 0:
					continue

			# draw_lazzo label on the mask
			mask = np.zeros(thresh.shape, dtype="uint8")
			mask[labels == label] = 255

			# detect contours in the mask and grab the largest one
			cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
			#im2, cnts, hierarchy = cv2.findContours(mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
			cnts = imutils.grab_contours(cnts)
			#c = max(cnts, key=cv2.contourArea)
			for c in cnts:
				contours.append(c)

	# draw_lazzo new contours in red color
	for c in contours:
			#Ignore small contours
			x,y,_ = img.shape
			if cv2.contourArea(c) > 1 and cv2.contourArea(c) < (x*y)/4:
				color = (rng.randint(0,256), rng.randint(0,256), rng.randint(0,256))
				((x, y), r) = cv2.minEnclosingCircle(c)
				#color = (255,0,0)
				l = round(2*r*factor,2)
				if l > size:
								cv2.drawContours(temp_image,[c], 0, color,2)
				'''((x, y), r) = cv2.minEnclosingCircle(c)
				cv2.circle(temp_image, (int(x), int(y)), int(r), color, 1)
				cv2.putText(temp_image, "#{}".format(2*round(r,2)), (int(x) - 10, int(y)),cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)'''
				
	#print(i)
	#print(contours)
	return (temp_image,contours)

def er_add_lazzo(cnpoint):
	global fine_cnts,cnts
	valp = 2
	cnts.append(cnpoint)
	#print(cnpoint)
	#if valp == 2:
	#	cnts.append(cnpoint)
	#if valp == 1:
	#	fine_cnts.append(cnpoint)



#brute force for case 2
#brute force
def remove_inside_points_lazzo(contours,fine_cnts,ref_contour):
	#global fine_cnts,cnts
	try:
		for i in range(len(contours)):
			cnt = contours[i]
			cnt_zip = [[ref_contour, tuple(x[0])] for x in contours[i]]
			find = lambda x: cv2.pointPolygonTest(x[0], x[1], False)
			cnt_check = np.array(list(map(find,cnt_zip)))
			cnt_out = cnt[cnt_check <= 0] #points inside are removed, only points on and outside stays
			contours[i] = cnt_out
		for i in range(len(fine_cnts)):
			cnt = fine_cnts[i]
			cnt_zip = [[ref_contour, tuple(x[0])] for x in fine_cnts[i]]
			find = lambda x: cv2.pointPolygonTest(x[0], x[1], False)
			cnt_check = np.array(list(map(find,cnt_zip)))
			cnt_out = cnt[cnt_check <= 0] #points inside are removed, only points on and outside stays
			fine_cnts[i] = cnt_out
	except:
		return(0,0)

	return (contours,fine_cnts)

def draw_lazzo(path, factor,size,scale):
	global fine_cnts,cnts
	temp_image = cv2.imread(path)
	temp_image = cv2.resize(temp_image, (temp_image.shape[:2][1]//scale,temp_image.shape[:2][0]//scale))
	for c in cnts:
				#Ignore small contours
				x,y,_ = temp_image.shape
				if cv2.contourArea(c) > 1 and cv2.contourArea(c) < (x*y)/4:
					color = (rng.randint(0,256), rng.randint(0,256), rng.randint(0,256))
					#color = (255,0,0)
					((x, y), r) = cv2.minEnclosingCircle(c)
					#color = (255,0,0)
					l = round(2*r*factor,2)
					if l > size:
									cv2.drawContours(temp_image,[c], 0, color,2)
	for c in fine_cnts:
				#Ignore small contours
				x,y,_ = temp_image.shape
				if cv2.contourArea(c) > 1 and cv2.contourArea(c) < (x*y)/4:
					#color = (rng.randint(0,256), rng.randint(0,256), rng.randint(0,256))
					#color = (255,0,0)
					((x, y), r) = cv2.minEnclosingCircle(c)
					#color = (255,0,0)
					l = round(2*r*factor,2)
					if l > size:
						cv2.drawContours(temp_image,[c], 0, (0,0,255),2)
	#Saving contoured image to output file
	org_name = path.split('/')[-1]
	out_name = 'output/'+ org_name.replace('_O.','_F.')
	cv2.imwrite(out_name,temp_image)
	
	return(temp_image)
				
	
#def drawing_contour_lazzo(img,cnts,path):
def drawing_contour_lazzo(img):
		contour_points = []
		def line_drawing(event,x,y,flags,param):#, drawing = False,pt1_x = None,pt1_y = None):
				global pt1_x,pt1_y,drawing
				if event==cv2.EVENT_LBUTTONDOWN:
						drawing=True
						pt1_x,pt1_y=x,y
						#print(path)
						#print(pt1_x,pt1_y)
						contour_points.append([[pt1_x,pt1_y]])

				elif event==cv2.EVENT_MOUSEMOVE:
						if drawing==True:
								cv2.line(img,(pt1_x,pt1_y),(x,y),color=(255,0,0),thickness=5)
								pt1_x,pt1_y=x,y
								#print(pt1_x,pt1_y)
								contour_points.append([[pt1_x,pt1_y]])

				elif event==cv2.EVENT_LBUTTONUP:
						drawing=False
						cv2.line(img,(pt1_x,pt1_y),(x,y),color=(255,0,0),thickness=5) 
						#print(pt1_x,pt1_y)
						contour_points.append([[pt1_x,pt1_y]])
						'''cnts = remove_inside(cnts,contour_points)
						cnts.append(contour_points)
						img = draw_lazzo(path, cnts)'''


		#img = cv2.imread(path)
		x,y,_ = img.shape
		#img = cv2.resize(img,(y//4,x//4))
		cv2.namedWindow('Manual Countouring Tool',cv2.WINDOW_NORMAL)

		cv2.setMouseCallback('Manual Countouring Tool',line_drawing)#,drawing = False,pt1_x = None,pt1_y = None))

		while(1):
				cv2.imshow('Manual Countouring Tool',img)
				if cv2.waitKey(1) & 0xFF == 27:
						break
						
		contour_points = np.array(contour_points)
		return contour_points


def calc_dia_lazzo(factor,size,img):
	global fine_cnts,cnts
	dia=[]
	fines=[]
	temp_image = img.copy()
	for c in cnts:
			#Ignore small contours
			x,y,_ = img.shape
			if cv2.contourArea(c) > 1 and cv2.contourArea(c) < (x*y)/4:
				#color = (rng.randint(0,256), rng.randint(0,256), rng.randint(0,256))
				((x, y), r) = cv2.minEnclosingCircle(c)
				#color = (255,0,0)
				l = round(2*r*factor,2)
				if l > size:
					dia.append(l)
					cv2.putText(temp_image, "#{}".format(2*round(r*factor,2)), (int(x) - 10, int(y)),cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,0,0), 2)
	for c in fine_cnts:
			#Ignore small contours
			x,y,_ = img.shape
			if cv2.contourArea(c) > 1 and cv2.contourArea(c) < (x*y)/4:
				fines.append(cv2.contourArea(c))
				cv2.putText(temp_image, "#{}".format(2*round(r*factor,2)), (int(x) - 10, int(y)),cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,0), 2)
	return(dia,temp_image,fines)
	
def NONE(val):
	pass

def mancon_lazzo(img_path,blur_val,cann,size,dst_val,factor,scale,name,PTrnpilesphotosId,PUserby):
	global fine_cnts,cnts
	#temp_image,cnts = process_lazzo_image(file_path,C3PO.blurr_val,C3PO.canny,C3PO.size,C3PO.dst_val,luke_skywalker.factor,int(e2.get()))
	#cv2.namedWindow('valp', cv2.WINDOW_NORMAL)
	#cv2.createTrackbar('valp','valp',0,2,NONE)
	temp_image=draw_lazzo(img_path, factor,size,scale)
	while(1):
		contour_points = drawing_contour_lazzo(temp_image)
		c,b = remove_inside_points_lazzo(cnts,fine_cnts,contour_points) #added
		if c == 0:
			break
		else:
			cnts = c
			fine_cnts = b
		er_add_lazzo(contour_points)
		temp_image = draw_lazzo(img_path,factor,size,scale)
		
	diameter,dia_image,fines = calc_dia_lazzo(factor,size,temp_image)
	x,y,_ = temp_image.shape
	#print(cnts)
	k = img_path.rfind("O")
	img_pat = img_path[:k] + "F" + img_path[k+1:]
	k = name.rfind("O")
	img_name = name[:k] + "F" + name[k+1:]
	
	path = r'C:\Users\USER\Manual contouring' # Location of modified image
	cv2.imwrite(os.path.join(path ,'AUTOSAVED_IMAGE_Manual_contouring.jpeg'),temp_image)
	
	cv2.imwrite(img_pat,dia_image)
	cv2.destroyAllWindows()
	#print(fines)
	db=MySQLdb.connect("75.126.169.58", "Xliconmys0618", "XlServMys1706#", "iocllive",3306,autocommit = True)
	cursor = db.cursor()
	lis=[int(PTrnpilesphotosId),img_name,img_pat,int(PUserby),int(1)]
	print(lis)
	result_args = cursor.callproc('PythonUpdatePilesPhotos', lis)
	
	cursor.close()
	db.close()

	#print(fines)
	return(diameter,fines,x*y)

#--------------------------------------------------------------------------Manual contouring/Undo
import cv2
import numpy as np
import random as rng
from functools import partial
pt1_x , pt1_y = None , None
drawing = False
import os


def process_undo_image(img_path,blur_val,cann,size,dst_val,factor,scale):
	img = cv2.imread(img_path)
	#img = cv2.resize(img, (1500, 1000))
	#img= cv2.add(img,np.array([-50.0]))
	img = cv2.resize(img, (img.shape[:2][1]//scale,img.shape[:2][0]//scale))
	temp_image = img.copy()
	temp = img.copy()
	img = cv2.bilateralFilter(img,blur_val,75,75)
	
	#gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY,(0.1,0.2,0.7),1)
	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	kernel = np.ones((5,5),np.uint8)
	#gray = cv2.GaussianBlur(gray,(5,5),0)
	#gray = cv2.Canny(gray,50,100,(5,5),5,8)
	gray = cv2.Canny(gray,cann,2*cann)
	gray = cv2.dilate(gray,kernel,iterations = 1)
	ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

	# noise removal
	kernel = np.ones((5,5),np.uint8)
	#kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
	opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 1)
	closing = cv2.morphologyEx(opening,cv2.MORPH_CLOSE,kernel, iterations = 1)
	#closing = cv2.erode(closing,kernel,iterations = 2)
	#cv2.imshow('mati',closing)
	
	# sure background area
	sure_bg = cv2.dilate(thresh,kernel,iterations=1)

	# Finding sure foreground area
	dist_transform = cv2.distanceTransform(sure_bg,cv2.DIST_L2,3)

	# Threshold
	ret, sure_fg = cv2.threshold(dist_transform,dst_val*dist_transform.max(),255,0)

	# Finding unknown region
	sure_fg = np.uint8(sure_fg)
	unknown = cv2.subtract(sure_bg,sure_fg)

	# Marker labelling
	ret, markers = cv2.connectedComponents(sure_fg)

	# Add one to all labels so that sure background is not 0, but 1
	markers = markers+1

	# Now, mark the region of unknown with zero
	markers[unknown==255] = 0

	markers = cv2.watershed(img,markers)
	
	img[markers == -1] = [255,0,0]

	#------------------------------------
	import imutils
	import random as rng
	contours = []

	# loop over the unique labels, and append contours to all_cnts
	labels = markers
	for label in np.unique(labels):
			if label == 0:
					continue

			# draw_undo label on the mask
			mask = np.zeros(thresh.shape, dtype="uint8")
			mask[labels == label] = 255

			# detect contours in the mask and grab the largest one
			cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
			#im2, cnts, hierarchy = cv2.findContours(mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
			cnts = imutils.grab_contours(cnts)
			#c = max(cnts, key=cv2.contourArea)
			for c in cnts:
				contours.append(c)

	# draw_undo new contours in red color
	for c in contours:
			#Ignore small contours
			x,y,_ = img.shape
			if cv2.contourArea(c) > 1 and cv2.contourArea(c) < (x*y)/4:
				color = (rng.randint(0,256), rng.randint(0,256), rng.randint(0,256))
				((x, y), r) = cv2.minEnclosingCircle(c)
				#color = (255,0,0)
				l = round(2*r*factor,2)
				if l > size:
								cv2.drawContours(temp_image,[c], 0, color,2)
				'''((x, y), r) = cv2.minEnclosingCircle(c)
				cv2.circle(temp_image, (int(x), int(y)), int(r), color, 1)
				cv2.putText(temp_image, "#{}".format(2*round(r,2)), (int(x) - 10, int(y)),cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)'''
				
	#print(i)
	#print(contours)
	return (temp_image,contours)

def er_add_undo(cnpoint):
	global fine_cnts,cnts
	valp = 0
	#print(cnpoint)
	#if valp == 2:
	#	cnts.append(cnpoint)
	#if valp == 1:
	#	fine_cnts.append(cnpoint)



#brute force for case 2
#brute force
def remove_inside_points_undo(contours,fine_cnts,ref_contour):
	#global fine_cnts,cnts
	try:
		for i in range(len(contours)):
			cnt = contours[i]
			cnt_zip = [[ref_contour, tuple(x[0])] for x in contours[i]]
			find = lambda x: cv2.pointPolygonTest(x[0], x[1], False)
			cnt_check = np.array(list(map(find,cnt_zip)))
			cnt_out = cnt[cnt_check <= 0] #points inside are removed, only points on and outside stays
			contours[i] = cnt_out
		for i in range(len(fine_cnts)):
			cnt = fine_cnts[i]
			cnt_zip = [[ref_contour, tuple(x[0])] for x in fine_cnts[i]]
			find = lambda x: cv2.pointPolygonTest(x[0], x[1], False)
			cnt_check = np.array(list(map(find,cnt_zip)))
			cnt_out = cnt[cnt_check <= 0] #points inside are removed, only points on and outside stays
			fine_cnts[i] = cnt_out
	except:
		return(0,0)

	return (contours,fine_cnts)

def draw_undo(path, factor,size,scale):
	global fine_cnts,cnts
	temp_image = cv2.imread(path)
	temp_image = cv2.resize(temp_image, (temp_image.shape[:2][1]//scale,temp_image.shape[:2][0]//scale))
	for c in cnts:
				#Ignore small contours
				x,y,_ = temp_image.shape
				if cv2.contourArea(c) > 1 and cv2.contourArea(c) < (x*y)/4:
					color = (rng.randint(0,256), rng.randint(0,256), rng.randint(0,256))
					#color = (255,0,0)
					((x, y), r) = cv2.minEnclosingCircle(c)
					#color = (255,0,0)
					l = round(2*r*factor,2)
					if l > size:
									cv2.drawContours(temp_image,[c], 0, color,2)
	for c in fine_cnts:
				#Ignore small contours
				x,y,_ = temp_image.shape
				if cv2.contourArea(c) > 1 and cv2.contourArea(c) < (x*y)/4:
					#color = (rng.randint(0,256), rng.randint(0,256), rng.randint(0,256))
					#color = (255,0,0)
					((x, y), r) = cv2.minEnclosingCircle(c)
					#color = (255,0,0)
					l = round(2*r*factor,2)
					if l > size:
						cv2.drawContours(temp_image,[c], 0, (0,0,255),2)
	#Saving contoured image to output file
	org_name = path.split('/')[-1]
	out_name = 'output/'+ org_name.replace('_O.','_F.')
	cv2.imwrite(out_name,temp_image)
	
	return(temp_image)
				
	
#def drawing_contour_undo(img,cnts,path):
def drawing_contour_undo(img):
		contour_points = []
		def line_drawing(event,x,y,flags,param):#, drawing = False,pt1_x = None,pt1_y = None):
				global pt1_x,pt1_y,drawing
				if event==cv2.EVENT_LBUTTONDOWN:
						drawing=True
						pt1_x,pt1_y=x,y
						#print(path)
						#print(pt1_x,pt1_y)
						contour_points.append([[pt1_x,pt1_y]])

				elif event==cv2.EVENT_MOUSEMOVE:
						if drawing==True:
								cv2.line(img,(pt1_x,pt1_y),(x,y),color=(255,0,0),thickness=5)
								pt1_x,pt1_y=x,y
								#print(pt1_x,pt1_y)
								contour_points.append([[pt1_x,pt1_y]])

				elif event==cv2.EVENT_LBUTTONUP:
						drawing=False
						cv2.line(img,(pt1_x,pt1_y),(x,y),color=(255,0,0),thickness=5) 
						#print(pt1_x,pt1_y)
						contour_points.append([[pt1_x,pt1_y]])
						'''cnts = remove_inside(cnts,contour_points)
						cnts.append(contour_points)
						img = draw_undo(path, cnts)'''


		#img = cv2.imread(path)
		x,y,_ = img.shape
		#img = cv2.resize(img,(y//4,x//4))
		cv2.namedWindow('Manual Countouring Tool',cv2.WINDOW_NORMAL)

		cv2.setMouseCallback('Manual Countouring Tool',line_drawing)#,drawing = False,pt1_x = None,pt1_y = None))

		while(1):
				cv2.imshow('Manual Countouring Tool',img)
				if cv2.waitKey(1) & 0xFF == 27:
						break
						
		contour_points = np.array(contour_points)
		return contour_points


def calc_dia_undo(factor,size,img):
	global fine_cnts,cnts
	dia=[]
	fines=[]
	temp_image = img.copy()
	for c in cnts:
			#Ignore small contours
			x,y,_ = img.shape
			if cv2.contourArea(c) > 1 and cv2.contourArea(c) < (x*y)/4:
				#color = (rng.randint(0,256), rng.randint(0,256), rng.randint(0,256))
				((x, y), r) = cv2.minEnclosingCircle(c)
				#color = (255,0,0)
				l = round(2*r*factor,2)
				if l > size:
					dia.append(l)
					cv2.putText(temp_image, "#{}".format(2*round(r*factor,2)), (int(x) - 10, int(y)),cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,0,0), 2)
	for c in fine_cnts:
			#Ignore small contours
			x,y,_ = img.shape
			if cv2.contourArea(c) > 1 and cv2.contourArea(c) < (x*y)/4:
				fines.append(cv2.contourArea(c))
				cv2.putText(temp_image, "#{}".format(2*round(r*factor,2)), (int(x) - 10, int(y)),cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,0), 2)
	return(dia,temp_image,fines)
	
def NONE(val):
	pass

def mancon_undo(img_path,blur_val,cann,size,dst_val,factor,scale,name,PTrnpilesphotosId,PUserby):
	global fine_cnts,cnts
	#temp_image,cnts = process_undo_image(file_path,C3PO.blurr_val,C3PO.canny,C3PO.size,C3PO.dst_val,luke_skywalker.factor,int(e2.get()))
	#cv2.namedWindow('valp', cv2.WINDOW_NORMAL)
	#cv2.createTrackbar('valp','valp',0,2,NONE)
	temp_image=draw_undo(img_path, factor,size,scale)
	while(1):
		contour_points = drawing_contour_undo(temp_image)
		c,b = remove_inside_points_undo(cnts,fine_cnts,contour_points) #added
		if c == 0:
			break
		else:
			cnts = c
			fine_cnts = b
		er_add_undo(contour_points)
		temp_image = draw_undo(img_path,factor,size,scale)
		
	diameter,dia_image,fines = calc_dia_undo(factor,size,temp_image)
	x,y,_ = temp_image.shape
	#print(cnts)
	k = img_path.rfind("O")
	img_pat = img_path[:k] + "F" + img_path[k+1:]
	k = name.rfind("O")
	img_name = name[:k] + "F" + name[k+1:]
	
	path = r'C:\Users\USER\Manual contouring' # Location of modified image
	cv2.imwrite(os.path.join(path ,'AUTOSAVED_IMAGE_Manual_contouring.jpeg'),temp_image)
	
	cv2.imwrite(img_pat,dia_image)
	cv2.destroyAllWindows()
	#print(fines)
	db=MySQLdb.connect("75.126.169.58", "Xliconmys0618", "XlServMys1706#", "iocllive",3306,autocommit = True)
	cursor = db.cursor()
	lis=[int(PTrnpilesphotosId),img_name,img_pat,int(PUserby),int(1)]
	print(lis)
	result_args = cursor.callproc('PythonUpdatePilesPhotos', lis)
	
	cursor.close()
	db.close()
	return(diameter,fines,x*y)

#--------------------------------------------------------------------------Manual contouring/Draw
import cv2
import numpy as np
import random as rng
from functools import partial
pt1_x , pt1_y = None , None
drawing = False
import os

def process_two_image(img_path,blur_val,cann,size,dst_val,factor,scale):
	img = cv2.imread(img_path)
	#img = cv2.resize(img, (1500, 1000))
	#img= cv2.add(img,np.array([-50.0]))
	img = cv2.resize(img, (img.shape[:2][1]//scale,img.shape[:2][0]//scale))
	temp_image = img.copy()
	temp = img.copy()
	img = cv2.bilateralFilter(img,blur_val,75,75)
	
	#gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY,(0.1,0.2,0.7),1)
	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	kernel = np.ones((5,5),np.uint8)
	#gray = cv2.GaussianBlur(gray,(5,5),0)
	#gray = cv2.Canny(gray,50,100,(5,5),5,8)
	gray = cv2.Canny(gray,cann,2*cann)
	gray = cv2.dilate(gray,kernel,iterations = 1)
	ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

	# noise removal
	kernel = np.ones((5,5),np.uint8)
	#kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
	opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 1)
	closing = cv2.morphologyEx(opening,cv2.MORPH_CLOSE,kernel, iterations = 1)
	#closing = cv2.erode(closing,kernel,iterations = 2)
	#cv2.imshow('mati',closing)
	
	# sure background area
	sure_bg = cv2.dilate(thresh,kernel,iterations=1)

	# Finding sure foreground area
	dist_transform = cv2.distanceTransform(sure_bg,cv2.DIST_L2,3)

	# Threshold
	ret, sure_fg = cv2.threshold(dist_transform,dst_val*dist_transform.max(),255,0)

	# Finding unknown region
	sure_fg = np.uint8(sure_fg)
	unknown = cv2.subtract(sure_bg,sure_fg)

	# Marker labelling
	ret, markers = cv2.connectedComponents(sure_fg)

	# Add one to all labels so that sure background is not 0, but 1
	markers = markers+1

	# Now, mark the region of unknown with zero
	markers[unknown==255] = 0

	markers = cv2.watershed(img,markers)
	
	img[markers == -1] = [255,0,0]

	#------------------------------------
	import imutils
	import random as rng
	contours = []

	# loop over the unique labels, and append contours to all_cnts
	labels = markers
	for label in np.unique(labels):
			if label == 0:
					continue

			# draw label on the mask
			mask = np.zeros(thresh.shape, dtype="uint8")
			mask[labels == label] = 255

			# detect contours in the mask and grab the largest one
			cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
			#im2, cnts, hierarchy = cv2.findContours(mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
			cnts = imutils.grab_contours(cnts)
			#c = max(cnts, key=cv2.contourArea)
			for c in cnts:
				contours.append(c)

	# Draw new contours in red color
	for c in contours:
			#Ignore small contours
			x,y,_ = img.shape
			if cv2.contourArea(c) > 1 and cv2.contourArea(c) < (x*y)/4:
				color = (rng.randint(0,256), rng.randint(0,256), rng.randint(0,256))
				((x, y), r) = cv2.minEnclosingCircle(c)
				#color = (255,0,0)
				l = round(2*r*factor,2)
				if l > size:
								cv2.drawContours(temp_image,[c], 0, color,2)
				'''((x, y), r) = cv2.minEnclosingCircle(c)
				cv2.circle(temp_image, (int(x), int(y)), int(r), color, 1)
				cv2.putText(temp_image, "#{}".format(2*round(r,2)), (int(x) - 10, int(y)),cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)'''
				
	#print(i)
	#print(contours)
	return (temp_image,contours)

def er_add(cnpoint):
	global fine_cnts,cnts
	valp = 1
	#global fine_cnts
	fine_cnts.append(cnpoint)
	##print(cnpoint)
	#if valp == 2:
	#	cnts.append(cnpoint)
	#if valp == 1:
	#	fine_cnts.append(cnpoint)



#brute force for case 2
#brute force
def remove_inside_points(contours,fine_cnts,ref_contour):
	#global fine_cnts,cnts
	#global fine_cnts
	try:
		for i in range(len(contours)):
			cnt = contours[i]
			cnt_zip = [[ref_contour, tuple(x[0])] for x in contours[i]]
			find = lambda x: cv2.pointPolygonTest(x[0], x[1], False)
			cnt_check = np.array(list(map(find,cnt_zip)))
			cnt_out = cnt[cnt_check <= 0] #points inside are removed, only points on and outside stays
			contours[i] = cnt_out
		for i in range(len(fine_cnts)):
			cnt = fine_cnts[i]
			cnt_zip = [[ref_contour, tuple(x[0])] for x in fine_cnts[i]]
			find = lambda x: cv2.pointPolygonTest(x[0], x[1], False)
			cnt_check = np.array(list(map(find,cnt_zip)))
			cnt_out = cnt[cnt_check <= 0] #points inside are removed, only points on and outside stays
			fine_cnts[i] = cnt_out
	except:
		return(0,0)

	return (contours,fine_cnts)

def draw(path,factor,size,scale):
	#global cnts
	global fine_cnts,cnts
	temp_image = cv2.imread(path)
	temp_image = cv2.resize(temp_image, (temp_image.shape[:2][1]//scale,temp_image.shape[:2][0]//scale))
	for c in cnts:
				#Ignore small contours
				x,y,_ = temp_image.shape
				if cv2.contourArea(c) > 1 and cv2.contourArea(c) < (x*y)/4:
					color = (rng.randint(0,256), rng.randint(0,256), rng.randint(0,256))
					#color = (255,0,0)
					((x, y), r) = cv2.minEnclosingCircle(c)
					#color = (255,0,0)
					l = round(2*r*factor,2)
					if l > size:
									cv2.drawContours(temp_image,[c], 0, color,2)
	for c in fine_cnts:
				#Ignore small contours
				x,y,_ = temp_image.shape
				if cv2.contourArea(c) > 1 and cv2.contourArea(c) < (x*y)/4:
					#color = (rng.randint(0,256), rng.randint(0,256), rng.randint(0,256))
					#color = (255,0,0)
					((x, y), r) = cv2.minEnclosingCircle(c)
					#color = (255,0,0)
					l = round(2*r*factor,2)
					if l > size:
						cv2.drawContours(temp_image,[c], 0, (0,0,255),2)
	#Saving contoured image to output file
	org_name = path.split('/')[-1]
	out_name = 'output/'+ org_name.replace('_O.','_F.')
	cv2.imwrite(out_name,temp_image)
	
	return(temp_image)
				
	
#def drawing_contour(img,cnts,path):
def drawing_contour(img):
		#global cnts
		contour_points = []
		def line_drawing(event,x,y,flags,param):#, drawing = False,pt1_x = None,pt1_y = None):
				global pt1_x,pt1_y,drawing
				if event==cv2.EVENT_LBUTTONDOWN:
						drawing=True
						pt1_x,pt1_y=x,y
						#print(path)
						#print(pt1_x,pt1_y)
						contour_points.append([[pt1_x,pt1_y]])

				elif event==cv2.EVENT_MOUSEMOVE:
						if drawing==True:
								cv2.line(img,(pt1_x,pt1_y),(x,y),color=(255,0,0),thickness=3)
								pt1_x,pt1_y=x,y
								#print(pt1_x,pt1_y)
								contour_points.append([[pt1_x,pt1_y]])

				elif event==cv2.EVENT_LBUTTONUP:
						drawing=False
						cv2.line(img,(pt1_x,pt1_y),(x,y),color=(255,0,0),thickness=3) 
						#print(pt1_x,pt1_y)
						contour_points.append([[pt1_x,pt1_y]])
						'''cnts = remove_inside(cnts,contour_points)
						cnts.append(contour_points)
						img = draw(path, cnts)'''


		#img = cv2.imread(path)
		x,y,_ = img.shape
		#img = cv2.resize(img,(y//4,x//4))
		cv2.namedWindow('Manual Countouring Tool',cv2.WINDOW_NORMAL)

		cv2.setMouseCallback('Manual Countouring Tool',line_drawing)#,drawing = False,pt1_x = None,pt1_y = None))

		while(1):
				cv2.imshow('Manual Countouring Tool',img)
				if cv2.waitKey(1) & 0xFF == 27:
						break
						
		contour_points = np.array(contour_points)
		return contour_points


def calc_dia(factor,size,img):
	global fine_cnts,cnts
	dia=[]
	fines=[]
	temp_image = img.copy()
	for c in cnts:
			#Ignore small contours
			x,y,_ = img.shape
			if cv2.contourArea(c) > 1 and cv2.contourArea(c) < (x*y)/4:
				#color = (rng.randint(0,256), rng.randint(0,256), rng.randint(0,256))
				((x, y), r) = cv2.minEnclosingCircle(c)
				#color = (255,0,0)
				l = round(2*r*factor,2)
				if l > size:
					dia.append(l)
					cv2.putText(temp_image, "#{}".format(2*round(r*factor,2)), (int(x) - 10, int(y)),cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,0,0), 2)
	for c in fine_cnts:
			#Ignore small contours
			x,y,_ = img.shape
			if cv2.contourArea(c) > 1 and cv2.contourArea(c) < (x*y)/4:
				fines.append(cv2.contourArea(c))
				cv2.putText(temp_image, "#{}".format(2*round(r*factor,2)), (int(x) - 10, int(y)),cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,0), 2)
	return(dia,temp_image,fines)
	
def NONE(val):
	pass

def mancon(img_path,blur_val,cann,size,dst_val,factor,scale,name,PTrnpilesphotosId,PUserby):
	global fine_cnts,cnts
	#temp_image,_ = process_two_image(file_path,C3PO.blurr_val,C3PO.canny,C3PO.size,C3PO.dst_val,luke_skywalker.factor,int(e2.get()))
	#cv2.namedWindow('valp', cv2.WINDOW_NORMAL)
	#cv2.createTrackbar('valp','valp',0,2,NONE)
	temp_image=draw(img_path, factor,size,scale)
	while(1):
		contour_points = drawing_contour(temp_image)
		c,b = remove_inside_points(cnts,fine_cnts,contour_points) #added
		if c == 0:
			break
		else:
			cnts = c
			fine_cnts = b
		er_add(contour_points)
		temp_image = draw(img_path,factor,size,scale)
		
	diameter,dia_image,fines = calc_dia(factor,size,temp_image)
	x,y,_ = temp_image.shape
	#print(cnts)
	k = img_path.rfind("O")
	img_pat = img_path[:k] + "F" + img_path[k+1:]
	k = name.rfind("O")
	img_name = name[:k] + "F" + name[k+1:]
	
	path = r'C:\Users\USER\Manual contouring' # Location of modified image
	cv2.imwrite(os.path.join(path ,'AUTOSAVED_IMAGE_Manual_contouring.jpeg'),temp_image)
	
	cv2.imwrite(img_pat,dia_image)
	cv2.destroyAllWindows()

	db=MySQLdb.connect("75.126.169.58", "Xliconmys0618", "XlServMys1706#", "iocllive",3306,autocommit = True)
	cursor = db.cursor()
	lis=[int(PTrnpilesphotosId),img_name,img_pat,int(PUserby),int(1)]
	print(lis)
	result_args = cursor.callproc('PythonUpdatePilesPhotos', lis)
	#com = 'call PythonUpdatePilesPhotos(18,"hi","h",5,"2021-5-15 16:46:00",1);'
	#print(com)
	#cursor.execute(com)
	cursor.close()
	db.close()
	return(diameter,fines,x*y)

#--------------------------------------------------------------------------Auto-Contouring
diameters=[]

def process_one_image(val,path,factor,scale):
    global temp_image
    img = cv2.imread(path)
    x,y,_ = img.shape
    img = cv2.resize(img,(y//scale,x//scale))
    
    kernel = np.ones((5,5),np.uint8)
    blurr_val = slider1.get()
    #print(blurr_val)
    canny = slider2.get()
    size = slider3.get()
    #size = s
    dst_val = slider4.get()
    dst_val = dst_val/100
    temp_image = img.copy()
    img = cv2.bilateralFilter(img,blurr_val,75,75)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    
    
    #gray = cv2.Canny(gray,canny_val,2*canny_val)
    gray = cv.Canny(gray, threshold1 = canny , threshold2 = 2*canny)
    
    
    
    gray = cv2.dilate(gray,kernel,iterations = 1)
    ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)


    # noise removal
    opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 1)
    closing = cv2.morphologyEx(opening,cv2.MORPH_CLOSE,kernel, iterations = 1)
  
    # sure background area
    sure_bg = cv2.dilate(thresh,kernel,iterations=1)

    # Finding sure foreground area
    dist_transform = cv2.distanceTransform(sure_bg,cv2.DIST_L2,3)

    # Threshold
    ret, sure_fg = cv2.threshold(dist_transform,dst_val*dist_transform.max(),255,0)

    # Finding unknown region
    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg,sure_fg)

    # Marker labelling
    ret, markers = cv2.connectedComponents(sure_fg)

    # Add one to all labels so that sure background is not 0, but 1
    markers = markers+1

    # Now, mark the region of unknown with zero
    markers[unknown==255] = 0

    markers = cv2.watershed(img,markers)
  
    img[markers == -1] = [255,0,0]
    


  #------------------------------------
    import imutils
    import random as rng
    contours = []

    # loop over the unique labels, and append contours to all_cnts
    labels = markers
    for label in np.unique(labels):
        if label == 0:
            continue

        # draw label on the mask
        mask = np.zeros(thresh.shape, dtype="uint8")
        mask[labels == label] = 255

        # detect contours in the mask and grab the largest one
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        #im2, cnts, hierarchy = cv2.findContours(mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        c = max(cnts, key=cv2.contourArea)
        for c in cnts:
            contours.append(c)
    contours = sorted(contours, key=lambda x: cv2.contourArea(x),reverse = True)[2:]
        
    global diameters
    for c in contours:
        #Ignore small contours
        x,y,_ = img.shape
        if cv2.contourArea(c) > 1 and cv2.contourArea(c) < (x*y)/4:
            color = (rng.randint(0,256), rng.randint(0,256), rng.randint(0,256))
            ((x, y), r) = cv2.minEnclosingCircle(c) #finding diameters of contours
            l = round(2*r*factor,2)
            if l > size:
                diameters.append(l)
                cv2.drawContours(temp_image,[c], 0, color,2)
                #cv2.circle(temp_image, (int(x), int(y)), int(r),(0,255,0), 1)
                #cv2.putText(temp_image, "{}cm".format(2*round(r*factor,2)), (int(x) - 10, int(y)),cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)
                
    cv2.imshow('Auto-Contouring', temp_image)
    


def fine_tune(path,factor,scale):
	global cnts
	
	'''
	cv2.namedWindow('blur', cv2.WINDOW_NORMAL)
	cv2.createTrackbar('blur','blur',25,500,partial(process_one_image,path=path,factor = factor,scale = scale))

	cv2.namedWindow('canny', cv2.WINDOW_NORMAL)
	cv2.createTrackbar('canny','canny',100,255,partial(process_one_image,path=path,factor = factor,scale = scale))
	cv2.namedWindow('Low size', cv2.WINDOW_NORMAL)
	cv2.createTrackbar('size','Low size',1,500,partial(process_one_image,path=path,factor = factor,scale = scale))
	cv2.namedWindow('dst_va', cv2.WINDOW_NORMAL)
	cv2.createTrackbar('dst_va','dst_va',10,500,partial(process_one_image,path=path,factor = factor,scale = scale))
	'''

	process_one_image(0,path,luke_skywalker.factor,int(e2.get()))

	
	blurr_val = slider1.get()
	canny = slider2.get()
	size = slider3.get()
	#size = size/10
	dst_val = slider4.get()
	dst_val = dst_val/100
	path1 = r'C:\Users\USER\Manual contouring' # Location of modified image
	while(1):

		#cv2.imshow('Auto-Contouring Tool',temp_image)
		
		if cv2.waitKey(1) & 0xFF == 27:
		 	cv2.imwrite(os.path.join(path1 ,'AUTOSAVED_IMAGE_Auto-Contouring.jpeg'),temp_image)
		 	break
	
	_,cnts=process_two_image(path,blurr_val,canny,size,dst_val,factor,scale)

	

	cv2.destroyAllWindows()
	
	return (blurr_val,canny,size,dst_val)


#--------------------------------------------------------------------------GUI Functions

#global factor,acc_ball,scale,blurr_val,canny,size,dst_val
'''
file_path=''
def select_image():
    show_page(page1)
    global file_path
    file_path = filedialog.askopenfilename()
    if file_path:
        image=Image.open(file_path)
        image1 = image.resize((1000, 700), Image.ANTIALIAS)
        
        canvas.image_tk = ImageTk.PhotoImage(image1)
        image_id = canvas.create_image(0,0, anchor="nw",image=canvas.image_tk)
        canvas.itemconfigure(image_id, image=canvas.image_tk)
    
        
        image_id= canvas_page2.create_image(0,0, anchor="nw",image=canvas.image_tk)
        canvas_page2.itemconfigure(image_id, image=canvas.image_tk)
'''


#fine_dia = 1
#get factor to find actual length

# Pic 2.jpg 

#fine_dia = int(input('Approx fines diameter: '))
'''file_path = 'Input/Level 3 Pic 2-002_O.jpg'
acc_ball = float(13)
scale = 6'''


def luke_skywalker():

    acc_ball = float(e1.get())
    scale = int(e2.get())
    luke_skywalker.factor = length(path,acc_ball,scale)
    if path:
        image=Image.open(path)
        image1 = image.resize((1000, 700), Image.ANTIALIAS)
        
        canvas.image_tk = ImageTk.PhotoImage(image1)
        image_id = canvas.create_image(0,0, anchor="nw",image=canvas.image_tk)
        canvas.itemconfigure(image_id, image=canvas.image_tk)
    
        
        image_id= canvas_page2.create_image(0,0, anchor="nw",image=canvas.image_tk)
        canvas_page2.itemconfigure(image_id, image=canvas.image_tk)
    show_page(page2)

def C3PO():# fine tune parameters for auto contouring
    #diameters = []
    


    #show_page(page2)
    acc_ball = float(e1.get())
    scale = int(e2.get())
    C3PO.blurr_val,C3PO.canny,C3PO.size,C3PO.dst_val = fine_tune(path,luke_skywalker.factor,scale)
    
    img2= Image.open(r'C:\Users\USER\Manual contouring\AUTOSAVED_IMAGE_Auto-Contouring.jpeg')
    img3=img2.resize((1000, 700), Image.ANTIALIAS)  
    canvas.image_tk = ImageTk.PhotoImage(img3)
    image_id = canvas.create_image(0,0, anchor="nw",image=canvas.image_tk)
    canvas.itemconfigure(image_id, image=canvas.image_tk)
       
    canvas_page2.image_tk = ImageTk.PhotoImage(img3)
    image_id= canvas_page2.create_image(0,0, anchor="nw",image=canvas.image_tk)
    canvas_page2.itemconfigure(image_id, image=canvas.image_tk)

    canvas_page3.image_tk = ImageTk.PhotoImage(img3)
    image_id= canvas_page3.create_image(0,0, anchor="nw",image=canvas.image_tk)
    canvas_page3.itemconfigure(image_id, image=canvas.image_tk)


diameter=[1,32]

def yoda():
    global diameter
    #diameter.clear()
    acc_ball = float(e1.get())
    scale = int(e2.get())
    #Tool to draw manual contours
    yoda.diameter,yoda.fines,yoda.arr = mancon(path,C3PO.blurr_val,C3PO.canny,C3PO.size,C3PO.dst_val,luke_skywalker.factor,scale,str(sys.argv[2]),str(sys.argv[3]),str(sys.argv[4]))
    diameter=yoda.diameter
    print('yoda')
    print(diameter)
    img2= Image.open(r'C:\Users\USER\Manual contouring\AUTOSAVED_IMAGE_Manual_contouring.jpeg')
    img3=img2.resize((1000, 700), Image.ANTIALIAS)  
    
    canvas.image_tk = ImageTk.PhotoImage(img3)
    image_id = canvas.create_image(0,0, anchor="nw",image=canvas.image_tk)
    canvas.itemconfigure(image_id, image=canvas.image_tk)
    
       
    canvas_page3.image_tk = ImageTk.PhotoImage(img3)
    image_id= canvas_page3.create_image(0,0, anchor="nw",image=canvas.image_tk)
    canvas_page3.itemconfigure(image_id, image=canvas.image_tk)
    

def yoda_undo():
    acc_ball = float(e1.get())
    scale = int(e2.get())
    #Tool to draw manual contours
    yoda.diameter,yoda.fines,yoda.arr = mancon_undo(path,C3PO.blurr_val,C3PO.canny,C3PO.size,C3PO.dst_val,luke_skywalker.factor,scale,str(sys.argv[2]),str(sys.argv[3]),str(sys.argv[4]))
    img2= Image.open(r'C:\Users\USER\Manual contouring\AUTOSAVED_IMAGE_Manual_contouring.jpeg')
    img3=img2.resize((1000, 700), Image.ANTIALIAS)  
    
    canvas.image_tk = ImageTk.PhotoImage(img3)
    image_id = canvas.create_image(0,0, anchor="nw",image=canvas.image_tk)
    canvas.itemconfigure(image_id, image=canvas.image_tk)
    
       
    canvas_page3.image_tk = ImageTk.PhotoImage(img3)
    image_id= canvas_page3.create_image(0,0, anchor="nw",image=canvas.image_tk)
    canvas_page3.itemconfigure(image_id, image=canvas.image_tk)
    	
def yoda_lazzo():
    acc_ball = float(e1.get())
    scale = int(e2.get())
    #Tool to draw manual contours
    yoda.diameter,yoda.fines,yoda.arr = mancon_lazzo(path,C3PO.blurr_val,C3PO.canny,C3PO.size,C3PO.dst_val,luke_skywalker.factor,scale,str(sys.argv[2]),str(sys.argv[3]),str(sys.argv[4]))
    img2= Image.open(r'C:\Users\USER\Manual contouring\AUTOSAVED_IMAGE_Manual_contouring.jpeg')
    img3=img2.resize((1000, 700), Image.ANTIALIAS)  
    
    canvas.image_tk = ImageTk.PhotoImage(img3)
    image_id = canvas.create_image(0,0, anchor="nw",image=canvas.image_tk)
    canvas.itemconfigure(image_id, image=canvas.image_tk)
    
       
    canvas_page3.image_tk = ImageTk.PhotoImage(img3)
    image_id= canvas_page3.create_image(0,0, anchor="nw",image=canvas.image_tk)
    canvas_page3.itemconfigure(image_id, image=canvas.image_tk)


  
  

#plot(diameter,path,unit_bins,dper,total)
#def jedi():
#	jedi.unit_bins = get_units(yoda.diameter)

    
#n = input('Enter x vals for Dx with spaces(enter for default):')
#if n != '':
# jedi.dper = [int(i) for i in n.split(' ')]
# jedi.dper.sort()
#global unit_bins

def plot():
	#global diameter
	name=str(sys.argv[2])
	PTrnpilesphotosId=str(sys.argv[3])
	PUserby=str(sys.argv[4])

	data=yoda.diameter
	print('DATA')
	print(data)
	#path=path
	#unit_bins=get_units(yoda.diameter)
	dper=[1,10,25,50,75,99]
	
	merge=0
	total = sum(yoda.fines)
	total = float(float(total/yoda.arr)*100)
	fine_tot=total

	unit_dic ={'mm':10,'cm':1,'m':0.01}
	#bins = 10 # default
	#unit = 'cm' # default 
	unit= units_dic[v.get()]
	bins= var.get()
	lsl,usl = slider98.getValues()

	#unit, bins, lsl,usl =('cm', 10, 3.5442105263157893, 16.085263157894737)
	print(unit, bins, lsl,usl)
	#print(data)

	org_name = path.split('.')[0]
	org_name = org_name[:-2]
	out_name = org_name +'.txt'
	diameter_string = ''
	for i in yoda.diameter:
		diameter_string += str(i) + ' '
	with open(out_name, "w") as file:
		file.write(diameter_string+' '+str(total))
	
	diameters = np.array(data)*unit_dic[unit]
	data = np.array(data)*unit_dic[unit]
	mul = int((max(data)-min(data))/bins)+1
	divisions = [(int(min(data))+i*mul,int(min(data))+((i+1)*mul)) for i in range(bins)] #user input
	#diameters = np.array(data)*unit_dic[unit] #diameter input
	lsl = lsl*unit_dic[unit]
	usl = usl*unit_dic[unit]

	freq = {}
	#print(len(data))
	csum = 0
	for i in divisions:
		c = 0
		for k in diameters:
			if k >= i[0] and k < i[1]:
				c+=1
		csum += c
		freq[i] = [c,csum]


	#print(freq)
	perdata = {}
	bardata = {}
	tabdata = []
	su = 0
	lsli = 0
	usli = 0
	for f in freq:
		su = round(su + round((freq[f][0]/csum)*100,2) ,2)
		perdata[str(f[0])+'-'+str(f[1])] = su
		bardata[ str(f[0])+'-'+str(f[1])] = round((freq[f][0]/csum)*100,2)
		tabdata.append([f[1], su])
		if f[0] <= lsl and f[1] >= lsl:
			lsli = str(f[0])+'-'+str(f[1])
		if f[0] <= usl and f[1] >= usl:
			usli = str(f[0])+'-'+str(f[1])

	#print(perdata)
	dper_data=[]
	data.sort()
	one_per = (float(1)/float(len(data)))*100
	#print(data)
	#print(len(data))
	#print(one_per)
	for i in dper:
		dper_data.append([i,data[int(i/one_per)]])
		#print(int(i/one_per))
	#print(dper_data)
	ranges = list(perdata.keys())
	freq1 = list(perdata.values())
	freq2 = list(bardata.values())
	fig, axs =plt.subplots(1,2, gridspec_kw={'width_ratios': [3, 1]})
	
	#update------------------------------------------
	from datetime import date
	import time
	today = date.today()
	# Textual month, day and year	
	current_date = today.strftime("%B %d, %Y")
	current_time = time.strftime('%H:%M:%S')
	main_time = current_date+' '+current_time
	fig.suptitle(main_time,ha = 'right')
	#-------------------------------------------------
	
	axs[1].axis('tight')
	axs[1].axis('off')
	#clust_data = np.random.random((10,3))
	collabel=("Size ("+unit+")", "% of passing")
	clust_data = np.array(tabdata)
	dx_data = np.array(dper_data)
	#print(clust_data)
	the_table = axs[1].table(cellText=clust_data,colLabels=collabel,loc='center',cellLoc='center',colColours =["silver"] * 2,colWidths=[0.75,0.75])
	#the_tabl = axs[1].table(cellText=dx_data,colLabels=("x", "Dx"),loc='bottom',cellLoc='center',colColours =["silver"] * 2,colWidths=[0.75,0.75])
	
	
	the_table.set_fontsize(18)
	#the_table.scale(1, 1)
	

	axs[0].bar(ranges, freq2, color ='maroon',width = 0.4)
	axs[0].plot(ranges, freq1, '-o')

	lsl_x = ranges.index(lsli)-0.5
	axs[0].axvline(x=lsl_x,color='red', linestyle='--',label='LSL')
	axs[0].text(lsl_x, 0.75, ' LSL ('+str(round(lsl,1))+' '+unit+')', transform=axs[0].get_xaxis_transform(),fontsize =  'x-small')
	usl_x = ranges.index(usli)-0.5
	axs[0].axvline(x=usl_x,color='red', linestyle='--',label='USL')
	axs[0].text(usl_x, 0.75, ' USL ('+str(round(usl,1))+' '+unit+')', transform=axs[0].get_xaxis_transform(),fontsize =  'x-small')
	#axs[0].plot(ranges, freq3, '-o')

	axs[0].tick_params(axis="x", labelsize=6)

	
	for i in range(len(dper_data)):
		k = dper_data[i]
		#s = 'D'+str(k[0])+' = '+str(round(k[1]*unit_dic[unit],2))
		s = 'D'+str(('0' if k[0]<10 else '')+str(k[0]))+' = '+str(round(k[1]*unit_dic[unit],2))
		if i < len(dper_data)/2:
			axs[1].text(-0.05, 1.05-((i+1)/25),s,horizontalalignment='left',verticalalignment='top', transform = axs[1].transAxes,fontsize =  'x-small')
			#print(((i+1)/25))
		else:
			i1 = i-len(dper_data)//2
			axs[1].text(0.5, 1.05-((i1+1)/25),s,horizontalalignment='left',verticalalignment='top', transform = axs[1].transAxes,fontsize =  'x-small')
		
	
	#fine_tot = float(10)
	fine_tot = float(10)
	print('FINES')
	print(fine_tot)
	if fine_tot != float(0):
		s = 'Fines = '+str(round(fine_tot,2))+'% of area with respect to \nthe area of all the photos'
		#axs[0].text(0.025,1-((len(dper_data)+1)/25),s,horizontalalignment='left',verticalalignment='top', transform = axs[0].transAxes,fontsize =  'x-small')
		#axs[1].text(-0.076, -0.035, s, fontsize='x-small')
		axs[1].text(-0.2, 1.0-((len(dper_data)//2+1))/25, s, horizontalalignment='left', fontsize = 'x-small')

	axs[0].set_xlabel("Object diameters in "+unit)
	axs[0].set_ylabel(" % of passing")
	axs[0].set_title(" Diameters vs % of passing ")

	#plt.show()

	#saving plot
	#org_name = path.split('\'')[-1]
	if merge == 0:
		k = path.rfind("O")
		img_pat = path[:k] + "HG" + path[k+1:]
		k = name.rfind("O")
		img_name = name[:k] + "HG" + name[k+1:]
		db=MySQLdb.connect("75.126.169.58", "Xliconmys0618", "XlServMys1706#", "iocllive",3306,autocommit = True)
		cursor = db.cursor()
		lis=[int(PTrnpilesphotosId),img_name,img_pat,int(PUserby),2]
		print(lis)
		result_args = cursor.callproc('PythonUpdatePilesPhotos', lis)
		cursor.close()
		db.close()
	else:
		img_pat = path+"_CHG.jpg"
		img_name = name+"_CHG.jpg"
		db=MySQLdb.connect("75.126.169.58", "Xliconmys0618", "XlServMys1706#", "iocllive",3306,autocommit = True)
		cursor = db.cursor()
		lis=[PTrnpilesphotosId,img_name,img_pat,int(PUserby),3]
		print(lis)
		result_args = cursor.callproc('PythonUpdatePilesPhotos', lis)
		print(result_args)
		print(cursor.fetchall())
		cursor.close()
		db.close()
		
	#fig.savefig(img_pat)
	
	
    
	

	plt.savefig(r'C:\Users\USER\Manual contouring\PLOT.png')
	img2= Image.open(r'C:\Users\USER\Manual contouring\PLOT.png')
	img3=img2.resize((1050, 750), Image.ANTIALIAS)  
	canvas_page4.image_tk = ImageTk.PhotoImage(img3)
	image_id = canvas_page4.create_image(0,0, anchor="nw",image=canvas_page4.image_tk)
	canvas.itemconfigure(image_id, image=canvas_page4.image_tk)



def plotX(data,path,dper,fine_tot,merge,name,PTrnpilesphotosId,PUserby):
	unit_dic = {'mm':10,'cm':1,'m':0.01}
	bins = 10 # default
	unit = 'cm' # default
	name= str(sys.argv[2])
	PTrnpilesphotosId= str(sys.argv[3])
	PUserby= str(sys.argv[4])

	unit_dic ={'mm':10,'cm':1,'m':0.01}
	#bins = 10 # default
	#unit = 'cm' # default 
	unit= units_dic[v.get()]
	bins= var.get()
	lsl,usl = slider98.getValues()
	
	diameters = np.array(data)*unit_dic[unit] #diameter input
	data = np.array(data)*unit_dic[unit]
	mul = int((max(data)-min(data))/bins)+1
	divisions = [(int(min(data))+i*mul,int(min(data))+((i+1)*mul)) for i in range(bins)] #user input
	#data = np.array(data)*unit_dic[unit]
	lsl = lsl*unit_dic[unit]
	usl = usl*unit_dic[unit]

	freq = {}
	#print(len(data))
	csum = 0
	for i in divisions:
		c = 0
		for k in diameters:
			if k >= i[0] and k < i[1]:
				c+=1
		csum += c
		freq[i] = [c,csum]


	#print(freq)
	perdata = {}
	bardata = {}
	tabdata = []
	su = 0
	lsli = 0
	usli = 0
	for f in freq:
		su = round(su + round((freq[f][0]/csum)*100,2) ,2)
		perdata[str(f[0])+'-'+str(f[1])] = su
		bardata[ str(f[0])+'-'+str(f[1])] = round((freq[f][0]/csum)*100,2)
		tabdata.append([f[1], su])
		if f[0] <= lsl and f[1] >= lsl:
			lsli = str(f[0])+'-'+str(f[1])
		if f[0] <= usl and f[1] >= usl:
			usli = str(f[0])+'-'+str(f[1])

	#print(perdata)
	dper_data=[]
	data.sort()
	one_per = (float(1)/float(len(data)))*100
	#print(data)
	#print(len(data))
	#print(one_per)
	for i in dper:
		dper_data.append([i,data[int(i/one_per)]])
		#print(int(i/one_per))
	#print(dper_data)
	ranges = list(perdata.keys())
	freq1 = list(perdata.values())
	freq2 = list(bardata.values())
	fig, axs =plt.subplots(1,2, gridspec_kw={'width_ratios': [3, 1]})

	#update------------------------------------------
	from datetime import date
	import time
	today = date.today()
	# Textual month, day and year	
	current_date = today.strftime("%B %d, %Y")
	current_time = time.strftime('%H:%M:%S')
	main_time = current_date+' '+current_time
	fig.suptitle(main_time,ha = 'right')
	#-------------------------------------------------

	axs[1].axis('tight')
	axs[1].axis('off')
	#clust_data = np.random.random((10,3))
	collabel=("Size ("+unit+")", "% of passing")
	clust_data = np.array(tabdata)
	dx_data = np.array(dper_data)
	#print(clust_data)
	the_table = axs[1].table(cellText=clust_data,colLabels=collabel,loc='center',cellLoc='center',colColours =["silver"] * 2,colWidths=[0.75,0.75])
	#the_tabl = axs[1].table(cellText=dx_data,colLabels=("x", "Dx"),loc='bottom',cellLoc='center',colColours =["silver"] * 2,colWidths=[0.75,0.75])
	
	
	the_table.set_fontsize(18)
	#the_table.scale(1, 1)
	

	axs[0].bar(ranges, freq2, color ='maroon',width = 0.4)
	axs[0].plot(ranges, freq1, '-o')

	lsl_x = ranges.index(lsli)-0.5
	axs[0].axvline(x=lsl_x,color='red', linestyle='--',label='LSL')
	axs[0].text(lsl_x, 0.75, ' LSL ('+str(round(lsl,1))+' '+unit+')', transform=axs[0].get_xaxis_transform(),fontsize =  'x-small')
	usl_x = ranges.index(usli)-0.5
	axs[0].axvline(x=usl_x,color='red', linestyle='--',label='USL')
	axs[0].text(usl_x, 0.75, ' USL ('+str(round(usl,1))+' '+unit+')', transform=axs[0].get_xaxis_transform(),fontsize =  'x-small')
	#axs[0].plot(ranges, freq3, '-o')

	axs[0].tick_params(axis="x", labelsize=6)

	
	for i in range(len(dper_data)):
		k = dper_data[i]
		#s = 'D'+str(k[0])+' = '+str(round(k[1]*unit_dic[unit],2))
		s = 'D'+str(('0' if k[0]<10 else '')+str(k[0]))+' = '+str(round(k[1]*unit_dic[unit],2))
		if i < len(dper_data)/2:
			axs[1].text(-0.05, 1.05-((i+1)/25),s,horizontalalignment='left',verticalalignment='top', transform = axs[1].transAxes,fontsize =  'x-small')
			#print(((i+1)/25))
		else:
			i1 = i-len(dper_data)//2
			axs[1].text(0.5, 1.05-((i1+1)/25),s,horizontalalignment='left',verticalalignment='top', transform = axs[1].transAxes,fontsize =  'x-small')

	
	#fine_tot = float(10)
	if fine_tot != float(0):
		s = 'Fines = '+str(round(fine_tot,2))+'% of area with respect to \nthe area of all the photos'
		#axs[0].text(0.025,1-((len(dper_data)+1)/25),s,horizontalalignment='left',verticalalignment='top', transform = axs[0].transAxes,fontsize =  'x-small')
		#axs[1].text(-0.076, -0.035, s, fontsize='x-small')
		axs[1].text(-0.2, 1.0-((len(dper_data)//2+1))/25, s, horizontalalignment='left', fontsize = 'x-small')

	axs[0].set_xlabel("Object diameters in "+unit)
	axs[0].set_ylabel(" % of passing")
	axs[0].set_title(" Diameters vs % of passing ")

	#plt.show()

	#saving plot
	#org_name = path.split('\'')[-1]
	if merge == 0:
		k = path.rfind("O")
		img_pat = path[:k] + "HG" + path[k+1:]
		k = name.rfind("O")
		img_name = name[:k] + "HG" + name[k+1:]
		db=MySQLdb.connect("75.126.169.58", "Xliconmys0618", "XlServMys1706#", "iocllive",3306,autocommit = True)
		cursor = db.cursor()
		lis=[int(PTrnpilesphotosId),img_name,img_pat,int(PUserby),2]
		print(lis)
		result_args = cursor.callproc('PythonUpdatePilesPhotos', lis)
		cursor.close()
		db.close()
	else:
		img_pat = path+"_CHG.jpg"
		img_name = name+"_CHG.jpg"
		db=MySQLdb.connect("75.126.169.58", "Xliconmys0618", "XlServMys1706#", "iocllive",3306,autocommit = True)
		cursor = db.cursor()
		lis=[PTrnpilesphotosId,img_name,img_pat,int(PUserby),3]
		print(lis)
		result_args = cursor.callproc('PythonUpdatePilesPhotos', lis)
		print(result_args)
		print(cursor.fetchall())
		cursor.close()
		db.close()
		
	#fig.savefig(img_pat)

	plt.savefig(r'C:\Users\USER\Manual contouring\PLOT2.png')
	img2= Image.open(r'C:\Users\USER\Manual contouring\PLOT2.png')
	img3=img2.resize((1050, 750), Image.ANTIALIAS)  
	canvas_page5.image_tk = ImageTk.PhotoImage(img3)
	image_id = canvas_page5.create_image(0,0, anchor="nw",image=canvas_page5.image_tk)
	canvas.itemconfigure(image_id, image=canvas_page5.image_tk)



def merge():
	name=str(sys.argv[2])
	PTrnpilesphotosId=str(sys.argv[3])
	PUserby=str(sys.argv[4])
	files = []
	k = path.rfind("-")
	img_pat = path[:k]
	k = name.rfind("-")
	name = name[:k]
	k = img_pat.rfind("/")
	if k== -1:
		k = img_pat.rfind("\\")
	img_pa = img_pat[:k+1]
	all_files = os.listdir(img_pa)
	txt_files = filter(lambda x: x[-4:] == '.txt', all_files)
	for i in txt_files:
		p = i[:-4]
		pi = p.rfind("-")
		p = p[:pi]
		if img_pat[k+1:] == p:
			files.append(img_pa+i)

	#merged diameters
	diameter = []
	fines = []
	for file in files:
		with open(file) as f:
			content = f.read().split()
			fines.append(float(content[-1]))
			diameter += list(map(float,content[:-1]))
	try:
    		total = round(sum(fines)/len(fines),2)
	except:
    		total = round(sum(fines),2)
	#unit_bins = get_units(diameter)
	dper = [1,10,25,50,75,99]
	#n = input('Enter x vals for Dx with spaces(enter for default):')
	#if n != '':
	#	dper = [int(i) for i in n.split(' ')]
	#	dper.sort()
	plotX(diameter,img_pat,dper,total,1,str(sys.argv[2]),str(sys.argv[3]),str(sys.argv[4]))





#--------------------------------------------------------------------------GUI Functions

root = Tk()
root.attributes('-fullscreen', True)
width= root.winfo_screenwidth()               
height= root.winfo_screenheight()             
root.geometry('%dx%d' % (width, height))





#root.geometry('900x600+500+500')


root.title('Fragilytix')
root.iconbitmap('C:/Users/USER/Downloads/Indian-Oil-jobs.ico')
root.rowconfigure(0,weight=1)
root.columnconfigure(0,weight=1)
root.bind("<Escape>", lambda x: root.destroy())


def show_page(pages):
    pages.tkraise()

page0=LabelFrame(root,background='black')
page1=LabelFrame(root,highlightbackground='black',highlightthickness=4,background='grey')
#page1.grid(row=0,column=0,sticky='nsew')
page2=LabelFrame(root,background='grey',highlightbackground='black',highlightthickness=4)
#page2.grid(row=0,column=0,sticky='nsew')
page3=LabelFrame(root,background='grey',highlightbackground='black',highlightthickness=4)
page4=LabelFrame(root,background='grey',highlightbackground='black',highlightthickness=4)
page5=LabelFrame(root,background='grey',highlightbackground='black',highlightthickness=4)


for pages in (page0,page1,page2,page3,page4,page5):
    pages.grid(row=0,column=0,sticky='nsew')




#-----------------------------------------------------------------Page0
canvas = Canvas(page0, width= 750, height=750, bg="black",highlightbackground='black')
canvas.grid(row=0,column=0,padx=405,rowspan=8)

img2= Image.open(r'C:\Users\USER\NEW BUTTONS 5\tot_v8\Button images\nice_logo3.PNG')
img3=img2.resize((750, 750), Image.ANTIALIAS)  
canvas.image_tk = ImageTk.PhotoImage(img3)
image_id = canvas.create_image(0,0, anchor="nw",image=canvas.image_tk)
canvas.itemconfigure(image_id, image=canvas.image_tk)

all_btn = PhotoImage(file=r'C:\Users\USER\NEW BUTTONS 5\tot_v8\Button images\button_select-image (4).png')
#bt1 = Button(page0, text="Select Image",font="Bahnschrift 19 bold",command=select_image,image=all_btn,borderwidth=0,bg='black',activebackground='black')
#bt1.grid(row=9,column=0,sticky='n')

    
	
    




#-----------------------------------------------------------------Page1


#frame=LabelFrame(page1,width=900,height=600,highlightbackground='black',highlightthickness=6)
#frame.grid(row=0,column=0,padx=20,pady=20)

#frame1=LabelFrame(page1,width=300,height=600,highlightbackground='black')
#frame1.grid(row=0,column=1,padx=100,pady=20)
# the canvas where the image will be displayed


#i=Image.open(r'C:\Users\USER\NEW BUTTONS 2\Input\left-arrow.png')
#i=i.resize((50,50),Image.ANTIALIAS)
next_btn = PhotoImage(file=r'C:\Users\USER\NEW BUTTONS 5\tot_v8\Button images\icons8-next-page-100.png')
next_btn =next_btn.subsample(2,2)

back_btn = PhotoImage(file=r'C:\Users\USER\NEW BUTTONS 5\tot_v8\Button images\icons8-back-to-100.png')
back_btn =back_btn.subsample(2,2)

canvas = Canvas(page1, width= 1000, height=700,highlightbackground='white',highlightthickness=3,background='black')
canvas.grid(row=0,column=0,rowspan=7,padx=30,pady=30)

canvas32 = Canvas(page1, width= 80, height=80, background='grey',highlightthickness=0)
canvas32.grid(row=7,column=0,padx=30,sticky='nw')
img2= Image.open(r'C:\Users\USER\NEW BUTTONS 5\tot_v8\Button images\Indian-Oil-jobs.jpg')
img3=img2.resize((80, 80), Image.ANTIALIAS)  
canvas32.image_tk = ImageTk.PhotoImage(img3)
image_id = canvas32.create_image(0,0, anchor="nw",image=canvas32.image_tk)
canvas32.itemconfigure(image_id, image=canvas32.image_tk)

l123 = Label(page1,text='Scaling Object Diameter',font="Bahnschrift 30 bold",background='grey',fg='white')
l123.grid(row=0,column=3,columnspan=9,sticky='ns')


l1 = Label(page1,text='Diameter :',font="Bahnschrift 24 bold",background='grey')
l1.grid(row=1,column=3,columnspan=4,sticky='ns')



e1 = Entry(page1,width=10,bg='white',fg='black',font=('Bahnschrift', 24,'bold'))
e1.grid(row=2,column=4,sticky='n',columnspan=3,padx=100)


l11 = Label(page1,text='cm',font="Bahnschrift 24 bold",background='grey')
l11.grid(row=2,column=6,sticky='n')

l2 = Label(page1,text='Scale down by :',font="Bahnschrift 24 bold",background='grey')
l2.grid(row=3,column=3,columnspan=4,sticky='ns')

e2 = Entry(page1,width=10,bg='white',fg='black',font=('Bahnschrift', 24,'bold'))
e2.grid(row=4,column=4,columnspan=3,sticky='n')

ball_btn = PhotoImage(file=r'C:\Users\USER\NEW BUTTONS 5\tot_v8\Button images\button_ball-length-detection (3).png')
bt2 = Button(page1,text ='Ball Length Detection',command = luke_skywalker,image=ball_btn,borderwidth=0,bg='grey',activebackground='grey')
bt2.grid(row=6,column=2,columnspan=6,sticky='ne',padx=10)



bt4 = Button(page1,text ='Next',command =lambda:show_page(page2),image=next_btn,width=60,height=60,borderwidth=0,bg='grey',activebackground='grey')
bt4.grid(row=7,column=7,sticky='e',columnspan=3)

bt47 = Button(page1,text ='Back',command =lambda:show_page(page0),image=back_btn,width=60,height=60,borderwidth=0,bg='grey',activebackground='grey')
bt47.grid(row=7,column=2,sticky='w',columnspan=3)











#image_id = canvas.create_image(0,0, anchor="nw")
#image_id2 = canvas_page2.create_image(0,0, anchor="nw")
#--------------------------------------------------------------------------Page2 Auto_contouring
#frame_page2=LabelFrame(page2,width=900,height=600,highlightbackground='black',highlightthickness=3)
#frame_page2.grid(row=0,column=0,padx=20,pady=20)

#frame1_page2=LabelFrame(page2,width=500,height=600,highlightbackground='black',highlightthickness=3)
#frame1_page2.grid(row=0,column=0)
ball_btn1 = PhotoImage(file=r'C:\Users\USER\NEW BUTTONS 5\tot_v8\Button images\button_view-result (1).png')

canvas_page2 = Canvas(page2, width= 1000, height=700 ,highlightbackground='white',highlightthickness=3,background='black')
canvas_page2.grid(row=0,column=0,rowspan=7,padx=30,pady=30)

canvas32 = Canvas(page2, width= 80, height=80, background='grey',highlightthickness=0)
canvas32.grid(row=7,column=0,padx=30,sticky='nw')
img2= Image.open(r'C:\Users\USER\NEW BUTTONS 5\tot_v8\Button images\Indian-Oil-jobs.jpg')
img3=img2.resize((80, 80), Image.ANTIALIAS)  
canvas32.image_tk = ImageTk.PhotoImage(img3)
image_id = canvas32.create_image(0,0, anchor="nw",image=canvas32.image_tk)
canvas32.itemconfigure(image_id, image=canvas32.image_tk)


l12345 = Label(page2,text='Auto-Contouring',font="Bahnschrift 34 bold",background='grey',fg='white')
l12345.grid(row=0,column=1,columnspan=3)



l3=Label(page2,text='Blur',font="Bahnschrift 23 bold",background='grey')
l3.grid(row=1,column=1,pady=10,sticky='w')
slider1 =Scale(page2,from_=25,to=500,orient=HORIZONTAL,troughcolor = 'blue',background='grey',highlightbackground='black',length=230)
slider1.grid(row=1,column=2,pady=10)

l4=Label(page2,text='Canny',font="Bahnschrift 23 bold",background='grey')
l4.grid(row=2,column=1,sticky='w')
slider2 =Scale(page2,from_=100,to=255,orient=HORIZONTAL,troughcolor ='blue',background='grey',highlightbackground='black',length=230)
slider2.grid(row=2,column=2,padx=20,pady=20)

l5=Label(page2,text='Size',font="Bahnschrift 23 bold",background='grey')
l5.grid(row=3,column=1,sticky='w')
slider3 =Scale(page2,from_=1,to=500,orient=HORIZONTAL,troughcolor = 'blue',background='grey',highlightbackground='black',length=230)
slider3.grid(row=3,column=2,padx=20,pady=20)

l6=Label(page2,text='dst_va',font="Bahnschrift 23 bold",background='grey')
l6.grid(row=4,column=1,sticky='w')
slider4 =Scale(page2,from_=10,to=500,orient=HORIZONTAL,troughcolor = 'blue',background='grey',highlightbackground='black',length=230)
slider4.grid(row=4,column=2,padx=20,pady=20)


bt3 = Button(page2,text ='Auto-Contouring',command = C3PO,bg='grey',image=ball_btn1,borderwidth=0,activebackground='grey')
bt3.grid(row=5,column=2)

bt41 = Button(page2,text ='Next',command =lambda:show_page(page3),image=next_btn,width=60,height=60,borderwidth=0,bg='grey',activebackground='grey')
bt41.grid(row=7,column=3,padx=6,pady=10,sticky='e')

bt42 = Button(page2,text ='Back',command =lambda:show_page(page1),image=back_btn,width=60,height=60,borderwidth=0,bg='grey',activebackground='grey')
bt42.grid(row=7,column=1,padx=10,pady=10,sticky='w')





#--------------------------------------------------------------------------

#--------------------------------------------------------------------------For Displaying selected image in page 1
if path:
    image=Image.open(path)
    image1 = image.resize((1000, 700), Image.ANTIALIAS)

    canvas.image_tk = ImageTk.PhotoImage(image1)
    image_id = canvas.create_image(0,0, anchor="nw",image=canvas.image_tk)
    canvas.itemconfigure(image_id, image=canvas.image_tk)

    image_id= canvas_page2.create_image(0,0, anchor="nw",image=canvas.image_tk)
    canvas_page2.itemconfigure(image_id, image=canvas.image_tk)

#--------------------------------------------------------------------------Page3 Manual Contouring
#frame_page3 =LabelFrame(page3,width=900,height=600,highlightbackground='black',highlightthickness=3)
#frame_page3.grid(row=0,column=0,padx=20,pady=20)
#
#frame1_page3=LabelFrame(page3,width=500,height=600,highlightbackground='black')
#frame1_page3.grid(row=0,column=2,padx=100,pady=20)
canvas_page3 = Canvas(page3, width= 1000, height=700, bg="black",highlightbackground='white',highlightthickness=3)
canvas_page3.grid(row=0,column=0,rowspan=7,padx=30,pady=30)

canvas32 = Canvas(page3, width= 80, height=80, background='grey',highlightthickness=0)
canvas32.grid(row=8,column=0,padx=30,sticky='sw')
img2= Image.open(r'C:\Users\USER\NEW BUTTONS 5\tot_v8\Button images\Indian-Oil-jobs.jpg')
img3=img2.resize((80, 80), Image.ANTIALIAS)  
canvas32.image_tk = ImageTk.PhotoImage(img3)
image_id = canvas32.create_image(0,0, anchor="nw",image=canvas32.image_tk)
canvas32.itemconfigure(image_id, image=canvas32.image_tk)

l12378 = Label(page3,text='Manual Contouring',font="Bahnschrift 34 bold",background='grey',fg='white')
l12378.grid(row=0,column=1,columnspan=7,sticky='ns')



#slider5 =Scale(page3,from_=0,to=2,orient=HORIZONTAL,command=slide,troughcolor = '#7FFF00',background='grey',highlightbackground='black',length=150)
#slider5.grid(row=2,column=2,padx=20)
draw_btn1 = PhotoImage(file=r'C:\Users\USER\NEW BUTTONS 5\tot_v8\Button images\icons8-edit-100.png')
bt5= Button(page3,text ='Draw Fines',command =yoda,bg='blue',image=draw_btn1,width=100,height=100,borderwidth=2,activebackground='grey')
bt5.grid(row=1,column=2,padx=100,columnspan=3,sticky='e')
l6255=Label(page3,text='Draw Fines',font="Bahnschrift 19 bold",background='grey')
l6255.grid(row=2,column=2,padx=100,sticky='ne',columnspan=3)


delete_btn1 = PhotoImage(file=r'C:\Users\USER\NEW BUTTONS 5\tot_v8\Button images\icons8-delete-bin-100.png')
bt51= Button(page3,text ='Delete',command =yoda_undo,bg='blue',image=delete_btn1,width=100,height=100,borderwidth=2,activebackground='grey')
bt51.grid(row=3,column=2,padx=100,sticky='e',columnspan=3)
l62=Label(page3,text='Delete',font="Bahnschrift 19 bold",background='grey')
l62.grid(row=4,column=2,padx=100,sticky='ne',columnspan=3)


lasso_btn1 = PhotoImage(file=r'C:\Users\USER\NEW BUTTONS 5\tot_v8\Button images\icons8-lasso-tool-100.png')
bt512= Button(page3,text ='lasso',command =yoda_lazzo,bg='blue',image=lasso_btn1,width=100,height=100,borderwidth=2,activebackground='grey')
bt512.grid(row=5,column=2,padx=100,sticky='e',columnspan=3)
l621=Label(page3,text='Lasso',font="Bahnschrift 19 bold",background='grey')
l621.grid(row=6,column=2,padx=100,sticky='ne',columnspan=3)


bt4= Button(page3,text ='back',command =lambda:show_page(page2),image=back_btn,width=60,height=60,borderwidth=0,bg='grey',activebackground='grey')
bt4.grid(row=8,column=1,sticky='w')

bt48= Button(page3,text ='Next',command =lambda:show_page(page4),image=next_btn,width=60,height=60,borderwidth=0,bg='grey',activebackground='grey')
bt48.grid(row=8,column=5,sticky='e')




#bt6= Button(frame1_page2,text ='Select Scale',command=R2D2)
#bt6.grid(row=5,column=0,padx=20,pady=20,sticky='n')

#bt7.grid(row=8,column=0,sticky='n')




#--------------------------------------------------------------------------Page4 Histogram


canvas_page4 = Canvas(page4, width= 1000, height=700, bg="black",highlightbackground='black',highlightthickness=5)
canvas_page4.grid(row=0,column=0,padx=30,pady=30,rowspan=13)

report_btn1 = PhotoImage(file=r'C:\Users\USER\NEW BUTTONS 5\tot_v8\Button images\button_generate-report (2).png')

bt7= Button(page4,text ='Generate Report',background='#8A2BE2',fg='white',command =plot,font="Bahnschrift 19 bold",image=report_btn1,bg='grey',activebackground='grey',borderwidth=0)
bt7.grid(row=13,column=0,sticky='n')

l123789 = Label(page4,text='Histogram',font="Bahnschrift 34 bold",background='grey',fg='white')
l123789.grid(row=0,column=1,columnspan=4,sticky='ns')


l69=Label(page4,text="Select desired unit of measurement:",font="Bahnschrift 17 bold",background='grey')
l69.grid(row=1,column=2,pady=10,sticky='sw')

v = IntVar()
v.set("2")  # initializing the choice

rad45=Radiobutton(page4,text="Millimeters (mm)",padx = 20,bg='grey',font="Bahnschrift 16 bold",variable=v,value=1)
rad45.grid(row=2,column=2,sticky='nw')

rad451=Radiobutton(page4,text="Centimeters (cm)",padx = 20,bg='grey',font="Bahnschrift 16 bold",variable=v,value=2)
rad451.grid(row=3,column=2,sticky='nw')

rad452=Radiobutton(page4,text="Meters (m)",padx = 20,bg='grey',font="Bahnschrift 16 bold",variable=v,value=3)
rad452.grid(row=4,column=2,sticky='nw')

l345=Label(page4,text="Select number of bins for the graph output:",font="Bahnschrift 17 bold",background='grey')
l345.grid(row=6,column=2,sticky='nw')

var = IntVar()
var.set(10)
sca = Scale(page4 , variable = var ,from_=1, to=50,orient=HORIZONTAL,troughcolor = 'blue',background='grey',highlightbackground='black',length=400)
sca.grid(row=7,column=2,sticky='nw',padx=20)

l1234=Label(page4,text="Select LSL and USL values:",font="Bahnschrift 17 bold",background='grey')
l1234.grid(row=10,column=2,sticky='nw')

#diameter=[1.83, 3.5, 2.45, 5.42, 8.66, 1.98, 6.12, 4.86, 3.04, 3.36, 1.52, 8.0, 1.75, 1.92, 2.4, 2.74, 5.37, 3.13, 8.68, 3.96, 2.96, 4.77, 1.52, 3.4, 5.57, 3.0, 1.98, 6.05, 1.07, 4.09, 9.02, 15.83, 5.48, 5.7, 4.31, 1.44, 1.73, 1.22, 2.28, 8.71, 1.7, 1.83, 12.77, 3.68, 4.66, 2.28, 1.98, 8.66, 12.24, 5.94, 6.12, 2.59, 2.17, 1.92, 15.49, 17.18, 4.73, 9.02, 1.83, 1.92, 15.7, 13.93, 7.82, 17.71, 20.72, 3.13, 2.45, 1.7, 3.14, 4.43, 5.09, 8.4, 1.92]

print('DIAMETER')
print(diameter)
  #lsl and usl selection
lsl = min(diameter)
unit_factor = {1:10,2:1,3:0.01}

slider98 = Slider(page4, width = 400, height = 60, min_val = min(diameter)*unit_factor[v.get()], max_val = max(diameter)*unit_factor[v.get()], init_lis = [min(diameter)*unit_factor[v.get()],max(diameter)*unit_factor[v.get()]], show_value = True)
slider98.grid(row=11,column=2,sticky='nw')

units_dic = {1:'mm',2:'cm',3:'m'}
bins = var.get()
lsl,usl = slider98.getValues()


bt478= Button(page4,text ='back',command =lambda:show_page(page3),image=back_btn,width=60,height=60,borderwidth=0,bg='grey',activebackground='grey')
bt478.grid(row=13,column=2,sticky='w')

bt481= Button(page4,text ='Next',command =lambda:show_page(page5),image=next_btn,width=60,height=60,borderwidth=0,bg='grey',activebackground='grey')
bt481.grid(row=13,column=2,sticky='e')



canvas32 = Canvas(page4, width= 80, height=80, background='grey',highlightthickness=0)
canvas32.grid(row=13,column=0,sticky='nw',padx=30)
img2= Image.open(r'C:\Users\USER\NEW BUTTONS 5\tot_v8\Button images\Indian-Oil-jobs.jpg')
img3=img2.resize((80, 80), Image.ANTIALIAS)  
canvas32.image_tk = ImageTk.PhotoImage(img3)
image_id = canvas32.create_image(0,0, anchor="nw",image=canvas32.image_tk)
canvas32.itemconfigure(image_id, image=canvas32.image_tk)
#--------------------------------------------------------------------------Page5 Merged Histogram

canvas_page5 = Canvas(page5, width= 1000, height=700, bg="black",highlightbackground='black',highlightthickness=5)
canvas_page5.grid(row=0,column=0,padx=30,pady=30,rowspan=13)

bt4781= Button(page5,text ='back',command =lambda:show_page(page4),image=back_btn,width=60,height=60,borderwidth=0,bg='grey',activebackground='grey')
bt4781.grid(row=13,column=2,sticky='w')

bt4812= Button(page5,text ='Next',command =lambda:show_page(page5),image=next_btn,width=60,height=60,borderwidth=0,bg='grey',activebackground='grey')
bt4812.grid(row=13,column=8,sticky='e')

report_btn2 = PhotoImage(file=r'C:\Users\USER\NEW BUTTONS 5\tot_v8\Button images\button_generate-merged-report.png')
bt722= Button(page5,text ='Merge Plot',background='#8A2BE2',fg='white',command =merge,font="Bahnschrift 19 bold",image=report_btn2,bg='grey',activebackground='grey',borderwidth=0)
bt722.grid(row=8,column=2,sticky='n',columnspan=7)

l1237891 = Label(page5,text='Histogram II',font="Bahnschrift 34 bold",background='grey',fg='white')
l1237891.grid(row=0,column=4,sticky='ns')

canvas32 = Canvas(page5, width= 80, height=80, background='grey',highlightthickness=0)
canvas32.grid(row=13,column=0,sticky='nw',padx=30)
img2= Image.open(r'C:\Users\USER\NEW BUTTONS 5\tot_v8\Button images\Indian-Oil-jobs.jpg')
img3=img2.resize((80, 80), Image.ANTIALIAS)  
canvas32.image_tk = ImageTk.PhotoImage(img3)
image_id = canvas32.create_image(0,0, anchor="nw",image=canvas32.image_tk)
canvas32.itemconfigure(image_id, image=canvas32.image_tk)

#--------------------------------------------------------------------------
show_page(page1)

root.mainloop()
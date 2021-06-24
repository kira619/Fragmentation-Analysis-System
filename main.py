from find_fac import length
from fine_tune import fine_tune
from manual import mancon
from histogram import plotX
from unit_selection import get_units
from merge import merge
import sys
import cv2

#take input
#C:\Users\USER\NEW BUTTONS 5\tot_v8\Input\Level 3 Pic 3-003_O.jpgpath=''
path=''
#path = input('Enter the location of image: ')


try:
	path = str(sys.argv[1])+"\\" +str(sys.argv[2])
	print(path)
	buff1 = cv2.imread(path)
	buff2 = buff1.shape
except AttributeError:
	path = str(sys.argv[1])+"/" +str(sys.argv[2])
	buff1 = cv2.imread(path)
	buff2 = buff1.shape

acc_ball = float(input('Enter the diameter of the scaling object in cm: '))
scale = int(input('Scale down by: '))

#get factor to find actual lenght 
factor = length(path,acc_ball,scale)

# fine tune parameters for auto contouring
blurr_val,canny,size,dst_val = fine_tune(path,factor,scale)

#Tool to draw manual contours
diameter,fines,arr = mancon(path,blurr_val,canny,size,dst_val,factor,scale)

#print(fines)
total = sum(fines)
total = float(float(total/arr)*100)
unit_bins = get_units(diameter)


#saving diameter
org_name = path.split('.')[0]
org_name = org_name[:-2]

out_name = org_name +'.txt'
diameter_string = ''
for i in diameter:
	diameter_string += str(i) + ' '
with open(out_name, "w") as file:
    file.write(diameter_string+' '+str(total))

dper = [1,10,25,50,75,99]
n = input('Enter x vals for Dx with spaces(enter for default):')
if n != '':
	dper = [int(i) for i in n.split(' ')]
	dper.sort()

#plot the histogram

plot(diameter,path,unit_bins,dper,total)
merge(path)

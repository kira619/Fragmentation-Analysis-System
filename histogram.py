import matplotlib.pyplot as plt
import numpy as np
import MySQLdb

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

	plt.show()

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
		
	fig.savefig(img_pat)

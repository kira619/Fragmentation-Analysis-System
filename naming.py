from tkinter import filedialog
file_path = filedialog.askopenfilename()
print(file_path)
org_name = file_path.split('/')[-1]#.split("\\")[-1]
print(org_name)
out_name = "C:/Users/USER/NEW BUTTONS 5/tot_v8/output/" + org_name.split('_O.')[0]+'.txt'
#out_name = org_name +'.txt'
print(out_name)
import csv
import operator
from forex_python.bitcoin import BtcConverter
from tkinter.filedialog import askdirectory
from datetime import datetime, timedelta
import fnmatch
import os
#if you are using single file enable this instead
#filename = askopenfilename() 
#print(filename)

#if you are using multiple files in a single folder enable this instead
path = askdirectory(title ='Select Folder')

date_format_csv = '%Y-%m-%d %H:%M:%S'
date_format = '%d/%m/%Y %H:%M' 
date_min = "11/12/2020 0:10" #starting counting date 
date_max = "12/12/2020 0:10" #end counting date
username = ["PigDog","Imampunya","Ammar","qidds","jantc"] #keyword that the algo will search for in the folder
totalmined = [] #total mined for each username
GMT_convert = timedelta(hours=8) #timezone convert since NiceHash extract UTC timezone
mined = []
for names in username:
    for filename in os.listdir(path):
        if fnmatch.fnmatch(filename,names+'*.csv'):
            with open(path+"/"+filename,'r') as file:                
                csv_reader = csv.reader(file)
                print("Found", filename)
                file.seek(0)
                mined = []                                       
                next(csv_reader)        
                sort = sorted(csv_reader, key=operator.itemgetter(1,0))
                for row in sort:
                    if((datetime.strptime(row[0], date_format_csv) + GMT_convert) >= datetime.strptime(date_min, date_format) and (datetime.strptime(row[0], date_format_csv) + GMT_convert) <= datetime.strptime(date_max, date_format)):
                        mined.append(row[3])

    totalmined.append(0)
    for i in range(len(mined)):
        if(i+1 < len(mined)):
            if(float(mined[i+1]) < float(mined[i])):
                totalmined[len(totalmined)-1]+= float(mined[i])
        else:
            totalmined[len(totalmined)-1]+= float(mined[i])

    #print("Date: ",date_min," - ",date_max )
    #print("Total Mined: {:.8f} BTC".format(totalmined[len(totalmined)-1]))
    #print("Approx: RM{:.2f}".format(totalmined[len(totalmined)-1]*BtcConverter().get_latest_price("MYR")))

for i in range(len(username)):
    print(username[i],"\n{:.8f} BTC".format(totalmined[i]),"\nRM{:.2f}\n".format(totalmined[i]*BtcConverter().get_latest_price("MYR")))
#library
#--------------------------------------
import csv
from csv import reader, writer 
import operator
from forex_python.bitcoin import BtcConverter
from tkinter.filedialog import askdirectory
from datetime import datetime, timedelta, date
import fnmatch
import os
#--------------------------------------

#file-read
#--------------------------------------
#if you are using single file enable this instead
#filename = askopenfilename() 
#print(filename)

#if you are using multiple files in a single folder enable this instead
#path = askdirectory(title ='Select Folder') #if you want to use prompt
path = "C:/Users/AIMAN/Downloads" #if you dont want to use prompt
#--------------------------------------

#date-to-count
#--------------------------------------
date_format_csv = '%Y-%m-%d %H:%M:%S'
date_format = '%d-%m-%Y %H-%M'
today = date.today()

#date_min = "24-12-2020 00-10" #starting counting date
#date_max = "25-12-2020 00-00" #end counting date
date_min = (today - timedelta(days=1)).strftime('%d-%m-%Y 00-10')
date_max = today.strftime('%d-%m-%Y 00-00')
GMT_convert = timedelta(hours=8) #timezone convert since NiceHash extract UTC timezone, this is for UTC+8 Singapore, Hong Kong, Kuala Lumpur
#--------------------------------------


username = ["Imampunya","qidds","PigDog","Ammar","ja2060","Ren","Jai","Bocah","Mika"] #keyword that the algo will search for in the folder
totalmined = [] #total mined for each username
for names in username:
    mined_date = []
    totalmined.append(0)
    for filename in os.listdir(path):
        if fnmatch.fnmatch(filename,names+'*.csv'):
            with open(path+"/"+filename,'r') as file:                
                print("Found", filename)
                csv_reader = csv.reader(file)                
                file.seek(0)     #reset reader                                 
                next(csv_reader) #skip header
                sort = sorted(csv_reader, key=operator.itemgetter(0)) #sort csv by date
                for row in sort:
                    if((datetime.strptime(row[0], date_format_csv) + GMT_convert) >= datetime.strptime(date_min, date_format) and (datetime.strptime(row[0], date_format_csv) + GMT_convert) <= datetime.strptime(date_max, date_format)):
                        if(row[0][-4] == '9'): #find minutes that ends with 9 because that is when the total accumulated gets into balance
                            if(len(mined_date) == 0):
                                mined_date.append(row[0])
                                totalmined[len(totalmined)-1]+= float(row[2])
                            elif(mined_date[len(mined_date)-1] != row[0]):
                                mined_date.append(row[0])
                                totalmined[len(totalmined)-1]+= float(row[2])
print('')
print (date_min,'-',date_max,'\n')

for i in range(len(totalmined)):
    print(username[i],"\n{:.8f} BTC".format(totalmined[i]),"\nRM{:.2f}\n".format(totalmined[i]*BtcConverter().get_latest_price("MYR")))

formattedmined = []
for x in totalmined:
    formattedmined.append("{:.8f}".format(x))

import pathlib
x = 'D:\AIMAN\OneDrive - Universiti Teknologi MARA\AIMAN\Project\Last Hope Business\Mining'
a = [list(username),list(formattedmined)]
with open(x+"\\"+(today - timedelta(days=1)).strftime('%d-%m-%Y')+'.csv','w',newline='') as file:
    csv.writer(file, delimiter=',').writerows(a)

    

import csv
import operator
from forex_python.bitcoin import BtcConverter
from tkinter.filedialog import askopenfilename
from datetime import datetime, timedelta

filename = askopenfilename()
print(filename)
date_format_csv = '%Y-%m-%d %H:%M:%S'
date_format = '%d/%m/%Y %H:%M'
date_min = "8/12/2020 8:00"
date_max = "8/12/2020 23:55"
GMT_convert = timedelta(hours=8)
mined = []

with open(filename,'r') as file:
    csv = csv.reader(file)
    next(csv)
    sort = sorted(csv, key=operator.itemgetter(1,0))
    for row in sort:
        if((datetime.strptime(row[0], date_format_csv) + GMT_convert) >= datetime.strptime(date_min, date_format) and (datetime.strptime(row[0], date_format_csv) + GMT_convert) <= datetime.strptime(date_max, date_format)):
            mined.append(row[3])

totalmined = float(0)
for i in range(len(mined)):
    if(i+1 < len(mined)):
        if(float(mined[i+1]) < float(mined[i])):
            totalmined+= float(mined[i])
    else:
        totalmined+= float(mined[i])

print("Date: ",date_min," - ",date_max )
print("Total Mined: {:.8f} BTC".format(totalmined))
print("Approx: RM{:.2f}".format(totalmined*BtcConverter().get_latest_price("MYR")))
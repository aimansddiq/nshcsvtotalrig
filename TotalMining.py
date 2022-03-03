# library
# --------------------------------------
from sys import exit
import discord
import mysql.connector
import csv
from csv import reader, writer
import operator
from forex_python.bitcoin import BtcConverter
from tkinter.filedialog import askdirectory
from datetime import datetime, timedelta, date
import fnmatch
import os
import ctypes
import pyperclip
import webbrowser
import requests
# --------------------------------------

# file-read
# --------------------------------------
# if you are using single file enable this instead
#filename = askopenfilename()
# print(filename)

# if you are using multiple files in a single folder enable this instead
# path = askdirectory(title ='Select Folder') #if you want to use prompt
path = "C:/Users/AIMAN/Downloads"  # if you dont want to use prompt
# --------------------------------------

# variables
# --------------------------------------
btcprice = BtcConverter().get_latest_price("MYR")

date_format_export = '%Y-%m-%d'
date_format_csv = '%Y-%m-%d %H:%M:%S'
date_format = '%d-%m-%Y %H-%M'
today = date.today()

# date_min = "24-12-2020 00-10" #starting counting date
# date_max = "25-12-2020 00-00" #end counting date
date_min = (today - timedelta(days=1)).strftime('%d-%m-%Y 00-10')
date_max = today.strftime('%d-%m-%Y 00-00')
#date_max = (today - timedelta(days=1)).strftime('%d-%m-%Y 00-10')
date_csv = today.strftime(date_format_export)
yesterday = (today - timedelta(days=1)).strftime(date_format_export)
# timezone convert since NiceHash extract UTC timezone, this is for UTC+8 Singapore, Hong Kong, Kuala Lumpur
GMT_convert = timedelta(hours=8)
# --------------------------------------
def delete_prevfiles(names):
    mined_date = []
    total = 0
    for filename in os.listdir(path):
        if fnmatch.fnmatch(filename, names+'*'+yesterday+'.csv'):
            os.remove(path+"/"+filename)
                

def insert_into(link,page):
    url = link+page
    print(url)
    myobj = {'querysubmit': True, 'query': clipboard}
    try:
        x = requests.post(url, data=myobj)
        print(x.text)
    except Exception:
        print("Fail to update to ",link)

def send_discord(total):
    date_min = (today - timedelta(days=1)).strftime('%d-%m-%Y')
    message = "\nUPDATED FOR "+date_min+"\n"+link
    channel_id = 756761323593007194
    token = "NzAxMDM2OTQxMjEwMjg4MTU4.Xprphw.1UcLlS-76MWpQWmLfpxWC4LD3ec"
    client = discord.Client()

    @client.event
    async def on_ready():
        channel = client.get_channel(channel_id)
        await channel.send("TOTAL TODAY: "+'{:,.8f}'.format(total)+" BTC"+"\nTOTAL TODAY: RM "+'{:,.2f}'.format(total*btcprice)+"\nRATES: RM"+'{:,.2f}\n'.format(btcprice)+text+message)
        await client.close()
    client.run(token)

def open_file_and_calculate(names):
    mined_date = []
    total = 0
    for filename in os.listdir(path):
        if fnmatch.fnmatch(filename, names+'*'+date_csv+'.csv'):
            with open(path+"/"+filename, 'r') as file:
                print("Found", filename)
                csv_reader = csv.reader(file)
                file.seek(0)  # reset reader
                next(csv_reader)  # skip header
                # sort csv by date
                sort = sorted(csv_reader, key=operator.itemgetter(0))
                for row in sort:
                    if((datetime.strptime(row[0], date_format_csv) + GMT_convert) >= datetime.strptime(date_min, date_format) and (datetime.strptime(row[0], date_format_csv) + GMT_convert) <= datetime.strptime(date_max, date_format)):
                        # find minutes that ends with 9 because that is when the total accumulated gets into balance
                        if(row[0][-4] == '9'):
                            if(len(mined_date) == 0 or mined_date[len(mined_date)-1] != row[0]):
                                mined_date.append(row[0])
                                total += float(row[2])
    return total


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="lasthopemining"
)
mycursor = mydb.cursor(dictionary=True)
mycursor.execute("SELECT * FROM worker, miner WHERE worker.miner = miner.name")
results = mycursor.fetchall()
username = []
users = []
for x in results:
    username.append(x["worker_name"])
    users.append(x["name"])
print(username)
print(users)

try:
    for x in username:
        delete_prevfiles(x) # delete yesterday files
except:
    print("Failed to delete files")

totalmined = []  # total mined for each username
for names in username:
    mined_date = []
    totalmined.append(0)
    if(isinstance(names, list)):
        for i in names:
            #pass
            totalmined[len(totalmined)-1] += open_file_and_calculate(i)
    else:
        #pass
        totalmined[len(totalmined)-1] += open_file_and_calculate(names)
print('')
print(date_min, '-', date_max, '\n')

discord_ids = {
    "Harith": '<@286243149032980480>',
    "Bada" : '<@263117794806071296>',
    "Imam": '<@312210250465935361>',
    "Danial": '<@367700222517968896>',
    "Mija": '<@310414485552889857>',
    "Aiman": '<@130736886074441728>'
}

text = ""
for i in range(len(totalmined)):
    if(totalmined[i] > 0):
        try:
            tmp_name = discord_ids[users[i]]
        except:
            tmp_name = users[i]
        text += "**"+tmp_name+"**```\n{:.8f} BTC".format(
            totalmined[i])+"\nRM{:.2f}\n".format(totalmined[i]*btcprice)+"```"
        print(tmp_name, "\n{:.8f} BTC".format(
            totalmined[i]), "\nRM{:.2f}\n".format(totalmined[i]*btcprice))

# insert into database
date_sql = (today - timedelta(days=1)).strftime('%Y-%m-%d')
clipboard = "INSERT INTO mined (worker, amount, date) VALUES "
for i in range(len(totalmined)):
    if(totalmined[i] > 0):
        sql = "INSERT INTO mined (worker, amount, date) VALUES (%s, %s, %s)"
        val = (username[i], totalmined[i], date_sql)
        clipboard += "('"+str(username[i])+"', '" + \
            str(totalmined[i])+"', '"+str(date_sql)+"'),"
        try:
            #pass
            mycursor.execute(sql, val)
        except Exception:
            pass
        mydb.commit()
clipboard = clipboard[:-1]
print(clipboard)
link = 'https://lasthopemining.000webhostapp.com/'

insert_into(link,'action.php')

total_day = 0

for x in totalmined:
    total_day += x


print("Mined recorded")

# send message to discord
# ------------------------
send_discord(total_day)

webbrowser.open(link)
webbrowser.open("https://www.nicehash.com/my/dashboard")
webbrowser.open("https://shopee.com.my/shopee-coins/")
webbrowser.open("https://www.powerlanguage.co.uk/wordle/")

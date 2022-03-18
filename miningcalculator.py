import json
import nicehash
from datetime import datetime, timedelta
import urllib.parse
from forex_python.bitcoin import BtcConverter

def jsondata(file):
    f = open(file)
    data = json.load(f)
    return data

def list_rigs():
    path = '/main/api/v2/mining/rigs2'
    method = 'GET'
    rig_list = private_api.request(method, path, '', None)
    miners = {}
    for i in rig_list['miningRigs']:
        miners[i['name']] = i['rigId']
    return miners

def calculate_miners(miner, rigId):
    query = "rigId={}&afterTimestamp={}&beforeTimestamp={}".format(
        urllib.parse.quote_plus(rigId), yesterday_ts, today_ts)
    rig_details = private_api.request(
        'GET', '/main/api/v2/mining/rig/stats/unpaid', query, None)
    total = 0
    if (len(rig_details['data']) > 0):
        try:
            for j in range(len(rig_details['data'])):
                ts = rig_details['data'][j][0]
                dt = datetime.fromtimestamp(ts/1000)
                if(dt.strftime('%M') == '59'):
                    unpaid_amount = rig_details['data'][j][3]
                    total += unpaid_amount
        except:
            print('Fail')
    return total

btcprice = BtcConverter().get_latest_price("MYR")
data = jsondata('apikeys.json')
orgid = data["orgID"]
apikey = data['api-key-code']
secret = data["api-secret-code"]

host = 'https://api2.nicehash.com'
private_api = nicehash.private_api(host, orgid, apikey, secret)
today = datetime.now()
today = today.replace(hour=00, minute=3, second=0, microsecond=0)
yesterday = today - timedelta(days=1)
print("current time:-", today)
print("yesterday-", yesterday)
today_ts = int(today.timestamp() * 1000)
yesterday_ts = int(yesterday.timestamp() * 1000)

miners = list_rigs()
for i in miners:
    total = calculate_miners(i, miners[i])
    if(total > 0):
        print(i,"total BTC{0:.8f}".format(total),"/RM{0:.2f}".format(total*btcprice))
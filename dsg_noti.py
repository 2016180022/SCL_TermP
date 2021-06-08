#!/usr/bin/python
# coding=utf-8

import sys
import time
import sqlite3
import telepot
from pprint import pprint
import re
from datetime import date, datetime, timedelta
import traceback
import urllib.request
import urllib.parse
import http.client
import json

server = 'api.neople.co.kr'
apikey = 'rDbaGyKaYdUlFoFDidXiyOoeMB0mrR5M'
TOKEN = '1805503123:AAF33RL7yxA5M2CsGQ137IT77-Y30J2g4m8'
MAX_MSG_LENGTH = 300
conn = http.client.HTTPSConnection(server)
# baseurl = 'http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTrade?ServiceKey='+key

bot = telepot.Bot(TOKEN)

def getData(itemName):
    # res_list = []
    # url = baseurl+'&LAWD_CD='+loc_param+'&DEAL_YMD='+date_param
    eitemName = urllib.parse.quote(str(itemName).encode('UTF-8'))
    conn.request('GET', '/df/auction?itemName=' + eitemName + '&wordType=front&sort=unitPrice:asc,reinforce:<reinforce>,auctionNo:<auctionNo>&limit=10&apikey=' + apikey)
    response = conn.getresponse()
    cLen = response.getheader('Content-Length')
    result = response.read(int(cLen)).decode('UTF-8')

    Info = json.loads(result)

    unitPrice = {}
    for i in range(len(Info['rows'])):
        key = Info['rows'][i]['itemName']
        value = Info['rows'][i]['unitPrice']
        unitPrice[key] = value
        # unitPrice.append(Info['rows'][i]['itemName'])
        # unitPrice.append(Info['rows'][i]['unitPrice'])
    # #print(url)
    # res_body = urlopen(url).read()
    # #print(res_body)
    # soup = BeautifulSoup(res_body, 'html.parser')
    # items = soup.findAll('item')
    # for item in items:
    #     item = re.sub('<.*?>', '|', item.text)
    #     parsed = item.split('|')
    #     try:
    #         row = parsed[3]+'/'+parsed[6]+'/'+parsed[7]+', '+parsed[4]+' '+parsed[5]+', '+parsed[8]+'m², '+parsed[11]+'F, '+parsed[1].strip()+'만원\n'
    #     except IndexError:
    #         row = item.replace('|', ',')

    #     if row:
    #         res_list.append(row.strip())
    return unitPrice

def sendMessage(user, msg):
    try:
        bot.sendMessage(user, msg)
    except:
        traceback.print_exc(file=sys.stdout)

def run(date_param, param='11710'):
    conn = sqlite3.connect('logs.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS logs( user TEXT, log TEXT, PRIMARY KEY(user, log) )')
    conn.commit()

    user_cursor = sqlite3.connect('users.db').cursor()
    user_cursor.execute('CREATE TABLE IF NOT EXISTS users( user TEXT, location TEXT, PRIMARY KEY(user, location) )')
    user_cursor.execute('SELECT * from users')

    for data in user_cursor.fetchall():
        user, param = data[0], data[1]
        print(user, date_param, param)
        res_list = getData( param, date_param )
        msg = ''
        for r in res_list:
            try:
                cursor.execute('INSERT INTO logs (user,log) VALUES ("%s", "%s")'%(user,r))
            except sqlite3.IntegrityError:
                # 이미 해당 데이터가 있다는 것을 의미합니다.
                pass
            else:
                print( str(datetime.now()).split('.')[0], r )
                if len(r+msg)+1>MAX_MSG_LENGTH:
                    sendMessage( user, msg )
                    msg = r+'\n'
                else:
                    msg += r+'\n'
        if msg:
            sendMessage( user, msg )
    conn.commit()

if __name__=='__main__':
    today = date.today()
    current_month = today.strftime('%Y%m')

    print( '[',today,']received token :', TOKEN )

    pprint( bot.getMe() )

    #run(current_month)
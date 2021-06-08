#!/usr/bin/python
# coding=utf-8

import sys
import time
import sqlite3
import telepot
from pprint import pprint
from urllib.request import urlopen
#from bs4 import BeautifulSoup
import re
from datetime import date, datetime, timedelta
import traceback

import dsg_noti

def replyAptData(user, itemName = '시간의 결정'):
    print(user, itemName)
    martketPrice = dsg_noti.getData( itemName )
    msg = ''
    print(str(datetime.now()).split('.')[0] + ', 현재 가격')
    msg += str(datetime.now()).split('.')[0] + ', 현재 가격\n'
    for k, v in martketPrice.items():
        print(k + ', ' + str(v) + ' 골드')
        msg += k + ': '
        msg += str(v) + ' 골드\n'
    if msg:
        dsg_noti.sendMessage( user, msg )
    else:
        dsg_noti.sendMessage( user, '아이템을 찾을 수 없습니다.')

def save( user, loc_param ):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users( user TEXT, location TEXT, PRIMARY KEY(user, location) )')
    try:
        cursor.execute('INSERT INTO users(user, location) VALUES ("%s", "%s")' % (user, loc_param))
    except sqlite3.IntegrityError:
        dsg_noti.sendMessage( user, '이미 해당 정보가 저장되어 있습니다.' )
        return
    else:
        dsg_noti.sendMessage( user, '저장되었습니다.' )
        conn.commit()

def check( user ):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users( user TEXT, location TEXT, PRIMARY KEY(user, location) )')
    cursor.execute('SELECT * from users WHERE user="%s"' % user)
    for data in cursor.fetchall():
        row = 'id:' + str(data[0]) + ', location:' + data[1]
        dsg_noti.sendMessage( user, row )


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type != 'text':
        dsg_noti.sendMessage(chat_id, '난 텍스트 이외의 메시지는 처리하지 못해요.')
        return

    text = msg['text']
    args = text.split(' ')

    if text.startswith('가격') and len(args)>1:
        print('가격을 검색합니다', args[1])
        replyAptData(chat_id, args[1] )
    elif text.startswith('저장')  and len(args)>1:
        print('아이템을 저장합니다', args[1])
        save( chat_id, args[1] )
    elif text.startswith('확인'):
        print('저장된 아이템을 확인합니다')
        check( chat_id )
    else:
        dsg_noti.sendMessage(chat_id, '모르는 명령어입니다.\n가격 [아이템 이름], 저장 [아이템 이름], 확인 중 하나의 명령을 입력하세요.')


def run():
    today = date.today()
    current_month = today.strftime('%Y%m')

    print( '[',today,']received token :', dsg_noti.TOKEN )

    bot = telepot.Bot(dsg_noti.TOKEN)
    pprint( bot.getMe() )

    bot.message_loop(handle)

    print('Listening...')

    # while 1:
    #  time.sleep(10)

if __name__ == '__main__':
    run()
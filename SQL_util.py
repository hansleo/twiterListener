#-*- coding:utf8 -*-
import pymysql

conn = pymysql.connect(host='127.0.0.1', port=, user=, passwd=, db=, charset='utf8')


def select(data, option = ''):
    curs = conn.cursor()

    command = "SELECT " + str(data) + " FROM tweet "
    if str(option) != '':
        command += str(option)
    command += ';'
    print(command)
    curs.execute(command)

    return curs


def insert(data):
    curs = conn.cursor()
    command = "INSERT INTO tweet(DateTime, tweet_id, Text)  VALUES( " + data + ' ) ;'
    try:
        curs.execute(command)
        print('command', command)
        conn.commit()
    except:
        print('error')
        conn.rollback()


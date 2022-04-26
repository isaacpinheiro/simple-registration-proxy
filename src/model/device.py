#!/usr/bin/python
# -*- coding: utf-8 -*-

from src.config.mysql import connect

class Device:

    def find_by_token(self, token):

        obj = None
        conn = connect()
        cursor = conn.cursor()

        sql = 'select * from device where access_token = %s;'
        cursor.execute(sql, token)
        results = cursor.fetchall()

        if len(results) > 0:

            obj = {
                '_id': results[0][0],
                'dev_eui': results[0][1],
                'access_token': results[0][2]
            }

        cursor.close()
        conn.close()

        return obj

    def insert(self, obj):

        conn = connect()
        cursor = conn.cursor()

        sql = 'insert into device(dev_eui, access_token) values (%s, %s);'
        cursor.execute(sql, (obj['dev_eui'], obj['access_token']))
        conn.commit()
        _id = cursor.lastrowid

        cursor.close()
        conn.close()

        return _id


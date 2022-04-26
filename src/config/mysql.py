#!/usr/bin/python
# -*- coding: utf-8 -*-

from config import config
import pymysql

def connect():

    conn = pymysql.connect(
        config['db_host'],
        config['db_user'],
        config['db_pass'],
        config['db_name'],
    )

    return conn


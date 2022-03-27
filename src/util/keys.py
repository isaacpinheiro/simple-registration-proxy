#!/usr/bin/python
# -*- coding: utf-8 -*-

from random import randrange

def generate_random_key():

    res = ''

    for i in range(0, 32):

        n = randrange(0, 16)

        if n == 10: res += 'a'
        elif n == 11: res += 'b'
        elif n == 12: res += 'c'
        elif n == 13: res += 'd'
        elif n == 14: res += 'e'
        elif n == 15: res += 'f'
        else: res += str(n)

    return res



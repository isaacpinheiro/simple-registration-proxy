#!/usr/bin/python
# -*- coding: utf-8 -*-

import base64

# Convert hex values to Base64 bytes
def base64_bytes(hex_str):

    b64_str = base64.b64encode(bytearray.fromhex(hex_str)).decode()
    res = ''

    for b in b64_str:
        res += hex(ord(b))[2:]

    return res


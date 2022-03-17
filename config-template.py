#!/usr/bin/python
# -*- coding: utf-8 -*-

config = {}

# Proxy Configuration
config['proxy_host'] = '0.0.0.0'
config['proxy_port'] = 5000

# Identity Manager Configuration
config['idm_host'] = 'http://localhost'
config['idm_port'] = 3001
config['idm_ssl_verification'] = True # Always use True in production!

#ChirpStack Configuration
config['cs_host'] = 'http://localhost'
config['cs_port'] = 8080
config['cs_ssl_verification'] = True # Always use True in production!
config['cs_api_key'] = ''


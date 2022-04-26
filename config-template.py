#!/usr/bin/python
# -*- coding: utf-8 -*-

config = {}

# Proxy Configuration
config['db_host'] = 'localhost'
config['db_user'] = ''
config['db_pass'] = ''
config['db_name'] = 'simple_registration_proxy'
config['mqtt_broker'] = '127.0.0.1'
config['mqtt_port'] = 1883
config['mqtt_topic'] = 'proxy/+/#'
config['mqtt_client_id'] = 'simple-registration-proxy-1'
config['topic_regex'] = '^proxy/application/[0-9]*/device/[a-zA-Z0-9]*/event/up$'

# MQTT + TLS
config['mqtt_tls'] = False
config['mqtt_ca_cert'] = ''
config['mqtt_tls_cert'] = ''
config['mqtt_tls_key'] = ''
config['mqtt_tls_insecure'] = False # Always use False in production!

# Identity Manager Configuration
config['idm_https'] = False
config['idm_host'] = '127.0.0.1'
config['idm_port'] = 3001
config['idm_ssl_verification'] = True # Always use True in production!

#ChirpStack Configuration
config['cs_https'] = False
config['cs_host'] = '127.0.0.1'
config['cs_port'] = 8080
config['cs_ssl_verification'] = True # Always use True in production!
config['cs_api_key'] = ''


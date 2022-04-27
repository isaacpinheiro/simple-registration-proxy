#!/usr/bin/python
# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt
import http.client
import ssl
import json
import re

from config import config
from src.model.device import Device

def get_http_connection(url, https, verification):

    http_conn = None

    if https == True and verification == False:

        http_conn = http.client.HTTPSConnection(url, context = ssl._create_unverified_context())

    elif https == True and verification == True:

        http_conn = http.client.HTTPSConnection(url)

    else:

        http_conn = http.client.HTTPConnection(url)

    return http_conn

def verify_access_token(token):

    authorized = False
    idm_url = '/user?access_token=' + token

    http_conn = get_http_connection(
        config['idm_host'] + ':' + str(config['idm_port']),
        config['idm_https'],
        config['idm_ssl_verification']
    )

    http_conn.request('GET', idm_url)
    obj = json.loads(http_conn.getresponse().read().decode())
    http_conn.close()

    if obj.get('app_id') != None:
        authorized = True

    return authorized

def register_device(payload):
    pass

def connect_mqtt() -> mqtt:

    def on_connect(client, userdata, flags, rc):

        if rc == 0:
            print('Connected to MQTT Broker!')
        else:
            print('Failed to connect, return code %d\n', rc)

    client = mqtt.Client(config['mqtt_client_id'])
    #client.username_pw_set(username, password)
    client.on_connect = on_connect

    if config['mqtt_tls'] == True:
        client.tls_set(config['mqtt_ca_cert'], certfile = config['mqtt_tls_cert'], keyfile = config['mqtt_tls_key'])
        client.tls_insecure_set(config['mqtt_tls_insecure'])

    client.connect(config['mqtt_broker'], config['mqtt_port'])
    return client

def subscribe(client: mqtt):

    def on_message(client, userdata, msg):

        if re.match(config['topic_regex'], msg.topic) != None:

            payload = json.loads(msg.payload.decode())

            if verify_access_token(payload.get('access_token')) == False:
                client.publish('access', 'unauthorized')
            else:

                dvc = Device()
                d = dvc.find_by_token(payload.get('access_token'))
                integration_topic = msg.topic.split('proxy/')[1]

                if d != None and d.get('dev_eui') != payload.get('devEUI'):

                    client.publish('access', 'unauthorized')

                elif d != None and d.get('dev_eui') == payload.get('devEUI'):

                    client.publish(integration_topic, msg.payload.decode())

                else:

                    obj = {
                        'dev_eui': payload['devEUI'],
                        'access_token': payload['access_token']
                    }

                    dvc.insert(obj)
                    register_device(payload)
                    client.publish(integration_topic, msg.payload.decode())

    client.subscribe(config['mqtt_topic'])
    client.on_message = on_message

if __name__ == '__main__':
    print('simple-auth-proxy\n')
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()



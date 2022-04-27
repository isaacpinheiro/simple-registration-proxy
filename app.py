#!/usr/bin/python
# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt
import requests as req
import ssl
import json
import re

from config import config
from src.model.device import Device

def verify_access_token(token):

    authorized = False
    idm_url = config['idm_host'] + ':' + str(config['idm_port']) + '/user?access_token=' + token

    if config['idm_https'] == True:
        idm_url = 'https://' + idm_url
    else:
        idm_url = 'http://' + idm_url

    res = req.request('GET', idm_url, verify=config['idm_ssl_verification'])
    obj = json.loads(res.text)
    res.close()

    if obj.get('app_id') != None:
        authorized = True

    return authorized

def register_device(payload):

    cs_url = config['cs_host'] + ':' + str(config['cs_port']) + '/api/devices'

    if config['cs_https'] == True:
        cs_url = 'https://' + cs_url
    else:
        cs_url = 'http://' + cs_url

    header = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Grpc-Metadata-Authorization': 'Bearer ' + config['cs_api_key']
    }

    payload_body = {
        'device': {
            'applicationID': payload['applicationID'],
            'description': 'Device ' + payload['devEUI'],
            'devEUI': payload['devEUI'],
            'deviceProfileID': payload['deviceProfileID'],
            'isDisabled': True,
            'name': 'Device ' + payload['devEUI'],
            'referenceAltitude': 0,
            'skipFCntCheck': True,
            'tags': {},
            'variables': {}
        }
    }

    res = req.request(
        'POST',
        cs_url,
        verify=config['cs_ssl_verification'],
        json=payload_body,
        headers=header
    )

    res.close()

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



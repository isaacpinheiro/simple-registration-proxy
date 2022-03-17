#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask
from config import config
from src.controller.device_controller import device_controller

app = Flask(__name__)
app.register_blueprint(device_controller, url_prefix='/device')

@app.route('/')
def index():
    return 'simple-auth-proxy\n'

if __name__ == '__main__':
    app.run(host=config['proxy_host'], port=config['proxy_port'])


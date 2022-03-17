#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Blueprint

device_controller = Blueprint('device_controller', __name__)

@device_controller.route('/msg', methods=['GET'])
def device_msg():
    # TODO
    return {'msg': 'success'}


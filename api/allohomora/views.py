"""
Api endpoints
"""
from multiprocessing import Process
from flask import jsonify

from allohomora import app, Doorbell
import config

doorbell = Doorbell(config.RELAY_IO, config.RELAY_IO)


@app.route("/")
def hello():
    return jsonify(hello='world')


@app.route("/open")
def door_open():
    Process(target=doorbell.open, args=(config.OPEN_TIME,)).start()
    return jsonify(status='opened')

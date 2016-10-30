"""
Api endpoints
"""
import multiprocessing
from flask import jsonify

from allohomora import app, Doorbell
import config

doorbell = Doorbell(config.RELAY_IO, config.RELAY_IO)


@app.route("/")
def hello():
    return jsonify(hello='world')


@app.route("/open")
def door_open():
    if len(multiprocessing.active_children()) < 1:
        multiprocessing.Process(target=doorbell.open, args=(config.OPEN_TIME,)).start()
    return jsonify(status='opened')

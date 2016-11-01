"""
Api endpoints
"""
from flask import jsonify

from allohomora import app, Doorbell
from allohomora.doorbell import open_signal
import config

doorbell = Doorbell(config.RELAY_IO, config.BELL_IO, config.OPEN_IO)

@app.route("/")
def hello():
    return jsonify(hello='world')


@app.route("/open")
def door_open():
    open_signal.send(source='api')
    doorbell.open(config.OPEN_TIME)
    return jsonify(status='opened')

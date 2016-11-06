"""
Api endpoints
"""

from flask import jsonify

from allohomora import app, doorbell
from allohomora.doorbell import open_signal
import config


@app.route("/")
def hello():
    return jsonify(hello='world')


@app.route("/open")
def door_open():
    if doorbell.open(config.OPEN_TIME):
        open_signal.send(source='api')
    return jsonify(status='opened')

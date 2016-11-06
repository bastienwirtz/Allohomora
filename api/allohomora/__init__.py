from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
import config

app = Flask(__name__)
CORS(app)

socketio = SocketIO(app)

from .event import Event
from .doorbell import Doorbell

doorbell = Doorbell(config.RELAY_IO, config.BELL_IO, config.OPEN_IO)
doorbell.start_read_inputs()

import sys
import signal
import config
from allohomora import app, socketio, views, Event
from allohomora.doorbell import open_signal, bell_signal

open_signal.connect(Event.open)
bell_signal.connect(Event.ring)

def shutdown(signum, frame):
    sys.exit(0)

signal.signal(signal.SIGINT, shutdown)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", debug=config.DEBUG)

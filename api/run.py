import sys
import signal
from allohomora import app, views


def shutdown(signum, frame):
    sys.exit(0)

signal.signal(signal.SIGINT, shutdown)

if __name__ == "__main__":
    app.run(host="0.0.0.0")

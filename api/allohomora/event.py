"""
Event handling
"""

from allohomora import socketio
from datetime import datetime

class Event(object):

    @staticmethod
    def open(sender, source):
        socketio.emit("opened", {'source': source, "time": datetime.now().isoformat()})

    @staticmethod
    def ring(sender):
        socketio.emit('ringing')


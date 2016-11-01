"""
Event handling
"""

from allohomora import socketio


class Event(object):

    @staticmethod
    def open(sender, source):
        socketio.emit('opened', {'source': source}, namespace='/')

    @staticmethod
    def ring(sender):
        socketio.emit('ringing', namespace='/')


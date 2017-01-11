import time
from datetime import datetime
from threading import Thread
import multiprocessing
import RPi.GPIO as GPIO
from picamera import PiCamera

from blinker import signal
open_signal = signal('open')
bell_signal = signal('bell')


class Doorbell(object):
    """
    Manage raspberry pi doorbell
    """

    def __init__(self, gpio_relay, gpio_bell, gpio_open):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(gpio_relay, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(gpio_bell, GPIO.IN, GPIO.PUD_UP)
        GPIO.setup(gpio_open, GPIO.IN, GPIO.PUD_UP)

        self.input_bell = {"channel": gpio_bell, "state": None, "signal": bell_signal}
        self.input_open = {"channel": gpio_open, "state": None, "signal": open_signal, "relay": gpio_relay}
        self.input_thread = None

        self.camera = PiCamera()
        self.camera.start_preview(alpha=200)

    def _read_inputs(self):
        while bool(self.input_bell):
            ring_current_state = GPIO.input(self.input_bell["channel"])
            open_current_state = GPIO.input(self.input_open["channel"])

            # Doorbell open button detection.
            if self.input_open["state"] != open_current_state:
                if open_current_state:
                    GPIO.output(self.input_open["relay"], GPIO.HIGH)
                else:
                    self.input_open["signal"].send(source="input")
                    GPIO.output(self.input_open["relay"], GPIO.LOW)
                self.input_open["state"] = open_current_state

            # Doorbell ring button detection.
            if self.input_bell["state"] != ring_current_state:
                if not GPIO.input(self.input_bell["channel"]):
                    now = datetime.now().replace(microsecond=0).isoformat()
                    self.camera.capture("/var/www/html/capture/capture-%s.jpg" % (now,))
                    self.input_bell["signal"].send()
                self.input_bell["state"] = ring_current_state

            time.sleep(0.2)

    def start_read_inputs(self):
        if self.input_thread is None:
            self.input_thread = Thread(target=self._read_inputs, daemon=True)
            self.input_thread.start()

    def _open(self, duration):
        GPIO.output(self.input_open["relay"], GPIO.LOW)
        time.sleep(duration)
        GPIO.output(self.input_open["relay"], GPIO.HIGH)

    def open(self, duration):
        if len(multiprocessing.active_children()) < 1:
            multiprocessing.Process(target=self._open, args=(duration,)).start()
            return True

        # Door already open
        return False

    def shutdown(self):
        self.camera.stop_preview()
        self.input_bell = None
        GPIO.cleanup()

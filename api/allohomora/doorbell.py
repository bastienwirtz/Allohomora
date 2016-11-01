import time
import multiprocessing
import RPi.GPIO as GPIO

from blinker import signal
open_signal = signal('open')
bell_signal = signal('bell')

class Doorbell(object):
    """
    Manage raspberry pi doorbell
    """

    def __init__(self, gpio_relay, gpio_bell, gpio_open):
        self.gpio_relay = gpio_relay
        self.gpio_bell = gpio_bell
        self.gpio_open = gpio_open

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_relay, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(self.gpio_bell, GPIO.IN, GPIO.PUD_UP)
        GPIO.setup(self.gpio_open, GPIO.IN, GPIO.PUD_UP)

        GPIO.add_event_detect(self.gpio_bell, GPIO.FALLING, callback=self.ring, bouncetime=300)
        GPIO.add_event_detect(self.gpio_open, GPIO.BOTH, callback=self._push_open, bouncetime=50)

    def _push_open(self, channel):
        if GPIO.input(channel):
            GPIO.output(self.gpio_relay, GPIO.HIGH)
        else:
            open_signal.send(source="button")
            GPIO.output(self.gpio_relay, GPIO.LOW)

    def _open(self, duration):
        GPIO.output(self.gpio_relay, GPIO.LOW)
        time.sleep(duration)
        GPIO.output(self.gpio_relay, GPIO.HIGH)

    def open(self, duration):
        if len(multiprocessing.active_children()) < 1:
            multiprocessing.Process(target=self._open, args=(duration,)).start()

    def ring(self, channel):
        bell_signal.send()

    def __del__(self):
        GPIO.cleanup()

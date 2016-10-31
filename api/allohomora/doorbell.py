import time
import multiprocessing
import RPi.GPIO as GPIO

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

        GPIO.add_event_detect(self.gpio_bell, GPIO.FALLING, callback=self.printio, bouncetime=350)
        GPIO.add_event_detect(self.gpio_open, GPIO.FALLING, callback=self.printio, bouncetime=350)

    def _open(self, duration):
        GPIO.output(self.gpio_relay, GPIO.LOW)
        time.sleep(duration)
        GPIO.output(self.gpio_relay, GPIO.HIGH)

    def open(self, duration):
        print(multiprocessing.active_children())
        if len(multiprocessing.active_children()) < 1:
            multiprocessing.Process(target=self._open, args=(duration,)).start()

    def printio(self, channel):
        print("Detected (%s)" % channel)

    def __del__(self):
        GPIO.cleanup()

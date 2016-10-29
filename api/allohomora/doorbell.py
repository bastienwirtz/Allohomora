import time
import RPi.GPIO as GPIO

class Doorbell(object):
    """
    Manage raspberry pi doorbell
    """

    def __init__(self, gpio_relay, gpio_bell):
        self.gpio_relay = gpio_relay
        self.gpio_bell = gpio_bell

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_relay, GPIO.OUT)

    def open(self, duration):
        GPIO.output(self.gpio_relay, GPIO.HIGH)
        time.sleep(duration)
        GPIO.output(self.gpio_relay, GPIO.LOW)

    def __del__(self):
        GPIO.cleanup()

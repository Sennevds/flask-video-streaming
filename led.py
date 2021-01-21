import RPi.GPIO as GPIO

class Led():
    _pin = 0
    def __init__(self, pin):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        if(pin is not None):
            self._pin = pin
        GPIO.setup(self._pin, GPIO.OUT)

    def status(self):
        return GPIO.input(self._pin)
    def leds_on(self):
        return self.status() == 1
    def switch_leds(self, on):
        if(on):
            GPIO.output(self._pin, GPIO.HIGH)
        else:
            GPIO.output(self._pin, GPIO.LOW)

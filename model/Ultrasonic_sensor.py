import time
from RPi import GPIO

class Ultrasonic_sensor:
    def __init__(self, echo, trigger):
        self.echo = echo
        self.trigger = trigger
        self.__setup()

    def __setup(self):
        GPIO.setup(self.echo, GPIO.IN)
        GPIO.setup(self.trigger, GPIO.OUT)
        GPIO.output(self.trigger, GPIO.LOW)
        time.sleep(1)

    def ultrasonic_sensor_uitlezen(self):
        GPIO.output(self.trigger, True)
        time.sleep(0.00001)
        GPIO.output(self.trigger, False)
        time_start = time.time()
        pulse_start = time.time()
        while GPIO.input(self.echo)==0:              # de sensor zet de echo pin achteraf evenlang high als het gedruurt heeft voor de trigger puls terug te keren
            pulse_start = time.time()
            if (time.time()-time_start) > 0.01:
               return 20000
        while GPIO.input(self.echo)==1:
            pulse_end = time.time()
            if (time.time()-pulse_start) > 0.01:
               return 20000
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150
        return round(distance, 2)
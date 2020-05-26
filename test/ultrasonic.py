import time
from RPi import GPIO

echo = 19
trigger = 26

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(echo, GPIO.IN)
    GPIO.setup(trigger, GPIO.OUT)
    GPIO.output(trigger, GPIO.LOW)
    time.sleep(2)

def ultrasonic_sensor():
    GPIO.output(trigger, True)
    time.sleep(0.00001)
    GPIO.output(trigger, False)
    pulse_start = time.time()
    while GPIO.input(echo)==0:              # de sensor zet de echo pin achteraf evenlang high als het gedruurt heeft voor de trigger puls terug te keren
        pulse_start = time.time()
    while GPIO.input(echo)==1:
        pulse_end = time.time()
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    return round(distance, 2)

try:
    setup()
    while True:
        distance = ultrasonic_sensor()
        print(f'Distance: {distance}cm.')
        time.sleep(0.05)
except KeyboardInterrupt as e:
    print(e)
finally:
    GPIO.cleanup()
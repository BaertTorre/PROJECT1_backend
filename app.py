from repositories.DataRepository import DataRepository
from flask import Flask, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS
from RPi import GPIO
import pigpio
import time

# klasses importeren
from model.Ultrasonic_sensor import Ultrasonic_sensor
from model.Esp8266 import Esp8266
from model.PWM_reader import PWM_reader
from model.GPS import GPS

# pinnen
channel1_pin = 13
channel2_pin = 6
channel3_pin = 5
#channel4_pin = 22
servo_pin = 16
esc_pin_hover = 21
esc_pin_forward = 20
trigger_rechts = 26
echo_rechts = 19
trigger_midden = 12
echo_midden = 25
trigger_links = 24
echo_links = 23
spots = 18

# var
object_avoidance = False
automatic_spots = True
led_aan = False

# methodes
def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(channel1_pin, GPIO.IN)
    GPIO.setup(channel2_pin, GPIO.IN)
    GPIO.setup(channel3_pin, GPIO.IN)
    GPIO.setup(spots, GPIO.OUT)
    #GPIO.setup(channel4_pin, GPIO.IN)

def omvormen_voor_servo(value):
    puls_width = 530 + ((value - 1000) * 1.870)         # bij elke servo anders, min 530, max 2400
    return puls_width

def omvormen_voor_esc(value):
    return value

try:
    setup()
    pi = pigpio.pi()
    GPS1 = GPS()
    begin_time = time.time()
    # PWM reader objecten maken
    channel1 = PWM_reader(pi, channel1_pin)
    channel2 = PWM_reader(pi, channel2_pin)
    channel3 = PWM_reader(pi, channel3_pin)
    #channel4 = PWM_reader(pi, channel4_pin)

    # ultrasonic sensors objecten maken
    ultrasonic_sensor_rechts = Ultrasonic_sensor(echo_rechts, trigger_rechts)
    ultrasonic_sensor_links = Ultrasonic_sensor(echo_links, trigger_links)
    ultrasonic_sensor_midden = Ultrasonic_sensor(echo_midden, trigger_midden)
    while True:
        if channel1.pulse_width():              # checken of er al verbinding is met de controller
            puls_width1 = omvormen_voor_servo(channel1.pulse_width())
            puls_width2 = omvormen_voor_esc(channel2.pulse_width())
            puls_width3 = omvormen_voor_esc(channel3.pulse_width())
            #puls_width4 = omvormen_voor_esc(channel4.pulse_width())
            ultrasonic_rechts_afstand = ultrasonic_sensor_rechts.ultrasonic_sensor_uitlezen()
            ultrasonic_midden_afstand = ultrasonic_sensor_midden.ultrasonic_sensor_uitlezen()
            ultrasonic_links_afstand = ultrasonic_sensor_links.ultrasonic_sensor_uitlezen()
            if object_avoidance == True:
                if ultrasonic_rechts_afstand > 100 and ultrasonic_midden_afstand > 100 and ultrasonic_links_afstand > 100:
                    pi.set_servo_pulsewidth(servo_pin, puls_width1)
                    pi.set_servo_pulsewidth(esc_pin_hover, puls_width3)
                    pi.set_servo_pulsewidth(esc_pin_forward, puls_width2)
                elif ultrasonic_rechts_afstand < 100 and ultrasonic_midden_afstand > 20 and ultrasonic_rechts_afstand < ultrasonic_links_afstand:
                    pi.set_servo_pulsewidth(servo_pin, 2400)
                    pi.set_servo_pulsewidth(esc_pin_hover, puls_width3)
                    pi.set_servo_pulsewidth(esc_pin_forward, puls_width2)
                elif ultrasonic_links_afstand < 100 and ultrasonic_midden_afstand > 20 and ultrasonic_links_afstand < ultrasonic_rechts_afstand:
                    pi.set_servo_pulsewidth(servo_pin, 530)
                    pi.set_servo_pulsewidth(esc_pin_hover, puls_width3)
                    pi.set_servo_pulsewidth(esc_pin_forward, puls_width2)
                elif ultrasonic_midden_afstand > 20 and ultrasonic_rechts_afstand > 10 and ultrasonic_links_afstand > 10:
                    pi.set_servo_pulsewidth(servo_pin, 530)
                    pi.set_servo_pulsewidth(esc_pin_hover, puls_width3)
                    pi.set_servo_pulsewidth(esc_pin_forward, puls_width2)
                else:
                    pi.set_servo_pulsewidth(esc_pin_hover, 0)
                    pi.set_servo_pulsewidth(esc_pin_forward, 0)
            else:
                pi.set_servo_pulsewidth(servo_pin, puls_width1)
                pi.set_servo_pulsewidth(esc_pin_hover, puls_width3)
                pi.set_servo_pulsewidth(esc_pin_forward, puls_width2)
        else:
            pi.set_servo_pulsewidth(esc_pin_hover, 0)
            pi.set_servo_pulsewidth(esc_pin_forward, 0)
            pi.set_servo_pulsewidth(servo_pin, 0)
        
        # om de 5 seconden 
        if (begin_time + 5) < time.time():
            #coordinaten = GPS1.read_GPS_cor()
            LDR_value = Esp8266.read_LDR()
            if automatic_spots == True:
                if LDR_value < 600:
                    GPIO.output(spots, GPIO.HIGH)
                    led_aan = True
                else:
                    GPIO.output(spots, GPIO.LOW)
                    led_aan = False
            # add to database
            id_time = DataRepository.make_time_event(200)
            DataRepository.add_ldr_waarde(LDR_value, id_time)
            DataRepository.add_led_waarde(led_aan, id_time)
            DataRepository.add_ultrasone_waarde(ultrasonic_rechts_afstand, ultrasonic_midden_afstand,ultrasonic_links_afstand, id_time)
            begin_time = time.time()
except KeyboardInterrupt as e:
    print(e)
finally:
    channel1.cancel()
    channel2.cancel()
    channel3.cancel()
    #channel4.cancel()
    pi.set_servo_pulsewidth(servo_pin, 0)
    GPIO.cleanup()
    pi.stop()

# SOCKET IO
app = Flask(__name__)
app.config['SECRET_KEY'] = 'Hier mag je om het even wat schrijven, zolang het maar geheim blijft en een string is'

socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)

@socketio.on('connect')             # connect ontvangt hij standaard bij connectie
def initial_connection():
    print('A new client connect')

@socketio.on('F2B_ultrasonic')
def ultrasonic():
    distance = []
    distance.append(ultrasonic_sensor1.ultrasonic_sensor_uitlezen())
    i = 0
    for value in distance:
        DataRepository.add_ultrasone_waarde(value, i)
    socketio.emit('B2F_ultrasonic_data', distance)


# if __name__ == '__main__':
#     socketio.run(app, debug=False, host='0.0.0.0')

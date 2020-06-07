from repositories.DataRepository import DataRepository
from flask import Flask, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS
from RPi import GPIO
import pigpio
import time
from threading import Thread

# klasses importeren
from model.Ultrasonic_sensor import Ultrasonic_sensor
from model.Esp8266 import Esp8266
from model.PWM_reader import PWM_reader
from model.GPS import GPS

# socket setup
app = Flask(__name__)
app.config['SECRET_KEY'] = 'Goeie J'

socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)

# pinnen
channel1_pin = 13
channel2_pin = 6
channel3_pin = 5
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
running = True

# methodes
def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(channel1_pin, GPIO.IN)
    GPIO.setup(channel2_pin, GPIO.IN)
    GPIO.setup(channel3_pin, GPIO.IN)
    GPIO.setup(spots, GPIO.OUT)

def omvormen_voor_servo(value):
    puls_width = 530 + ((value - 1000) * 1.870)         # bij elke servo anders, min 530, max 2400
    return puls_width

def omvormen_voor_esc(value):
    return value

def uitlezen_ultrasone_sensors():
    global ultrasonic_rechts_afstand
    global ultrasonic_midden_afstand
    global ultrasonic_links_afstand
    global running
    # ultrasonic sensors uitlezen
    while running == True:
        ultrasonic_rechts_afstand = ultrasonic_sensor_rechts.read()
        ultrasonic_midden_afstand = ultrasonic_sensor_midden.read()
        ultrasonic_links_afstand = ultrasonic_sensor_links.read()
        time.sleep(0.1)

def besturing():
    global ultrasonic_rechts_afstand
    global ultrasonic_midden_afstand
    global ultrasonic_links_afstand
    if channel1.pulse_width():              # checken of er verbinding is met de controller
        puls_width1 = omvormen_voor_servo(channel1.pulse_width())
        puls_width2 = omvormen_voor_esc(channel2.pulse_width())
        puls_width3 = omvormen_voor_esc(channel3.pulse_width())
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

def serieel_uitlezen_ldr():
    global running 
    while running == True:
        data = Esp8266.read_LDR()
        LDR_verwerken(data)
        time.sleep(2)

def LDR_verwerken(LDR_data):
    global running
    global LDR_value
    global led_aan
    if LDR_data is not None:
        LDR_value = LDR_data
        if automatic_spots == True:
            if LDR_value < 600:
                GPIO.output(spots, GPIO.HIGH)
                led_aan = True
            else:
                GPIO.output(spots, GPIO.LOW)
                led_aan = False

def serieel_uitlezen_gps():
    global running
    global coordinaten
    while running == True:
        # coordinaten = GPS1.read_GPS_cor()
        pass

def socket_start():
    socketio.run(app, debug=False, host='0.0.0.0')

def database_wegschrijven():
    global running
    global LDR_value
    global led_aan
    global coordinaten
    global ultrasonic_rechts_afstand
    global ultrasonic_midden_afstand
    global ultrasonic_links_afstand
    while running == True:
        time.sleep(5)
        id_time = DataRepository.make_time_event(200)
        DataRepository.add_ldr_waarde(LDR_value, id_time)
        DataRepository.add_led_waarde(led_aan, id_time)
        DataRepository.add_ultrasone_waarde(ultrasonic_rechts_afstand, ultrasonic_midden_afstand, ultrasonic_links_afstand, id_time)
        # DataRepository.add_gps_data(coordinaten[0], coordinaten[1], coordinaten[2], id_time)
    
# SOCKET IO
@socketio.on('connect')             # connect ontvangt hij standaard bij connectie
def initial_connection():
    print('A new client connect')

@socketio.on('F2B_ultrasonic')
def ultrasonic():
    global ultrasonic_rechts_afstand
    global ultrasonic_midden_afstand
    global ultrasonic_links_afstand
    distance = [ultrasonic_links_afstand, ultrasonic_midden_afstand, ultrasonic_rechts_afstand]
    socketio.emit('B2F_ultrasonic_data', distance)

try:
    setup()
    pi = pigpio.pi()
    GPS1 = GPS()
    begin_time = time.time()

    # PWM reader objecten maken
    channel1 = PWM_reader(pi, channel1_pin)
    channel2 = PWM_reader(pi, channel2_pin)
    channel3 = PWM_reader(pi, channel3_pin)

    # ultrasone sensors objecten aanmaken
    ultrasonic_sensor_rechts = Ultrasonic_sensor(pi, echo_rechts, trigger_rechts)
    ultrasonic_sensor_links = Ultrasonic_sensor(pi, echo_links, trigger_links)
    ultrasonic_sensor_midden = Ultrasonic_sensor(pi, echo_midden, trigger_midden)

    # ultrasonic sensors thread starten
    thread_ultrasoon = Thread(target=uitlezen_ultrasone_sensors, args=())
    thread_ultrasoon.start()

    # serieel uitlezen ldr thread starten
    thread_ldr = Thread(target=serieel_uitlezen_ldr, args=())
    thread_ldr.start()

    # serieel uitlezen gps thread starten
    thread_gps = Thread(target=serieel_uitlezen_gps, args=())
    thread_gps.start()

    # database thread starten
    thread_database = Thread(target=database_wegschrijven, args=())
    thread_database.start()

    # socket thread starten
    thread_socket = Thread(target=socket_start, args=())
    thread_socket.start()

    time.sleep(0.5)

    while True: 
        print(ultrasonic_rechts_afstand, ultrasonic_midden_afstand, ultrasonic_links_afstand)       
        besturing()
        time.sleep(0.1)
except KeyboardInterrupt as e:
    print(e)
finally:
    running = False
    channel1.cancel()
    channel2.cancel()
    channel3.cancel()
    ultrasonic_sensor_rechts.cancel()
    ultrasonic_sensor_links.cancel()
    ultrasonic_sensor_midden.cancel()
    pi.set_servo_pulsewidth(servo_pin, 0)
    pi.set_servo_pulsewidth(esc_pin_hover, 0)
    pi.set_servo_pulsewidth(esc_pin_forward, 0)
    socketio.stop()
    time.sleep(6)                                       # zodat alle threads mooi kunnen afsluiten
    GPIO.cleanup()
    pi.stop()

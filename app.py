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

# pinnen
channel1_pin = 13
channel2_pin = 6
channel3_pin = 5
channel4_pin = 22
servo_pin = 16

# var


# methodes
def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(channel1_pin, GPIO.IN)
    GPIO.setup(channel2_pin, GPIO.IN)
    GPIO.setup(channel3_pin, GPIO.IN)
    GPIO.setup(channel4_pin, GPIO.IN)

def omvormen_voor_servo(value):
    puls_width = 530 + ((value - 1000) * 1.870)         # bij elke servo anders, min 530, max 2400
    return puls_width

try:
    setup()
    pi = pigpio.pi()
    # PWM reader objecten maken
    channel1 = PWM_reader(pi, channel1_pin)
    channel2 = PWM_reader(pi, channel2_pin)
    channel3 = PWM_reader(pi, channel3_pin)
    channel4 = PWM_reader(pi, channel4_pin)
    # ultrasonic sensors objecten maken
    ultrasonic_sensor1 = Ultrasonic_sensor(19, 26)
    while True:
        puls_width = omvormen_voor_servo(channel1.pulse_width())
        if 529 < puls_width < 2401:
            pi.set_servo_pulsewidth(servo_pin, puls_width)
        print(f'{channel1.pulse_width()}    {channel2.pulse_width()}    {channel3.pulse_width()}    {channel4.pulse_width()}    ')
except KeyboardInterrupt as e:
    print(e)
finally:
    channel1.cancel()
    channel2.cancel()
    channel3.cancel()
    channel4.cancel()
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

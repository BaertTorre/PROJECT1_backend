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

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Hier mag je om het even wat schrijven, zolang het maar geheim blijft en een string is'

socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)

# ultrasonic sensors objecten maken
ultrasonic_sensor1 = Ultrasonic_sensor(19, 26)

# SOCKET IO
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


if __name__ == '__main__':
    socketio.run(app, debug=False, host='0.0.0.0')
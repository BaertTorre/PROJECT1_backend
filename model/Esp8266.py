import serial

ser = serial.Serial('/dev/serial0')     # open serial port (serial0 is altijd de seriele poort en geen bluetooth ongeacht de config)

class Esp8266:
    @staticmethod
    def read_serial():
        data = ser.readline()
        return data

    @staticmethod
    def read_LDR():
        ser.write(b'LDR')                     # write a string de 'b' zorgt ervoor dat de tekst gecodeert wordt in bytes
        data = Esp8266.read_serial()
        return data
import serial

ser = serial.Serial('/dev/ttyS0')     # open serial port, dit is de eerste seriele poort op de pi 4

class Esp8266:
    @staticmethod
    def read_serial():
        data = ser.readline()
        return data

    @staticmethod
    def read_LDR():
        ser.write(b'LDR')                     # write a string de 'b' zorgt ervoor dat de tekst gecodeert wordt in bytes
        data = Esp8266.read_serial()
        try:
            data = int(data)
        except Exception:
            data = None
        return data
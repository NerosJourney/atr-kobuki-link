import serial
import time

bluetooth_serial = 'rfcomm0'
ser = serial.Serial(f'/dev/{bluetooth_serial}', 115200, timeout=10)

def process_msg():
    s = ser.readline()
    print(s)

def send_msg():
    # ser.write(b'\xcc\xff\x55\x01\x09\x02\x01\x04\x07\x02\x02\x90\x07\x05\xff\n')
    ser.write(b'\xcc\xff\x55\x01\x07\x04\x04\x02\x00\x00\x01\x00\xff\n')
    # ser.write(b'\xcc\xff\x55\x01\x04\x02\x01\x09\x11\xff\n')

time.sleep(4)

# send_msg()

while True:
    send_msg()
    time.sleep(2)
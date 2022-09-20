import serial
import time

# In Ubuntu, you use 'rfcomm bind' to connect to the hc-06 on the arduino
bluetooth_serial = 'rfcomm0'
ser = serial.Serial(f'/dev/{bluetooth_serial}', 115200, timeout=10)

# def process_msg():
#     s = ser.readline()
#     print(s)

# def send_msg():
#     # ser.write(b'\xcc\xff\x55\x01\x09\x02\x01\x04\x07\x02\x02\x90\x07\x05\xff\n')
#     ser.write(b'\xcc\xff\x55\x01\x07\x04\x04\x02\x00\x00\x01\x00\xff\n')
#     # ser.write(b'\xcc\xff\x55\x01\x04\x02\x01\x09\x11\xff\n')

# move forward for 1 second
def forward_fast():
    ser.write(b'\xcc\xff\x55\x01\x07\x04\x04\x02\xfe\x00\x00\x00\xff\n')

def forward():
    ser.write(b'\xcc\xff\x55\x01\x07\x04\x04\x02\x8e\x00\x00\x00\xff\n')


# turn counter-clockwise 90 degrees in 1 second
def turn():
    ser.write(b'\xcc\xff\x55\x01\x07\x04\x04\x02\xfe\x00\x01\x00\xff\n')

def stop():
    ser.write(b'\xcc\xff\x55\x01\x07\x04\x04\x02\x00\x00\x00\x00\xff\n')

# Wait for 4 seconds to connect to bluetooth
time.sleep(4)

# send_msg()

while True:
    x = input()
    if x == 'f':
        forward()
    elif x == 'ff':
        forward_fast()
    elif x == 't':
        turn()
    else:
        stop()
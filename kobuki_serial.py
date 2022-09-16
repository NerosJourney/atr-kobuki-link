##############
# Bailey Wimer/ KSU ATR Lab
# kobuki_serial.py
# Communicates over serial or bluetooth serial with an arduino which acts as a serial forwarder to the kobuki
# For protocol specifics, see the official kobuki protocol guide


import serial
import time

#Open serial port for USB0 at 115200bps
kobuki_direct = 'ttyUSB0'
arduino_passthrough = 'ttyACM0'
bluetooth_serial = 'rfcomm0'
ser = serial.Serial(f'/dev/{bluetooth_serial}', 115200, timeout=10)

dataSend = {
    "speed": 0,
    "radius": 0
}

#Parsese a sensor sub payload into usable data
def parseSensor(subMsg):
    print("Timestamp: ", (int(subMsg[1], 16) * 256 + int(subMsg[0], 16)))
    print("Bumper: ", subMsg[2])
    print("Wheel Drop: ", subMsg[3])
    print("Cliff: ", subMsg[4])
    print("Left Encoder: ", (int(subMsg[6], 16) * 256 + int(subMsg[5], 16)))
    print("Right Encoder: ", (int(subMsg[8], 16) * 256 + int(subMsg[7], 16)))
    print("Left PWM: ", subMsg[9])
    print("Right PWM: ", subMsg[10])
    print("Button: ", subMsg[11])
    print("Charge: ", subMsg[12])
    print("Battery: ", subMsg[13])
    print("Overccurent: ", subMsg[14])

#Parses a Docking IR Sub payload into usable data
def parseDocking(subMsg):
    pass

#Parses a single message, defined by 0xaa followed by 0x55 and a length
def parseMessage(msg):
    x = 0
    print(msg)
    while x < len(msg):
        subMsg = []
        length = int(msg[x+1], 16)
        for y in range(length):
            try:
                subMsg.append(msg[x+y+2])
            except:
                print("Sub message error, discarding")
        if(int(msg[x], 16) == 1):
            #print("Sensors: ", subMsg)
            parseSensor(subMsg)
        
        elif(int(msg[x], 16) == 3):
            #print("Docking IR: ", subMsg)
            pass

        elif(int(msg[x], 16) == 4):
            #print("Intertial: ", subMsg)
            pass

        elif(int(msg[x], 16) == 5):
            #print("Cliff: ", subMsg)
            pass
        
        elif(int(msg[x], 16) == 6):
            #print("Current: ", subMsg)
            pass

        elif(int(msg[x], 16) == 13):
            #print("Gyro: ", subMsg)
            pass
        
        elif(int(msg[x], 16) == 16):
            #print("Input: ", subMsg)
            pass

        x+= length+2


def processMessage():
    s = ser.readline()
    listOfBytes = list(s)
    listTestByteAsHex = [hex(x).split('x')[-1] for x in listOfBytes]
    for x in range(len(listTestByteAsHex)):
        msg = []
        if(listTestByteAsHex[x] == 'aa'):
            if(listTestByteAsHex[x+1] == '55'):
                length = int(listTestByteAsHex[x+2], 16)
                for y in range(length):
                    try: 
                        msg.append(listTestByteAsHex[x+y+3])
                    except:
                        print("discarding message!")
                        msg = []
                        break
                parseMessage(msg)


def sendMsg():
    header = b'\xaa\x55'
    length = b'\x06'
    checksum = b'\x00'
    ctrl = buildControlPayload()
    msg = header + length + ctrl + checksum
    ser.write(msg)

def buildControlPayload():
    global dataSend
    id = b'\x01'
    size = b'\x04'
    speed = dataSend['speed'].to_bytes(2, 'little', signed=True)
    radius = dataSend['radius'].to_bytes(2, 'little')
    return(id + size + speed + radius)


def setSpeed(speed):
    global dataSend
    dataSend["speed"] = speed
    dataSend["radius"] = 0

def setTurnSpeed(speed):
    global dataSend
    dataSend["speed"] = speed
    dataSend["radius"] = 1

while True:
    setTurnSpeed(250)
    sendMsg()
    processMessage()
    time.sleep(1)
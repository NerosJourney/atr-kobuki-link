# ATR-Kobuki Link
## Requirements:
### Arduino:
1. [ArduinoQueue.h](https://www.arduino.cc/reference/en/libraries/arduinoqueue/)
2. [Vector.h](https://www.arduino.cc/reference/en/libraries/vector/)
### Python:
1. [PySerial](https://pyserial.readthedocs.io/en/latest/)
## Use:
### kobuki_serial.py
This file should be used when the Kobuki Base is directly connected to a computer via usb.
### bt_test.py
This is a test file that is being used while the arduino code is in production.  
It currently sends one pregenerated message over bluetooth serial to the arduino.  
**Note**: In order to use bluetooth, it must be set up as a serial port on your device
### arduino
This file is designed for a Mega2560.  
To use, upload the file via Arduino IDE, connect the kobuki to tx0 and rx0, and an hc06 (or equivalent) to tx1 and rx1.  
Connect a common ground between all 3.
Now you can send serial message over bluetooth that fit the ATR Protocol.  
**Note**: In order to use bluetooth, it must be set up as a serial port on your device

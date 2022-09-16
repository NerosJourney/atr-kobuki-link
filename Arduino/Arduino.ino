////////////////
// Bailey Wimer
// KSU ATR Lab
// 9/13/22
// Kobuki Trash Can Control V3
//
// For use with Arduino Uno and a Kobuki base
//
// Converts a bluetooth message which fits the ATR Protocol into messages that fit
// the Kobuki Protocol (and vice versa)
//

#include <Vector.h>
#include <ArduinoQueue.h>
// The three header bytes which define the start of the frame.
#define headerbyte1  204
#define headerbyte2  255
#define headerbyte3  85

//The tail byte which defines the end of a frame
#define tailbyte     255

// The current version of this protocol
#define VERSION      1

// This struct holds information for each SPL, which will be queued to process in bulk at end of message
struct SubPayLoad
{
   int id;
   int len;
   int msg[50];
};


// This is the queue of sub-payloads to be executed once a message is fully interpreted
ArduinoQueue<SubPayLoad> taskQueue(50);

void setup() {
  // Serial connects to Kobuki
  Serial.begin(115200);
  // Serial1 connects to bluetooth
  Serial1.begin(115200);
  // Wait until you recieve a bluetooth message
  while(!Serial1.available()) {
    continue;
  }
  // For console logging purposes
  Serial.println("0001---------");
}

// Uses an implementation of std::vector for Arduino, which uses a 
// storage array but gives it the properties of a vector
int storage_array[1000];
Vector<int> msg(storage_array);

void loop() {
  // put your main code here, to run repeatedly:
  while(Serial1.available()){
    int current = Serial1.read();
    if(current == '\n') {
      interpretMessage();
      break;
    }
    // Stores each character in the msg vector
    msg.push_back(current);
  }
}

void interpretMessage() {
  if(!validateMessage()) {
    msg.clear();
    return;
  }

  // Index 5 in msg correlates to start of payload
  int i = 5;
  while(i < msg.size() - 1) {
    SubPayLoad spl;
    spl.id = msg[i];
    
    int len = msg[i+1] + 1;
    spl.len = len;

    // Fills spl's msg with -258, which is out of range of a byte
    for(int k = 0; k < 50; ++k)
      spl.msg[k] = -258;

    // Fills spl's msg with the data of the current sub-payload
    for(int j = i + 2; j < i + len + 2; ++j) {
      spl.msg[j - (i+2)] = msg[j];
    }
    //Queue's task to be handled later
    taskQueue.enqueue(spl);
    i += len + 2;
  }
  
  msg.clear();
}

// Checks message frame against protocol and version number
// Expects: msg to contain the message
// returns: true if valid, false otherwise
bool validateMessage() {
  if(msg[0] != headerbyte1 || msg[1] != headerbyte2 || msg[2] != headerbyte3) {
    Serial.println("Discarding Message: invalid header");
    return false;
  }
  
  if(msg[3] != VERSION) {
    Serial.println("Discarding Message: bad version");
    return false;
  }
  
  int payloadSize = msg[4];

  if(msg[4 + payloadSize + 1] != tailbyte) {
    Serial.println("Discarding Message: invalid tail");
    return false;
  }
  return true;
}

void printSPL(SubPayLoad spl) {
  for(int j = 0; j < 50; ++j) {
      if(spl.msg[j] == -258)
        break;
      Serial.println(spl.msg[j]);
    }
}

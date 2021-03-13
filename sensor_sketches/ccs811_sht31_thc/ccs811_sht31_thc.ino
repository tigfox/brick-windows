
// Modules for the temp & gas sensors
#include <Wire.h>
#include <Arduino.h>
#include "Adafruit_CCS811.h"
#include "Adafruit_SHT31.h"

// temp / humdity sensor
bool enableHeater = false;
uint8_t loopCnt = 0;
Adafruit_SHT31 sht31 = Adafruit_SHT31();

// Gas sensor object
Adafruit_CCS811 ccs;

// Modules for the radio feather
#include <SPI.h>
#include <RH_RF69.h>
#include <RHReliableDatagram.h>
#include <math.h>

// Frequency for radio - needs to match receiver.
#define RF69_FREQ 915.0

// Where to send packets to! This will be the floor receiver
#define DEST_ADDRESS   1
// change addresses for each client board, any number :)
#define MY_ADDRESS     3

#if defined(ADAFRUIT_FEATHER_M0) // Feather M0 w/Radio
  #define RFM69_CS      8
  #define RFM69_INT     3
  #define RFM69_RST     4
  #define LED           13
#endif

// Singleton instance of the radio driver
RH_RF69 rf69(RFM69_CS, RFM69_INT);

// Class to manage message delivery and receipt, using the driver declared above
RHReliableDatagram rf69_manager(rf69, MY_ADDRESS);

int16_t packetnum = 0;  // packet counter, we increment per xmission


void setup() {
  // First the temp sensor setup:
  Serial.begin(9600);
    Serial.println("SHT31 test");
  if (! sht31.begin(0x44)) {   // Set to 0x45 for alternate i2c addr
    Serial.println("Couldn't find SHT31");
    while (1) delay(1);

  Serial.println("CCS811 test");
  }
  if(!ccs.begin()){
    Serial.println("Failed to start sensor! Please check your wiring.");
    while(1);
  }
  
  // then the radio setup
  pinMode(LED, OUTPUT);     
  pinMode(RFM69_RST, OUTPUT);
  digitalWrite(RFM69_RST, LOW);

  Serial.println("Feather Addressed RFM69 TX Test!");
  Serial.println();

  // manual reset
  digitalWrite(RFM69_RST, HIGH);
  delay(10);
  digitalWrite(RFM69_RST, LOW);
  delay(10);
  
  if (!rf69_manager.init()) {
    Serial.println("RFM69 radio init failed");
    while (1);
  }
  Serial.println("RFM69 radio init OK!");
  // Defaults after init are 434.0MHz, modulation GFSK_Rb250Fd250, +13dbM (for low power module)
  // No encryption
  if (!rf69.setFrequency(RF69_FREQ)) {
    Serial.println("setFrequency failed");
  }

  // If you are using a high power RF69 eg RFM69HW, you *must* set a Tx power with the
  // ishighpowermodule flag set like this:
  rf69.setTxPower(20, true);  // range from 14-20 for power, 2nd arg must be true for 69HCW

  // The encryption key has to be the same as the one in the server
  uint8_t key[] = { 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08,
                    0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08};
  rf69.setEncryptionKey(key);
  
  pinMode(LED, OUTPUT);

  Serial.print("RFM69 radio @");  Serial.print((int)RF69_FREQ);  Serial.println(" MHz");
}

float get_temp() {
  float cur_temp_c = sht31.readTemperature();
  Serial.print("Temp: ");
  Serial.print(cur_temp_c, 2);
  Serial.println("*C");
  return cur_temp_c;
}

float get_hum() {
  float cur_hum_perc = sht31.readHumidity();
  return cur_hum_perc;
}

float get_co2() {
  if(ccs.available()){
    if(!ccs.readData()){
      Serial.print("CO2: ");
      Serial.print(ccs.geteCO2());
      Serial.print("ppm, TVOC: ");
      Serial.println(ccs.getTVOC());
      return ccs.geteCO2();
    }
    else{
      Serial.println("ERROR!");
      while(1);
    }
  }
}

// Dont put this on the stack:
uint8_t buf[RH_RF69_MAX_MESSAGE_LEN];
uint8_t data[] = "  OK";


void Blink(byte PIN, byte DELAY_MS, byte loops) {
  for (byte i=0; i<loops; i++)  {
    digitalWrite(PIN,HIGH);
    delay(DELAY_MS);
    digitalWrite(PIN,LOW);
    delay(DELAY_MS);
  }
}

bool send_packet(char sentype, float reading) {
  char radiopacket[20] = "";
  sprintf(radiopacket, ":%i:%c:%f", MY_ADDRESS, sentype, reading);
  Serial.println(radiopacket);
  // Serial.print("Sending "); Serial.println(radiopacket);

  // Send a message to the DESTINATION!
  if (rf69_manager.sendtoWait((uint8_t *)radiopacket, strlen(radiopacket), DEST_ADDRESS)) {
    // Now wait for a reply from the server
    uint8_t len = sizeof(buf);
    uint8_t from;   
    if (rf69_manager.recvfromAckTimeout(buf, &len, 2000, &from)) {
      buf[len] = 0; // zero out remaining string
      
      Serial.print("Got reply from #"); Serial.print(from);
      Serial.print(" [RSSI :");
      Serial.print(rf69.lastRssi());
      Serial.print("] : ");
      Serial.println((char*)buf);     
      Blink(LED, 40, 3); //blink LED 3 times, 40ms between blinks
      return true;
    } else {
      Serial.println("No reply, is anyone listening?");
      return false;
    }
  } else {
    Serial.println("Sending failed (no ack)");
    return false;
  }
}


void loop() {
  int counter;
  while(1) {
    float cur_hum_perc = get_hum();
    char sensortype = 'H';
    send_packet(sensortype, cur_hum_perc);
    counter++;
    delay(1000);
    float cur_temp_c = get_temp();
    sensortype = 'T';
    send_packet(sensortype, cur_temp_c);
    counter++;
    delay(5000);
    float cur_co2 = get_co2();
    sensortype = 'C';
    send_packet(sensortype, cur_co2);
    counter++;
    delay(5000);
    if(counter >= 5000) { // you really should put this in a function <fix>
        digitalWrite(RFM69_RST, HIGH);
        delay(10);
        digitalWrite(RFM69_RST, LOW);
        delay(10);
        rf69_manager.init();
        rf69.setFrequency(RF69_FREQ);
        rf69.setTxPower(20, true);
        uint8_t key[] = { 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08,
                    0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08};
        rf69.setEncryptionKey(key);
        counter = 0;
    }
  }
}

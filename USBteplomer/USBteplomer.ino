// EtherShield webserver demo
//#include "EtherShield.h"
#include <stdio.h>
//#include <Time.h>
//#include <avr/wdt.h>
#include "wdt.h"
#include "moje.h"
#include "rele.h"

/*
http://www.instructables.com/id/Arduino-TempHumidity-with-LCD-and-Web-Interface/?ALLSTEPS
VCC to Arduino Pin 3.3V
GND to Arduino Pin GND
CS to Arduino Digital Pin 10
SI to Arduino Digital Pin 11
SO to Arduino Digital Pin 12
SCK to Arduino Digital Pin 13
*/


#define RELE    6

void parseLong(char *str, unsigned long &num);

static char myBuff[11];
static unsigned int  sensBuf[SENSBUF_LEN];  // 6 Temps + 2 Vref

// Analog Inputs
AnalogIN sens(sensBuf);

// Digital outputs
Rele kotel(RELE);

void setup(){
  // RELE
  pinMode(RELE, OUTPUT);
  
  wdt_enable(WDTO_8S);
  Serial.begin(9600);
}

void loop(){
  while(1) {
    wdt_reset();
    if(Serial.available()>0){
      int incommingByte=Serial.read();
      switch(incommingByte){
        case 'a':
          kotel.on();
          break;
        case 'n':
          kotel.off();
          break;
        default:
          break;
      }
    }
    sens.cron();
    for(int i=0; i<8; i++) {
        Serial.print(sens.get(i),DEC);
        Serial.print("\t");
    }
    Serial.print(kotel.isOn());
    Serial.println(" ");
    delay(2000);
  }

}

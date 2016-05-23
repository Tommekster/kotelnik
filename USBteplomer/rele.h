#ifndef RELE_H
#define RELE_H

#include <Arduino.h>

class Rele{
  unsigned int pin;
  boolean ison;

public:
  Rele(unsigned int _pin):pin(_pin){off();}
  void on(){ison=true;digitalWrite(pin, HIGH);}
  void off(){ison=false;digitalWrite(pin, LOW);}
  boolean isOn()const{return ison;}
};

#endif

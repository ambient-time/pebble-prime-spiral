// Copyright 2026 Luke Steuber. MIT License.
#include "prime.h"
PrimeTime prime_time(int hour,int minute,int second,int millis){
  int64_t ms=((int64_t)hour*3600+minute*60+second)*1000+millis;
  return (PrimeTime){{(uint16_t)((ms%43200000)*65536/43200000),
    (uint16_t)((ms%3600000)*65536/3600000),(uint16_t)((ms%60000)*65536/60000)}};
}
uint8_t prime_intensity(const PrimeDot *dot,PrimeTime time){
  uint8_t brightest=0;
  for(int j=0;j<3;j++){
    if(!(dot->depths&(1<<j)))continue;
    int delta=(int)dot->angle-time.angle[j];
    if(delta<0) delta=-delta;
    if(delta>32768) delta=65536-delta;
    int sigma=j==2?404:808;
    int index=(delta*256+sigma/2)/sigma;
    if(index>768)continue;
    uint8_t value=PRIME_GAUSSIAN[index];if(value>brightest)brightest=value;
  }
  return brightest;
}

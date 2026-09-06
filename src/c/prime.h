// Copyright 2026 Luke Steuber. MIT License.
#pragma once
#include <stdint.h>
#include "field.h"
typedef struct {uint16_t angle[3];} PrimeTime;
PrimeTime prime_time(int hour,int minute,int second,int millis);
uint8_t prime_intensity(const PrimeDot *dot,PrimeTime time);
void prime_readout(char output[6],int hour,int minute);

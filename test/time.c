// Copyright 2026 Luke Steuber. MIT License.
#include "../src/c/prime.h"
#include <assert.h>
#include <math.h>
#include <stdio.h>
static int is_prime(int n){for(int p=2;p*p<=n;p++)if(n%p==0)return 0;return n>=2;}
int main(void){
  int primes=0;float maximum=0;
  const double tau=6.283185307179586,golden=3.141592653589793*(3-sqrt(5));
  for(int i=2;i<=1800;i++){
    const PrimeDot *dot=&PRIME_DOTS[i-2];assert(dot->prime==is_prime(i));primes+=dot->prime;
    double r=sqrt(i/1800.0),a=i*golden;
    assert(fabs(dot->x/16384.0-r*sin(a))<.00004);
    assert(fabs(dot->y/16384.0+r*cos(a))<.00004);
    assert(!!(dot->depths&1)==(r<.58));assert(!!(dot->depths&2)==(r<.8));assert(!!(dot->depths&4)==(r<1));
    for(int hour=0;hour<24;hour+=3)for(int minute=0;minute<60;minute+=7){
      PrimeTime t=prime_time(hour,minute,43,250);double expected=0;
      for(int j=0;j<3;j++){
        if(!(dot->depths&(1<<j)))continue;
        double delta=fabs(fmod(a-t.angle[j]/65536.0*tau,tau));if(delta>tau*.5)delta=tau-delta;
        double v=exp(-delta*delta/(j==2?.0015:.006));if(v>expected)expected=v;
      }
      float error=fabs(prime_intensity(dot,t)/255.0-expected);if(error>maximum)maximum=error;assert(error<.008);
    }
  }
  assert(primes==278);
  for(int s=0;s<86400;s++){
    int h=s/3600,m=s/60%60;PrimeTime t=prime_time(h,m,s%60,0);
    assert(t.angle[0]==(uint16_t)(((int64_t)s*1000%43200000)*65536/43200000));
  }
  PrimeTime end=prime_time(23,59,59,999),start=prime_time(0,0,0,0),noon=prime_time(12,0,0,0);
  assert(end.angle[0]>65530&&end.angle[1]>65530&&end.angle[2]>65530);
  assert(start.angle[0]==0&&start.angle[1]==0&&start.angle[2]==0&&noon.angle[0]==0);
  printf("PASS: %d exact primes through 1800, 1799 golden-angle points, depth limits, Gaussian maximum error %.5f, 86400 local-second bearings, noon and midnight.\n",primes,maximum);
}

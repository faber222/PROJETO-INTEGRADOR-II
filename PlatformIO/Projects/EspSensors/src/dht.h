
#ifndef __DHT_H__
#define __DHT_H__

#include <Arduino.h>
#include <SimpleDHT.h>
#include "DHT.h"
#include <string>

// #define DHTTYPE DHT22     // DHT 22  (AM2302), AM2321

class Dht {
    public:
        Dht(int DHTPin = 4);

        float temperatura();

        float umidade();

    private:
        int DHTPin = 0;
        float Temperature = 0;
        float Humidity = 0;
        DHT dht;
};

#endif
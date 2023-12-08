#include "dht.h"

Dht::Dht(int DHTPin)
    : dht(DHTPin, DHT22){
        dht.begin();
        pinMode(DHTPin, INPUT);
}

float Dht::temperatura(){
    float Temperature = dht.readTemperature(); // Obtém os valores da temperatura
    return Temperature;
}

float Dht::umidade(){
    float Humidity = dht.readHumidity(); // Obtém os valores da temperatura
    return Humidity;
}
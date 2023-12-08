#ifndef __LDR_H__
#define __LDR_H__

#include <Arduino.h>
#include <Adafruit_ADS1X15.h>
#include <Adafruit_Sensor.h>
#include <ADS1X15.h>
#include <Adafruit_I2CDevice.h>
#include "Adafruit_ADS1X15.h" 

class LDR {
    public:
        LDR(int enderecoADS = 0x49);   // Definindo a constante para o pino D12

        float medidaAnalog();     // valor analógico

        float medidaTensao(int16_t adcValue, float voltageRange);     // valor tensão

        bool getStatus();       // valor atual

        void calibragem();      // só faz a comparação

        int obtemValorBase();

        bool begin();

        void configure();

    private:
        float valorAnalog = 0;
        float valorTensao = 0;
        float valorBase = 0;
        ADS1115 ADS;

};

#endif
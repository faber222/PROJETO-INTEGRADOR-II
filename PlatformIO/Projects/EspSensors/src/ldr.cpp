#include "ldr.h"

LDR::LDR(int enderecoADS) 
    : ADS(enderecoADS) {
}

bool LDR::begin(){
    return ADS.begin();
}

void LDR::configure(){
    ADS.setDataRate(0);  // Taxa de dados padrão

    // Ajuste do ganho interno p/ o maior ganho
    ADS.setGain(1);
    // ou ads.setGain(GAIN_ONE); 
}

float LDR::medidaAnalog(){
    // leitura do valor analógico(entrada) das portas
    valorAnalog = ADS.readADC(3);
    return valorAnalog;	// pino analógico 3
}

float LDR::medidaTensao(int16_t adcValue, float voltageRange){
    // voltageRange é a amplitude máxima da tensão que o ADC pode medir
    valorTensao = (adcValue / 32767.0) * voltageRange;
    return valorTensao;
}

bool LDR::getStatus(){
    // qual a margem de erro que devo inserir? Fazer medidas em casa!
    return valorAnalog > valorBase - 1000;
}

void LDR::calibragem(){
    valorBase = medidaAnalog();
}

int LDR::obtemValorBase(){
    return valorBase;
}
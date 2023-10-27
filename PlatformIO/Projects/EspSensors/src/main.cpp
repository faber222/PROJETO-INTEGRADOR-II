#include <Arduino.h>
#include <ADS1X15.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_I2CDevice.h>

#include <WiFi.h>
// #include <WebServer.h>
#include "DHT.h"
#include <SPI.h>

#define DHTTYPE DHT22     // DHT 22  (AM2302), AM2321

uint8_t DHTPin = 4;

DHT dht(DHTPin, DHTTYPE);
ADS1115 ADS(0x48);

float Temperature;
float Humidity;

const char* ssid = "espAcesso";
const char* password = "12345678";

WiFiServer server(80);

void setup() {
  Serial.begin(9600);
  delay(100);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("Wifi conectado!");
  Serial.print("Endereço de ip: ");
  Serial.println(WiFi.localIP());

  pinMode(DHTPin, INPUT);
  // pinMode();
  // ADS.begin();
  dht.begin();

  server.begin();
}

void loop() {
  if (WiFi.status() != WL_CONNECTED) {
    WiFi.reconnect();
    Serial.println("");
    Serial.println("Wifi conectado!");
    Serial.print("Endereço de ip: ");
    Serial.println(WiFi.localIP());
  } else {
    Temperature = dht.readTemperature(); // Obtém os valores da temperatura
    Humidity = dht.readHumidity(); // Obtém os valores da umidade

    // ADS.setGain(0);
    // int16_t val_0 = ADS.readADC(0);
    // int16_t val_1 = ADS.readADC(1);
    // int16_t val_2 = ADS.readADC(2);
    // int16_t val_3 = ADS.readADC(3);

    // float f = ADS.toVoltage(1);

    Serial.print("Temperatura: ");
    Serial.print(Temperature);
    Serial.print("ºC");
    Serial.println("");

    Serial.print("Umidade: ");
    Serial.print(Humidity);
    Serial.print("g/m³");
    Serial.println("");
    delay(1000);
  }

}


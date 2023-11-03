#include <Arduino.h>
#include <ADS1X15.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_I2CDevice.h>

#include <WiFi.h>
// #include <WebServer.h>
#include "DHT.h"
#include <SPI.h>
#include <PubSubClient.h>
#include <string>
#include <iostream>

#define DHTTYPE DHT22     // DHT 22  (AM2302), AM2321

uint8_t DHTPin = 4;

DHT dht(DHTPin, DHTTYPE);
ADS1115 ADS(0x48);

float Temperature;
float Humidity;

const char* ssid = "FABER";
const char* password = "faber180975";
const char* mqtt_server = "15.228.247.200";
const char* topic = "test";
const char* tempTopic = "temperature";
const char* humidityTopic = "humidity";

WiFiServer server(80);
WiFiClient espClient;
PubSubClient client(espClient);

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Tópico recebido: ");
  Serial.println(topic);

  Serial.print("Mensagem recebida: ");
  for (int i = 0; i < length; i++) {
    Serial.print(( char ) payload[i]);
  }
  Serial.println();
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Conectando ao MQTT Broker...");
    if (client.connect("ESP32Client")) {
      Serial.println("Conectado");
      client.subscribe("test");
    } else {
      Serial.print("Falha, rc=");
      Serial.print(client.state());
      Serial.println(" Tentando novamente em 5 segundos");
      delay(5000);
    }
  }
}

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
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
}

void reconnect_wifi() 
{
    /* se já está conectado a rede WI-FI, nada é feito. 
       Caso contrário, são efetuadas tentativas de conexão */
    if (WiFi.status() == WL_CONNECTED)
        return;
         
    WiFi.begin(ssid, password);
     
    while (WiFi.status() != WL_CONNECTED) 
    {
        delay(100);
        Serial.print(".");
    }
   
    Serial.println();
    Serial.print("Conectado com sucesso na rede ");
    Serial.print(ssid);
    Serial.println("IP obtido: ");
    Serial.println(WiFi.localIP());
}

void verifica_conexoes_wifi_mqtt(void)
{
  /* se não há conexão com o WiFI, a conexão é refeita */
  reconnect_wifi();
  /* se não há conexão com o Broker, a conexão é refeita */
  if (!client.connected())
    reconnect();
}

void loop() {
    verifica_conexoes_wifi_mqtt();
    Temperature = dht.readTemperature(); // Obtém os valores da temperatura
    Humidity = dht.readHumidity(); // Obtém os valores da umidade

    // ADS.setGain(0);
    // int16_t val_0 = ADS.readADC(0);
    // int16_t val_1 = ADS.readADC(1);
    // int16_t val_2 = ADS.readADC(2);
    // int16_t val_3 = ADS.readADC(3);

    // float f = ADS.toVoltage(1);
    if (!client.connected()) {
      reconnect();
    }

    Serial.print("Temperatura: ");
    Serial.print(Temperature);
    Serial.print("ºC");
    Serial.println("");

    Serial.print("Umidade: ");
    Serial.print(Humidity);
    Serial.print("g/m³");
    Serial.println("");
    delay(500);

    char tempString[8];
    char humString[8];
    dtostrf(Temperature, 1, 2, tempString);
    dtostrf(Humidity, 1, 2, humString);

    String payload = String("Temperature: ") + String(tempString) + "°C, Humidity: " + String(humString) + "%";
    String payloadTemp = String("Temperature: ") + String(tempString) + "ºC";
    String payloadHumidity = "Humidity: " + String(humString) + "%";
    
    client.publish(topic, ( char* ) payload.c_str());
    client.publish(tempTopic, ( char* ) payloadTemp.c_str());
    client.publish(humidityTopic, ( char* ) payloadHumidity.c_str());

    client.loop();
    delay(1000);
  
}


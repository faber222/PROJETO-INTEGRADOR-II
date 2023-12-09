#include <Arduino.h>
#include <WiFi.h>
#include <SPI.h>
#include <PubSubClient.h>
#include <string>
#include <math.h>
#include <SimpleDHT.h>
#include "ldr.h"
#include "dht.h"

int pin_D12 = 12; // Definindo a constante para o pino D12
LDR ldr;          // inicializando o construtor ldr.h
Dht tempUmi;

float Temperature;
float Humidity;
float Luminosity;

unsigned long lastMsg = 0;
int value = 0;

const char* ssid = "{WIRELESS_SSID}";
const char* password = "{WIRELESS_PASSWD}";
const char* mqtt_server = "{MQTT_IP}";
const char* mqtt_user = "{MQTT_USER}";
const char* mqtt_password = "{MQTT_PASSWD}";
const char* tempTopic = "{TEMP_TOPIC}";
const char* humidityTopic = "{HUMIDY_TOPIC}";
const char* lumTopic = "{LUMENS_TOPIC}";
const char* lampada = "{LAMP_TOPIC}";
const char* ar_condicionado = "{AIR_TOPIC}";
const char* idEsp = "{ESP_ID}";
const char* mensagemRecebida;
const char* ack = "_status";
const char* ackStatus;
const char* statusAr;
const char* statusLampada;

String lampTopic;
String arTopic;

WiFiServer server(80);
WiFiClient espClient;
PubSubClient client(espClient);

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Tópico recebido: ");
  Serial.println(topic);

  String message(reinterpret_cast< char* >(payload), length);
  Serial.print("Mensagem recebida: ");
  Serial.println(message);

  mensagemRecebida = message.c_str();

  if (String(topic).equals(String(lampTopic))) {
    if (String(mensagemRecebida) == "0") {
      statusLampada = "0";
    } else if (String(mensagemRecebida) == "1") {
      statusLampada = "1";
    }
  }
  else if (String(topic).equals(String(arTopic))) {
    if (String(mensagemRecebida) == "0") {
      statusAr = "0";
    } else if (String(mensagemRecebida) == "1") {
      statusAr = "1";
    }
  }

  String ackEspStatus = String(topic) + "" + String(ack);
  ackStatus = ackEspStatus.c_str();

  client.publish(ackStatus, "1");

}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Conectando ao MQTT Broker...");
    // Criar ou associar o ID do cliente
    // Tentativa de conexão
    if (client.connect("ESP32Client", mqtt_user, mqtt_password)) {
      Serial.println("Conectado");
      client.subscribe(lampTopic.c_str());
      client.subscribe(arTopic.c_str());
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

  server.begin();
  client.setServer(mqtt_server, 1883);

  String lampadaTopic = String(idEsp) + "" + String(lampada);
  String arCondTopic = String(idEsp) + "" + String(ar_condicionado);
  Serial.println(lampadaTopic);
  Serial.println(arCondTopic);
  lampTopic = lampadaTopic;
  arTopic = arCondTopic;

  client.subscribe(lampTopic.c_str());
  client.subscribe(arTopic.c_str());

  client.setCallback(callback);

  if (!ldr.begin()) {
    Serial.println("Falha ao iniciar ADS!");
    while (1);
  }

  ldr.configure();
  ldr.calibragem();
  pinMode(2, OUTPUT); // Configurando o pino D12 como saída
  reconnect();
}

void reconnect_wifi() {
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

void verifica_conexoes_wifi_mqtt(void) {
  /* se não há conexão com o WiFI, a conexão é refeita */
  reconnect_wifi();
  /* se não há conexão com o Broker, a conexão é refeita */
  if (!client.connected())
    reconnect();
}

void loop() {
  verifica_conexoes_wifi_mqtt();

  Temperature = tempUmi.temperatura();
  Humidity = tempUmi.umidade();

  Serial.print("Temperatura: ");
  Serial.print(Temperature);
  Serial.println("ºC");

  Serial.print("Umidade: ");
  Serial.print(Humidity);
  Serial.println("g/m³");

  Serial.print("Luminosidade: ");
  if (Luminosity == 1) {
    Serial.println("Claro");
  } else {
    Serial.println("Escuro");
  }
  
  Serial.println(Luminosity);
  Serial.println(lampTopic);
  Serial.println(arTopic);

  randomSeed(micros());

  unsigned long now = millis();

  if (now - lastMsg > 2000) {
    lastMsg = now;
    ++value;

    if (ldr.getStatus()) {
      Luminosity = 1;
    } else {
      Luminosity = 0;
    }
  }
  if (( String ) statusLampada == "1") {
    Serial.println("LUZ LIGADAAAAA");
    digitalWrite(2, HIGH);
  } else if (( String ) statusLampada == "0") {
    Serial.println("LUZ DESLIGADAAAAA");
    digitalWrite(2, LOW);
  }

  Serial.print("Valor base: ");
  Serial.println(ldr.obtemValorBase());

  Serial.print("Valor atual: ");
  Serial.println(ldr.medidaAnalog());

  char tempString[8];
  char humString[8];

  dtostrf(Temperature, 1, 2, tempString);
  dtostrf(Humidity, 1, 2, humString);

  String payloadTemp = String(idEsp) + ";" + String(tempString);
  String payloadHumidity = String(idEsp) + ";" + String(humString);
  String payloadLuminosity = String(idEsp) + ";" + String(Luminosity);

  client.publish(tempTopic, ( char* ) payloadTemp.c_str());
  client.publish(humidityTopic, ( char* ) payloadHumidity.c_str());
  client.publish(lumTopic, ( char* ) payloadLuminosity.c_str());

  client.loop();
  delay(pow(10, 3));

}
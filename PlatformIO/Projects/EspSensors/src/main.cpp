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
char msg[0];
int value = 0;

const char* ssid = "Familia Fonseca";
const char* password = "aflf1950";
const char* mqtt_server = "ec2-18-231-159-19.sa-east-1.compute.amazonaws.com";
const char* mqtt_user = "esp";
const char* mqtt_password = "espsensors";
const char* tempTopic = "temperature";
const char* humidityTopic = "humidity";
const char* lumTopic = "lumens";
const char* lampada = "lampada";
const char* ar_condicionado = "ar_condicionado";
const char* idEsp = "1234";
const char* lampTopic;
const char* arTopic;
const char* mensagemRecebida;
const char* ack = "_status";
const char* ackStatus;

WiFiServer server(80);
WiFiClient espClient;
PubSubClient client(espClient);

void reconnect() {
  while (!client.connected()) {
    Serial.print("Conectando ao MQTT Broker...");
    // Criar ou associar o ID do cliente
    // Tentativa de conexão
    if (client.connect("ESP32Client", mqtt_user, mqtt_password)) {
      Serial.println("Conectado");
      client.subscribe(lampTopic);
      client.subscribe(arTopic);
    } else {
      Serial.print("Falha, rc=");
      Serial.print(client.state());
      Serial.println(" Tentando novamente em 5 segundos");
      delay(5000);
    }
  }
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

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Tópico recebido: ");
  Serial.println(topic);
  String message = "";
  
  // Copiar os dados do payload para a memória alocada dinamicamente
  for (int i = 0; i < length; i++) {
    message += static_cast<char>(payload[i]);
  }
  Serial.print("Mensagem recebida: ");
  Serial.println(message);

  mensagemRecebida = message.c_str();

  // Lógica específica para o primeiro tópico
  if (strcmp(topic, lampTopic) == 0) {
    // Faça algo específico para o tópico1
    Serial.println("Lógica para o tópico1");
    if (strcmp("0", mensagemRecebida)) {
      // desliga lampada
    } else if (strcmp("1", mensagemRecebida)) {
      // liga lampada
    }
  }
  // Lógica específica para o segundo tópico
  else if (strcmp(topic, arTopic) == 0) {
    // Faça algo específico para o tópico2
    Serial.println("Lógica para o tópico2");
    if (strcmp("0", mensagemRecebida)) {
      // desliga ar
    } else if (strcmp("1", mensagemRecebida)) {
      // liga ar
    }
  }
  // // Tamanho total necessário para a nova string
  // size_t tamanhoAck = strlen(topic) + strlen(ack) + 1;
  // // Alocar memória para a nova string
  // char* bufferAck = new char[tamanhoAck];
  // // Copiar a primeira string para o resultado
  // strlcpy(bufferAck, topic, tamanhoAck);
  // // Concatenar a segunda string no resultado
  // strlcat(bufferAck, ack, tamanhoAck);
  String ackEspStatus = String(topic) + "" + String(ack);
  ackStatus = ackEspStatus.c_str();

  client.publish(ackStatus, "True");
  // delete[] bufferAck;
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

  // // Tamanho total necessário para a nova string
  // size_t tamanhoTotal1 = strlen(idEsp) + strlen(lampada) + 1;
  // // Tamanho total necessário para a nova string
  // size_t tamanhoTotal2 = strlen(idEsp) + strlen(ar_condicionado) + 1;
  // // Alocar memória para a nova string
  // char* buffer1 = new char[tamanhoTotal1];
  // // Alocar memória para a nova string
  // char* buffer2 = new char[tamanhoTotal2];

  // // Copiar a primeira string para o resultado
  // strlcpy(buffer1, idEsp, tamanhoTotal1);
  // // Concatenar a segunda string no resultado
  // strlcat(buffer1, lampada);
  // // Copiar a primeira string para o resultado
  // strlcpy(buffer2, idEsp);
  // // Concatenar a segunda string no resultado
  // strlcat(buffer2, ar_condicionado);

  String lampadaTopic = String(idEsp) + "" + String(lampada);
  String arCondTopic = String(idEsp) + "" + String(ar_condicionado);
  lampTopic = lampadaTopic.c_str();
  arTopic = lampadaTopic.c_str();

  client.subscribe(lampTopic);
  client.subscribe(lampTopic);

  client.setCallback(callback);

  if (!ldr.begin()) {
    Serial.println("Falha ao iniciar ADS!");
    while (1);
  }

  ldr.configure();
  ldr.calibragem();
  pinMode(2, OUTPUT); // Configurando o pino D12 como saída
}

void loop() {
  verifica_conexoes_wifi_mqtt();

  if (!client.connected()) {
    reconnect();
  }

  Serial.print("Temperatura: ");
  Serial.println(tempUmi.temperatura());
  Serial.print("ºC");
  Serial.println("");

  Serial.print("Umidade: ");
  Serial.println(tempUmi.umidade());
  Serial.print("g/m³");
  Serial.println("");

  randomSeed(micros());

  unsigned long now = millis();

  if (now - lastMsg > 2000) {
    lastMsg = now;
    ++value;
    Serial.print("Publicando mensagem: ");
    Serial.println(msg);
    // client.publish(topic, msg);

    if (ldr.getStatus()) {
      if (msg[0] == '1') {
        Serial.println("LUZ LIGADAAAAA");
        digitalWrite(2, HIGH);
      } else {
        Serial.println("LUZ DESLIGADAAAAA");
        digitalWrite(2, LOW);
      }
    }
  }
  Serial.print("Valor base: ");
  Serial.println(ldr.obtemValorBase());

  Serial.print("Valor atual: ");
  Serial.println(ldr.medidaAnalog());

  Serial.println("\n");

  delay(500);

  char tempString[8];
  char humString[8];
  char lumString[8];


  dtostrf(Temperature, 1, 2, tempString);
  dtostrf(Humidity, 1, 2, humString);
  dtostrf(Luminosity, 1, 2, lumString);

  String payload = String("Temperature: ") + String(tempString) + "°C, Humidity: " + String(humString) + "%, Ligado: " + String(lumString);
  String payloadTemp = String(idEsp) + ";" + String(tempString);
  String payloadHumidity = String(idEsp) + ";" + String(humString);
  String payloadLuminosity = String(idEsp) + ";" + String(lumString);

  client.publish(tempTopic, ( char* ) payloadTemp.c_str());
  client.publish(humidityTopic, ( char* ) payloadHumidity.c_str());
  client.publish(lumTopic, ( char* ) payloadLuminosity.c_str());

  client.loop();
  delete[] arTopic;
  delete[] lampTopic;
  delay(pow(10, 4));

}
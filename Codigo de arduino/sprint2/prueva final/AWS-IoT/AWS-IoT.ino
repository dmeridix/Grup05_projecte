#include "secrets.h"
#include <WiFiClientSecure.h>
#include <MQTTClient.h>
#include <ArduinoJson.h>
#include "WiFi.h"
#include <SPI.h>
#include <MFRC522.h>

#define AWS_IOT_SUBSCRIBE_TOPIC "esp32/sub"
#define AWS_IOT_PUBLISH_TOPIC "esp32/pub"
#define ledPin 32
#define RST_PIN 22
#define SS_PIN 21

WiFiClientSecure net = WiFiClientSecure();
MQTTClient client = MQTTClient(256);
MFRC522 rfid(SS_PIN, RST_PIN);

// NUIDs conocidos
byte nuidKnown1[] = {0xE3, 0x33, 0x88, 0x18};
byte nuidKnown2[] = {0x73, 0xBA, 0xE2, 0x12};

void connectAWS() {
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.println("Conectando al Wi-Fi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  net.setCACert(AWS_CERT_CA);
  net.setCertificate(AWS_CERT_CRT);
  net.setPrivateKey(AWS_CERT_PRIVATE);
  client.begin(AWS_IOT_ENDPOINT, 8883, net);
  client.onMessage(messageHandler);
  Serial.print("Conectando a AWS IoT");
  while (!client.connect(THINGNAME)) {
    Serial.print(".");
    delay(100);
  }
  if (!client.connected()) {
    Serial.println("¡Timeout de AWS IoT!");
    return;
  }
  client.subscribe(AWS_IOT_SUBSCRIBE_TOPIC);
  Serial.println("¡Conectado a AWS IoT!");
}

void messageHandler(String &topic, String &payload) {
  Serial.println("Mensaje entrante: " + topic + " - " + payload);
  StaticJsonDocument<200> doc;
  deserializeJson(doc, payload);
  int message = doc["led"];
  Serial.println(message);  
  if (message == 1) {
    digitalWrite(ledPin, HIGH);
    Serial.println("Encendiendo LED");
  } else if (message == 0) {
    digitalWrite(ledPin, LOW);
    Serial.println("Apagando LED");
  }
}

void setup() {
  Serial.begin(115200);
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW);

  // Inicialización del lector RFID y Wi-Fi
  SPI.begin();
  rfid.PCD_Init();
  connectAWS();

  Serial.println("Escaneo de tarjetas activado.");
}

void loop() {
  // Revisa si hay una nueva tarjeta presente
  if (!rfid.PICC_IsNewCardPresent()) return;
  if (!rfid.PICC_ReadCardSerial()) return;

  // Variable para verificar si el NUID es conocido
  bool isKnown = false;

  // Comparar el NUID leído con los NUIDs conocidos
  if (memcmp(rfid.uid.uidByte, nuidKnown1, 4) == 0) {
    Serial.println("Benvingut Ilyas!");
    isKnown = true;
  } else if (memcmp(rfid.uid.uidByte, nuidKnown2, 4) == 0) {
    Serial.println("Benvingut Ricardo!");
    isKnown = true;
  }

  // Si el NUID no coincide con ningún NUID conocido
  if (!isKnown) {
    Serial.println("Accés denegat: targeta desconeguda.");
  }

  // Publicar evento a AWS IoT
  StaticJsonDocument<200> doc;
  doc["tag"] = isKnown ? "known" : "unknown";
  doc["user"] = isKnown ? (memcmp(rfid.uid.uidByte, nuidKnown1, 4) == 0 ? "Ilyas" : "Ricardo") : "desconegut";
  char jsonBuffer[256];
  serializeJson(doc, jsonBuffer);
  Serial.println("Enviando...");
  Serial.println(jsonBuffer);
  client.publish(AWS_IOT_PUBLISH_TOPIC, jsonBuffer);

  // Finalizar la comunicación con la tarjeta
  rfid.PICC_HaltA();
  rfid.PCD_StopCrypto1();

  client.loop();
}
#include <WiFi.h>
#include <PubSubClient.h>
#include <SPI.h>
#include <MFRC522.h>

// Configuración Wi-Fi
const char* ssid = "Xiaomi11Lite5GNE";
const char* password = "Handiuns12";

// Configuración AWS IoT Core MQTT
const char* mqtt_server = "a2ipr50pyrhnar-ats.iot.us-east-1.amazonaws.com"; // Endpoint de AWS IoT Core
const int mqtt_port = 8883;
const char* mqtt_topic = "esp32/rfid";

// Certificados y claves de AWS IoT Core
const char* aws_root_ca_cert = \
"-----BEGIN CERTIFICATE-----\n" \
"MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA7v0DKJ9rO4Z+Gp5AL19N\n" \
"Q69Lk/aNq2XaI8F5G5MZIVvE4GX8ryy+3Tvh1uKIsTYc2U9NRfpm4kQLsvfC5AF5\n" \
"+nHc3m7dfv7SAzpHb+FUR6AFNMI5k7P/4RODmPyP2lNf/vDf2oB6XxyMC8Jwhr18\n" \
"1Gf8K8v0F4tp/Db/5UuUe6oO/bwQz27Um9MUP3kWaFkWzBNCZczsMft8nqQYyUqj\n" \
"1pQjZ50h0Vk4CQ6R9lTzjBGdFRuDd3xr3pZ2iX+ffNg8bB//NLWNdmfHi1Hv5CvI\n" \
"iE6g29vT5u6fLQKkIMLlkB9peZ4SxHBgcBcZdsQ9QEAUMuMFP6tKztCCFvnG1wIDA\n" \
"QAB\n" \
"-----END CERTIFICATE-----";

const char* certificate = \
"-----BEGIN CERTIFICATE-----\n" \
"MIIB4TCCAYmgAwIBAgIUNyAZz5IwF2XNKwXisNfD3jttA9MwDQYJKoZIhvcNAQEL\n" \
"BQAwWTELMAkGA1UEBhMCRVMxEjAQBgNVBAgMCVBhcXVlcmNpYTEQMA4GA1UEBwwH\n" \
"U29tZUNpdHkxEzARBgNVBAoMClNvbWVDb21wYW55MRQwEgYDVQQDDAtNeUNlcnRp\n" \
"ZmljYXRlMB4XDTIzMDgxMTE0MjAwMFoXDTI0MDgxMDE0MjAwMFowWTELMAkGA1UE\n" \
"BhMCRVMxEjAQBgNVBAgMCVBhcXVlcmNpYTEQMA4GA1UEBwwHU29tZUNpdHkxEzAR\n" \
"BgNVBAoMClNvbWVDb21wYW55MRQwEgYDVQQDDAtNeUNlcnRpZmljYXRlMFwwDQYJ\n" \
"KoZIhvcNAQEBBQADSwAwSAJBAJBCZGJDWD+ucZG9bdgDZIX+BW/ZkAjkEP6j1mdf\n" \
"TlPzknke8MECeI4keU5WxnzHVccy3kzBoZJtFzEzEFgklQsCAwEAAaNTMFEwHQYD\n" \
"VR0OBBYEFK6t8CAVLLQlRUguMmOlw7HXBQa2MB8GA1UdIwQYMBaAFK6t8CAVLLQl\n" \
"RUguMmOlw7HXBQa2MA8GA1UdEwEB/wQFMAMBAf8wDQYJKoZIhvcNAQELBQADQQBl\n" \
"ADzjtbFGL8GD3Zj7w6ZmkFVJvcKt/ptFS79XjgyenfFfhZ2H9t5A5gGQ7D/RDbIH\n" \
"dpOjFl+XKl9cJ1dXLJm9\n" \
"-----END CERTIFICATE-----";

const char* private_key = \
"-----BEGIN PRIVATE KEY-----\n" \
"MIIBVwIBADANBgkqhkiG9w0BAQEFAASCAT8wggE7AgEAAkEA4jChpHkqjIHrljrg\n" \
"BtYhtQgm8fUnw5lIYZklsb0E+a/O2JXlWo3vJKdo60tJLPusKHw4f7NKnvQi3Trl\n" \
"HMeKYQIDAQABAkBwvYfFfPEV1xi0Sw2ufUXX8m5RhlAYq1Y6z0FfxSCv/EnKNfbb\n" \
"MKkB1bb7aMfM6AcQwWl0DjC8zwTk2uNc1MCBAiEA/9pq6dQyQfBmqCv+TPHZzExG\n" \
"9LoYUE4NwACF8IoMQB3U6HkCIQDiz0HbpdZ+jwC9RmD5VEpn2BkYHBkzMwYNWwPb\n" \
"vDJwVQIhAIVi8jCm59OkzJw3mrCPTcRAGnEPF6MFRMRb5TkO5uElAiEAkz7+LzPz\n" \
"laHhc83Rf2FSvBlCv0vAo6pcpiOh0RIx1nsCIQDIEl3DmkAgnTz0oUDmEYhjbCGZ\n" \
"sfP8aMJ8hE5DPmWyvw==\n" \
"-----END PRIVATE KEY-----";

// Configuración MFRC522
#define SS_PIN 5
#define RST_PIN 22
MFRC522 rfid(SS_PIN, RST_PIN);

WiFiClientSecure wifiClient;
PubSubClient mqttClient(wifiClient);

void setup() {
  Serial.begin(115200);
  SPI.begin();
  rfid.PCD_Init();

  // Configurar Wi-Fi y conexión MQTT
  conectarWiFi();
  configurarMQTT();
}

void loop() {
  if (!mqttClient.connected()) {
    reconectarMQTT();
  }
  mqttClient.loop();

  if (rfid.PICC_IsNewCardPresent() && rfid.PICC_ReadCardSerial()) {
    String nuid = leerNUID();
    enviarEventoAWS(nuid);

    rfid.PICC_HaltA();
    rfid.PCD_StopCrypto1();
  }
}

void conectarWiFi() {
  Serial.print("Conectando a Wi-Fi");
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println(" Conectado a Wi-Fi");
}

void configurarMQTT() {
  wifiClient.setCACert(aws_root_ca_cert);
  wifiClient.setCertificate(certificate);
  wifiClient.setPrivateKey(private_key);

  mqttClient.setServer(mqtt_server, mqtt_port);
}

void reconectarMQTT() {
  while (!mqttClient.connected()) {
    Serial.print("Conectando a AWS IoT Core...");
    if (mqttClient.connect("ESP32_RFID")) {
      Serial.println(" Conectado a AWS IoT Core");
    } else {
      Serial.print(" Fallo de conexión, rc=");
      Serial.print(mqttClient.state());
      Serial.println(" Intentando de nuevo en 5 segundos");
      delay(5000);
    }
  }
}

String leerNUID() {
  String nuid = "";
  for (byte i = 0; i < 4; i++) {
    nuid += String(rfid.uid.uidByte[i], HEX);
    if (i < 3) nuid += " ";
  }
  nuid.toUpperCase();
  Serial.println("NUID leído: " + nuid);
  return nuid;
}

void enviarEventoAWS(String nuid) {
  String payload = "{ \"NUID\": \"" + nuid + "\" }";
  Serial.println("Enviando mensaje: " + payload);

  if (mqttClient.publish(mqtt_topic, payload.c_str())) {
    Serial.println("Mensaje enviado a AWS IoT Core correctamente");
  } else {
    Serial.println("Error al enviar el mensaje a AWS IoT Core");
  }

#include <SPI.h>
#include <MFRC522.h>
#include <WiFi.h>

// Configuración de pines para el lector RFID
#define SS_PIN 5
#define RST_PIN 0

// Credenciales Wi-Fi
const char* ssid = "Xiaomi11Lite5GNE";
const char* password = "Handiuns12";

// Instancias para RFID y Wi-Fi
MFRC522 rfid(SS_PIN, RST_PIN);

// Arrays para almacenar los NUIDs conocidos
byte nuidKnown1[4] = {0xE3, 0x33, 0x88, 0x18}; // NUID de la primera tarjeta
byte nuidKnown2[4] = {0x73, 0xBA, 0xE2, 0x12}; // NUID de la segunda tarjeta

// Función para inicializar Wi-Fi
void initWiFi() {
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  Serial.println("Conectando a WiFi...");
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print('.');
    delay(1000);
  }
  Serial.println("\nConectado a WiFi");
  Serial.print("IP: ");
  Serial.println(WiFi.localIP());
}

void setup() {
  Serial.begin(115200); // Velocidad del monitor serie
  SPI.begin(); // Inicializa el bus SPI

  // Inicializa el lector RFID y Wi-Fi
  rfid.PCD_Init();
  initWiFi();

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

  // Finalizar la comunicación con la tarjeta
  rfid.PICC_HaltA();
  rfid.PCD_StopCrypto1();
}
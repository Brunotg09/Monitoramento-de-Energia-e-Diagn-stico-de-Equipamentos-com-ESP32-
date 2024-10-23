// Aqui está o codigo para ser colocado no Arduino IDE
/*
Esse codigo e uma repesentação de como seria esp32 para cada sensor! 

// Código para cada ESP32 sensor
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BMP085_U.h>
#include <DHT.h>
#include <WiFi.h>
#include <HTTPClient.h>

#define DHTPIN 4      // GPIO4 do ESP32 para o DHT22
#define DHTTYPE DHT22

DHT dht(DHTPIN, DHTTYPE);
Adafruit_BMP085_Unified bmp = Adafruit_BMP085_Unified(10085);

const char *ssid = "NOME-WIFI";
const char *password = "SENHA-WIFI";
const char* centralServer = "http://192.168.x.x:5000/sensorData"; // IP do ESP32 central

void setup() {
  Serial.begin(9600);
  dht.begin();
  if (!bmp.begin()) {
    Serial.println("Erro ao iniciar BMP085!");
    while (1);
  }
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("WiFi conectado");
}

void loop() {
  delay(2000);
  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();
  sensors_event_t event;
  bmp.getEvent(&event);
  float pressure = event.pressure;

  if(WiFi.status() == WL_CONNECTED){
    HTTPClient http;
    http.begin(centralServer);
    http.addHeader("Content-Type", "application/json");
    String jsonData = "{\"sensor\":\"ESP32_1\",\"humidity\":" + String(humidity) + ",\"temperature\":" + String(temperature) + ",\"pressure\":" + String(pressure) + "}";
    
    int httpResponseCode = http.POST(jsonData);
    
    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.println(httpResponseCode);
      Serial.println(response);
    }
    else {
      Serial.print("Erro na POST request: ");
      Serial.println(httpResponseCode);
    }
    
    http.end();
  }
  else {
    Serial.println("WiFi não conectado");
  }
}
*/

/*
Esse seria o código para o ESP32 Central Recebendo Dados de Múltiplos Sensores

#include <WiFi.h>
#include <WiFiClient.h>
#include <WebServer.h>

const char *ssid = "NOME-WIFI";
const char *password = "SENHA-WIFI";
WiFiServer server(5000);

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("WiFi conectado");
  server.begin();
}

void loop() {
  WiFiClient client = server.available();
  if (client) {
    String data = "";
    while (client.connected()) {
      if (client.available()) {
        char c = client.read();
        data += c;
        if (c == '\n') {
          break;
        }
      }
    }
    client.stop();
    Serial.println("Dados recebidos: " + data);
    processSensorData(data);
  }
}

void processSensorData(String data) {
  // Supondo que os dados estão no formato JSON, faça parsing do JSON aqui
  // Por exemplo: {"sensor":"ESP32_1","humidity":45.0,"temperature":25.0,"pressure":1012.0}
  
  DynamicJsonDocument doc(1024);
  DeserializationError error = deserializeJson(doc, data);

  if (error) {
    Serial.print("Erro ao fazer parsing do JSON: ");
    Serial.println(error.c_str());
    return;
  }

  const char* sensor = doc["sensor"];
  float humidity = doc["humidity"];
  float temperature = doc["temperature"];
  float pressure = doc["pressure"];
  float voltage = doc["voltage"];
  float current = doc["current"];

  // Processa os dados conforme necessário
  Serial.print("Sensor: "); Serial.println(sensor);
  Serial.print("Umidade: "); Serial.println(humidity);
  Serial.print("Temperatura: "); Serial.println(temperature);
  Serial.print("Pressão: "); Serial.println(pressure);
  Serial.print("Voltagem: "); Serial.println(voltage);
  Serial.print("Corrente: "); Serial.println(current);

  // Envia os dados para o servidor
  sendToServer(data);
}

void sendToServer(String data) {
  if (WiFi.status() == WL_CONNECTED) {
    WiFiClient client;
    if (client.connect("SEU_IP_DO_SERVIDOR", 5000)) {
      client.println(data);
      client.stop();
    } else {
      Serial.println("Falha ao conectar ao servidor");
    }
  } else {
    Serial.println("WiFi não conectado");
  }
}
*/


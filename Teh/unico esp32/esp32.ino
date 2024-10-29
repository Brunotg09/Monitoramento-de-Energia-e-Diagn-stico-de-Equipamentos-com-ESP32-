// Aqui está o codigo para ser colocado no Arduino IDE
/*

#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BMP085_U.h>
#include <DHT.h>
#include <WiFi.h>

#define DHTPIN 4 // GPIO4 do ESP32 para o DHT22
#define DHTTYPE DHT22
#define VOLTAGE_PIN 36 // GPIO36 do ESP32 (ADC1_CHANNEL_0)
#define CURRENT_PIN 39 // GPIO39 do ESP32 (ADC1_CHANNEL_3)

DHT dht(DHTPIN, DHTTYPE);
Adafruit_BMP085_Unified bmp = Adafruit_BMP085_Unified(10085);

const char *ssid = "NOME-WIFI";
const char *password = "SENHA-WIFI";

void setup()
{
    Serial.begin(9600);
    dht.begin();
    if (!bmp.begin())
    {
        Serial.println("Erro ao iniciar BMP085!");
        while (1);
    }
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED)
    {
        delay(500);
        Serial.print(".");
    }
    Serial.println("WiFi conectado");
}

void loop()
{
    delay(2000);
    float humidity = dht.readHumidity();
    float temperature = dht.readTemperature();
    sensors_event_t event;
    bmp.getEvent(&event);
    float pressure = event.pressure;
    float voltage = analogRead(VOLTAGE_PIN) * (3.3 / 4095.0) * 11.0; // Divisor de tensão 11:1
    float current = analogRead(CURRENT_PIN) * (5.0 / 1023.0) - 2.5;  // Offset de 2.5V
    String data = String(humidity) + "," + String(temperature) + "," + String(pressure) + "," + String(voltage) + "," + String(current);
    sendDataToPython(data);
}

void sendDataToPython(String data)
{
    if (WiFi.status() == WL_CONNECTED)
    {
        WiFiClient client;

    //como encontrar o IP do seu servidor:
    //No Windows:
    //Abra o prompt de comando (Cmd).
    //Digite ipconfig e pressione Enter.
    //Procure pelo endereço IPv4 correspondente à sua rede local. Será algo como 192.168.x.x.
    
        if (client.connect("SEU_IP_DO_SERVIDOR", 5000))
        {
            client.println(data);
            client.stop();
        }
        else
        {
            Serial.println("Falha ao conectar ao servidor");
        }
    }
    else
    {
        Serial.println("WiFi não conectado");
    }
}
*/

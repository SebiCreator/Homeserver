#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
#include "DHT.h"
#include "Private.h"

#define DHT_TYPE DHT22
#define DHT_PIN D2

WiFiUDP UDP;
DHT dht(DHT_PIN, DHT_TYPE);

char packet[255];
char msg[20];

void setup()
{
  Serial.begin(115200);
  Serial.println();

  dht.begin();
  WiFi.begin(WIFI_SSID, WIFI_PASS);

  Serial.print("Connecting to ");
  Serial.print(WIFI_SSID);
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(100);
    Serial.print(".");
  }

  UDP.begin(UDP_PORT);
  Serial.print("Listening on UDP port ");
  Serial.println(UDP_PORT);
}

void loop()
{
  float h = dht.readHumidity();
  float t = dht.readTemperature();

  sprintf(msg, "temp=%.2f,hum=%.2f", t, h);

  UDP.beginPacket(BASE_IP, BASE_PORT);
  UDP.write(msg);
  UDP.endPacket();
  Serial.print("Sending: ");
  Serial.println(msg);
  delay(1000 * INTERVALL);
}

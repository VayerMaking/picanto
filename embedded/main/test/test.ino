#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <ESP8266HTTPClient.h>
#include <NTPClient.h>
#include <WiFiUdp.h>


// Replace with your network credentials
const char* ssid = "RedmiNote";
const char* password = "lolgyere";
//offset for timezone
const long utcOffsetInSeconds = 3600; 
String message = "Timer start";

float data;
const char *URL = "http://145.93.37.119:8080/oven_start";
WiFiClient client;
HTTPClient httpClient;

int button_state = 0;
int prev_state = 0;

WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP, "pool.ntp.org", utcOffsetInSeconds);

void setup(void) {

  delay(1000);
  pinMode(D1,INPUT);
  Serial.begin(115200);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());


}

void loop(void) {

  if (WiFi.status() == WL_CONNECTED) {
    button_state = digitalRead(D1);
    timeClient.update();
    
    if (button_state == HIGH && prev_state == 0) {
       String response = "";
    response += "{";
    response += "\"timestamp\":\"";
    response += timeClient.getFormattedTime();
    response += "\"}";

  Serial.println(response);
      
      httpClient.begin(client, URL);
      httpClient.addHeader("Content-Type", "application/json");
      httpClient.POST(response);
      Serial.println("response sent");
      String content = httpClient.getString();
      httpClient.end();
  
      Serial.println(content);
  
      prev_state = 1;
    } else if (button_state == LOW) {
      prev_state = 0;
    }
   delay(10);

  }
}

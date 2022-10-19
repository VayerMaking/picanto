// esp code
#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <ESP8266HTTPClient.h>
#include <NTPClient.h>
#include <WiFiUdp.h>

// Replace with your network credentials
const char* ssid = "HonorNote10";
const char* password = "lolgyere";

const long utcOffsetInSeconds = 7200;

float data;
const char *URL = "http://192.168.88.254:8080/oven_start";
WiFiClient client;
HTTPClient httpClient;

WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP, "pool.ntp.org", utcOffsetInSeconds);


void setup(void) {

  delay(1000);
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

  if(WiFi.status()== WL_CONNECTED){ 

    
  // If the button is pressed
  //if(digitalRead(BUTTON) == LOW) {

    // Wait for the button to be released
    //while(digitalRead(BUTTON) == LOW) {
      //delay(100);    
    //}

  String message = "Timer start";
  timeClient.update();

  String response = "";
    response += "{";
    response += "\"timestamp\":";
    response += timeClient.getFormattedTime();
    response += ",\"message\":";
    response += message;
    response += "}";
  Serial.println(response);
  
  
  httpClient.begin(client, URL);
  httpClient.addHeader("Content-Type", "application/json");
  httpClient.POST(response);
  String content = httpClient.getString();
  httpClient.end();

    Serial.println(content);
    delay(5000);
  
  }
}
/**
 * BasicHTTPClient.ino
 *
 *  Created on: 24.05.2015
 *
 */

#include <Arduino.h>

#include <WiFi.h>
#include <WiFiMulti.h>
#include <stdlib.h>
#include <stdio.h>
#include <HTTPClient.h>

#define USE_SERIAL Serial

WiFiMulti wifiMulti;

int on_time, off_time;



void setup() {
  pinMode(4, OUTPUT);
  USE_SERIAL.begin(115200);

  USE_SERIAL.println();
  USE_SERIAL.println();
  USE_SERIAL.println();

  for (uint8_t t = 4; t > 0; t--) {
    USE_SERIAL.printf("[SETUP] WAIT %d...\n", t);
    USE_SERIAL.flush();
    delay(1000);
  }

  wifiMulti.addAP("HUAWEI nova 5T", "erfan800");
}

void loop() {
  if ((wifiMulti.run() == WL_CONNECTED)) {

    HTTPClient http;

    USE_SERIAL.print("[HTTP] begin...\n");
    http.begin("http://192.168.43.177:8000/timing/");  //HTTP

    // start connection and send HTTP header
    int httpCode = http.GET();

    if (httpCode > 0) {
      USE_SERIAL.printf("[HTTP] GET... code: %d\n", httpCode);

      // file found at server
      if (httpCode == 200) {
        String payload = http.getString();

      USE_SERIAL.println(payload);

        int seprator_index = payload.indexOf("&");
        String on_value_str = payload.substring(0, seprator_index);
        String off_value_str = payload.substring(seprator_index + 1, payload.length());

        USE_SERIAL.println(on_value_str);
        USE_SERIAL.println(off_value_str);

        int on_value = on_value_str.toInt();
        int off_value = off_value_str.toInt();

        digitalWrite(4, HIGH);
        delay(on_value);

        digitalWrite(4, LOW);
        delay(off_value);
      }
      else {
        USE_SERIAL.println("Error");
      }
    } 

    http.end();
  }

}

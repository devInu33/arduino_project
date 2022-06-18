#include "Arduino.h"

// brownout
#include "soc/soc.h"
#include "soc/rtc_cntl_reg.h"

#include "const.h"


#define SERIAL_DEBUG true
#define SEND_INTERVAL 60000
#define WIFI_CONNECT_INTERVAL 1000
#if defined(SERIAL_DEBUG)
    #define DBG(x) Serial.println(x)
#else
    #define DBG(...)
#endif

#include "./connect.h"
#include "./ftp.h"
#include "./cam.h"
int LED_BUILTIN = 2;
void setup() {
    WRITE_PERI_REG(RTC_CNTL_BROWN_OUT_REG, 0); // disable brownout detector
    pinMode(LED_BUILTIN,OUTPUT);
    pinMode(4, OUTPUT);
    digitalWrite(4, LOW);

#ifdef SERIAL_DEBUG
    Serial.begin(115200);
    Serial.setDebugOutput(true);
#endif
    WiFi.mode(WIFI_STA); //Optional
    WiFi.begin(ssid,pass);
    Serial.println("\nConnecting");
    while (WiFi.status() != WL_CONNECTED) {
      delay(500);
      Serial.println("...");
    }

      Serial.print("WiFi connected with IP: ");
      Serial.println(WiFi.localIP());

}

void loop() {
    unsigned long current_millis = millis();
    WiFiClient client;
    if (!client.connect(host, port)) {

      Serial.println("Connection to host failed");

      delay(1000);
      return;
  }

      if (current_millis - send_timer >= SEND_INTERVAL) {
          send_timer = current_millis;

          if (!cam_init_ok) {
              cam_init_ok = cameraInit();
          }

          if (cam_init_ok) {
              DBG("Taking picture now");
              camera_fb_t *fb = NULL;
              fb = esp_camera_fb_get();

              if (!fb) {
                  DBG("Camera capture failed");
                  return;
              }

              DBG("Camera capture success");
              client.print("Shape->width:");
              client.print(fb->width);
              client.print("height:");
              client.println(fb->height);
              delay(1000);
              const char *data = (const char *)fb->buf;
              client.write(data,fb->len);

              esp_camera_fb_return(fb);
              DBG("Disconecting...");
          }
      }
    while(client.available()){
      char alram = client.read();
      DBG(alarm);
    }
    client.stop();
    delay(2000);

    yield();
}
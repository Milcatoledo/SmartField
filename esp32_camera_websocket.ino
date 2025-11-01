/*
 * ESP32 Camera WebSocket - Ultra Estable
 */

#include <WiFi.h>
#include <WebSocketsClient.h>
#include <esp_camera.h>
#include <base64.h>
#include "soc/soc.h"
#include "soc/rtc_cntl_reg.h"

const char* ssid = "WILLIAN-BUCAY";
const char* password = "Willian2002";
const char* ws_server = "192.168.1.7";
const int ws_port = 5000;
const char* ws_path = "/ws";

WebSocketsClient webSocket;

void setupCamera() {
  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = 5;
  config.pin_d1 = 18;
  config.pin_d2 = 19;
  config.pin_d3 = 21;
  config.pin_d4 = 36;
  config.pin_d5 = 39;
  config.pin_d6 = 34;
  config.pin_d7 = 35;
  config.pin_xclk = 0;
  config.pin_pclk = 22;
  config.pin_vsync = 25;
  config.pin_href = 23;
  config.pin_sscb_sda = 26;
  config.pin_sscb_scl = 27;
  config.pin_pwdn = 32;
  config.pin_reset = -1;
  config.xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_JPEG;
  config.frame_size = FRAMESIZE_QQVGA;
  config.jpeg_quality = 25;
  config.fb_count = 1;
  config.fb_location = CAMERA_FB_IN_PSRAM;
  config.grab_mode = CAMERA_GRAB_LATEST;

  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("CAM ERROR: 0x%x\n", err);
    delay(3000);
    ESP.restart();
  }
  Serial.println("CAM: OK");
}

void wsEvent(WStype_t type, uint8_t* payload, size_t length) {
  if (type == WStype_CONNECTED) {
    Serial.println("WS: CONNECTED");
  } else if (type == WStype_DISCONNECTED) {
    Serial.println("WS: DISCONNECTED");
  }
}

void sendFrame() {
  camera_fb_t* fb = esp_camera_fb_get();
  if (!fb) {
    Serial.println("NO FRAME");
    return;
  }

  Serial.printf("IMG: %db | RAM: %d\n", fb->len, ESP.getFreeHeap());

  String b64 = base64::encode(fb->buf, fb->len);
  String json = "{\"event\":\"image_frame\",\"image\":\"" + b64 + "\"}";
  
  webSocket.sendTXT(json);
  Serial.println("SENT");

  esp_camera_fb_return(fb);
}

void setup() {
  // DESHABILITAR BROWNOUT Y WATCHDOG
  WRITE_PERI_REG(RTC_CNTL_BROWN_OUT_REG, 0);
  
  Serial.begin(115200);
  delay(3000);
  
  Serial.println("\n\n=== SMARTFIELD CAM v3 ===");
  Serial.printf("FREE RAM: %d bytes\n", ESP.getFreeHeap());

  // Reducir frecuencia para estabilidad
  setCpuFrequencyMhz(160);
  Serial.println("CPU: 160MHz");

  // WiFi con delays largos
  Serial.println("WIFI: Starting...");
  WiFi.mode(WIFI_STA);
  WiFi.setSleep(false);  // Deshabilitar sleep mode
  WiFi.begin(ssid, password);
  
  int tries = 0;
  while (WiFi.status() != WL_CONNECTED && tries < 40) {
    delay(1000);  // Delay MÁS LARGO
    Serial.print(".");
    tries++;
    yield();
  }
  
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("\nWIFI: TIMEOUT");
    delay(5000);
    ESP.restart();
  }
  
  Serial.println("\nWIFI: CONNECTED");
  Serial.print("IP: ");
  Serial.println(WiFi.localIP());
  Serial.printf("RAM: %d\n", ESP.getFreeHeap());

  delay(1000);

  // Cámara
  Serial.println("Starting camera...");
  setupCamera();
  Serial.printf("RAM: %d\n", ESP.getFreeHeap());

  delay(1000);

  // WebSocket
  Serial.printf("WS: %s:%d%s\n", ws_server, ws_port, ws_path);
  webSocket.begin(ws_server, ws_port, ws_path);
  webSocket.onEvent(wsEvent);
  webSocket.setReconnectInterval(5000);
  
  Serial.println("\n=== READY ===\n");
}

void loop() {
  webSocket.loop();
  yield();
  
  static unsigned long lastFrame = 0;
  if (millis() - lastFrame > 5000) {
    if (WiFi.status() == WL_CONNECTED && webSocket.isConnected()) {
      sendFrame();
    }
    lastFrame = millis();
  }
  
  delay(100);
}
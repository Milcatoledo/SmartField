/*
 * ESP32 WebSocket Video Streaming para SmartField
 * Captura frames de cámara y los envía vía WebSocket
 */

#include <WiFi.h>
#include <WebSocketsClient.h>
#include <ArduinoJson.h>
#include <esp_camera.h>
#include <base64.h>

// Configuración WiFi
const char* ssid = "TU_SSID";
const char* password = "TU_PASSWORD";

// Configuración WebSocket
const char* websocket_server = "192.168.1.100";  // IP de tu servidor
const int websocket_port = 5000;
const char* websocket_path = "/socket.io/?EIO=4&transport=websocket";

// Cliente WebSocket
WebSocketsClient webSocket;

// Configuración de cámara (ESP32-CAM)
camera_config_t config;

void setupCamera() {
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
  config.frame_size = FRAMESIZE_VGA;  // 640x480
  config.jpeg_quality = 12;           // 0-63, menor número = mejor calidad
  config.fb_count = 1;

  // Inicializar cámara
  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("Error inicializando cámara: 0x%x", err);
    return;
  }
  Serial.println("Cámara inicializada correctamente");
}

void webSocketEvent(WStype_t type, uint8_t * payload, size_t length) {
  switch(type) {
    case WStype_DISCONNECTED:
      Serial.println("WebSocket Desconectado");
      break;
      
    case WStype_CONNECTED:
      Serial.printf("WebSocket Conectado a: %s\n", payload);
      break;
      
    case WStype_TEXT:
      Serial.printf("Mensaje recibido: %s\n", payload);
      break;
      
    default:
      break;
  }
}

void sendFrame() {
  // Capturar frame
  camera_fb_t * fb = esp_camera_fb_get();
  if (!fb) {
    Serial.println("Error capturando imagen");
    return;
  }

  // Convertir a base64
  String imageBase64 = base64::encode(fb->buf, fb->len);
  String dataUrl = "data:image/jpeg;base64," + imageBase64;

  // Crear payload JSON
  DynamicJsonDocument doc(imageBase64.length() + 200);
  doc["image"] = dataUrl;

  String jsonString;
  serializeJson(doc, jsonString);

  // Enviar por WebSocket
  webSocket.sendTXT("42[\"image_frame\"," + jsonString + "]");

  Serial.printf("Frame enviado - Tamaño: %d bytes\n", fb->len);

  // Liberar memoria
  esp_camera_fb_return(fb);
}

void setup() {
  Serial.begin(115200);
  Serial.println("Iniciando ESP32 WebSocket Camera...");

  // Configurar cámara
  setupCamera();

  // Conectar WiFi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("WiFi conectado - IP: ");
  Serial.println(WiFi.localIP());

  // Configurar WebSocket
  webSocket.begin(websocket_server, websocket_port, websocket_path);
  webSocket.onEvent(webSocketEvent);
  webSocket.setReconnectInterval(5000);
}

void loop() {
  webSocket.loop();
  
  // Enviar frame cada 2 segundos (ajustable)
  static unsigned long lastFrame = 0;
  if (millis() - lastFrame > 2000) {
    if (WiFi.status() == WL_CONNECTED && webSocket.isConnected()) {
      sendFrame();
    }
    lastFrame = millis();
  }
  
  delay(100);
}
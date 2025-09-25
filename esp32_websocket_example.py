# Ejemplo básico MicroPython para ESP32: envío de imagen simulada por WebSocket a SmartField
# Reemplaza TU_SSID, TU_PASSWORD y TU_IP_LOCAL por tus datos reales

import network
import time
import ubinascii
import ujson
import usocket
from esp32_camera import Camera

SSID = 'NETLIFE-GOMEZ'
PASSWORD = '0916770431'

sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.connect(SSID, PASSWORD)
while not sta.isconnected():
    time.sleep(1)

print('WiFi conectado:', sta.ifconfig())

def send_image():
    cam = Camera()
    cam.init()
    img = cam.capture()
    img_base64 = ubinascii.b2a_base64(img).decode().replace('\n', '')
    model = "acm"
    payload = ujson.dumps({"image": "data:image/jpeg;base64," + img_base64, "model": model})

    sock = usocket.socket()
    addr = usocket.getaddrinfo('196.168.100.223', 5000)[0][-1]
    sock.connect(addr)
    sock.send(b"GET /socket.io/?EIO=4&transport=websocket HTTP/1.1\r\n"
              b"Host: 196.168.100.223:5000\r\n"
              b"Upgrade: websocket\r\n"
              b"Connection: Upgrade\r\n"
              b"Sec-WebSocket-Key: x3JJHMbDL1EzLkh9GBhXDw==\r\n"
              b"Sec-WebSocket-Version: 13\r\n\r\n")
    time.sleep(2)
    sock.send(payload.encode())
    sock.close()

send_image()

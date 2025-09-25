#!/usr/bin/env python3
"""
Script para simular streaming de cámara en tiempo real
Envía imágenes secuencialmente cada X segundos para simular video stream
"""

import os
import base64
import socketio
import time
import argparse
from pathlib import Path

# Configuración
SERVER_URL = 'http://localhost:5000'
IMAGES_DIR = './images'

def encode_image(image_path):
    """Codifica imagen a base64"""
    with open(image_path, 'rb') as f:
        img_data = f.read()
        img_base64 = base64.b64encode(img_data).decode('utf-8')
        return f"data:image/jpeg;base64,{img_base64}"

def list_images():
    """Lista las imágenes disponibles"""
    images = []
    if os.path.exists(IMAGES_DIR):
        for file in os.listdir(IMAGES_DIR):
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                images.append(file)
    return sorted(images)

def main():
    parser = argparse.ArgumentParser(description='Simular streaming de cámara en tiempo real')
    parser.add_argument('--interval', '-t', type=float, default=3.0,
                       help='Intervalo en segundos entre imágenes (default: 3.0)')
    parser.add_argument('--loop', '-l', action='store_true',
                       help='Repetir secuencia infinitamente')
    parser.add_argument('--single', '-s', 
                       help='Enviar solo una imagen específica (ej: c1.jpg)')
    
    args = parser.parse_args()
    
    # Obtener imágenes
    images = list_images()
    if not images:
        print("❌ No hay imágenes en la carpeta 'images/'")
        return
    
    # Si se especifica una sola imagen
    if args.single:
        if args.single not in images:
            print(f"❌ Imagen '{args.single}' no encontrada")
            print(f"Imágenes disponibles: {', '.join(images)}")
            return
        images = [args.single]
        args.loop = False
    
    print(f"📹 Simulando cámara en tiempo real")
    print(f"📁 Imágenes: {len(images)} encontradas")
    print(f"⏰ Intervalo: {args.interval}s")
    print(f"🔄 Loop: {'Sí' if args.loop else 'No'}")
    print(f"🌐 Servidor: {SERVER_URL}")
    print(f"📱 Ver en: http://localhost:5000/stream")
    print("=" * 50)
    
    # Conectar WebSocket
    sio = socketio.Client()
    connected = False
    
    @sio.event
    def connect():
        nonlocal connected
        connected = True
        print("✓ Conectado al WebSocket")
    
    @sio.event
    def disconnect():
        nonlocal connected
        connected = False
        print("🔌 Desconectado del WebSocket")
    
    try:
        print("🔗 Conectando al servidor...")
        sio.connect(SERVER_URL)
        sio.sleep(1)  # Esperar conexión
        
        if not connected:
            print("❌ No se pudo conectar al servidor")
            return
        
        # Streaming continuo
        image_count = 0
        loop_count = 1
        
        while True:
            for img_name in images:
                if not connected:
                    print("❌ Conexión perdida")
                    return
                
                image_path = os.path.join(IMAGES_DIR, img_name)
                
                try:
                    # Codificar imagen
                    img_base64 = encode_image(image_path)
                    payload = {'image': img_base64}
                    
                    # Enviar
                    sio.emit('image_frame', payload)
                    image_count += 1
                    
                    print(f"📤 [{image_count:03d}] Enviada: {img_name} (Loop {loop_count})")
                    
                    # Esperar antes de la siguiente imagen
                    time.sleep(args.interval)
                    
                except Exception as e:
                    print(f"❌ Error enviando {img_name}: {e}")
                    continue
            
            # Si no es loop, salir
            if not args.loop:
                break
                
            loop_count += 1
            print(f"🔄 Comenzando loop {loop_count}...")
        
        print(f"✓ Streaming completado. Total imágenes enviadas: {image_count}")
        
    except KeyboardInterrupt:
        print(f"\n⏹️  Streaming detenido por usuario. Imágenes enviadas: {image_count}")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        if connected:
            sio.disconnect()

if __name__ == '__main__':
    main()
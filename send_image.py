#!/usr/bin/env python3
"""
Script para enviar imágenes desde la carpeta 'images' a SmartField vía WebSocket
Permite escoger el modelo y la imagen a analizar
"""

import os
import base64
import socketio
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
    parser = argparse.ArgumentParser(description='Enviar imagen a SmartField WebSocket')
    parser.add_argument('--image', '-i', help='Nombre de la imagen (ej: c1.jpg)')
    parser.add_argument('--list', '-l', action='store_true', 
                       help='Listar imágenes disponibles')
    
    args = parser.parse_args()
    
    # Listar imágenes disponibles
    if args.list:
        images = list_images()
        print("Imágenes disponibles:")
        for i, img in enumerate(images, 1):
            print(f"  {i}. {img}")
        print("\nNota: El modelo se selecciona desde la página web")
        return
    
    # Validar imagen
    if not args.image:
        images = list_images()
        if not images:
            print("No hay imágenes en la carpeta 'images/'")
            return
        print("Imágenes disponibles:")
        for i, img in enumerate(images, 1):
            print(f"  {i}. {img}")
        
        try:
            selection = int(input("\nSeleccione número de imagen: ")) - 1
            if 0 <= selection < len(images):
                args.image = images[selection]
            else:
                print("Selección inválida")
                return
        except (ValueError, KeyboardInterrupt):
            print("Selección cancelada")
            return
    
    image_path = os.path.join(IMAGES_DIR, args.image)
    if not os.path.exists(image_path):
        print(f"Imagen no encontrada: {image_path}")
        return
    
    print(f"Enviando imagen: {args.image}")
    print(f"Servidor: {SERVER_URL}")
    print("Nota: El modelo se seleccionará desde la página web")
    
    # Conectar a WebSocket
    sio = socketio.Client()
    
    @sio.event
    def connect():
        print("✓ Conectado al WebSocket")
        
        # Codificar y enviar imagen
        try:
            img_base64 = encode_image(image_path)
            payload = {
                'image': img_base64
            }
            
            print("📤 Enviando imagen...")
            sio.emit('image_frame', payload)
            print("✓ Imagen enviada exitosamente")
            
            # Desconectar después de enviar (la respuesta va a los clientes web)
            sio.sleep(1)
            sio.disconnect()
            
        except Exception as e:
            print(f"❌ Error enviando imagen: {e}")
            sio.disconnect()
    
    @sio.event
    def disconnect():
        print("🔌 Desconectado del WebSocket")
    
    try:
        print("🔗 Conectando al servidor...")
        sio.connect(SERVER_URL)
        sio.wait()
        print("📱 La imagen debe aparecer en la página web: http://localhost:5000/stream")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")

if __name__ == '__main__':
    main()
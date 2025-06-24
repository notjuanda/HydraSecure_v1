from PIL import Image
import math
import base64

def empaquetar_resultado_png(cifrado, ruta_salida="mensaje.png"):
    # Codifica el string cifrado en base64 para asegurar solo caracteres válidos
    cifrado_b64 = base64.b64encode(cifrado.encode("utf-8")).decode("ascii")
    datos = [ord(c) for c in cifrado_b64]
    # Calcula tamaño cuadrado mínimo
    lado = math.ceil(len(datos) ** 0.5)
    # Rellena con ceros si es necesario
    while len(datos) < lado * lado:
        datos.append(0)
    # Crea imagen RGB (solo canal R, G y B en 0)
    img = Image.new("RGB", (lado, lado))
    for i in range(lado * lado):
        x, y = i % lado, i // lado
        img.putpixel((x, y), (datos[i], 0, 0))
    img.save(ruta_salida)
    return ruta_salida

def extraer_resultado_png(ruta):
    img = Image.open(ruta).convert("RGB")
    lado = img.size[0]
    datos = []
    for y in range(lado):
        for x in range(lado):
            px = img.getpixel((x, y))
            if not isinstance(px, tuple) or len(px) != 3:
                continue  # ignora píxeles corruptos o inesperados
            r, g, b = px
            if r == 0:
                continue  # padding
            datos.append(r)
    cifrado_b64 = ''.join(chr(v) for v in datos)
    cifrado_b64 = cifrado_b64.rstrip(chr(0))
    cifrado = base64.b64decode(cifrado_b64).decode("utf-8")
    return cifrado 
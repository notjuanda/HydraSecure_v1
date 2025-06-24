# HydraSecure_v1

## Descripción

HydraSecure es un pipeline de cifrado modular y reversible, diseñado para aplicar múltiples capas de transformación a mensajes de texto (y fácilmente extensible a archivos). Cada mensaje pasa por limpieza, fragmentación, funciones de cifrado por bloque (rotación, inversión, XOR, permutación, mutación ADN), reensamblado seguro y verificación de integridad.

## Características
- Limpieza y normalización de texto (ASCII seguro)
- Clave dinámica: clave base + timestamp + UUID
- Fragmentación en bloques
- Funciones múltiples por bloque, seleccionadas de forma determinista
- Reensamblado seguro (base64 por bloque, cabecera JSON oculta)
- Preparado para empaquetado en imagen/audio/texto (extensible)
- Verificación de integridad con SHA256
- Totalmente reversible y testeado

## Uso básico

```python
from hydra_secure.pipeline import cifrar_pipeline, descifrar_pipeline

mensaje = "Hola mundo! 123"
clave = "secreta"
id_usuario = "user123"

# Cifrar
cifrado, metadatos = cifrar_pipeline(mensaje, clave, id_usuario)

# Descifrar
descifrado = descifrar_pipeline(cifrado, clave, id_usuario, metadatos)

assert descifrado == mensaje  # Si el mensaje original es ASCII
```

## Flujo del pipeline

1. **Preparación:** Limpieza y normalización del mensaje
2. **Generación de semilla:** Clave base + timestamp + UUID
3. **Fragmentación:** División en bloques
4. **Funciones por bloque:** Rotación, inversión, XOR, permutación, mutación ADN
5. **Reensamblado:** Base64 por bloque + cabecera JSON
6. **(Opcional) Contenedor externo:** Preparado para imagen/audio/texto
7. **Verificación de integridad:** SHA256 del mensaje preparado

## Extensión
- Para cifrar archivos binarios, convierte el archivo a texto base64 antes de usar el pipeline.
- Para empaquetar en imagen/audio, implementa la función `empaquetar_resultado`.

## Requisitos
Ver `requirements.txt`.

## Tests

Ejecuta:
```bash
pytest -s
```
para ver todos los casos y la reversibilidad del pipeline.

# HydraSecure Chat Web (cifrado extremo a extremo)

## Requisitos
- Python 3.8+
- Instalar dependencias:
  ```bash
  pip install -r requirements.txt
  ```

## Servidor WebSocket (FastAPI)

Para iniciar el servidor en la IP local (por ejemplo, 0.0.0.0:8000):

```bash
uvicorn server:app --host 0.0.0.0 --port 8000
```

Esto levanta el WebSocket en `/ws` y sirve el frontend en `/`.

## Frontend web

Abre tu navegador y accede a `http://<IP_DEL_SERVIDOR>:8000/`.

- Ingresa tu nombre y clave secreta.
- Escribe mensajes: solo quienes tengan la clave correcta podrán leerlos.
- El cifrado y descifrado ocurre **en el navegador** (extremo a extremo).

## Seguridad
- El servidor solo retransmite mensajes cifrados, nunca ve el contenido en claro.
- El pipeline de cifrado está portado a JavaScript para máxima privacidad.

## Archivos
- `server.py`: Servidor FastAPI + WebSocket.
- `static/index.html`: Frontend web de chat.
- `static/pipeline.js`: Lógica de cifrado/descifrado en JS.

---

¡Listo para un chat seguro y moderno! 
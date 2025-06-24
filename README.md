# HydraSecure_v1

## Descripción

HydraSecure es un pipeline de cifrado modular, reversible y extensible, diseñado para aplicar múltiples capas de transformación a mensajes de texto (y fácilmente adaptable a archivos). El sistema es robusto, seguro y probado, con soporte para uso como librería, demo de consola y chat web cifrado extremo a extremo.

---

## Características principales
- Limpieza y normalización de texto (ASCII seguro)
- Clave dinámica: clave base + timestamp + UUID
- Fragmentación en bloques
- Funciones múltiples por bloque, seleccionadas de forma determinista (rotación, inversión, XOR, permutación, mutación ADN)
- Reensamblado seguro (base64 por bloque, cabecera JSON oculta)
- Opcional: empaquetado en imagen PNG
- Verificación de integridad con SHA256
- Totalmente reversible y testeado
- Chat web cifrado extremo a extremo (frontend JS + backend FastAPI)

---

## Modos de uso

### 1. Como librería Python
```python
from hydra_secure.pipeline import cifrar_pipeline, descifrar_pipeline

mensaje = "Hola mundo! 123"
clave = "secreta"
id_usuario = "user123"

# Cifrar
cifrado, metadatos = cifrar_pipeline(mensaje, clave, id_usuario)

# Descifrar
resultado = descifrar_pipeline(cifrado, clave, id_usuario, metadatos)
assert resultado == mensaje  # Si el mensaje original es ASCII
```

### 2. Demo de consola
Ejecuta:
```bash
python main.py
```
Sigue las instrucciones para cifrar y descifrar mensajes manualmente.

### 3. Chat web cifrado extremo a extremo
- Instala dependencias:
  ```bash
  pip install -r requirements.txt
  ```
- Inicia el servidor:
  ```bash
  uvicorn server:app --host 0.0.0.0 --port 8000
  ```
- Abre tu navegador en `http://localhost:8000/`.
- Ingresa tu nombre y clave secreta. Solo quienes tengan la clave correcta podrán leer los mensajes.

#### Detalles del frontend web
- El cifrado y descifrado ocurre **en el navegador** (JS, ver `static/pipeline.js`).
- El pipeline JS implementa salt, XOR y hash SHA256 (sin fragmentación ni PNG, para máxima compatibilidad y velocidad).
- El servidor solo retransmite mensajes cifrados, nunca ve el contenido en claro.
- Si la clave es incorrecta, el mensaje no se puede descifrar.
- Interfaz moderna, responsiva y fácil de usar.

#### Diferencias pipeline Python vs JS
- **Python:** pipeline completo, fragmentación, funciones por bloque, permutación, mutación ADN, PNG, etc.
- **JS (frontend):** versión simplificada (salt + XOR + hash SHA256, sin fragmentación ni PNG) para chat rápido y seguro.

---

## Flujo del pipeline (Python)
1. **Preparación:** Limpieza y normalización del mensaje
2. **Generación de semilla:** Clave base + timestamp + UUID
3. **Fragmentación:** División en bloques
4. **Funciones por bloque:** Rotación, inversión, XOR, permutación, mutación ADN
5. **Reensamblado:** Base64 por bloque + cabecera JSON
6. **(Opcional) Contenedor externo:** Empaquetado en imagen PNG
7. **Verificación de integridad:** SHA256 del mensaje preparado

---

## Extensión y personalización
- Puedes agregar nuevas funciones de bloque en `hydra_secure/funciones_bloque.py`.
- El empaquetado en PNG es opcional y desacoplado (`hydra_secure/contenedor_png.py`).
- Para cifrar archivos binarios, conviértelos a texto base64 antes de usar el pipeline.

---

## Tests

Ejecuta:
```bash
pytest -s
```
para ver todos los casos y la reversibilidad del pipeline.

Los tests cubren:
- Mensajes vacíos, largos, con caracteres especiales, tildes, binarios
- Claves y usuarios distintos
- Manipulación de datos (robustez)
- Reversibilidad y detección de manipulación

---

## Archivos principales
- `hydra_secure/`: Núcleo del pipeline (modular, cada archivo una etapa)
- `main.py`: Demo de consola
- `gui.py`: Interfaz gráfica local (Tkinter)
- `server.py`: Servidor FastAPI + WebSocket
- `static/`: Frontend web (HTML, JS, CSS)
- `requirements.txt`: Dependencias
- `README.md`: Este archivo

---

## Seguridad
- El servidor web solo retransmite mensajes cifrados, nunca ve el contenido en claro.
- El pipeline de cifrado está portado a JavaScript para máxima privacidad en el chat web.
- Si la clave es incorrecta, el mensaje no se puede descifrar ni manipular sin ser detectado.

---

¡Listo para un cifrado robusto, reversible y multiplataforma! 
from .preparacion import preparar_entrada
from .semilla import generar_semilla
from .fragmentacion import fragmentar_mensaje
from .funciones_bloque import procesar_bloques, revertir_bloques, xor_con_clave
from .reensamblado import reensamblar, desensamblar
from .integridad import generar_hash, verificar_hash
from .contenedor_png import empaquetar_resultado_png, extraer_resultado_png
from .iso_27001_compliance import secure_pipeline_wrapper, iso_compliance
import os
import string
import random

def generar_salt(longitud=8):
    # Salt alfanumérico seguro
    chars = string.ascii_letters + string.digits
    return ''.join(random.SystemRandom().choice(chars) for _ in range(longitud))

@secure_pipeline_wrapper
def cifrar_pipeline(mensaje, clave, id_usuario, contenedor_png=False, ruta_png="mensaje.png", doc_type=None):
    # Verificación de acceso ISO 27001 A.9.1.1
    tipo_doc = doc_type if doc_type else 'pipeline'
    if not iso_compliance.access_control(id_usuario, tipo_doc, 'encrypt'):
        raise PermissionError(f"Usuario {id_usuario} no tiene permisos para cifrar")
    
    # Log de inicio de operación
    iso_compliance.log_security_event('ENCRYPTION_STARTED', f"Starting encryption for user {id_usuario}")
    
    # 1. Preparación
    limpio = preparar_entrada(mensaje)
    # Salt aleatorio
    salt = generar_salt(8)
    limpio_con_salt = salt + limpio
    # XOR global antes de fragmentar
    limpio_xor = xor_con_clave(limpio_con_salt, clave)
    # 2. Semilla dinámica
    semilla, timestamp, uuid = generar_semilla(clave, id_usuario)
    # 3. Fragmentación
    bloques = fragmentar_mensaje(limpio_xor)
    # 4. Funciones por bloque (devuelve bloques_mod y permutaciones)
    bloques_mod, permutaciones = procesar_bloques(bloques, semilla, clave)
    # 5. Reensamblado (cabecera oculta JSON)
    cifrado, metadatos = reensamblar(bloques_mod, timestamp, uuid)
    metadatos['permutaciones'] = permutaciones
    metadatos['semilla'] = semilla
    metadatos['salt'] = salt
    # 6. (Opcional) Contenedor externo PNG
    if contenedor_png:
        ruta = empaquetar_resultado_png(cifrado, ruta_png)
        cifrado = ruta  # El resultado es la ruta del PNG
        metadatos['contenedor'] = 'png'
        metadatos['ruta_png'] = ruta_png
    # 7. Hash de verificación
    hash_verif = generar_hash(limpio)
    metadatos['hash'] = hash_verif
    
    # Log de éxito
    iso_compliance.log_security_event('ENCRYPTION_COMPLETED', f"Encryption completed for user {id_usuario}")
    
    return cifrado, metadatos


@secure_pipeline_wrapper
def descifrar_pipeline(cifrado, clave, id_usuario, metadatos, doc_type=None):
    # Verificación de acceso ISO 27001 A.9.1.1
    tipo_doc = doc_type if doc_type else 'pipeline'
    if not iso_compliance.access_control(id_usuario, tipo_doc, 'decrypt'):
        raise PermissionError(f"Usuario {id_usuario} no tiene permisos para descifrar")
    # Log de inicio de operación
    iso_compliance.log_security_event('DECRYPTION_STARTED', f"Starting decryption for user {id_usuario}")
    # 6. Extraer del contenedor externo PNG si corresponde
    if metadatos.get('contenedor') == 'png':
        cifrado = extraer_resultado_png(cifrado)
    # 5. Desensamblar (extrae bloques_mod, timestamp, uuid)
    bloques_mod, timestamp, uuid = desensamblar(cifrado)
    # 2. Recuperar semilla
    semilla = metadatos['semilla']
    # 4. Revertir funciones por bloque (usa permutaciones)
    permutaciones = metadatos.get('permutaciones')
    bloques = revertir_bloques(bloques_mod, semilla, clave, permutaciones)
    # 3. Reensamblar mensaje original (antes de quitar XOR global)
    limpio_xor = ''.join(bloques)
    # Revertir XOR global
    limpio_con_salt = xor_con_clave(limpio_xor, clave)
    # Quitar salt
    salt = metadatos.get('salt', '')
    if not limpio_con_salt.startswith(salt):
        iso_compliance.log_security_event('SALT_MISMATCH', f"Salt mismatch for user {id_usuario}", 'ERROR')
        raise ValueError('Salt incorrecto o clave incorrecta.')
    limpio = limpio_con_salt[len(salt):]
    # 7. Verificar hash
    if not verificar_hash(limpio, metadatos.get('hash', '')):
        iso_compliance.log_security_event('HASH_MISMATCH', f"Hash mismatch for user {id_usuario}", 'ERROR')
        raise ValueError('Hash de verificación no coincide.')
    # Log de éxito
    iso_compliance.log_security_event('DECRYPTION_COMPLETED', f"Decryption completed for user {id_usuario}")
    return limpio 
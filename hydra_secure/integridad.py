import hashlib

def generar_hash(mensaje):
    return hashlib.sha256(mensaje.encode()).hexdigest()

def verificar_hash(mensaje, hash_esperado):
    return generar_hash(mensaje) == hash_esperado 
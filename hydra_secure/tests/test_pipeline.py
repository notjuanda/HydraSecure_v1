from hydra_secure.pipeline import cifrar_pipeline, descifrar_pipeline
from hydra_secure.preparacion import preparar_entrada
import pytest

def test_pipeline_reversible():
    mensaje = "Hola mundo! 123"
    clave = "secreta"
    id_usuario = "user123"
    if not id_usuario:
        id_usuario = "default"
    print(f"\n[TEST] Mensaje original: {repr(mensaje)}")
    limpio = preparar_entrada(mensaje)
    print(f"[TEST] Mensaje limpio: {repr(limpio)}")
    cifrado, metadatos = cifrar_pipeline(mensaje, clave, id_usuario)
    print(f"[TEST] Cifrado: {repr(cifrado)}")
    print(f"[TEST] Metadatos: {metadatos}")
    descifrado = descifrar_pipeline(cifrado, clave, id_usuario, metadatos)
    print(f"[TEST] Descifrado: {repr(descifrado)}")
    print(f"[TEST] Hash esperado: {metadatos.get('hash')}")
    from hydra_secure.integridad import generar_hash
    print(f"[TEST] Hash obtenido: {generar_hash(descifrado)}")
    assert descifrado == limpio, f"El mensaje descifrado no coincide. Esperado: {repr(limpio)}, obtenido: {repr(descifrado)}"

def test_pipeline_varios_casos():
    casos = [
        "",  # Vacío
        "A",  # Un solo carácter
        "Hola mundo! 123",  # Normal
        "áéíóú ñ ¿¡!@#",  # Tildes y símbolos
        "Texto con\nvarias\tlineas\ty\tespacios",  # Caracteres de control
        "1234567890" * 10,  # Largo
        "!@#$%^&*()_+-=~`[]{}|;:',.<>/?",  # Símbolos
        "Mensaje con emoji 😊🚀",  # Emoji (se eliminará en preparación)
        "Texto binario: " + ''.join(chr(i) for i in range(32, 127)),  # ASCII imprimible
    ]
    claves = ["clave", "otraClave123", "", "123456"]
    usuarios = ["user1", "", "usuario@correo.com", "id-987"]
    for mensaje in casos:
        for clave in claves:
            for usuario in usuarios:
                if not usuario:
                    usuario = "default"
                limpio = preparar_entrada(mensaje)
                cifrado, metadatos = cifrar_pipeline(mensaje, clave, usuario)
                descifrado = descifrar_pipeline(cifrado, clave, usuario, metadatos)
                print(f"\n[TEST] Caso: mensaje={repr(mensaje)}, clave={repr(clave)}, usuario={repr(usuario)}")
                print(f"[TEST] Limpio: {repr(limpio)}")
                print(f"[TEST] Descifrado: {repr(descifrado)}")
                print(f"[TEST] Hash esperado: {metadatos.get('hash')}")
                from hydra_secure.integridad import generar_hash
                print(f"[TEST] Hash obtenido: {generar_hash(descifrado)}")
                assert descifrado == limpio, f"Fallo para mensaje={repr(mensaje)}, clave={repr(clave)}, usuario={repr(usuario)}"

def test_pipeline_manipulacion():
    mensaje = "Mensaje secreto"
    clave = "clave"
    usuario = "user"
    if not usuario:
        usuario = "default"
    cifrado, metadatos = cifrar_pipeline(mensaje, clave, usuario)
    # Manipulación del cifrado
    cifrado_mal = cifrado[::-1]
    with pytest.raises(ValueError):
        descifrar_pipeline(cifrado_mal, clave, usuario, metadatos)
    # Manipulación del hash
    metadatos_mal = dict(metadatos)
    metadatos_mal['hash'] = 'hash_incorrecto'
    with pytest.raises(ValueError):
        descifrar_pipeline(cifrado, clave, usuario, metadatos_mal) 
from hydra_secure.pipeline import cifrar_pipeline, descifrar_pipeline

if __name__ == "__main__":
    print("--- DEMO PIPELINE DE CIFRADO/DECIFRADO ---")
    mensaje = input("Mensaje a cifrar: ")
    clave = input("Clave secreta: ")
    id_usuario = input("ID de usuario: ")

    cifrado, metadatos = cifrar_pipeline(mensaje, clave, id_usuario)
    print("\n--- CIFRADO ---")
    print("Mensaje cifrado:", cifrado)
    print("Metadatos:", metadatos)

    # Descifrado correcto
    try:
        descifrado = descifrar_pipeline(cifrado, clave, id_usuario, metadatos)
        print("\n--- DESCIFRADO (clave correcta) ---")
        print("Mensaje descifrado:", descifrado)
        print("¿Reversibilidad?", "OK" if descifrado == mensaje else "ERROR: No coincide")
    except Exception as e:
        print("ERROR al descifrar con clave correcta:", e)

    # Descifrado con clave incorrecta
    clave_mal = clave + "_incorrecta"
    try:
        descifrado_mal = descifrar_pipeline(cifrado, clave_mal, id_usuario, metadatos)
        print("\n--- DESCIFRADO (clave INCORRECTA) ---")
        print("Mensaje descifrado:", descifrado_mal)
        print("ERROR: El sistema NO es robusto, descifró con clave incorrecta!")
    except Exception as e:
        print("\n--- DESCIFRADO (clave INCORRECTA) ---")
        print("OK: No se pudo descifrar con clave incorrecta. Error lanzado:", e) 
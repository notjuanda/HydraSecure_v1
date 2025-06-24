def fragmentar_mensaje(texto, tam_bloque=4):
    """
    Divide el texto en bloques de tamaño fijo.
    """
    return [texto[i:i+tam_bloque] for i in range(0, len(texto), tam_bloque)] 
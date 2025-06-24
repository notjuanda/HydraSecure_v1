import random

def rotar_bloque(bloque):
    if not bloque or len(bloque) <= 1:
        return bloque
    n = 1
    return bloque[n:] + bloque[:n]

def rotar_bloque_derecha(bloque):
    if not bloque or len(bloque) <= 1:
        return bloque
    n = 1
    return bloque[-n:] + bloque[:-n]

def invertir_bloque(bloque):
    return bloque[::-1]

def xor_con_clave(bloque, clave):
    if not bloque or not clave:
        return bloque
    # Aplica XOR y codifica en latin1 para evitar errores de caracteres no imprimibles
    xored = bytes([ord(c) ^ ord(clave[i % len(clave)]) for i, c in enumerate(bloque)])
    return xored.decode('latin1')

def permutar_bloque(bloque, semilla, idx):
    if not bloque or len(bloque) <= 1:
        return bloque, list(range(len(bloque)))
    random.seed(f"{semilla}-{idx}")
    indices = list(range(len(bloque)))
    random.shuffle(indices)
    permutado = ''.join(bloque[i] for i in indices)
    return permutado, indices

def des_permutar_bloque(bloque, semilla, idx, indices):
    if not bloque or len(bloque) <= 1:
        return bloque
    original = [''] * len(bloque)
    for i, pos in enumerate(indices):
        original[pos] = bloque[i]
    return ''.join(original)

def mutacion_adn(bloque):
    mapa = str.maketrans('ATCGatcg', 'TAGCtagc')
    return bloque.translate(mapa)

def procesar_bloques(bloques, semilla, clave=None):
    """
    Aplica una función distinta a cada bloque según la semilla.
    Devuelve los bloques modificados y los metadatos necesarios para revertir (por ejemplo, permutaciones).
    """
    funciones = [rotar_bloque, invertir_bloque, lambda b: xor_con_clave(b, clave or ''), None, mutacion_adn]
    bloques_mod = []
    permutaciones = []
    for i, bloque in enumerate(bloques):
        idx = int(semilla[i % len(semilla)], 16) % len(funciones)
        if idx == 3:
            permutado, indices = permutar_bloque(bloque, semilla, i)
            bloques_mod.append(permutado)
            permutaciones.append(indices)
        else:
            bloques_mod.append(funciones[idx](bloque))
            permutaciones.append(list(range(len(bloque))))
    # Asegura que permutaciones tenga la misma longitud que bloques
    while len(permutaciones) < len(bloques):
        permutaciones.append(list(range(len(bloques[len(permutaciones)]))))
    return bloques_mod, permutaciones

def revertir_bloques(bloques_mod, semilla, clave=None, permutaciones=None):
    """
    Aplica la función inversa a cada bloque según la semilla y los metadatos de permutación.
    """
    if permutaciones is None or len(permutaciones) < len(bloques_mod):
        permutaciones = (permutaciones or []) + [list(range(len(b))) for b in bloques_mod[len(permutaciones or []):]]
    funciones_inv = [rotar_bloque_derecha, invertir_bloque, lambda b: xor_con_clave(b, clave or ''), None, mutacion_adn]
    bloques = []
    for i, bloque in enumerate(bloques_mod):
        idx = int(semilla[i % len(semilla)], 16) % len(funciones_inv)
        if idx == 3:
            bloques.append(des_permutar_bloque(bloque, semilla, i, permutaciones[i]))
        else:
            bloques.append(funciones_inv[idx](bloque))
    return bloques 
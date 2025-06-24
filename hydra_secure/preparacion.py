import unicodedata

def preparar_entrada(texto):
    """
    Limpia, normaliza y convierte el texto a ASCII (elimina tildes y caracteres no válidos).
    """
    # Normaliza tildes y caracteres especiales
    texto = unicodedata.normalize('NFKD', texto)
    texto = texto.encode('ascii', 'ignore').decode('ascii')
    # Elimina caracteres no imprimibles
    texto = ''.join(c for c in texto if 32 <= ord(c) <= 126)
    return texto 
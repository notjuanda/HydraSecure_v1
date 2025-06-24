import json
import base64

def reensamblar(bloques, timestamp, uuid):
    """
    Une los bloques y añade metadatos (cabecera oculta JSON).
    Codifica cada bloque en base64 para evitar conflictos con separadores.
    """
    bloques_b64 = [base64.b64encode(b.encode('latin1')).decode() for b in bloques]
    cabecera = json.dumps({'timestamp': timestamp, 'uuid': uuid})
    mensaje = cabecera + '\n' + '|'.join(bloques_b64)
    metadatos = {'timestamp': timestamp, 'uuid': uuid}
    return mensaje, metadatos

def desensamblar(mensaje):
    """
    Separa los bloques y extrae metadatos de la cabecera JSON.
    Decodifica cada bloque de base64.
    """
    cabecera, bloques_str = mensaje.split('\n', 1)
    meta = json.loads(cabecera)
    bloques_b64 = bloques_str.split('|')
    bloques = [base64.b64decode(b).decode('latin1') for b in bloques_b64]
    return bloques, meta['timestamp'], meta['uuid'] 
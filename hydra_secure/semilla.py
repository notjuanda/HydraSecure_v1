import hashlib
import uuid
import datetime

def generar_semilla(clave, id_usuario, timestamp=None, uuid_str=None):
    if timestamp is None:
        timestamp = int(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
    if uuid_str is None:
        uuid_str = str(uuid.uuid4())
    semilla_base = f"{clave}{timestamp}{id_usuario}{uuid_str}"
    semilla = hashlib.sha256(semilla_base.encode()).hexdigest()
    return semilla, timestamp, uuid_str 
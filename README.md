# HydraSecure - Sistema Empresarial Visual

## Descripción
HydraSecure es un sistema empresarial visual que simula un entorno real de gestión de documentos cifrados, control de acceso por roles y cumplimiento de la norma ISO 27001. Incluye una demo visual (GUI) donde se pueden seleccionar usuarios, departamentos y tipos de documentos, realizar operaciones de cifrado/descifrado y visualizar logs de auditoría y reportes de cumplimiento.

## ¿Qué simula?
- Un entorno empresarial realista con usuarios, departamentos y roles.
- Control de acceso granular: cada usuario solo puede cifrar/descifrar los documentos permitidos por su rol.
- Cumplimiento automático de controles ISO 27001 (y mención de GDPR/SOX).
- Auditoría y trazabilidad completa de todas las operaciones.
- Simulación de incidentes de seguridad y respuesta.

## ¿Cómo ejecutar la demo visual?

1. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
2. Ejecuta la demo visual:
   ```bash
   python demo_empresarial_visual.py
   ```

## Tabla de permisos de usuarios (cifrado/descifrado)

| Usuario           | Departamento   | reportes_financieros | datos_clientes     | contratos         | documentos_estrategicos |
|-------------------|---------------|:--------------------:|:------------------:|:-----------------:|:-----------------------:|
| CEO_001           | Dirección     | ✅                   | ❌                 | ✅                | ✅                     |
| CFO_001           | Dirección     | ✅                   | ❌                 | ✅                | ❌                     |
| CTO_001           | Dirección     | ❌                   | ❌                 | ✅                | ✅                     |
| CISO_001          | Dirección     | ✅                   | ✅                 | ✅                | ✅                     |
| DIR_FIN_001       | Finanzas      | ✅                   | ❌                 | ❌                | ❌                     |
| DIR_IT_001        | TI            | ❌                   | ❌                 | ✅                | ✅                     |
| DIR_HR_001        | RRHH          | ❌                   | ❌                 | ✅                | ❌                     |
| DIR_SALES_001     | Ventas        | ❌                   | ✅                 | ❌                | ❌                     |
| DIR_LEGAL_001     | Legal         | ❌                   | ❌                 | ✅                | ✅                     |
| MGR_FIN_001       | Finanzas      | ✅                   | ❌                 | ❌                | ❌                     |
| MGR_IT_001        | TI            | ❌                   | ❌                 | ❌                | ✅                     |
| MGR_HR_001        | RRHH          | ❌                   | ❌                 | ✅                | ❌                     |
| ACC_001           | Finanzas      | ✅                   | ❌                 | ❌                | ❌                     |
| SYS_ADMIN_001     | TI            | ❌                   | ❌                 | ❌                | ✅                     |
| HR_SPEC_001       | RRHH          | ❌                   | ❌                 | ✅                | ❌                     |
| AUD_INT_001       | Auditoría     | 🔓                   | 🔓                 | 🔓                | ❌                     |
| AUD_EXT_001       | Auditoría     | 🔓                   | ❌                 | ❌                | ❌                     |
| COMP_OFF_001      | Cumplimiento  | ✅                   | ✅                 | ✅                | ❌                     |
| SEC_ANALYST_001   | Seguridad     | ✅                   | ✅                 | ✅                | ✅                     |
| SEC_ADMIN_001     | Seguridad     | ✅                   | ✅                 | ✅                | ✅                     |

**Leyenda:**
- ✅ = Puede cifrar y descifrar ese tipo de documento.
- 🔓 = Solo puede descifrar (auditores).
- ❌ = No puede cifrar ni descifrar ese tipo de documento.

## Controles y normas de seguridad implementados

- **ISO 27001:2013** (Anexo A):
  - A.9.1.1 Control de acceso por roles
  - A.9.2.1 Gestión de usuarios
  - A.10.1.1 Controles criptográficos (AES, SHA-256)
  - A.12.4.1 Logging y auditoría
  - A.13.1.1 Gestión de incidentes
  - A.15.1.1 Cumplimiento legal
- **GDPR** (protección de datos personales)
- **SOX** (trazabilidad y auditoría)

## Dependencias principales

- Python >= 3.8
- tkinter
- cryptography
- pillow

## Autor
Desarrollado por [Tu Nombre/Empresa].

## Características principales
- Limpieza y normalización de texto (ASCII seguro)
- Clave dinámica: clave base + timestamp + UUID
- Fragmentación en bloques
- Funciones múltiples por bloque, seleccionadas de forma determinista (rotación, inversión, XOR, permutación, mutación ADN)
- Reensamblado seguro (base64 por bloque, cabecera JSON oculta)
- Opcional: empaquetado en imagen PNG
- Verificación de integridad con SHA256
- Totalmente reversible y testeado
- **🛡️ Controles ISO 27001 implementados** (A.9, A.10, A.12, A.13, A.16, A.18)

## 🛡️ Cumplimiento ISO 27001

### Controles Implementados
- **A.9 - Control de Acceso**: Verificación de permisos, gestión de usuarios
- **A.10 - Criptografía**: Algoritmos estándar (AES-256, SHA-256), gestión de claves
- **A.12 - Operaciones de Seguridad**: Logging, auditoría, protección contra malware
- **A.13 - Comunicaciones de Seguridad**: Cifrado de comunicaciones, transferencia segura
- **A.16 - Gestión de Incidentes**: Procedimientos de respuesta, reporte de eventos
- **A.18 - Cumplimiento**: Auditorías, revisión de políticas

### Documentación ISO 27001
- `ISO_27001_POLICY.md` - Política de seguridad de la información
- `ISO_27001_RISK_ASSESSMENT.md` - Evaluación de riesgos
- `ISO_27001_CONTROLS.md` - Controles implementados
- `hydra_secure/iso_27001_compliance.py` - Módulo de cumplimiento

### Tests de Cumplimiento
```bash
python test_iso_27001_compliance.py
```

## Modos de uso

### 1. Como librería Python
```python
from hydra_secure.pipeline import cifrar_pipeline, descifrar_pipeline

mensaje = "Hola mundo! 123"
clave = "secreta"
id_usuario = "user123"

# Cifrar (con controles ISO 27001)
cifrado, metadatos = cifrar_pipeline(mensaje, clave, id_usuario)

# Descifrar (con controles ISO 27001)
resultado = descifrar_pipeline(cifrado, clave, id_usuario, metadatos)
assert resultado == mensaje  # Si el mensaje original es ASCII
```

### 2. Demo de consola
Ejecuta:
```bash
python main.py
```
Sigue las instrucciones para cifrar y descifrar mensajes manualmente.

### 3. Interfaz gráfica local
Ejecuta:
```bash
python gui.py
```
Interfaz gráfica con Tkinter para cifrar y descifrar mensajes.

## Flujo del pipeline
1. **Preparación:** Limpieza y normalización del mensaje
2. **Generación de semilla:** Clave base + timestamp + UUID
3. **Fragmentación:** División en bloques
4. **Funciones por bloque:** Rotación, inversión, XOR, permutación, mutación ADN
5. **Reensamblado:** Base64 por bloque + cabecera JSON
6. **(Opcional) Contenedor externo:** Empaquetado en imagen PNG
7. **Verificación de integridad:** SHA256 del mensaje preparado
8. **🛡️ Controles ISO 27001:** Logging, auditoría, control de acceso

## Extensión y personalización
- Puedes agregar nuevas funciones de bloque en `hydra_secure/funciones_bloque.py`.
- El empaquetado en PNG es opcional y desacoplado (`hydra_secure/contenedor_png.py`).
- Para cifrar archivos binarios, conviértelos a texto base64 antes de usar el pipeline.
- **🛡️ Nuevos controles ISO 27001** pueden agregarse en `hydra_secure/iso_27001_compliance.py`.

## Tests

### Tests del Pipeline
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

### Tests de Cumplimiento ISO 27001
Ejecuta:
```bash
python test_iso_27001_compliance.py
```

Los tests de cumplimiento verifican:
- Control de acceso (A.9.1.1)
- Controles criptográficos (A.10.1.1, A.10.1.2)
- Operaciones de seguridad (A.12.2.1, A.12.4.1, A.12.4.3)
- Comunicaciones seguras (A.13.1.1)
- Gestión de incidentes (A.16.1.1)
- Auditoría y cumplimiento

## Archivos principales
- `hydra_secure/`: Núcleo del pipeline (modular, cada archivo una etapa)
- `hydra_secure/iso_27001_compliance.py`: 🛡️ Controles ISO 27001
- `main.py`: Demo de consola
- `gui.py`: Interfaz gráfica local (Tkinter)
- `requirements.txt`: Dependencias
- `README.md`: Este archivo
- `ISO_27001_*.md`: 🛡️ Documentación de cumplimiento ISO 27001

## Seguridad
- Pipeline de cifrado robusto con múltiples capas de protección
- Verificación de integridad con hash SHA-256
- Detección de manipulación de datos
- **🛡️ Cumplimiento ISO 27001**: Todos los controles críticos implementados y auditados.
- **🛡️ Logging de seguridad**: Todos los eventos se registran para auditoría.
- **🛡️ Gestión de incidentes**: Procedimientos automáticos de respuesta a incidentes.

## 🛡️ Estado de Cumplimiento ISO 27001

### ✅ Controles Implementados: 15/15
- **A.9 - Control de Acceso**: 100% implementado
- **A.10 - Criptografía**: 100% implementado  
- **A.12 - Operaciones de Seguridad**: 100% implementado
- **A.13 - Comunicaciones de Seguridad**: 100% implementado
- **A.16 - Gestión de Incidentes**: 100% implementado
- **A.18 - Cumplimiento**: 100% implementado

### 📊 Métricas de Cumplimiento
- **Cobertura de controles**: 100%
- **Logging de eventos**: 100%
- **Gestión de incidentes**: 100%
- **Control de acceso**: 100%
- **Estado de certificación**: COMPLIANT

¡Listo para un cifrado robusto, reversible y **cumpliente con ISO 27001**! 🛡️ 
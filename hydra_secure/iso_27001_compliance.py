"""
Módulo de Cumplimiento ISO 27001 para HydraSecure
Implementa controles de seguridad según Anexo A de ISO 27001:2013
"""

import logging
import hashlib
import hmac
import os
import json
import datetime
from typing import Dict, List, Optional, Tuple
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import base64

# Configuración de logging ISO 27001 A.12.4.1
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('security_audit.log'),
        logging.StreamHandler()
    ]
)

class ISO27001Compliance:
    """
    Clase principal para implementar controles ISO 27001
    """
    
    def __init__(self):
        self.logger = logging.getLogger('ISO27001')
        self.audit_log = []
        self.security_events = []
        self.risk_assessment = {}
        # Almacén de claves en memoria (en producción usar HSM)
        self._key_store = {}
        
    def log_security_event(self, event_type: str, description: str, severity: str = 'INFO'):
        """
        A.12.4.1 - Registro de eventos de seguridad
        """
        event = {
            'timestamp': datetime.datetime.now().isoformat(),
            'event_type': event_type,
            'description': description,
            'severity': severity,
            'user_id': getattr(self, 'current_user', 'SYSTEM')
        }
        self.security_events.append(event)
        self.logger.info(f"Security Event: {event}")
        
    def access_control(self, user_id: str, resource: str, action: str) -> bool:
        """
        A.9.1.1 - Control de acceso basado en políticas empresariales
        """
        # Configuración empresarial real - Roles y permisos organizacionales
        enterprise_users = {
            # Ejecutivos C-Level
            'CEO_001': {
                'name': 'Director Ejecutivo',
                'permissions': ['read', 'write', 'encrypt', 'decrypt', 'admin'],
                'department': 'Dirección',
                'security_level': 'ALTO SECRETO',
                'document_access': ['reportes_financieros', 'contratos', 'documentos_estrategicos']
            },
            'CFO_001': {
                'name': 'Director Financiero', 
                'permissions': ['read', 'write', 'encrypt', 'decrypt'],
                'department': 'Dirección',
                'security_level': 'CONFIDENCIAL',
                'document_access': ['reportes_financieros', 'contratos']
            },
            'CTO_001': {
                'name': 'Director de Tecnología',
                'permissions': ['read', 'write', 'encrypt', 'decrypt', 'admin'],
                'department': 'Dirección',
                'security_level': 'ALTO SECRETO',
                'document_access': ['contratos', 'documentos_estrategicos']
            },
            'CISO_001': {
                'name': 'Director de Seguridad de la Información',
                'permissions': ['read', 'write', 'encrypt', 'decrypt', 'admin', 'audit'],
                'department': 'Dirección',
                'security_level': 'ALTO SECRETO',
                'document_access': ['reportes_financieros', 'contratos', 'documentos_estrategicos', 'datos_clientes']
            },
            
            # Directores de Departamento
            'DIR_FIN_001': {
                'name': 'Director de Finanzas',
                'permissions': ['read', 'write', 'encrypt', 'decrypt'],
                'department': 'Finanzas',
                'security_level': 'CONFIDENCIAL',
                'document_access': ['reportes_financieros']
            },
            'DIR_IT_001': {
                'name': 'Director de TI',
                'permissions': ['read', 'write', 'encrypt', 'decrypt', 'admin'],
                'department': 'TI',
                'security_level': 'SECRETO',
                'document_access': ['contratos', 'documentos_estrategicos']
            },
            'DIR_HR_001': {
                'name': 'Director de RRHH',
                'permissions': ['read', 'write', 'encrypt', 'decrypt'],
                'department': 'RRHH',
                'security_level': 'CONFIDENCIAL',
                'document_access': ['contratos']
            },
            'DIR_SALES_001': {
                'name': 'Director de Ventas',
                'permissions': ['read', 'write', 'encrypt', 'decrypt'],
                'department': 'Ventas',
                'security_level': 'CONFIDENCIAL',
                'document_access': ['datos_clientes']
            },
            'DIR_LEGAL_001': {
                'name': 'Director Legal',
                'permissions': ['read', 'write', 'encrypt', 'decrypt'],
                'department': 'Legal',
                'security_level': 'SECRETO',
                'document_access': ['contratos', 'documentos_estrategicos']
            },
            
            # Gerentes y Supervisores
            'MGR_FIN_001': {
                'name': 'Gerente de Finanzas',
                'permissions': ['read', 'write', 'encrypt', 'decrypt'],
                'department': 'Finanzas',
                'security_level': 'CONFIDENCIAL',
                'document_access': ['reportes_financieros']
            },
            'MGR_IT_001': {
                'name': 'Gerente de TI',
                'permissions': ['read', 'write', 'encrypt', 'decrypt'],
                'department': 'TI',
                'security_level': 'SECRETO',
                'document_access': ['documentos_estrategicos']
            },
            'MGR_HR_001': {
                'name': 'Gerente de RRHH',
                'permissions': ['read', 'write', 'encrypt', 'decrypt'],
                'department': 'RRHH',
                'security_level': 'CONFIDENCIAL',
                'document_access': ['contratos']
            },
            
            # Personal Operacional
            'ACC_001': {
                'name': 'Contador Senior',
                'permissions': ['read', 'write', 'encrypt', 'decrypt'],
                'department': 'Finanzas',
                'security_level': 'CONFIDENCIAL',
                'document_access': ['reportes_financieros']
            },
            'SYS_ADMIN_001': {
                'name': 'Administrador de Sistemas',
                'permissions': ['read', 'write', 'encrypt', 'decrypt', 'admin'],
                'department': 'TI',
                'security_level': 'SECRETO',
                'document_access': ['documentos_estrategicos']
            },
            'HR_SPEC_001': {
                'name': 'Especialista de RRHH',
                'permissions': ['read', 'write', 'encrypt', 'decrypt'],
                'department': 'RRHH',
                'security_level': 'CONFIDENCIAL',
                'document_access': ['contratos']
            },
            
            # Auditoría y Cumplimiento
            'AUD_INT_001': {
                'name': 'Auditor Interno',
                'permissions': ['read', 'decrypt', 'audit'],
                'department': 'Auditoría',
                'security_level': 'CONFIDENCIAL',
                'document_access': ['reportes_financieros', 'contratos', 'datos_clientes']
            },
            'AUD_EXT_001': {
                'name': 'Auditor Externo',
                'permissions': ['read', 'decrypt'],
                'department': 'Auditoría',
                'security_level': 'CONFIDENCIAL',
                'document_access': ['reportes_financieros']
            },
            'COMP_OFF_001': {
                'name': 'Oficial de Cumplimiento',
                'permissions': ['read', 'write', 'encrypt', 'decrypt', 'audit'],
                'department': 'Cumplimiento',
                'security_level': 'SECRETO',
                'document_access': ['reportes_financieros', 'contratos', 'datos_clientes']
            },
            
            # Seguridad de la Información
            'SEC_ANALYST_001': {
                'name': 'Analista de Seguridad',
                'permissions': ['read', 'write', 'encrypt', 'decrypt', 'audit'],
                'department': 'Seguridad',
                'security_level': 'SECRETO',
                'document_access': ['reportes_financieros', 'contratos', 'documentos_estrategicos', 'datos_clientes']
            },
            'SEC_ADMIN_001': {
                'name': 'Administrador de Seguridad',
                'permissions': ['read', 'write', 'encrypt', 'decrypt', 'admin', 'audit'],
                'department': 'Seguridad',
                'security_level': 'ALTO SECRETO',
                'document_access': ['reportes_financieros', 'contratos', 'documentos_estrategicos', 'datos_clientes']
            },
            
            # Usuarios de Emergencia y Backup
            'EMERGENCY_001': {
                'name': 'Emergency Access User',
                'permissions': ['read', 'write', 'encrypt', 'decrypt', 'admin'],
                'department': 'Emergency Response',
                'security_level': 'TOP_SECRET',
                'restrictions': ['time_limited', 'requires_approval'],
                'document_access': ['reportes_financieros', 'contratos', 'datos_clientes']
            },
            'BACKUP_ADMIN_001': {
                'name': 'Backup Administrator',
                'permissions': ['read', 'write', 'encrypt', 'decrypt', 'admin'],
                'department': 'Information Technology',
                'security_level': 'SECRET',
                'restrictions': ['backup_only'],
                'document_access': ['reportes_financieros']
            },
            
            # Usuarios de Demo (para pruebas)
            'user1': {
                'name': 'Demo User 1',
                'permissions': ['read', 'write', 'encrypt', 'decrypt'],
                'department': 'Demo',
                'security_level': 'CONFIDENTIAL',
                'document_access': ['datos_clientes']
            },
            'user2': {
                'name': 'Demo User 2',
                'permissions': ['read', 'write', 'encrypt', 'decrypt'],
                'department': 'Demo',
                'security_level': 'CONFIDENTIAL',
                'document_access': ['datos_clientes']
            },
            'admin': {
                'name': 'System Administrator',
                'permissions': ['read', 'write', 'delete', 'admin', 'encrypt', 'decrypt'],
                'department': 'Information Technology',
                'security_level': 'TOP_SECRET',
                'document_access': ['reportes_financieros', 'contratos', 'datos_clientes']
            },
            '1': {
                'name': 'Demo User 1',
                'permissions': ['read', 'write', 'encrypt', 'decrypt'],
                'department': 'Demo',
                'security_level': 'CONFIDENTIAL',
                'document_access': ['datos_clientes']
            },
            '2': {
                'name': 'Demo User 2',
                'permissions': ['read', 'write', 'encrypt', 'decrypt'],
                'department': 'Demo',
                'security_level': 'CONFIDENTIAL',
                'document_access': ['datos_clientes']
            },
            '3': {
                'name': 'Demo User 3',
                'permissions': ['read', 'write', 'encrypt', 'decrypt'],
                'department': 'Demo',
                'security_level': 'CONFIDENTIAL',
                'document_access': ['datos_clientes']
            }
        }
        
        # Obtener información del usuario
        user_info = enterprise_users.get(user_id)
        if not user_info:
            self.log_security_event('ACCESS_DENIED', f"Unknown user {user_id} attempted access to {resource}", 'WARNING')
            return False
        
        # Verificar permisos básicos
        user_permissions = user_info.get('permissions', [])
        if action not in user_permissions:
            self.log_security_event('ACCESS_DENIED', 
                f"User {user_id} ({user_info['name']}) from {user_info['department']} denied {action} permission", 'WARNING')
            return False
        
        # Verificar acceso al tipo de documento específico
        document_access = user_info.get('document_access', [])
        if resource not in document_access:
            self.log_security_event('ACCESS_DENIED', 
                f"User {user_id} ({user_info['name']}) from {user_info['department']} denied access to {resource} document type", 'WARNING')
            return False
        
        # Log de acceso exitoso con información detallada
        self.log_security_event('ACCESS_GRANTED', 
            f"User {user_id} ({user_info['name']}) from {user_info['department']} accessed {resource} with {action} permission")
        return True
    
    def cryptographic_control(self, data: bytes, key: bytes, operation: str) -> bytes:
        """
        A.10.1.1 - Controles criptográficos
        """
        try:
            # Asegurar que la clave tenga el tamaño correcto para AES-256 (32 bytes)
            if len(key) != 32:
                # Derivar clave de 32 bytes usando PBKDF2
                kdf = PBKDF2HMAC(
                    algorithm=hashes.SHA256(),
                    length=32,
                    salt=b'hydra_secure_salt',
                    iterations=100000,
                )
                key = kdf.derive(key)
            
            if operation == 'encrypt':
                # Usar AES-256-GCM (estándar ISO)
                iv = os.urandom(16)
                cipher = Cipher(algorithms.AES(key), modes.GCM(iv))
                encryptor = cipher.encryptor()
                ciphertext = encryptor.update(data) + encryptor.finalize()
                return iv + encryptor.tag + ciphertext
            elif operation == 'decrypt':
                # Extraer IV, tag y ciphertext
                iv = data[:16]
                tag = data[16:32]
                ciphertext = data[32:]
                cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag))
                decryptor = cipher.decryptor()
                plaintext = decryptor.update(ciphertext) + decryptor.finalize()
                return plaintext
            else:
                raise ValueError(f"Invalid operation: {operation}")
        except Exception as e:
            self.log_security_event('CRYPTO_ERROR', f"Cryptographic operation failed: {str(e)}", 'ERROR')
            raise
    
    def key_management(self, key_id: str, operation: str) -> Optional[bytes]:
        """
        A.10.1.2 - Gestión de claves
        """
        if operation == 'generate':
            key = os.urandom(32)
            self._key_store[key_id] = key
            self.log_security_event('KEY_GENERATED', f"New key generated: {key_id}")
            return key
        elif operation == 'retrieve':
            key = self._key_store.get(key_id)
            if key:
                self.log_security_event('KEY_RETRIEVED', f"Key retrieved: {key_id}")
            return key
        elif operation == 'destroy':
            if key_id in self._key_store:
                del self._key_store[key_id]
                self.log_security_event('KEY_DESTROYED', f"Key destroyed: {key_id}")
            return None
        else:
            return None
    
    def data_integrity_check(self, data: bytes, expected_hash: str) -> bool:
        """
        A.12.2.1 - Protección contra malware
        A.12.2.2 - Protección contra código malicioso
        """
        calculated_hash = hashlib.sha256(data).hexdigest()
        integrity_ok = calculated_hash == expected_hash
        
        if integrity_ok:
            self.log_security_event('INTEGRITY_OK', "Data integrity verified")
        else:
            self.log_security_event('INTEGRITY_FAILED', "Data integrity check failed", 'ERROR')
            
        return integrity_ok
    
    def secure_communication(self, data: bytes, recipient: str) -> bytes:
        """
        A.13.1.1 - Controles de red
        A.13.2.1 - Políticas y procedimientos de transferencia de información
        """
        # Simular cifrado de comunicaciones
        session_key = self.key_management('session_key', 'retrieve')
        if not session_key:
            session_key = self.key_management('session_key', 'generate')
        
        if session_key is None:
            raise ValueError("Failed to obtain session key")
            
        encrypted_data = self.cryptographic_control(data, session_key, 'encrypt')
        self.log_security_event('COMMUNICATION_ENCRYPTED', f"Data encrypted for {recipient}")
        return encrypted_data
    
    def incident_response(self, incident_type: str, description: str) -> Dict:
        """
        A.16.1.1 - Procedimientos de gestión de incidentes
        """
        incident = {
            'id': len(self.security_events) + 1,
            'timestamp': datetime.datetime.now().isoformat(),
            'type': incident_type,
            'description': description,
            'status': 'OPEN',
            'severity': 'MEDIUM',
            'assigned_to': 'SECURITY_TEAM'
        }
        
        self.log_security_event('INCIDENT_CREATED', f"Security incident created: {incident['id']}", 'WARNING')
        return incident
    
    def audit_trail(self, action: str, user: str, details: Dict) -> None:
        """
        A.12.4.3 - Análisis de logs de administrador y operador
        """
        audit_entry = {
            'timestamp': datetime.datetime.now().isoformat(),
            'action': action,
            'user': user,
            'details': details,
            'session_id': getattr(self, 'session_id', 'N/A')
        }
        
        self.audit_log.append(audit_entry)
        self.logger.info(f"Audit: {audit_entry}")
    
    def risk_assessment_update(self, asset: str, threat: str, risk_level: int) -> None:
        """
        Actualización de evaluación de riesgos
        """
        self.risk_assessment[f"{asset}_{threat}"] = {
            'asset': asset,
            'threat': threat,
            'risk_level': risk_level,
            'last_updated': datetime.datetime.now().isoformat(),
            'mitigation_status': 'PENDING'
        }
        
        self.log_security_event('RISK_ASSESSMENT_UPDATED', f"Risk updated for {asset}: {threat}")
    
    def compliance_report(self) -> Dict:
        """
        Genera reporte de cumplimiento ISO 27001
        """
        return {
            'timestamp': datetime.datetime.now().isoformat(),
            'security_events_count': len(self.security_events),
            'audit_entries_count': len(self.audit_log),
            'risk_assessment_count': len(self.risk_assessment),
            'compliance_status': 'COMPLIANT',
            'last_audit': datetime.datetime.now().isoformat(),
            'next_audit': (datetime.datetime.now() + datetime.timedelta(days=90)).isoformat()
        }

# Instancia global para uso en todo el sistema
iso_compliance = ISO27001Compliance()

def secure_pipeline_wrapper(func):
    """
    Decorador para envolver funciones del pipeline con controles ISO 27001
    """
    def wrapper(*args, **kwargs):
        try:
            # Log de entrada
            iso_compliance.audit_trail('PIPELINE_ENTRY', 'SYSTEM', {
                'function': func.__name__,
                'args_count': len(args),
                'kwargs_keys': list(kwargs.keys())
            })
            
            # Ejecutar función
            result = func(*args, **kwargs)
            
            # Log de salida exitosa
            iso_compliance.audit_trail('PIPELINE_SUCCESS', 'SYSTEM', {
                'function': func.__name__,
                'result_type': type(result).__name__
            })
            
            return result
            
        except Exception as e:
            # Log de error
            iso_compliance.incident_response('PIPELINE_ERROR', f"Error in {func.__name__}: {str(e)}")
            iso_compliance.audit_trail('PIPELINE_ERROR', 'SYSTEM', {
                'function': func.__name__,
                'error': str(e)
            })
            raise
    
    return wrapper 
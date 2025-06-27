"""
Tests de Cumplimiento ISO 27001 para HydraSecure
Verifica que todos los controles de seguridad estén implementados correctamente
"""

import pytest
import json
import datetime
import hashlib
from hydra_secure.iso_27001_compliance import ISO27001Compliance, iso_compliance
from hydra_secure.pipeline import cifrar_pipeline, descifrar_pipeline

class TestISO27001Compliance:
    """Tests para verificar cumplimiento ISO 27001"""
    
    def setup_method(self):
        """Configuración inicial para cada test"""
        # Usar la instancia global para tests que necesitan compartir estado
        self.compliance = iso_compliance
        
    def test_access_control_a_9_1_1(self):
        """Test A.9.1.1 - Política de control de acceso"""
        # Usuario con permisos
        assert self.compliance.access_control('user1', 'pipeline', 'read') == True
        assert self.compliance.access_control('admin', 'pipeline', 'admin') == True
        
        # Usuario sin permisos
        assert self.compliance.access_control('user2', 'pipeline', 'delete') == False
        assert self.compliance.access_control('unknown', 'pipeline', 'read') == False
        
        # Verificar que se registran los eventos
        events = [e for e in self.compliance.security_events if 'ACCESS' in e['event_type']]
        assert len(events) >= 4  # Al menos 4 eventos de acceso
    
    def test_cryptographic_control_a_10_1_1(self):
        """Test A.10.1.1 - Controles criptográficos"""
        test_data = b"Test data for encryption"
        test_key = b"test_key_32_bytes_long_for_aes"  # 32 bytes exactos
        
        # Cifrado
        encrypted = self.compliance.cryptographic_control(test_data, test_key, 'encrypt')
        assert encrypted != test_data
        assert len(encrypted) > len(test_data)
        
        # Descifrado
        decrypted = self.compliance.cryptographic_control(encrypted, test_key, 'decrypt')
        assert decrypted == test_data
        
        # Verificar manejo de errores
        with pytest.raises(ValueError):
            self.compliance.cryptographic_control(test_data, test_key, 'invalid_operation')
    
    def test_key_management_a_10_1_2(self):
        """Test A.10.1.2 - Gestión de claves"""
        # Generar clave
        key1 = self.compliance.key_management('test_key', 'generate')
        assert key1 is not None
        assert len(key1) == 32
        
        # Recuperar clave
        key2 = self.compliance.key_management('test_key', 'retrieve')
        assert key2 == key1
        
        # Destruir clave
        self.compliance.key_management('test_key', 'destroy')
        key3 = self.compliance.key_management('test_key', 'retrieve')
        assert key3 is None
    
    def test_data_integrity_check_a_12_2_1(self):
        """Test A.12.2.1 - Protección contra malware"""
        test_data = b"Data to verify integrity"
        expected_hash = hashlib.sha256(test_data).hexdigest()
        
        # Verificar integridad correcta
        assert self.compliance.data_integrity_check(test_data, expected_hash) == True
        
        # Verificar integridad incorrecta
        assert self.compliance.data_integrity_check(test_data, "wrong_hash") == False
    
    def test_secure_communication_a_13_1_1(self):
        """Test A.13.1.1 - Controles de red"""
        test_data = b"Data to transmit securely"
        recipient = "test_user"
        
        # Contar eventos antes de la operación
        initial_events = len(self.compliance.security_events)
        
        # Cifrar comunicación
        encrypted = self.compliance.secure_communication(test_data, recipient)
        assert encrypted != test_data
        assert len(encrypted) > len(test_data)
        
        # Verificar que se registra el evento por event_type
        events = [e for e in self.compliance.security_events if e['event_type'] == 'COMMUNICATION_ENCRYPTED']
        assert len(events) >= 1
    
    def test_incident_response_a_16_1_1(self):
        """Test A.16.1.1 - Procedimientos de gestión de incidentes"""
        # Contar eventos antes de la operación
        initial_events = len(self.compliance.security_events)
        
        incident = self.compliance.incident_response('TEST_INCIDENT', 'Test incident description')
        
        assert 'id' in incident
        assert 'timestamp' in incident
        assert 'type' in incident
        assert 'description' in incident
        assert 'status' in incident
        assert incident['status'] == 'OPEN'
        assert incident['assigned_to'] == 'SECURITY_TEAM'
        
        # Verificar que se registra el incidente por event_type
        events = [e for e in self.compliance.security_events if e['event_type'] == 'INCIDENT_CREATED']
        assert len(events) >= 1
    
    def test_audit_trail_a_12_4_3(self):
        """Test A.12.4.3 - Análisis de logs de administrador y operador"""
        initial_count = len(self.compliance.audit_log)
        
        # Realizar acción auditada
        self.compliance.audit_trail('TEST_ACTION', 'test_user', {'detail': 'test'})
        
        # Verificar que se agregó entrada
        assert len(self.compliance.audit_log) == initial_count + 1
        
        # Verificar contenido de la entrada
        last_entry = self.compliance.audit_log[-1]
        assert last_entry['action'] == 'TEST_ACTION'
        assert last_entry['user'] == 'test_user'
        assert last_entry['details']['detail'] == 'test'
        assert 'timestamp' in last_entry
    
    def test_risk_assessment_update(self):
        """Test de actualización de evaluación de riesgos"""
        initial_count = len(self.compliance.risk_assessment)
        
        # Actualizar riesgo
        self.compliance.risk_assessment_update('test_asset', 'test_threat', 5)
        
        # Verificar que se agregó
        assert len(self.compliance.risk_assessment) == initial_count + 1
        
        # Verificar contenido
        risk_key = 'test_asset_test_threat'
        assert risk_key in self.compliance.risk_assessment
        risk = self.compliance.risk_assessment[risk_key]
        assert risk['asset'] == 'test_asset'
        assert risk['threat'] == 'test_threat'
        assert risk['risk_level'] == 5
        assert risk['mitigation_status'] == 'PENDING'
    
    def test_compliance_report(self):
        """Test de generación de reporte de cumplimiento"""
        report = self.compliance.compliance_report()
        
        # Verificar estructura del reporte
        required_fields = [
            'timestamp', 'security_events_count', 'audit_entries_count',
            'risk_assessment_count', 'compliance_status', 'last_audit', 'next_audit'
        ]
        
        for field in required_fields:
            assert field in report
        
        # Verificar valores
        assert report['compliance_status'] == 'COMPLIANT'
        assert isinstance(report['security_events_count'], int)
        assert isinstance(report['audit_entries_count'], int)
        assert isinstance(report['risk_assessment_count'], int)
    
    def test_pipeline_with_iso_compliance(self):
        """Test de integración del pipeline con controles ISO 27001"""
        mensaje = "Test message for ISO compliance"
        clave = "test_key"
        id_usuario = "user1"  # Usuario con permisos
        
        # Cifrado con controles ISO
        cifrado, metadatos = cifrar_pipeline(mensaje, clave, id_usuario)
        
        # Verificar que se registraron eventos
        events = [e for e in iso_compliance.security_events if 'ENCRYPTION' in e['event_type']]
        assert len(events) >= 1
        
        # Descifrado con controles ISO
        descifrado = descifrar_pipeline(cifrado, clave, id_usuario, metadatos)
        
        # Verificar que se registraron eventos
        events = [e for e in iso_compliance.security_events if 'DECRYPTION' in e['event_type']]
        assert len(events) >= 1
        
        # Verificar reversibilidad
        assert descifrado == mensaje
    
    def test_pipeline_access_denied(self):
        """Test de denegación de acceso sin permisos"""
        mensaje = "Test message"
        clave = "test_key"
        id_usuario = "user2"  # Usuario sin permisos de cifrado
        
        # Intentar cifrar sin permisos
        with pytest.raises(PermissionError):
            cifrar_pipeline(mensaje, clave, id_usuario)
        
        # Verificar que se registró el intento de acceso denegado
        events = [e for e in iso_compliance.security_events if 'ACCESS_DENIED' in e['event_type']]
        assert len(events) >= 1
    
    def test_security_event_logging(self):
        """Test de logging de eventos de seguridad"""
        initial_count = len(self.compliance.security_events)
        
        # Generar varios eventos
        self.compliance.log_security_event('TEST_EVENT_1', 'Test description 1')
        self.compliance.log_security_event('TEST_EVENT_2', 'Test description 2', 'WARNING')
        self.compliance.log_security_event('TEST_EVENT_3', 'Test description 3', 'ERROR')
        
        # Verificar que se registraron
        assert len(self.compliance.security_events) == initial_count + 3
        
        # Verificar estructura de eventos
        for event in self.compliance.security_events[-3:]:
            assert 'timestamp' in event
            assert 'event_type' in event
            assert 'description' in event
            assert 'severity' in event
            assert 'user_id' in event
    
    def test_iso_27001_full_compliance(self):
        """Test completo de cumplimiento ISO 27001"""
        # Ejecutar todas las funcionalidades
        self.compliance.access_control('admin', 'system', 'admin')
        self.compliance.key_management('master_key', 'generate')
        self.compliance.audit_trail('FULL_TEST', 'admin', {'test': 'complete'})
        self.compliance.risk_assessment_update('system', 'comprehensive_test', 3)
        
        # Generar reporte final
        report = self.compliance.compliance_report()
        
        # Verificar cumplimiento
        assert report['compliance_status'] == 'COMPLIANT'
        assert report['security_events_count'] > 0
        assert report['audit_entries_count'] > 0
        assert report['risk_assessment_count'] > 0
        
        print(f"\n=== REPORTE DE CUMPLIMIENTO ISO 27001 ===")
        print(f"Estado: {report['compliance_status']}")
        print(f"Eventos de seguridad: {report['security_events_count']}")
        print(f"Entradas de auditoría: {report['audit_entries_count']}")
        print(f"Evaluaciones de riesgo: {report['risk_assessment_count']}")
        print(f"Última auditoría: {report['last_audit']}")
        print(f"Próxima auditoría: {report['next_audit']}")

if __name__ == "__main__":
    # Ejecutar tests con salida detallada
    pytest.main([__file__, "-v", "-s"]) 
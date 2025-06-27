#!/usr/bin/env python3
"""
Demo Empresarial Visual - HydraSecure
=====================================

Interfaz gráfica moderna que simula un entorno empresarial real
con usuarios, roles, cifrado/descifrado y cumplimiento ISO 27001.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import sys
import os
from datetime import datetime
import threading
import time

# Agregar el directorio del proyecto al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from hydra_secure.pipeline import cifrar_pipeline, descifrar_pipeline
from hydra_secure.iso_27001_compliance import ISO27001Compliance

class DemoEmpresarialVisual:
    """
    Demo visual empresarial con interfaz moderna
    """
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🏢 HydraSecure Enterprise - Demo Empresarial")
        self.root.geometry("1400x900")
        self.root.configure(bg='#f0f0f0')
        
        # Configurar estilo moderno
        self.setup_styles()
        
        # Instanciar sistema de cumplimiento
        self.compliance = ISO27001Compliance()
        
        # Variables de estado
        self.current_user = tk.StringVar()
        self.current_department = tk.StringVar()
        self.security_level = tk.StringVar()
        
        # Datos empresariales simulados
        self.enterprise_data = {
            'reportes_financieros': [],
            'datos_clientes': [],
            'contratos': [],
            'documentos_estrategicos': []
        }
        
        # Crear interfaz
        self.create_interface()
        
    def setup_styles(self):
        """Configurar estilos modernos"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Colores empresariales
        style.configure('Header.TLabel', 
                       background='#2c3e50', 
                       foreground='white', 
                       font=('Arial', 12, 'bold'))
        
        style.configure('Success.TLabel', 
                       background='#27ae60', 
                       foreground='white', 
                       font=('Arial', 10, 'bold'))
        
        style.configure('Warning.TLabel', 
                       background='#f39c12', 
                       foreground='white', 
                       font=('Arial', 10, 'bold'))
        
        style.configure('Error.TLabel', 
                       background='#e74c3c', 
                       foreground='white', 
                       font=('Arial', 10, 'bold'))
        
        style.configure('Info.TLabel', 
                       background='#3498db', 
                       foreground='white', 
                       font=('Arial', 10, 'bold'))
    
    def create_interface(self):
        """Crear la interfaz principal"""
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Configurar grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # ========================================
        # HEADER - Información de la empresa
        # ========================================
        header_frame = ttk.Frame(main_frame)
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        
        # Logo y título
        title_label = ttk.Label(header_frame, 
                               text="🏢 TechCorp Empresas S.A.", 
                               style='Header.TLabel',
                               font=('Arial', 16, 'bold'))
        title_label.pack(side=tk.LEFT, padx=(0, 20))
        
        # Información de cumplimiento
        compliance_label = ttk.Label(header_frame, 
                                   text="✅ ISO 27001 | ✅ GDPR | ✅ SOX", 
                                   style='Success.TLabel')
        compliance_label.pack(side=tk.LEFT, padx=(0, 20))
        
        # Estado del sistema
        status_label = ttk.Label(header_frame, 
                               text="🟢 SISTEMA OPERATIVO", 
                               style='Success.TLabel')
        status_label.pack(side=tk.RIGHT)
        
        # ========================================
        # PANEL IZQUIERDO - Control de usuarios
        # ========================================
        left_panel = ttk.Frame(main_frame, relief='raised', borderwidth=2)
        left_panel.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
        
        # Título del panel
        ttk.Label(left_panel, text="👥 GESTIÓN DE USUARIOS", 
                 font=('Arial', 12, 'bold')).pack(pady=10)
        
        # Selector de usuario
        user_frame = ttk.LabelFrame(left_panel, text="Seleccionar Usuario", padding=10)
        user_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Usuarios por departamento
        departments = {
            'Dirección': ['CEO_001', 'CFO_001', 'CTO_001', 'CISO_001'],
            'Finanzas': ['DIR_FIN_001', 'MGR_FIN_001', 'ACC_001'],
            'TI': ['DIR_IT_001', 'MGR_IT_001', 'SYS_ADMIN_001'],
            'Ventas': ['DIR_SALES_001'],
            'Legal': ['DIR_LEGAL_001'],
            'Auditoría': ['AUD_INT_001', 'AUD_EXT_001'],
            'Seguridad': ['SEC_ANALYST_001', 'SEC_ADMIN_001']
        }
        
        # Combobox para departamento
        ttk.Label(user_frame, text="Departamento:").pack(anchor=tk.W)
        dept_var = tk.StringVar()
        dept_combo = ttk.Combobox(user_frame, textvariable=dept_var, 
                                 values=list(departments.keys()), state='readonly')
        dept_combo.pack(fill=tk.X, pady=(0, 10))
        dept_combo.bind('<<ComboboxSelected>>', 
                       lambda e: self.update_user_list(dept_var.get(), user_combo, departments))
        
        # Combobox para usuario
        ttk.Label(user_frame, text="Usuario:").pack(anchor=tk.W)
        user_combo = ttk.Combobox(user_frame, textvariable=self.current_user, state='readonly')
        user_combo.pack(fill=tk.X, pady=(0, 10))
        user_combo.bind('<<ComboboxSelected>>', lambda e: self.update_user_info())
        
        # Información del usuario
        user_info_frame = ttk.LabelFrame(left_panel, text="Información del Usuario", padding=10)
        user_info_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(user_info_frame, text="Departamento:").pack(anchor=tk.W)
        ttk.Label(user_info_frame, textvariable=self.current_department, 
                 font=('Arial', 10, 'bold')).pack(anchor=tk.W)
        
        ttk.Label(user_info_frame, text="Nivel de Seguridad:").pack(anchor=tk.W, pady=(10, 0))
        ttk.Label(user_info_frame, textvariable=self.security_level, 
                 font=('Arial', 10, 'bold')).pack(anchor=tk.W)
        
        # ========================================
        # PANEL DERECHO - Operaciones
        # ========================================
        right_panel = ttk.Frame(main_frame)
        right_panel.grid(row=1, column=1, sticky="nsew")
        right_panel.columnconfigure(0, weight=1)
        right_panel.rowconfigure(1, weight=1)
        
        # Panel de operaciones
        operations_frame = ttk.LabelFrame(right_panel, text="🔐 OPERACIONES DE CIFRADO", padding=10)
        operations_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        
        # Tipo de documento
        doc_frame = ttk.Frame(operations_frame)
        doc_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(doc_frame, text="Tipo de Documento:").pack(side=tk.LEFT)
        self.doc_type = tk.StringVar(value="reportes_financieros")
        doc_combo = ttk.Combobox(doc_frame, textvariable=self.doc_type, 
                                values=['reportes_financieros', 'datos_clientes', 'contratos', 'documentos_estrategicos'],
                                state='readonly', width=20)
        doc_combo.pack(side=tk.LEFT, padx=(10, 0))
        
        # Contenido del documento
        content_frame = ttk.Frame(operations_frame)
        content_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(content_frame, text="Contenido:").pack(anchor=tk.W)
        self.content_text = scrolledtext.ScrolledText(content_frame, height=4, width=50)
        self.content_text.pack(fill=tk.X, pady=(0, 10))
        
        # Botones de operación
        button_frame = ttk.Frame(operations_frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(button_frame, text="🔒 CIFRAR", 
                  command=self.encrypt_document).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="🔓 DESCIFRAR", 
                  command=self.decrypt_document).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="📋 VER DOCUMENTOS", 
                  command=self.show_documents).pack(side=tk.LEFT)
        
        # ========================================
        # PANEL INFERIOR - Logs y Auditoría
        # ========================================
        logs_frame = ttk.LabelFrame(right_panel, text="📊 LOGS DE AUDITORÍA ISO 27001", padding=10)
        logs_frame.grid(row=1, column=0, sticky="nsew", pady=(10, 0))
        
        # Logs en tiempo real
        self.logs_text = scrolledtext.ScrolledText(logs_frame, height=15, width=80)
        self.logs_text.pack(fill=tk.BOTH, expand=True)
        
        # Botones de control
        control_frame = ttk.Frame(logs_frame)
        control_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(control_frame, text="🔄 ACTUALIZAR LOGS", 
                  command=self.update_logs).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(control_frame, text="📊 REPORTE CUMPLIMIENTO", 
                  command=self.show_compliance_report).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(control_frame, text="🧪 SIMULAR INCIDENTE", 
                  command=self.simulate_incident).pack(side=tk.LEFT)
        
        # Inicializar con primer departamento
        if departments:
            first_dept = list(departments.keys())[0]
            dept_combo.set(first_dept)
            self.update_user_list(first_dept, user_combo, departments)
    
    def update_user_list(self, department, user_combo, departments):
        """Actualizar lista de usuarios según departamento"""
        if department in departments:
            users = departments[department]
            user_combo['values'] = users
            if users:
                user_combo.set(users[0])
                self.update_user_info()
    
    def update_user_info(self):
        """Actualizar información del usuario seleccionado"""
        user_id = self.current_user.get()
        if user_id:
            # Simular información del usuario
            user_info = {
                'CEO_001': {'dept': 'Executive', 'level': 'TOP_SECRET'},
                'CFO_001': {'dept': 'Finance', 'level': 'CONFIDENTIAL'},
                'CTO_001': {'dept': 'Technology', 'level': 'TOP_SECRET'},
                'CISO_001': {'dept': 'Information Security', 'level': 'TOP_SECRET'},
                'DIR_FIN_001': {'dept': 'Finance', 'level': 'CONFIDENTIAL'},
                'DIR_IT_001': {'dept': 'Information Technology', 'level': 'SECRET'},
                'DIR_SALES_001': {'dept': 'Sales', 'level': 'CONFIDENTIAL'},
                'DIR_LEGAL_001': {'dept': 'Legal', 'level': 'SECRET'},
                'AUD_INT_001': {'dept': 'Internal Audit', 'level': 'CONFIDENTIAL'},
                'AUD_EXT_001': {'dept': 'External Audit', 'level': 'CONFIDENTIAL'},
            }
            
            info = user_info.get(user_id, {'dept': 'Unknown', 'level': 'UNKNOWN'})
            self.current_department.set(info['dept'])
            self.security_level.set(info['level'])
    
    def log_event(self, message, level='INFO'):
        """Agregar evento al log"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        user = self.current_user.get() or 'SYSTEM'
        
        # Colores según nivel
        colors = {
            'INFO': 'black',
            'SUCCESS': 'green',
            'WARNING': 'orange',
            'ERROR': 'red'
        }
        
        log_entry = f"[{timestamp}] {user}: {message}\n"
        
        self.logs_text.insert(tk.END, log_entry)
        self.logs_text.see(tk.END)
        
        # Aplicar color
        start = self.logs_text.index("end-2c linestart")
        end = self.logs_text.index("end-1c")
        self.logs_text.tag_add(level, start, end)
        self.logs_text.tag_config(level, foreground=colors.get(level, 'black'))
        
        # También registrar en el sistema de cumplimiento
        self.compliance.log_security_event(level, f"{user}: {message}")
    
    def encrypt_document(self):
        """Cifrar documento"""
        user_id = self.current_user.get()
        if not user_id:
            messagebox.showerror("Error", "Debe seleccionar un usuario")
            return
        
        content = self.content_text.get("1.0", tk.END).strip()
        if not content:
            messagebox.showerror("Error", "Debe ingresar contenido para cifrar")
            return
        
        doc_type = self.doc_type.get()
        
        try:
            # Depuración: mostrar valores enviados a access_control
            print(f"DEBUG: user_id={user_id}, doc_type={doc_type}, action='encrypt'")
            # Verificar permisos
            if not self.compliance.access_control(user_id, doc_type, 'encrypt'):
                self.log_event("Acceso denegado para cifrado", 'ERROR')
                messagebox.showerror("Acceso Denegado", 
                                   f"El usuario {user_id} no tiene permisos para cifrar {doc_type}")
                return
            
            # Cifrar documento
            self.log_event(f"Iniciando cifrado de {doc_type}", 'INFO')
            
            # Generar clave basada en usuario y tipo de documento
            key = f"{user_id}_{doc_type}_2024!"
            
            cifrado, metadatos = cifrar_pipeline(
                content,
                key,
                user_id,
                contenedor_png=True,
                ruta_png=f'{doc_type}_{user_id}.png',
                doc_type=doc_type
            )
            
            # Guardar en datos empresariales
            doc_id = f"{doc_type.upper()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            self.enterprise_data[doc_type].append({
                'id': doc_id,
                'encrypted_data': cifrado,
                'metadata': metadatos,
                'created_by': user_id,
                'created_at': datetime.now().isoformat(),
                'original_size': len(content),
                'encrypted_size': len(cifrado)
            })
            
            self.log_event(f"Documento cifrado exitosamente - ID: {doc_id}", 'SUCCESS')
            self.log_event(f"Archivo PNG generado: {doc_type}_{user_id}.png", 'INFO')
            
            # Limpiar contenido
            self.content_text.delete("1.0", tk.END)
            
            messagebox.showinfo("Éxito", 
                              f"Documento cifrado exitosamente\nID: {doc_id}\nArchivo PNG generado")
            
        except Exception as e:
            self.log_event(f"Error en cifrado: {str(e)}", 'ERROR')
            messagebox.showerror("Error", f"Error al cifrar: {str(e)}")
    
    def decrypt_document(self):
        """Descifrar documento"""
        user_id = self.current_user.get()
        if not user_id:
            messagebox.showerror("Error", "Debe seleccionar un usuario")
            return
        
        doc_type = self.doc_type.get()
        
        # Mostrar documentos disponibles
        if not self.enterprise_data[doc_type]:
            messagebox.showinfo("Info", f"No hay documentos cifrados de tipo {doc_type}")
            return
        
        # Crear ventana de selección
        dialog = tk.Toplevel(self.root)
        dialog.title("Seleccionar Documento para Descifrar")
        dialog.geometry("600x400")
        
        # Lista de documentos
        ttk.Label(dialog, text="Documentos disponibles:", 
                 font=('Arial', 12, 'bold')).pack(pady=10)
        
        # Treeview para documentos
        columns = ('ID', 'Creado por', 'Fecha', 'Tamaño')
        tree = ttk.Treeview(dialog, columns=columns, show='headings', height=10)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Llenar datos
        for doc in self.enterprise_data[doc_type]:
            tree.insert('', tk.END, values=(
                doc['id'],
                doc['created_by'],
                doc['created_at'][:19],
                f"{doc['encrypted_size']} bytes"
            ))
        
        def decrypt_selected():
            selection = tree.selection()
            if not selection:
                messagebox.showwarning("Advertencia", "Debe seleccionar un documento")
                return
            
            item = tree.item(selection[0])
            doc_id = item['values'][0]
            
            # Encontrar documento
            doc = next((d for d in self.enterprise_data[doc_type] if d['id'] == doc_id), None)
            if not doc:
                messagebox.showerror("Error", "Documento no encontrado")
                return
            
            try:
                # Verificar permisos
                if not self.compliance.access_control(user_id, doc_type, 'decrypt'):
                    self.log_event("Acceso denegado para descifrado", 'ERROR')
                    messagebox.showerror("Acceso Denegado", 
                                       f"El usuario {user_id} no tiene permisos para descifrar")
                    return
                
                # Descifrar
                self.log_event(f"Iniciando descifrado de {doc_id}", 'INFO')
                
                key = f"{doc['created_by']}_{doc_type}_2024!"
                
                contenido_descifrado = descifrar_pipeline(
                    doc['encrypted_data'],
                    key,
                    user_id,
                    doc['metadata'],
                    doc_type=doc_type
                )
                
                self.log_event(f"Documento descifrado exitosamente - ID: {doc_id}", 'SUCCESS')
                
                # Mostrar contenido
                content_window = tk.Toplevel(self.root)
                content_window.title(f"Contenido Descifrado - {doc_id}")
                content_window.geometry("800x600")
                
                ttk.Label(content_window, text="Contenido Descifrado:", 
                         font=('Arial', 12, 'bold')).pack(pady=10)
                
                content_text = scrolledtext.ScrolledText(content_window, height=25, width=80)
                content_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
                content_text.insert("1.0", contenido_descifrado)
                
                dialog.destroy()
                
            except Exception as e:
                self.log_event(f"Error en descifrado: {str(e)}", 'ERROR')
                messagebox.showerror("Error", f"Error al descifrar: {str(e)}")
        
        # Botones
        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(button_frame, text="🔓 DESCIFRAR", 
                  command=decrypt_selected).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="❌ CANCELAR", 
                  command=dialog.destroy).pack(side=tk.LEFT)
    
    def show_documents(self):
        """Mostrar todos los documentos"""
        dialog = tk.Toplevel(self.root)
        dialog.title("📋 Inventario de Documentos Empresariales")
        dialog.geometry("1000x600")
        
        # Notebook para diferentes tipos
        notebook = ttk.Notebook(dialog)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        for doc_type in self.enterprise_data.keys():
            frame = ttk.Frame(notebook)
            notebook.add(frame, text=doc_type.replace('_', ' ').title())
            
            # Treeview para documentos
            columns = ('ID', 'Creado por', 'Fecha', 'Tamaño Original', 'Tamaño Cifrado')
            tree = ttk.Treeview(frame, columns=columns, show='headings', height=15)
            
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=150)
            
            tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # Llenar datos
            for doc in self.enterprise_data[doc_type]:
                tree.insert('', tk.END, values=(
                    doc['id'],
                    doc['created_by'],
                    doc['created_at'][:19],
                    f"{doc['original_size']} bytes",
                    f"{doc['encrypted_size']} bytes"
                ))
    
    def update_logs(self):
        """Actualizar logs desde el sistema de cumplimiento"""
        self.logs_text.delete("1.0", tk.END)
        
        # Mostrar últimos 50 eventos
        events = self.compliance.security_events[-50:]
        
        for event in events:
            timestamp = event['timestamp'][11:19]  # Solo hora
            level = event['severity']
            description = event['description']
            
            self.logs_text.insert(tk.END, f"[{timestamp}] {description}\n")
            
            # Aplicar color
            start = self.logs_text.index("end-2c linestart")
            end = self.logs_text.index("end-1c")
            self.logs_text.tag_add(level, start, end)
            
            colors = {
                'INFO': 'black',
                'SUCCESS': 'green',
                'WARNING': 'orange',
                'ERROR': 'red'
            }
            self.logs_text.tag_config(level, foreground=colors.get(level, 'black'))
        
        self.logs_text.see(tk.END)
    
    def show_compliance_report(self):
        """Mostrar reporte de cumplimiento"""
        report = self.compliance.compliance_report()
        
        dialog = tk.Toplevel(self.root)
        dialog.title("📊 Reporte de Cumplimiento ISO 27001")
        dialog.geometry("800x600")
        
        # Contenido del reporte
        content = f"""
🏢 REPORTE DE CUMPLIMIENTO ISO 27001
{'='*50}

📅 Fecha del Reporte: {report['timestamp']}
📊 Eventos de Seguridad: {report['security_events_count']}
📋 Entradas de Auditoría: {report['audit_entries_count']}
⚠️  Evaluaciones de Riesgo: {report['risk_assessment_count']}

🏆 Estado de Cumplimiento: {report['compliance_status']}

📅 Última Auditoría: {report['last_audit']}
📅 Próxima Auditoría: {report['next_audit']}

🔐 CONTROLES IMPLEMENTADOS:
✅ A.9.1.1 - Control de acceso
✅ A.9.2.1 - Gestión de usuarios  
✅ A.10.1.1 - Controles criptográficos
✅ A.12.4.1 - Logging de eventos
✅ A.13.1.1 - Gestión de incidentes
✅ A.15.1.1 - Cumplimiento legal

📈 MÉTRICAS DE SEGURIDAD:
• Usuarios activos: {len(self.enterprise_data['financial_reports']) + len(self.enterprise_data['customer_data']) + len(self.enterprise_data['contracts'])}
• Documentos cifrados: {sum(len(docs) for docs in self.enterprise_data.values())}
• Eventos de seguridad: {report['security_events_count']}
• Tasa de cumplimiento: 100%
        """
        
        text_widget = scrolledtext.ScrolledText(dialog, height=30, width=80)
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        text_widget.insert("1.0", content)
    
    def simulate_incident(self):
        """Simular incidente de seguridad"""
        user_id = self.current_user.get() or 'HACKER_001'
        
        # Crear incidente
        incident = self.compliance.incident_response(
            'UNAUTHORIZED_ACCESS_ATTEMPT',
            f'Intento de acceso no autorizado por {user_id}'
        )
        
        self.log_event(f"🚨 INCIDENTE DETECTADO - ID: {incident['id']}", 'WARNING')
        self.log_event(f"Tipo: {incident['type']}", 'WARNING')
        self.log_event(f"Descripción: {incident['description']}", 'WARNING')
        self.log_event(f"Severidad: {incident['severity']}", 'WARNING')
        self.log_event(f"Asignado a: {incident['assigned_to']}", 'WARNING')
        
        messagebox.showwarning("🚨 Incidente de Seguridad", 
                              f"Se ha detectado un incidente de seguridad:\n\n"
                              f"ID: {incident['id']}\n"
                              f"Tipo: {incident['type']}\n"
                              f"Descripción: {incident['description']}\n"
                              f"Severidad: {incident['severity']}")
    
    def run(self):
        """Ejecutar la aplicación"""
        # Log inicial
        self.log_event("Sistema HydraSecure Enterprise iniciado", 'SUCCESS')
        self.log_event("Cumplimiento ISO 27001 verificado", 'SUCCESS')
        self.log_event("Todos los controles de seguridad activos", 'SUCCESS')
        
        # Iniciar loop principal
        self.root.mainloop()

def main():
    """Función principal"""
    app = DemoEmpresarialVisual()
    app.run()

if __name__ == "__main__":
    main() 
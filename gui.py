import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import uuid
from hydra_secure.pipeline import cifrar_pipeline, descifrar_pipeline

class PipelineLogger:
    def __init__(self, text_widget):
        self.text_widget = text_widget
        self.clear()
    def log(self, title, value):
        self.text_widget.insert(tk.END, f"\n--- {title} ---\n{value}\n")
        self.text_widget.see(tk.END)
    def clear(self):
        self.text_widget.delete(1.0, tk.END)

class ChatApp:
    def __init__(self, root):
        self.root = root
        root.title("HydraSecure Chat Demo")
        # Genera IDs de usuario automáticos
        self.user1_id = str(uuid.uuid4())[:8]
        self.user2_id = str(uuid.uuid4())[:8]
        # Frame principal
        main_frame = tk.Frame(root)
        main_frame.pack(fill="both", expand=True)
        # Usuario 1 (izquierda)
        left = tk.Frame(main_frame)
        left.grid(row=0, column=0, sticky="nsew")
        tk.Label(left, text=f"Usuario 1 (emisor) [{self.user1_id}]").pack()
        self.mensaje1 = tk.Text(left, height=3, width=40)
        self.mensaje1.pack()
        tk.Label(left, text="Clave:").pack(anchor="w")
        self.clave1 = tk.Entry(left, width=30, show="*")
        self.clave1.pack()
        tk.Button(left, text="Enviar mensaje cifrado", command=self.cifrar_enviar).pack(pady=5)
        tk.Label(left, text="Historial y paso a paso (emisor):").pack(anchor="w")
        self.log1 = tk.Text(left, height=18, width=50, bg="#f0f0f0")
        self.log1.pack()
        self.logger1 = PipelineLogger(self.log1)
        # Imagen PNG (centro)
        center = tk.Frame(main_frame)
        center.grid(row=0, column=1, sticky="nsew")
        tk.Label(center, text="Imagen PNG generada y enviada").pack()
        self.img_label = tk.Label(center)
        self.img_label.pack(padx=10, pady=10)
        # Usuario 2 (derecha)
        right = tk.Frame(main_frame)
        right.grid(row=0, column=2, sticky="nsew")
        tk.Label(right, text=f"Usuario 2 (receptor) [{self.user2_id}]").pack()
        tk.Label(right, text="Clave:").pack(anchor="w")
        self.clave2 = tk.Entry(right, width=30, show="*")
        self.clave2.pack()
        tk.Button(right, text="Descifrar mensaje recibido", command=self.descifrar_recibido).pack(pady=5)
        tk.Label(right, text="Historial y paso a paso (receptor):").pack(anchor="w")
        self.log2 = tk.Text(right, height=18, width=50, bg="#f0f0f0")
        self.log2.pack()
        self.logger2 = PipelineLogger(self.log2)
        # Estado
        self.historial = []  # [(mensaje, metadatos, ruta_png)]
        self.metadatos = None
        self.cifrado_actual = None
        self._img_ref = None
        # Layout expandible
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.columnconfigure(2, weight=1)

    def cifrar_enviar(self):
        mensaje = self.mensaje1.get("1.0", tk.END).strip()
        clave = self.clave1.get().strip()
        usuario = self.user1_id
        ruta_png = f"mensaje_{len(self.historial)+1}.png"
        if not mensaje or not clave:
            messagebox.showerror("Error", "Debes ingresar un mensaje y una clave.")
            return
        try:
            self.logger1.clear()
            self.logger1.log("Mensaje original", mensaje)
            cifrado, metadatos = cifrar_pipeline(mensaje, clave, usuario, contenedor_png=True, ruta_png=ruta_png)
            self.metadatos = metadatos
            self.cifrado_actual = cifrado
            self.historial.append((mensaje, metadatos, ruta_png))
            img = Image.open(ruta_png)
            img = img.resize((400, 400))
            img_tk = ImageTk.PhotoImage(img)
            self.img_label.configure(image=img_tk)
            self._img_ref = img_tk
            self.logger1.log("MENSAJE ENVIADO", f"Imagen: {ruta_png}")
            self.logger1.log("Metadatos", str(metadatos))
        except Exception as e:
            messagebox.showerror("Error al cifrar/enviar", str(e))

    def descifrar_recibido(self):
        clave = self.clave2.get().strip()
        usuario = self.user2_id
        if not self.cifrado_actual or not self.metadatos:
            messagebox.showerror("Error", "Primero recibe un mensaje.")
            return
        try:
            self.logger2.clear()
            resultado = descifrar_pipeline(self.cifrado_actual, clave, usuario, self.metadatos)
            self.logger2.log("MENSAJE DESCIFRADO", resultado)
            messagebox.showinfo("Descifrado exitoso", f"Mensaje descifrado: {resultado}")
        except Exception as e:
            self.logger2.clear()
            self.logger2.log("ERROR", f"Descifrado fallido: {str(e)}")
            messagebox.showerror("Error al descifrar", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop() 
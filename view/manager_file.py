import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import os
import PyPDF2

class ExploradorArchivos(tk.Toplevel):
    def __init__(self, top=None):
        self.top = top
        self.top.title("Explorador de Archivos")
        self.tree = ttk.Treeview(self.top)
        self.tree.pack(expand=True, fill="both")
        self.tree.heading("#0", text="Directorio", anchor=tk.W)
        self.tree.bind("<ButtonRelease-1>", self.mostrar_archivo)  # Cambio a ButtonRelease-1

        self.directorio_actual = os.path.join(os.getcwd(), "voucher")
        print("Directorio actual:", self.directorio_actual)  # Debugging
        self.mostrar_directorio(self.directorio_actual)

        self.txt_contenido = scrolledtext.ScrolledText(self.top, wrap=tk.WORD)
        self.txt_contenido.pack(expand=True, fill="both")

        # Botón para eliminar archivo
        self.button_eliminar_archivo = ttk.Button(self.top, text="Eliminar", style="danger-outline.TButton", command=self.eliminar_archivo)
        self.button_eliminar_archivo.pack(pady=5)
        self.button_eliminar_archivo.configure(cursor="hand2")

        # Variable de instancia para almacenar la ruta del archivo seleccionado
        self.ruta_seleccionada = None

    def mostrar_directorio(self, directorio):
        print("Mostrando directorio:", directorio)  # Debugging
        self.tree.delete(*self.tree.get_children())
        try:
            archivos = os.listdir(directorio)
            for archivo in archivos:
                ruta_completa = os.path.join(directorio, archivo)
                print("Archivo encontrado:", ruta_completa)  # Debugging
                es_directorio = os.path.isdir(ruta_completa)
                if es_directorio:
                    self.tree.insert("", "end", text=archivo, values=(ruta_completa,), open=False, tags=("directorio",))
                else:
                    self.tree.insert("", "end", text=archivo, values=(ruta_completa,), open=False, tags=("archivo",))
        except Exception as e:
            print("Error al listar archivos:", e)  # Debugging

    def mostrar_archivo(self, event):  # Nueva función para mostrar el archivo al hacer clic
        item_seleccionado = self.tree.selection()
        if item_seleccionado:
            item = self.tree.item(item_seleccionado)
            self.ruta_seleccionada = item["values"][0]
            ruta = self.ruta_seleccionada
            print("Archivo seleccionado:", ruta)  # Debugging
            if os.path.isfile(ruta):
                _, extension = os.path.splitext(ruta)
                if extension.lower() == ".pdf":
                    contenido = self.leer_pdf(ruta)
                    self.txt_contenido.delete('1.0', tk.END)
                    self.txt_contenido.insert(tk.END, contenido)
                else:
                    with open(ruta, "r", encoding="utf-8") as archivo:
                        contenido = archivo.read()
                        self.txt_contenido.delete('1.0', tk.END)
                        self.txt_contenido.insert(tk.END, contenido)

    def leer_pdf(self, ruta):
        contenido = ""
        with open(ruta, "rb") as archivo:
            lector_pdf = PyPDF2.PdfReader(archivo)
            for pagina in range(len(lector_pdf.pages)):
                contenido += lector_pdf.pages[pagina].extract_text()
        return contenido

    def abrir_carpeta(self):
        # Abre el explorador de archivos y obtiene la carpeta seleccionada por el usuario
        directorio_carpeta = filedialog.askdirectory()
        if directorio_carpeta:
            self.directorio_actual = directorio_carpeta
            self.mostrar_directorio(self.directorio_actual)

    def eliminar_archivo(self):
        if self.ruta_seleccionada:
            confirmacion = messagebox.askquestion("Confirmar Eliminación", "¿Estás seguro de que deseas eliminar este archivo?")
            if confirmacion == "yes":
                try:
                    os.remove(self.ruta_seleccionada)
                    print("Archivo eliminado:", self.ruta_seleccionada)
                    # Actualizar el árbol de archivos
                    self.mostrar_directorio(self.directorio_actual)
                except Exception as e:
                    print("Error al eliminar el archivo:", e)

# Ejemplo de uso
if __name__ == "__main__":
    app = tk.Tk()
    explorador = ExploradorArchivos(app)
    app.mainloop()

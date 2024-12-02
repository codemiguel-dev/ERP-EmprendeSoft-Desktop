import tkinter as tk
from tkinter import ttk
from openpyxl import Workbook
from tkinter import messagebox

def export_to_excel():
    # Crear un nuevo libro de trabajo de Excel
    wb = Workbook()
    # Seleccionar la hoja activa
    ws = wb.active
    
    # Encabezados de las columnas
    headers = ["Nombre", "Edad", "Email"]
    # Escribir los encabezados en la primera fila de la hoja de Excel
    ws.append(headers)
    
    # Obtener los datos de la tabla o de donde los tengas
    data = [
        ["Juan", 30, "juan@example.com"],
        ["María", 25, "maria@example.com"],
        ["Pedro", 40, "pedro@example.com"]
    ]
    
    # Escribir los datos en las filas siguientes
    for row in data:
        ws.append(row)
    
    try:
        # Guardar el libro de trabajo como un archivo Excel
        wb.save("datos.xlsx")
        messagebox.showinfo("Exportar a Excel", "Los datos se han exportado exitosamente a datos.xlsx")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo exportar a Excel: {str(e)}")

# Crear la ventana principal
root = tk.Tk()
root.title("Exportar a Excel")

# Botón para exportar a Excel
export_button = ttk.Button(root, text="Exportar a Excel", command=export_to_excel)
export_button.pack(pady=10)

# Iniciar el bucle principal de la aplicación
root.mainloop()

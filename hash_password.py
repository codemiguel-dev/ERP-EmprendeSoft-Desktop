import tkinter as tk
from tkinter import messagebox
from passlib.hash import bcrypt

def check_password():
    # Obtener la contraseña ingresada por el usuario
    password = password_entry.get()
    
    # Hash de la contraseña almacenada en la base de datos (simulado)
    stored_password_hash = "$2a$12$7CN6GewkAC/xhEapCyXVW.HLIMK6yG1ncioD/LPCZ16Q1B2BGAHwO"
    
    # Verificar si la contraseña ingresada coincide con el hash almacenado
    if bcrypt.verify(password, stored_password_hash):
        messagebox.showinfo("Inicio de sesión exitoso", "¡Bienvenido!")
    else:
        messagebox.showerror("Error", "Contraseña incorrecta")

# Crear la ventana principal
root = tk.Tk()
root.title("Inicio de sesión")

# Crear una entrada de contraseña
password_label = tk.Label(root, text="Contraseña:")
password_label.pack()
password_entry = tk.Entry(root, show="*")
password_entry.pack()

# Botón para iniciar sesión
login_button = tk.Button(root, text="Iniciar sesión", command=check_password)
login_button.pack()

# Iniciar el bucle principal de la aplicación
root.mainloop()

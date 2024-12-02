#==================imports===================
import sqlite3
import webbrowser
import re
from manager_file_emp import ExploradorArchivos
import os
#bliblioteca para persistencia del tema del software
import configparser
#herramienta para almacenar y iniciar sesión con hash de contraseña
import bcrypt
from passlib.hash import bcrypt
import random
import string
from ttkbootstrap import Style
from tkinter import *
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from time import strftime
from datetime import date
from tkinter import scrolledtext as tkst
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from fpdf import FPDF
from PIL import Image, ImageTk
from conexion import connect_to_database

#============================================

root = Tk()

root.geometry("1366x768")
root.title("Retail Manager")

user = StringVar()
passwd = StringVar()
fname = StringVar()
lname = StringVar()
new_user = StringVar()
new_passwd = StringVar()


cust_name = StringVar()
cust_num = StringVar()
cust_new_bill = StringVar()
cust_search_bill = StringVar()
bill_date = StringVar()

with connect_to_database() as db:
    cur = db.cursor()

def random_bill_number(stringLength):
    lettersAndDigits = string.ascii_letters.upper() + string.digits
    strr=''.join(random.choice(lettersAndDigits) for i in range(stringLength-2))
    return ('BB'+strr)


def valid_phone(phn):
    if re.match(r"[789]\d{9}$", phn):
        return True
    return False


def login(Event=None):
    global username
    username = user.get()
    password = passwd.get()

    with sqlite3.connect("./database/store.db") as db:
        cur = db.cursor()
    find_user = "SELECT * FROM employee WHERE name = ?"
    cur.execute(find_user, [username])
    user_data = cur.fetchone()    
    if user_data:
        # Obtenemos el hash de la contraseña almacenada en la base de datos
        stored_password_hash = user_data[5]  # Suponiendo que el hash está en la sexta columna
        # Verificamos si la contraseña ingresada coincide con el hash almacenado
        if bcrypt.verify(password, stored_password_hash):
            messagebox.showinfo("Iniciar Sesión", f"Usuario {username} inició sesión")
            page1.entry1.delete(0, END)
            page1.entry2.delete(0, END)
            root.withdraw()
            global biller
            global page2
            biller = Toplevel()
            page2 = bill_window(biller)
            page2.time()
            biller.protocol("WM_DELETE_WINDOW", exitt)
            biller.mainloop()
        else:
            messagebox.showerror("Error", "Contraseña incorrecta.")
            passwd.delete(0, END)  # Limpiar el campo de contraseña

    else:
        messagebox.showerror("Error", "Cuenta incorrecta")
        page1.entry2.delete(0, END)



def logout():
    sure = messagebox.askyesno("Salir", "¿Quiere salir?", parent=biller)
    if sure == True:
        biller.destroy()
        root.deiconify()
        page1.entry1.delete(0, END)
        page1.entry2.delete(0, END)

class login_page:
    def __init__(self, top=None):
        self.top = top
        self.top.geometry("800x500")
        self.top.resizable(0, 0)
        self.top.title("EmprendeSoft - Iniciar Sesión - Empleado")
        self.top.iconbitmap("img/icon.ico") 

        # frame_logo
        frame_logo = tk.Frame(
            self.top, bd=0, width=300, relief=tk.SOLID, padx=10, pady=10, bg="#BB2B2B"
        )
        frame_logo.pack(side="left", expand=tk.YES, fill=tk.BOTH)
        self.label_logo = tk.Label(frame_logo, bg="#BB2B2B")
        self.label_logo.place(x=0, y=0, relwidth=1, relheight=1)
        self.cargar_logo_guardado()
        icono = tk.PhotoImage(file="img/perfil_git.gif")
        self.top.iconphoto(True, icono)
        #self.center_window()
 
        # frame_form
        frame_form = tk.Frame(top, bd=0, relief=tk.SOLID, bg="#fcfcfc")
        frame_form.pack(side="right", expand=tk.YES, fill=tk.BOTH)
        # frame_form

        # frame_form_top
        frame_form_top = tk.Frame(
            frame_form, height=50, bd=0, relief=tk.SOLID, bg="black"
        )
        frame_form_top.pack(side="top", fill=tk.X)
        title = tk.Label(
            frame_form_top,
            text="Iniciar Sesión",
            font=("Times", 30),
            fg="#666a88",
            bg="#fcfcfc",
            pady=50,
        )
        title.pack(expand=tk.YES, fill=tk.BOTH)
        # end frame_form_top

        # frame_form_fill
        frame_form_fill = tk.Frame(
            frame_form, height=50, bd=0, relief=tk.SOLID, bg="#fcfcfc"
        )
        frame_form_fill.pack(side="bottom", expand=tk.YES, fill=tk.BOTH)

        # Etiqueta para usuario
        self.user_label = Label(
            root, text="Usuario", font=("Times", 15), foreground="#000000"
        )
        self.user_label.place(relx=0.6, rely=0.30)

        self.entry1 = Entry(root)
        self.entry1.place(relx=0.6, rely=0.35, width=300, height=24)
        self.entry1.configure(font="-family {Poppins} -size 10")
        self.entry1.configure(textvariable=user)

        # Etiqueta para contraseña
        self.user_label = Label(
            root, text="Contraseña", font=("Times", 15), foreground="#000000"
        )
        self.user_label.place(relx=0.6, rely=0.45)

        self.entry2 = Entry(root)
        self.entry2.place(relx=0.6, rely=0.50, width=300, height=24)
        self.entry2.configure(font="-family {Poppins} -size 10")
        self.entry2.configure(show="*")
        self.entry2.configure(textvariable=passwd)

        # Cargar el icono
        self.icono_login = Image.open("img/icon.ico")
        self.icono_login = self.icono_login.resize((32, 32), Image.LANCZOS)  # Utiliza LANCZOS en lugar de ANTIALIAS
        self.icono_login = ImageTk.PhotoImage(self.icono_login)
        top.iconphoto(True, self.icono_login)

        self.button1 = Button(root)
        self.button1.place(relx=0.366, rely=0.685, width=356, height=43)
        self.button1.configure(relief="flat")
        self.button1.configure(overrelief="flat")
        self.button1.configure(activebackground="#D2463E")
        self.button1.configure(cursor="hand2")
        self.button1.configure(foreground="#ffffff")
        self.button1.configure(background="#D2463E")
        self.button1.configure(font="-family {Poppins SemiBold} -size 20")
        self.button1.configure(borderwidth="0")
        self.button1.configure(text="""Iniciar Sesión""")
        self.button1.configure(command=login)

    def guardar_ruta_logo(self, ruta_logo):
        with open("config.txt", "w") as f:
            f.write(ruta_logo)

    def cargar_logo_guardado(self):
        if os.path.exists("config.txt"):
            with open("config.txt", "r") as f:
                ruta_logo = f.read()
                if os.path.exists(ruta_logo):
                    self.cargar_logo(ruta_logo)

    def cargar_logo(self, ruta_logo):
        imagen = Image.open(ruta_logo)
        imagen = imagen.resize((150, 150), resample=Image.LANCZOS)
        foto = ImageTk.PhotoImage(imagen)
        self.label_logo.config(image=foto)
        self.label_logo.image = foto

class Item:
    def __init__(self, name, price, qty):
        self.product_name = name
        self.price = price
        self.qty = qty

class Cart:
    def __init__(self):
        self.items = []
        self.dictionary = {}

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self):
        self.items.pop()

    def remove_items(self):
        self.items.clear()

    def total(self):
        total = 0.0
        for i in self.items:
            total += i.price * i.qty
        return total

    def isEmpty(self):
        if len(self.items)==0:
            return True
        
    def allCart(self):
        for i in self.items:
            if (i.product_name in self.dictionary):
                self.dictionary[i.product_name] += i.qty
            else:
                self.dictionary.update({i.product_name:i.qty})
    
def exitt():
    sure = messagebox.askyesno("Salir","¿Desea salir?", parent=biller)
    if sure == True:
        biller.destroy()
        root.destroy()

class bill_window:
    def __init__(self, top=None):
        # Función para cambiar el tema
        def change_theme(theme_name):
            # Guardar el tema seleccionado en el archivo de configuración
            config = configparser.ConfigParser()
            config['Theme'] = {'name': theme_name}

            with open('config.ini', 'w') as configfile:
                config.write(configfile)

            # Aplicar el nuevo tema
            Style(theme=theme_name)

        # Función para abrir el archivo de ayuda en PDF
        def open_help(file_path):
            # Abre el archivo PDF en el navegador predeterminado
            webbrowser.open(file_path)

        # Leer la configuración actual del archivo de configuración
        def read_theme_config():
            config = configparser.ConfigParser()
            config.read('config.ini')
            theme_name = config.get('Theme', 'name', fallback='default_theme')
            return theme_name
        # Agregar opciones de temas al menú
        self.menu_bar = Menu(top)
        top.config(menu=self.menu_bar)

        theme_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Configuración de Temas", menu=theme_menu)

        theme_menu.add_command(label="--Temas Claros--")
        theme_menu.add_command(label="Cerculean", command=lambda: change_theme("cerculean"))
        theme_menu.add_command(label="Simplex", command=lambda: change_theme("simplex"))
        theme_menu.add_command(label="Morph", command=lambda: change_theme("morph"))
        theme_menu.add_command(label="Yeti", command=lambda: change_theme("yeti"))
        theme_menu.add_command(label="United", command=lambda: change_theme("united"))
        theme_menu.add_command(label="Sandstone", command=lambda: change_theme("sandstone"))
        theme_menu.add_command(label="Pulse", command=lambda: change_theme("pulse"))
        theme_menu.add_command(label="Minty", command=lambda: change_theme("minty"))
        theme_menu.add_command(label="Lumen", command=lambda: change_theme("lumen"))
        theme_menu.add_command(label="Litera", command=lambda: change_theme("litera"))
        theme_menu.add_command(label="Journal", command=lambda: change_theme("journal"))
        theme_menu.add_command(label="Flatly", command=lambda: change_theme("flatly"))
        theme_menu.add_command(label="Cosmo", command=lambda: change_theme("cosmo"))
        theme_menu.add_command(label="--Temas Oscuros--")
        theme_menu.add_command(label="Solar", command=lambda: change_theme("solar"))
        theme_menu.add_command(label="Superhero", command=lambda: change_theme("superhero"))
        theme_menu.add_command(label="Oscuro", command=lambda: change_theme("darkly"))
        theme_menu.add_command(label="Cyborg", command=lambda: change_theme("cyborg"))
        theme_menu.add_command(label="Vapor", command=lambda: change_theme("vapor"))

        # Leer y aplicar el tema guardado previamente al iniciar la aplicación
        initial_theme = read_theme_config()
        change_theme(initial_theme)

        # Agregar menú de Ayuda con subcategorías
        help_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Ayuda", menu=help_menu)

        # Agregar opciones de ayuda con redirección a archivos PDF
        help_menu.add_command(label="Guía de Usuario", command=lambda: open_help("hoja.pdf"))
        help_menu.add_command(label="Manual del Administrador", command=lambda: open_help("ruta/al/manual_del_administrador.pdf"))

        top.geometry("1200x700")
        top.state('zoomed')
        top.title("Sistema de ventas")

        #self.label = Label(biller)
        #self.label.place(relx=0, rely=0, width=1366, height=768)
        #self.img = PhotoImage(file="./bill_window.png")
        #self.label.configure(image=self.img)

        self.message = Label(biller)
        self.message.place(relx=0.038, rely=0.055, width=136, height=30)
        self.message.configure(font="-family {Poppins} -size 10")
        self.message.configure(foreground="#fff")
        self.message.configure(text=username)
        self.message.configure(anchor="w")

        self.clock = Label(biller)
        self.clock.place(relx=0.9, rely=0.065, width=102, height=36)
        self.clock.configure(font="-family {Poppins Light} -size 12")
        self.clock.configure(foreground="#fff")

        # Etiqueta para boleta
        self.label_voucher = Label(
            top, text="Boleta de venta", font=("Times", 25), foreground="#fff"
        )
        self.label_voucher.place(relx=0.6, rely=0.150)

        # Etiqueta para boleta
        self.label_num_voucher = Label(
            top, text="N.", font=("Times", 13), foreground="#fff"
        )
        self.label_num_voucher.place(relx=0.450, rely=0.3)

        # Etiqueta para boleta
        self.label_name_voucher = Label(
            top, text="Nombre ", font=("Times", 13), foreground="#fff"
        )
        self.label_name_voucher.place(relx=0.450, rely=0.4)

        # Etiqueta para boleta
        self.label_phone_voucher = Label(
            top, text="Teléfono ", font=("Times", 13), foreground="#fff"
        )
        self.label_phone_voucher.place(relx=0.8, rely=0.3)

        # Etiqueta para boleta
        self.label_date_voucher = Label(
            top, text="Fecha ", font=("Times", 13), foreground="#fff"
        )
        self.label_date_voucher.place(relx=0.8, rely=0.4)

       # Etiqueta para nombre del cliente
        self.label_name_client = Label(
            top, text="Nombre del cliente", font=("Times", 15), foreground="#fff"
        )
        self.label_name_client.place(relx=0.035, rely=0.6)

        self.entry1 = ttk.Entry(top, style="info")
        self.entry1.place(relx=0.035, rely=0.650, width=240, height=24)
        self.entry1.configure(textvariable=cust_name)

        # Etiqueta para número de teléfono del cliente
        self.label_number = Label(
            top, text="Número de teléfono del cliente", font=("Times", 15), foreground="#fff"
        )
        self.label_number.place(relx=0.035, rely=0.7)

        self.entry2 = ttk.Entry(top, style="info")
        self.entry2.place(relx=0.035, rely=0.750, width=240, height=24)
        self.entry2.configure(textvariable=cust_num)

        self.button1 = ttk.Button(top, text="Cerrar Sesión", style="danger-outline.TButton", command=logout)
        self.button1.place(relx=0.035, rely=0.106, width=110, height=35)
        self.button1.configure(cursor="hand2")

        self.button_exportar_pdf = ttk.Button(top,text="Exportar a PDF", style="danger.TButton",command=self.exportar_a_pdf)
        self.button_exportar_pdf.place(relx=0.650, rely=0.750, width=120, height=40)
        self.button_exportar_pdf.configure(cursor="hand2")

        self.button3 = ttk.Button(top, text="Calcular Total", style="primary.TButton", command=self.total_bill)
        self.button3.place(relx=0.5, rely=0.885, width=110, height=30)
        self.button3.configure(cursor="hand2")

        self.button4 = ttk.Button(top, text="Ingresar Venta", style="info-outline.TButton", command=self.gen_bill)
        self.button4.place(relx=0.6, rely=0.885, width=110, height=30)
        self.button4.configure(cursor="hand2")

        self.button5 = ttk.Button(top, text="Limpiar Carro", style="warning-outline.TButton", command=self.clear_bill)
        self.button5.place(relx=0.7, rely=0.885, width=110, height=30)
        self.button5.configure(cursor="hand2")

        self.button6 = ttk.Button(top, text="Apagar", style="danger-outline.TButton", command=exitt)
        self.button6.place(relx=0.8, rely=0.885, width=110, height=30)
        self.button6.configure(cursor="hand2")

        self.button7 = ttk.Button(top, text="Agregar al carro", style="info-outline.TButton", command=self.add_to_cart)
        self.button7.place(relx=0.100, rely=0.885, width=110, height=30)
        self.button7.configure(cursor="hand2")

        self.button8 = ttk.Button(top, text="Limpiar Campos", style="warning-outline.TButton", command=self.clear_selection)
        self.button8.place(relx=0.200, rely=0.885, width=110, height=30)
        self.button8.configure(cursor="hand2")

        self.button9 = ttk.Button(top, text="Eliminar producto", style="danger-outline.TButton", command=self.remove_product)
        self.button9.place(relx=0.300, rely=0.885, width=150, height=30)
        self.button9.configure(cursor="hand2")

        self.button_boleta = ttk.Button(top,text="Ventas realizadas", style="danger.TButton",command=self.managervoucher)
        self.button_boleta.place(relx=0.400, rely=0.105, width=150, height=30)
        self.button_boleta.configure(cursor="hand2")

        # Etiqueta para nombre del producto
        self.label_category = Label(
            top, text="Seleccionar Categoría", font=("Times", 12), foreground="#fff"
        )
        self.label_category.place(relx=0.035, rely=0.2)

        text_font = ("Poppins", "8")
        self.combo1 = ttk.Combobox(top, style="info")
        self.combo1.place(relx=0.035, rely=0.250, width=477, height=26)

        find_category = "SELECT product_cat FROM raw_inventory"
        cur.execute(find_category)
        result1 = cur.fetchall()
        cat = []
        for i in range(len(result1)):
            if(result1[i][0] not in cat):
                cat.append(result1[i][0])

        self.combo1.configure(values=cat)
        self.combo1.configure(state="readonly")
        self.combo1.configure(font="-family {Poppins} -size 8")
        self.combo1.option_add("*TCombobox*Listbox.font", text_font)
        self.combo1.option_add("*TCombobox*Listbox.selectBackground", "#D2463E")

        # Etiqueta para sub categoría
        self.label_sub_category = Label(
            top, text="Seleccionar Sub Categoría", font=("Times", 12), foreground="#fff"
        )
        self.label_sub_category.place(relx=0.035, rely=0.3)

        self.combo2 = ttk.Combobox(top, style="info")
        self.combo2.place(relx=0.035, rely=0.350, width=477, height=26)
        self.combo2.configure(font="-family {Poppins} -size 8")
        self.combo2.option_add("*TCombobox*Listbox.font", text_font) 
        self.combo2.configure(state="disabled")

        # Etiqueta para nombre del producto
        self.label_name_product = Label(
            top, text="Nombre del producto", font=("Times", 12), foreground="#fff"
        )
        self.label_name_product.place(relx=0.035, rely=0.4)

        self.combo3 = ttk.Combobox(top, style="info")
        self.combo3.place(relx=0.035, rely=0.450, width=477, height=26)
        self.combo3.configure(state="disabled")
        self.combo3.configure(font="-family {Poppins} -size 8")
        self.combo3.option_add("*TCombobox*Listbox.font", text_font)

        # Etiqueta para nombre del producto
        self.label_cantidad_producto = Label(
            top, text="Cantidad de los productos", font=("Times", 12), foreground="#fff"
        )
        self.label_cantidad_producto.place(relx=0.035, rely=0.5)

        self.entry4 = ttk.Entry(top, style="info")
        self.entry4.place(relx=0.035, rely=0.550, width=477, height=26)
        self.entry4.configure(font="-family {Poppins} -size 8")
        self.entry4.configure(state="disabled")

        self.Scrolledtext1 = tkst.ScrolledText(top)
        self.Scrolledtext1.place(relx=0.439, rely=0.5, width=700, height=150)
        self.Scrolledtext1.configure(borderwidth=0)
        self.Scrolledtext1.configure(font="-family {Podkova} -size 8")
        self.Scrolledtext1.configure(state="disabled")

        self.combo1.bind("<<ComboboxSelected>>", self.get_category)
        
    def get_category(self, Event):
        self.combo2.configure(state="readonly")
        self.combo2.set('')
        self.combo3.set('')
        find_subcat = "SELECT product_subcat FROM raw_inventory WHERE product_cat = ?"
        cur.execute(find_subcat, [self.combo1.get()])
        result2 = cur.fetchall()
        subcat = []
        for j in range(len(result2)):
            if(result2[j][0] not in subcat):
                subcat.append(result2[j][0])
        
        self.combo2.configure(values=subcat)
        self.combo2.bind("<<ComboboxSelected>>", self.get_subcat)
        self.combo3.configure(state="disabled")

    def get_subcat(self, Event):
        self.combo3.configure(state="readonly")
        self.combo3.set('')
        find_product = "SELECT product_name FROM raw_inventory WHERE product_cat = ? and product_subcat = ?"
        cur.execute(find_product, [self.combo1.get(), self.combo2.get()])
        result3 = cur.fetchall()
        pro = []
        for k in range(len(result3)):
            pro.append(result3[k][0])

        self.combo3.configure(values=pro)
        self.combo3.bind("<<ComboboxSelected>>", self.show_qty)
        self.entry4.configure(state="disabled")

    def show_qty(self, Event):
        self.entry4.configure(state="normal")
        self.qty_label = Label(biller)
        self.qty_label.place(relx=0.250, rely=0.650, width=200, height=26)
        self.qty_label.configure(font="-family {Poppi ns} -size 8")
        self.qty_label.configure(anchor="w")

        product_name = self.combo3.get()
        find_qty = "SELECT stock FROM raw_inventory WHERE product_name = ?"
        cur.execute(find_qty, [product_name])
        results = cur.fetchone()
        self.qty_label.configure(text="Cantidad Disponibles: {}".format(results[0]))
    
    cart = Cart()
    def add_to_cart(self):
        self.Scrolledtext1.configure(state="normal")
        strr = self.Scrolledtext1.get('1.0', END)
        if strr.find('Total')==-1:
            product_name = self.combo3.get()
            if(product_name!=""):
                product_qty = self.entry4.get()
                find_mrp = "SELECT mrp, stock FROM raw_inventory WHERE product_name = ?"
                cur.execute(find_mrp, [product_name])
                results = cur.fetchall()
                stock = results[0][1]
                mrp = results[0][0]
                if product_qty.isdigit()==True:
                    if (stock-int(product_qty))>=0:
                        sp = mrp*int(product_qty)
                        item = Item(product_name, mrp, int(product_qty))
                        self.cart.add_item(item)
                        self.Scrolledtext1.configure(state="normal")
                        bill_text = "{}\t\t\t\t\t\t{}\t\t\t\t\t   {}\n".format(product_name, product_qty, sp)
                        self.Scrolledtext1.insert('insert', bill_text)
                        self.Scrolledtext1.configure(state="disabled")
                    else:
                        messagebox.showerror("Oops!", "Out of stock. Check quantity.", parent=biller)
                else:
                    messagebox.showerror("Oops!", "Invalid quantity.", parent=biller)
            else:
                messagebox.showerror("Oops!", "Choose a product.", parent=biller)
        else:
            self.Scrolledtext1.delete('1.0', END)
            new_li = []
            li = strr.split("\n")
            for i in range(len(li)):
                if len(li[i])!=0:
                    if li[i].find('Total')==-1:
                        new_li.append(li[i])
                    else:
                        break
            for j in range(len(new_li)-1):
                self.Scrolledtext1.insert('insert', new_li[j])
                self.Scrolledtext1.insert('insert','\n')
            product_name = self.combo3.get()
            if(product_name!=""):
                product_qty = self.entry4.get()
                find_mrp = "SELECT mrp, stock, product_id FROM raw_inventory WHERE product_name = ?"
                cur.execute(find_mrp, [product_name])
                results = cur.fetchall()
                stock = results[0][1]
                mrp = results[0][0]
                if product_qty.isdigit()==True:
                    if (stock-int(product_qty))>=0:
                        sp = results[0][0]*int(product_qty)
                        item = Item(product_name, mrp, int(product_qty))
                        self.cart.add_item(item)
                        self.Scrolledtext1.configure(state="normal")
                        bill_text = "{}\t\t\t\t\t\t{}\t\t\t\t\t   {}\n".format(product_name, product_qty, sp)
                        self.Scrolledtext1.insert('insert', bill_text)
                        self.Scrolledtext1.configure(state="disabled")
                    else:
                        messagebox.showerror("Oops!", "Out of stock. Check quantity.", parent=biller)
                else:
                    messagebox.showerror("Oops!", "Invalid quantity.", parent=biller)
            else:
                messagebox.showerror("Oops!", "Choose a product.", parent=biller)

    def remove_product(self):
        if(self.cart.isEmpty()!=True):
            self.Scrolledtext1.configure(state="normal")
            strr = self.Scrolledtext1.get('1.0', END)
            if strr.find('Total')==-1:
                try:
                    self.cart.remove_item()
                except IndexError:
                    messagebox.showerror("Error", "El carro está vacío", parent=biller)
                else:
                    self.Scrolledtext1.configure(state="normal")
                    get_all_bill = (self.Scrolledtext1.get('1.0', END).split("\n"))
                    new_string = get_all_bill[:len(get_all_bill)-3]
                    self.Scrolledtext1.delete('1.0', END)
                    for i in range(len(new_string)):
                        self.Scrolledtext1.insert('insert', new_string[i])
                        self.Scrolledtext1.insert('insert','\n')
                    
                    self.Scrolledtext1.configure(state="disabled")
            else:
                try:
                    self.cart.remove_item()
                except IndexError:
                    messagebox.showerror("Oops!", "Cart is empty", parent=biller)
                else:
                    self.Scrolledtext1.delete('1.0', END)
                    new_li = []
                    li = strr.split("\n")
                    for i in range(len(li)):
                        if len(li[i])!=0:
                            if li[i].find('Total')==-1:
                                new_li.append(li[i])
                            else:
                                break
                    new_li.pop()
                    for j in range(len(new_li)-1):
                        self.Scrolledtext1.insert('insert', new_li[j])
                        self.Scrolledtext1.insert('insert','\n')
                    self.Scrolledtext1.configure(state="disabled")

        else:
            messagebox.showerror("Error", "Agregar producto al carro", parent=biller)

    def wel_bill(self):
        self.name_message = Text(biller)
        self.name_message.place(relx=0.500, rely=0.4, width=176, height=30)
        self.name_message.configure(font="-family {Podkova} -size 10")
        self.name_message.configure(borderwidth=0)
        self.name_message.configure(foreground="#ffffff")

        self.num_message = Text(biller)
        self.num_message.place(relx=0.850, rely=0.3, width=90, height=30)
        self.num_message.configure(font="-family {Podkova} -size 10")
        self.num_message.configure(borderwidth=0)
        self.num_message.configure(foreground="#ffffff")
     
        self.bill_message = Text(biller)
        self.bill_message.place(relx=0.500, rely=0.3, width=176, height=26)
        self.bill_message.configure(font="-family {Podkova} -size 10")
        self.bill_message.configure(borderwidth=0)
        self.bill_message.configure(foreground="#ffffff")

        self.bill_date_message = Text(biller)
        self.bill_date_message.place(relx=0.850, rely=0.4, width=90, height=26)
        self.bill_date_message.configure(font="-family {Podkova} -size 10")
        self.bill_date_message.configure(borderwidth=0)
        self.bill_date_message.configure(foreground="#ffffff")
    
    def total_bill(self):
        if self.cart.isEmpty():
            messagebox.showerror("Error", "Debe agregar un producto", parent=biller)
        else:
            self.Scrolledtext1.configure(state="normal")
            strr = self.Scrolledtext1.get('1.0', END)
            if strr.find('Total')==-1:
                self.Scrolledtext1.configure(state="normal")
                divider = "\n\n\n"+("─"*61)
                self.Scrolledtext1.insert('insert', divider)
                total = "\nTotal\t\t\t\t\t\t\t\t\t\t\tCLP. {}".format(self.cart.total())
                self.Scrolledtext1.insert('insert', total)
                divider2 = "\n"+("─"*61)
                self.Scrolledtext1.insert('insert', divider2)
                self.Scrolledtext1.configure(state="disabled")
            else:
                return

    state = 1   

    def gen_bill(self):
        if self.state == 1:
            strr = self.Scrolledtext1.get('1.0', END)
            self.wel_bill()
            if(cust_name.get()==""):
                messagebox.showerror("Error", "Por favor ingresar nombre del cliente", parent=biller)
            elif(cust_num.get()==""):
                messagebox.showerror("Error", "Por favor ingresar teléfono del cliente", parent=biller)
            #elif valid_phone(cust_num.get())==False:
            #    messagebox.showerror("Oops!", "Please enter a valid number.", parent=biller)
            elif(self.cart.isEmpty()):
                messagebox.showerror("Error", "Agregar al carro de compras", parent=biller)
            else: 
                if strr.find('Total')==-1:
                    self.total_bill()
                    self.gen_bill()
                else:
                    self.name_message.insert(END, cust_name.get())
                    self.name_message.configure(state="disabled")
            
                    self.num_message.insert(END, cust_num.get())
                    self.num_message.configure(state="disabled")
            
                    cust_new_bill.set(random_bill_number(8))
                    num_boleta = str(random.randint(1000, 99999))
                    self.num_boleta = num_boleta

                    self.bill_message.insert(END, self.num_boleta)
                    self.bill_message.configure(state="disabled")
                
                    bill_date.set(str(date.today()))

                    self.bill_date_message.insert(END, bill_date.get())
                    self.bill_date_message.configure(state="disabled")

                    with sqlite3.connect("./database/store.db") as db:
                        cur = db.cursor()
                    insert = (
                        "INSERT INTO bill(bill_no, date, customer_name, customer_no, bill_details, total) VALUES(?,?,?,?,?,?)"
                    )
                    cur.execute(insert, [cust_new_bill.get(), bill_date.get(), cust_name.get(), cust_num.get(), self.Scrolledtext1.get('1.0', END), self.cart.total()])
                    db.commit()
                    #print(self.cart.items)
                    print(self.cart.allCart())
                    for name, qty in self.cart.dictionary.items():
                        update_qty = "UPDATE raw_inventory SET stock = stock - ? WHERE product_name = ?"
                        cur.execute(update_qty, [qty, name])
                        db.commit()
                    messagebox.showinfo("Información", "Venta generada", parent=biller)
                    self.entry1.configure(state="disabled", disabledbackground="#ffffff", disabledforeground="#000000")
                    self.entry2.configure(state="disabled", disabledbackground="#ffffff", disabledforeground="#000000")
                    self.state = 0
        else:
            return

    def exportar_a_pdf(self):

        # Verificar si num_boleta está definido
        if not hasattr(self, 'num_boleta') or self.num_boleta is None:
            messagebox.showerror("Error", "Debe ingresar venta para exporta la boleta de venta")
            return

        # Obtener los datos de la venta
        # Obtener los datos de la venta
        nombre_cliente = cust_name.get()
        numero_cliente = cust_num.get()
        detalles_venta = self.Scrolledtext1.get('1.0', 'end-1c')  # Obtener texto sin el último carácter (que es una nueva línea)

        # Crear un objeto PDF
        pdf = FPDF(orientation='L', unit='mm', format='A4')
        pdf.set_auto_page_break(auto=True, margin=15)

        # Agregar una nueva página
        pdf.add_page()
        pdf.set_font('Arial', '', 15)

        # título
        pdf.cell(w = 0, h = 15, txt = 'Boleta de venta', border = 1, ln=1, align = 'C', fill = 0)    
        pdf.cell(200, 10, txt="", ln=True, align='C')
        pdf.cell(200, 10, txt="Nombre del cliente: " + nombre_cliente, ln=True)
        pdf.cell(200, 10, txt="Número de teléfono cliente: " + numero_cliente, ln=True)
        # Agregar los detalles de la venta
        pdf.cell(w = 0, h = 15, txt = 'Detalle de la venta', border = 1, ln=1, align = 'C', fill = 0)    
        pdf.cell(200, 10, txt="", ln=True, align='C')

        # Restablecer la fuente
        pdf.set_font('Arial', '', 12)
        # Separar los detalles de venta en líneas y agregar cada línea como un párrafo en el PDF
        detalles_venta_lines = detalles_venta.split('\n')
        for line in detalles_venta_lines:
            try:
                pdf.cell(0, 10, txt=line.encode('latin-1', 'ignore').decode('latin-1'), ln=True)
            except UnicodeEncodeError:
               # Calcular y agregar el total
                total_venta = self.total_bill()
                pdf.set_font('Arial', 'B', 12)
                pdf.cell(0, 10, txt="Total de la Venta: CLP {}".format(total_venta), ln=True)


        # Agregar número de boleta
        pdf.cell(0, 10, txt="Número de boleta: {}".format(self.num_boleta), ln=True)

        # Guardar el PDF
        nombre_archivo = "voucher/boleta_de_venta{}.pdf".format(self.num_boleta)
        pdf.output(nombre_archivo)

        # Mostrar mensaje de éxito
        messagebox.showinfo("Éxito", "El archivo PDF se ha generado con éxito: " + nombre_archivo)

    def clear_bill(self):
        self.wel_bill()
        self.entry1.configure(state="normal")
        self.entry2.configure(state="normal")
        self.entry1.delete(0, END)
        self.entry2.delete(0, END)
        self.name_message.configure(state="normal")
        self.num_message.configure(state="normal")
        self.bill_message.configure(state="normal")
        self.bill_date_message.configure(state="normal")
        self.Scrolledtext1.configure(state="normal")
        self.name_message.delete(1.0, END)
        self.num_message.delete(1.0, END)
        self.bill_message.delete(1.0, END)
        self.bill_date_message.delete(1.0, END)
        self.Scrolledtext1.delete(1.0, END)
        self.name_message.configure(state="disabled")
        self.num_message.configure(state="disabled")
        self.bill_message.configure(state="disabled")
        self.bill_date_message.configure(state="disabled")
        self.Scrolledtext1.configure(state="disabled")
        self.cart.remove_items()
        self.state = 1

    def clear_selection(self):
        self.entry4.delete(0, END)
        self.combo1.configure(state="normal")
        self.combo2.configure(state="normal")
        self.combo3.configure(state="normal")
        self.combo1.delete(0, END)
        self.combo2.delete(0, END)
        self.combo3.delete(0, END)
        self.combo2.configure(state="disabled")
        self.combo3.configure(state="disabled")
        self.entry4.configure(state="disabled")
        try:
            self.qty_label.configure(foreground="#ffffff")
        except AttributeError:
            pass
             
    def search_bill(self):
        find_bill = "SELECT * FROM bill WHERE bill_no = ?"
        cur.execute(find_bill, [cust_search_bill.get().rstrip()])
        results = cur.fetchall()
        if results:
            self.clear_bill()
            self.wel_bill()
            self.name_message.insert(END, results[0][2])
            self.name_message.configure(state="disabled")
    
            self.num_message.insert(END, results[0][3])
            self.num_message.configure(state="disabled")
    
            self.bill_message.insert(END, results[0][0])
            self.bill_message.configure(state="disabled")

            self.bill_date_message.insert(END, results[0][1])
            self.bill_date_message.configure(state="disabled")

            self.Scrolledtext1.configure(state="normal")
            self.Scrolledtext1.insert(END, results[0][4])
            self.Scrolledtext1.configure(state="disabled")

            self.entry1.configure(state="disabled", disabledbackground="#ffffff", disabledforeground="#000000")
            self.entry2.configure(state="disabled", disabledbackground="#ffffff", disabledforeground="#000000")

            self.state = 0

        else:
            messagebox.showerror("Error!!", "Bill not found.", parent=biller)
            self.entry3.delete(0, END)
            
    def time(self):
        string = strftime("%H:%M:%S %p")
        self.clock.config(text=string)
        self.clock.after(1000, self.time)

    def managervoucher(self):
        # adm.withdraw()
        global vou
        global pagevou
        vou = tk.Toplevel()
        pagevou = ExploradorArchivos(vou)
        pagevou.time()
        vou.protocol("WM_DELETE_WINDOW")
        vou.mainloop()


page1 = login_page(root)
root.bind("<Return>", login)
root.mainloop()


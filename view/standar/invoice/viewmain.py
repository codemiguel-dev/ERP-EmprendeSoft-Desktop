import base64
import os
import tempfile
import uuid
from datetime import datetime

from PIL import Image
from PyQt5 import QtWidgets
from PyQt5.Qt import QIODevice
from PyQt5.QtCore import QBuffer, QByteArray, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QSizeGrip, QTableWidgetItem
from PyQt5.uic import loadUi
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from configuration.configuration_buttom import icon_configurate_top, icon_exit_program
from configuration.configuration_buttom_top import (
    control_bt_maximizar,
    control_bt_minimizar,
    control_bt_normal,
)
from configuration.configuration_config_theme import load_config
from configuration.configuration_delete_banner import delete_banner
from configuration.configuration_window_move import mousePressEvent, window_move
from controller.controllerbusiness import BusinessController
from controller.controllerclient import ClientController
from controller.controllerinventory import InventoryController
from controller.controllerinvoice import InvoiceController
from controller.controlleruser import UserController
from view.admin.inventory.viewadd import Viewadd
from view.admin.inventory.viewupdate import Viewupdate


class Viewmaininvoice(QtWidgets.QMainWindow):
    def __init__(self, id_user, username):
        super(Viewmaininvoice, self).__init__()
        self.theme = load_config(self)  # Lee la configuración al iniciar
        loadUi(f"design/standar/maininvoice{self.theme}.ui", self)
        self.sale_total = 0.0  # Inicializamos sale_total en 0

        self.id_user = id_user
        self.username = username

        # Inicializar el QSizeGrip y establecer su tamaño
        self.gripSize = 16  # Define el tamaño del grip
        self.grip = QSizeGrip(self)  # Crea un QSizeGrip para el redimensionamiento
        self.grip.resize(self.gripSize, self.gripSize)  # Ajusta el tamaño del QSizeGrip

        delete_banner(self)
        icon_configurate_top(self)
        icon_exit_program(self)

        # Maximizar la ventana por defecto
        self.showMaximized()

        # Asigna los eventos personalizados al frame superior
        self.frame_superior.mousePressEvent = lambda event: mousePressEvent(self, event)
        self.frame_superior.mouseMoveEvent = lambda event: window_move(self, event)

        # Control de botones de la barra de títulos
        self.bt_minimizar.clicked.connect(lambda: control_bt_minimizar(self))
        self.bt_restaurar.clicked.connect(lambda: control_bt_normal(self))
        self.bt_maximizar.clicked.connect(lambda: control_bt_maximizar(self))
        self.bt_cerrar.clicked.connect(lambda: self.close())
        self.bt_maximizar.hide()

        self.controllerinventory = InventoryController(self)
        self.controllerclient = ClientController(self)
        self.controlleruser = UserController(self)
        self.controllerinvoice = InvoiceController(self)
        self.controllerbusiness = BusinessController(self)

        self.show_inventory()
        self.show_client()
        self.show_user(self.username)

        self.comboboxproduct.currentIndexChanged.connect(self.update_stock_display)
        self.btn_add_cart.clicked.connect(self.add_cart)
        self.btn_delete.clicked.connect(self.delete_product)
        self.btn_get_code.clicked.connect(self.get_code)
        self.btn_register_sale.clicked.connect(self.add_sale)
        self.btn_exit.clicked.connect(self.close_program)
        self.btn_export_pdf.clicked.connect(self.export_pdf)

    def close_program(self):
        QApplication.quit()

    def reload_ui(self):
        self.close()  # Cierra la ventana actual
        self.__init__()  # Re-inicia la vista con el nuevo tema
        self.show()  # Vuelve a mostrar la ventana

    def show_inventory(self):
        # Desconectar la señal para evitar bucles infinitos
        self.comboboxproduct.blockSignals(True)

        self.comboboxproduct.clear()
        # Obtener datos de inventario desde el controlador
        products = self.controllerinventory.get_inventory()

        # Añadir productos al comboBox
        for product in products:
            uid = product[0]  # El primer elemento es el ID del producto
            product_name = product[2]  # El segundo elemento es el nombre del producto

            # Añadir el producto al combobox
            self.comboboxproduct.addItem(product_name, uid)

        # Reconectar la señal después de añadir los productos
        self.comboboxproduct.blockSignals(False)

        # Conectar la señal de cambio de región

    def show_client(self):
        # Desconectar la señal para evitar bucles infinitos
        self.comboboxclient.blockSignals(True)

        self.comboboxclient.clear()
        # Obtener datos de inventario desde el controlador
        clients = self.controllerclient.get()

        # Añadir productos al comboBox
        for client in clients:
            uid = client[0]  # El primer elemento es el ID del producto
            name = client[2]  # El segundo elemento es el nombre del producto

            # Añadir el producto al combobox
            self.comboboxclient.addItem(name, uid)

        # Reconectar la señal después de añadir los productos
        self.comboboxclient.blockSignals(False)

    def show_user(self, username):
        self.username = username
        self.usertxt.setText(self.username)

    def update_stock_display(self):
        current_index = self.comboboxproduct.currentIndex()
        if current_index >= 0:
            uid = self.comboboxproduct.itemData(current_index)
            products = self.controllerinventory.get_inventory()

            # Recorrer la lista de productos y encontrar el producto con el UID correspondiente
            product = None
            for p in products:
                if p[0] == uid:  # El primer elemento de la tupla es el ID del producto
                    product = p
                    break

            if product:
                # El producto es una tupla, acceder a los valores por índice
                product_image_blob = product[1]  # Imagen del producto en formato BLOB
                product_name = product[
                    2
                ]  # El segundo elemento es el nombre del producto
                product_stock = product[
                    4
                ]  # El tercer elemento es el stock del producto
                product_unit_price = product[
                    5
                ]  # El cuarto elemento es el precio del producto

                # Actualizar los campos en la interfaz
                self.labelname.setText(f"Nombre: {product_name}")
                self.labelstock.setText(f"Cantidad Disponible: {product_stock}")
                self.labeluprice.setText(f"Precio Unitario: {product_unit_price}")
                self.unitpricetxt.setText(f"{product_unit_price}")

                # Cargar la imagen desde el BLOB
                if product_image_blob:
                    pixmap = QPixmap()
                    pixmap.loadFromData(
                        product_image_blob
                    )  # Cargar imagen desde el BLOB

                    # Escalar la imagen al tamaño del QLabel y mantener la proporción
                    scaled_pixmap = pixmap.scaled(
                        self.labelimage.size(),
                        Qt.KeepAspectRatio,
                        Qt.SmoothTransformation,
                    )
                    self.labelimage.setPixmap(scaled_pixmap)
                else:
                    print("No hay imagen disponible")
                    self.labelimage.clear()

            else:
                # Si no se encuentra el producto, limpiar los campos
                self.labelname.setText("Nombre: No disponible")
                self.labelstock.setText("Cantidad Disponible: No disponible")
                self.labeluprice.setText("Precio Unitario: No disponible")

    def add_cart(self):
        # Obtener los valores de los QLineEdit como cadenas
        product_unit_price_str = self.unitpricetxt.text()
        product_quantity_str = self.quantitytxt.text()

        # Ajustar el tamaño de las filas y columnas
        self.table_cart.verticalHeader().setDefaultSectionSize(200)
        self.table_cart.horizontalHeader().setDefaultSectionSize(300)

        try:
            # Convertir las cadenas a números
            product_unit_price = float(product_unit_price_str)
            product_quantity = int(product_quantity_str)

            # Obtener datos del producto desde el controlador (suponiendo que `products` es una lista)
            products = self.controllerinventory.get_inventory()

            # Obtener el índice del producto seleccionado desde el combobox (en lugar de una clave)
            selected_product_index = self.comboboxproduct.currentIndex()

            # Verificar que el índice del producto sea válido
            if selected_product_index < 0 or selected_product_index >= len(products):
                QtWidgets.QMessageBox.warning(
                    self, "Advertencia", "Producto no encontrado."
                )
                return

            # Obtener el producto como lista (en lugar de diccionario)
            product = products[selected_product_index]

            # Suponiendo que los datos del producto están organizados como: [id, name, stock, unit_price, image_blob]
            product_id = product[0]
            product_image_blob = product[1]
            product_name = product[2]
            product_stock = int(product[4])
            product_total = int(product[7])

            # Verificar si la cantidad solicitada excede el stock disponible
            if product_quantity > product_stock:
                QtWidgets.QMessageBox.warning(
                    self,
                    "Advertencia",
                    "La cantidad solicitada excede el stock disponible.",
                )
                return

            # Calcular el total de cada producto
            total = product_unit_price * product_quantity

            # Sumar el total del producto al total acumulado
            self.sale_total += total

            # Mostrar el total acumulado en el QLabel
            self.labeltotal.setText(f"CLP {self.sale_total:.2f}")
            self.totalpricetxt.setText(f"{self.sale_total}")

            # Añadir el producto al carrito de compras
            row_position = self.table_cart.rowCount()
            self.table_cart.insertRow(row_position)

            # Crear un QLabel para la imagen y cargar el BLOB
            if product_image_blob:
                pixmap = QPixmap()
                pixmap.loadFromData(
                    product_image_blob
                )  # Cargar la imagen directamente desde el BLOB

                # Ajustar el tamaño del pixmap
                scaled_pixmap = pixmap.scaled(
                    300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation
                )

                label = QLabel()
                label.setPixmap(scaled_pixmap)
                label.setScaledContents(True)

                # Colocar el QLabel con la imagen en la celda
                self.table_cart.setCellWidget(row_position, 1, label)
            else:
                self.table_cart.setItem(row_position, 1, QTableWidgetItem("No Image"))

            # Agregar otros detalles del producto a la tabla
            self.table_cart.setItem(row_position, 0, QTableWidgetItem(str(product_id)))
            self.table_cart.setItem(row_position, 2, QTableWidgetItem(product_name))
            self.table_cart.setItem(
                row_position, 3, QTableWidgetItem(str(product_quantity))
            )
            self.table_cart.setItem(
                row_position, 4, QTableWidgetItem(f"{product_unit_price:.2f}")
            )
            self.table_cart.setItem(row_position, 5, QTableWidgetItem(f"{total:.2f}"))

        except ValueError:
            # Manejar el caso en el que la conversión falla
            self.labeltotal.setText("Error: Valores inválidos")

    def delete_product(self):
        # Obtener índice de la fila seleccionada
        selected_row = self.table_cart.currentRow()

        # Verificar si se ha seleccionado una fila
        if selected_row != -1:
            uid_item = self.table_cart.item(selected_row, 0).text()

            # Obtener el valor del total del producto que se va a eliminar
            total_item_str = self.table_cart.item(selected_row, 5).text()
            try:
                total_item = float(total_item_str)
            except ValueError:
                total_item = 0.0  # Usar 0.0 si no se puede convertir el total

            # Asegúrate de que self.sale_total sea un float
            try:
                self.sale_total = float(self.sale_total)
            except ValueError:
                self.sale_total = (
                    0.0  # Usar 0.0 si self.sale_total no es convertible a float
                )

            # Restar el total del producto del total acumulado
            self.sale_total -= total_item

            # Actualizar el QLabel con el total acumulado
            self.labeltotal.setText(f"CLP {self.sale_total:.2f}")
            self.totalpricetxt.setText(f"{self.sale_total:.2f}")

            # Eliminar la fila de la tabla en la interfaz gráfica
            self.table_cart.removeRow(selected_row)

            # Aquí deberías agregar la lógica para eliminar el producto de tu base de datos o estructura de datos.
            # Por ejemplo:
            # self.database.delete_product_by_uid(uid_item)

            # Mensaje de confirmación
            QtWidgets.QMessageBox.information(
                self, "Éxito", "El producto ha sido eliminado."
            )
        else:
            QtWidgets.QMessageBox.warning(
                self, "Error", "Por favor, seleccione una fila para eliminar."
            )

    def get_code(self):
        # Generar código único
        code = f"INV-{uuid.uuid4().hex[:8].upper()}"

        # Establecer el código en el campo de texto codetxt
        self.codetxt.setText(code)

    def add_sale(self):
        user = self.comboboxuser.currentData()  # obtiene id
        client = self.comboboxclient.currentData()  # obtiene id
        product = self.comboboxproduct.currentData()  # obtiene id
        total = self.totalpricetxt.text()
        code = self.codetxt.text()

        # print(user)
        # print(client)

        if not user or not client or not code:
            QtWidgets.QMessageBox.warning(
                self,
                "Advertencia",
                "Debe ingresar un cliente, usuario y generar código de factura",
            )
            return

        self.controllerinvoice.register(user, client, total, code)

        # Iterar sobre cada fila del carrito de compras

        for row in range(self.table_cart.rowCount()):
            # Obtener el ítem en la primera columna (ID del producto)
            product_id_item = self.table_cart.item(row, 0)
            product_id = product_id_item.text() if product_id_item else "Desconocido"

            # Obtener los ítems en las columnas restantes
            product_name_item = self.table_cart.item(row, 2)
            product_quantity_item = self.table_cart.item(row, 3)
            product_unit_price_item = self.table_cart.item(row, 4)
            product_total_item = self.table_cart.item(row, 5)

            product_quantity = (
                int(product_quantity_item.text()) if product_quantity_item else 0
            )
            product_unit_price = (
                float(product_unit_price_item.text())
                if product_unit_price_item
                else 0.0
            )
            product_total = (
                float(product_total_item.text()) if product_total_item else 0.0
            )

            # Registrar la venta del producto en la base de datos
            self.controllerinvoice.register_item(
                product_id, product_quantity, product_total, code
            )

        QtWidgets.QMessageBox.information(
            self, "Información", "Venta ingresada en la base de datos."
        )

        self.export_pdf()

    def export_pdf(self):
        # Obtener la fecha y hora actuales y formatearlas
        current_date = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Ruta y nombre del archivo PDF
        pdf_file = os.path.join(
            os.path.dirname(__file__), f"../print_sale/pdf/venta_{current_date}.pdf"
        )
        # Crear un lienzo
        c = canvas.Canvas(pdf_file, pagesize=letter)
        width, height = letter
        self.sale_total = self.totalpricetxt.text()
        self.id_client = self.comboboxclient.currentData()
        self.id_seller = self.comboboxuser.currentData()
        self.id_voucher = self.codetxt.text()

        users = self.controlleruser.get_user()
        clients = self.controllerclient.get()

        # Obtener datos desde el controlador (usando el INNER JOIN)
        Business_controller = self.controllerbusiness.get()

        business_id = None
        business_logo_path = None  # Añadimos una variable para la imagen temporal
        for i, business in enumerate(Business_controller):
            if isinstance(business, (tuple, list)):
                business_id = business[0]
                business_name = business[1]
                business_logo = business[2]  # Columna 3 contiene el BLOB de la imagen
                business_industry = business[4]
                business_country = business[7]
                business_region = business[8]
                business_description_address = business[9]
                # Mostrar la imagen almacenada como BLOB en el QLabel
                try:
                    # Si los datos están codificados en base64, decodifícalos
                    if isinstance(business_logo, str):
                        # Eliminar encabezado de datos si está presente (por ejemplo, "data:image/png;base64,")
                        if business_logo.startswith("data:image"):
                            business_logo = business_logo.split(",")[1]
                        business_logo = base64.b64decode(business_logo)

                    # Guardar el archivo temporal
                    with tempfile.NamedTemporaryFile(
                        delete=False, suffix=".png"
                    ) as temp_image:
                        temp_image.write(business_logo)
                        business_logo_path = temp_image.name

                    # Verificar si el archivo guardado es una imagen válida
                    image = Image.open(business_logo_path)
                    image.verify()  # Esto lanzará una excepción si la imagen no es válida
                except Exception as e:
                    print(f"Error al convertir el BLOB a imagen: {e}")
                    business_logo_path = None
            break

        if business_id is None:
            QtWidgets.QMessageBox.warning(
                self, "Advertencia", "No se encontró la empresa."
            )
            return

        user = None
        for u in users:
            if (
                u[0] == self.id_seller
            ):  # El primer elemento de la tupla es el ID del producto
                user = u
                break
        if user:
            user_name = user[2]  # El segundo elemento es el nombre del producto
            user_email = user[4]
            user_phone = user[5]

        client = None
        for cl in clients:
            if (
                cl[0] == self.id_client
            ):  # El primer elemento de la tupla es el ID del producto
                client = cl
                break
        if client:
            client_name = client[2]  # El segundo elemento es el nombre del producto
            client_last_name = client[3]
            client_email = client[4]
            client_phone = client[5]

            # Agregar la imagen desde el archivo temporal
        if business_logo_path:
            try:
                c.drawImage(business_logo_path, 500, height - 100, width=40, height=40)
            except Exception as e:
                print(f"Error al agregar la imagen: {e}")

        c.setFont("Helvetica-Bold", 20)
        c.drawString(50, height - 50, f"Código de la boleta: {self.id_voucher}")

        # Agregar datos de la empresa
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, height - 100, "Empresa")
        c.setFont("Helvetica", 12)
        c.drawString(50, height - 125, f"Nombre: {business_name}")
        c.drawString(50, height - 150, f"Industria: {business_industry}")
        c.drawString(
            50,
            height - 175,
            f"Dirección: {business_country} {business_region} {business_description_address}",
        )

        # Agregar datos del vendedor
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, height - 225, "Vendedor")
        c.setFont("Helvetica", 12)
        c.drawString(50, height - 250, f"Nombre: {user_name}")
        c.drawString(50, height - 275, f"Correo: {user_email}")
        c.drawString(50, height - 300, f"Teléfono: {user_phone}")

        # Agregar datos del cliente
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, height - 350, "Cliente")
        c.setFont("Helvetica", 12)
        c.drawString(50, height - 375, f"Nombre: {client_name}")
        c.drawString(50, height - 400, f"Correo: {client_email}")
        c.drawString(50, height - 425, f"Teléfono: {client_phone}")

        # Título del documento
        c.setFont("Helvetica-Bold", 16)
        c.drawString(100, height - 475, "Productos Comprados")
        c.drawString(450, height - 475, "Total: " + self.sale_total)

        # Coordenadas iniciales para la tabla
        y = height - 500
        x = 50
        c.setFont("Helvetica", 12)
        headers = ["Nombre", "Cantidad", "Precio Unitario", "Total"]
        for i, header in enumerate(headers):
            c.drawString(x + i * 150, y, header)
        y -= 20

        # Iterar sobre cada fila del carrito de compras y agregar los datos al PDF
        for row in range(self.table_cart.rowCount()):
            product_name = self.table_cart.item(row, 2).text()
            product_quantity = self.table_cart.item(row, 3).text()
            product_unit_price = self.table_cart.item(row, 4).text()
            product_total = self.table_cart.item(row, 5).text()
            c.drawString(x, y, product_name)
            c.drawString(x + 150, y, product_quantity)
            c.drawString(x + 300, y, product_unit_price)
            c.drawString(x + 450, y, product_total)
            y -= 20
            if y < 50:
                c.showPage()
                y = height - 50

        c.save()
        QtWidgets.QMessageBox.information(
            self,
            "Exportar a PDF",
            f"El carrito de compras ha sido exportado a {pdf_file}",
        )

    # Función auxiliar para convertir BLOB a QPixmap
    def convert_blob_to_pixmap(self, blob_data):
        """Convierte un BLOB de imagen a un QPixmap"""
        byte_array = QByteArray(blob_data)
        pixmap = QPixmap()
        buffer = QBuffer(byte_array)
        buffer.open(QIODevice.ReadOnly)
        pixmap.loadFromData(buffer.data())
        return pixmap

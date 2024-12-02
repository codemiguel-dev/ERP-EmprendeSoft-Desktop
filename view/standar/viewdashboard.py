import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.uic import loadUi
#from controller.controlleruser import UsersController
#from view.admin.user.viewformupdate import UpdateForm

class Viewdashboardstandar(QtWidgets.QMainWindow):
    def __init__(self):
        super(Viewdashboardstandar, self).__init__()
        loadUi('design/dashboard_standar.ui', self)
    
        # Configurar íconos de botones
        self.bt_minimizar.setIcon(QIcon('img/minus.svg'))
        self.bt_restaurar.setIcon(QIcon('img/chevron-up.svg'))
        self.bt_maximizar.setIcon(QIcon('img/chevron-down.svg'))
        self.bt_cerrar.setIcon(QIcon('img/x.svg'))
        self.bt_restaurar.hide()

        # Eliminar barra de título y hacer la ventana translúcida
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowOpacity(1)

        # Configurar SizeGrip para redimensionar la ventana
        self.gripSize = 10
        self.grip = QtWidgets.QSizeGrip(self)
        self.grip.resize(self.gripSize, self.gripSize)

        # Mover ventana con click y arrastre en la barra superior
        self.frame_superior.mouseMoveEvent = self.mover_ventana

        # Acceder a las páginas
        #self.bt_inicio.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_uno))
        #self.bt_uno.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page))
        #self.bt_dos.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_dos))
        #self.bt_tres.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_tres))
        #self.bt_cuatro.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_cuatro))
        #self.bt_cinco.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_cinco))

        # Control de botones de la barra de títulos
        self.bt_minimizar.clicked.connect(self.control_bt_minimizar)
        self.bt_restaurar.clicked.connect(self.control_bt_normal)
        self.bt_maximizar.clicked.connect(self.control_bt_maximizar)
        self.bt_cerrar.clicked.connect(lambda: self.close())
        self.bt_restaurar.hide()

        # Conectar botón de actualizar usuarios
        #self.buttom_update.clicked.connect(self.update_users)
        #self.buttomUpdateUser.clicked.connect(self.show_users)
        #self.buttom_delete.clicked.connect(self.delete_users)

        # Menú lateral
        #self.bt_menu.clicked.connect(self.mover_menu)

        # Instanciar el controlador de usuarios
        #self.controller = UsersController(self)

        # Configurar la tabla para mostrar usuarios
        #self.tableUser.setColumnCount(4)  # Columnas: UID, Nombre, Email, Contraseña
        #self.tableUser.setHorizontalHeaderLabels(['UID', 'Nombre', 'Email', 'Contraseña'])
		

    def control_bt_minimizar(self):
        self.showMinimized()

    def control_bt_normal(self):
        self.showNormal()
        self.bt_restaurar.hide()
        self.bt_maximizar.show()

    def control_bt_maximizar(self):
        self.showMaximized()
        self.bt_maximizar.hide()
        self.bt_restaurar.show()

    def mover_menu(self):
        # Animación para mostrar/ocultar menú lateral
        width = self.frame_lateral.width()
        extender = 200 if width == 0 else 0
        self.animacion = QtCore.QPropertyAnimation(self.frame_lateral, b'minimumWidth')
        self.animacion.setDuration(300)
        self.animacion.setStartValue(width)
        self.animacion.setEndValue(extender)
        self.animacion.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animacion.start()

    def resizeEvent(self, event):
        # Reposicionar el SizeGrip al redimensionar la ventana
        rect = self.rect()
        self.grip.move(rect.right() - self.gripSize, rect.bottom() - self.gripSize)

    def mousePressEvent(self, event):
        # Capturar posición de click para mover la ventana
        self.clickPosition = event.globalPos()

    def mover_ventana(self, event):
        # Mover la ventana si no está maximizada
        if not self.isMaximized() and event.buttons() == QtCore.Qt.LeftButton:
            self.move(self.pos() + event.globalPos() - self.clickPosition)
            self.clickPosition = event.globalPos()
            event.accept()

        if event.globalPos().y() <= 20:
            self.showMaximized()
        else:
            self.showNormal()

    def show_users(self):
        # Obtener datos de usuarios desde el controlador
        users = self.controller.get_users()

        # Limpiar la tabla
        self.tableUser.setRowCount(0)

        # Mostrar usuarios en la tabla
        for i, (uid, user) in enumerate(users.items()):
            self.tableUser.insertRow(i)
            self.tableUser.setItem(i, 0, QtWidgets.QTableWidgetItem(user.get('uid', '')))
            self.tableUser.setItem(i, 1, QtWidgets.QTableWidgetItem(user.get('name', '')))
            self.tableUser.setItem(i, 2, QtWidgets.QTableWidgetItem(user.get('email', '')))
            self.tableUser.setItem(i, 3, QtWidgets.QTableWidgetItem(user.get('password', '')))  # Ajustar según la estructura de datos

    def update_users(self):
        # Obtener índice de la fila seleccionada
        selected_row = self.tableUser.currentRow()

        # Verificar si se ha seleccionado una fila
        if selected_row != -1:
            uid_item = self.tableUser.item(selected_row, 0)
            name_item = self.tableUser.item(selected_row, 1)
            email_item = self.tableUser.item(selected_row, 2)
            password_item = self.tableUser.item(selected_row, 3)

            if uid_item and name_item and email_item and password_item:
                uid = uid_item.text()
                name = name_item.text()
                email = email_item.text()
                password = password_item.text()

                # Abrir el nuevo formulario de actualización
                #self.update_form = UpdateForm(self.controller,uid, name, email, password)
                self.update_form.show()
        else:
            QtWidgets.QMessageBox.warning(self, "Error", "Por favor, seleccione una fila para actualizar.")


    def delete_users(self):
        # Obtener índice de la fila seleccionada
        selected_row = self.tableUser.currentRow()
		# Verificar si se ha seleccionado una fila
        if selected_row != -1:
            uid_item = self.tableUser.item(selected_row, 0)

            if uid_item:
                uid = uid_item.text()

                # Confirmar eliminación
                reply = QtWidgets.QMessageBox.question(self, 'Confirmar Eliminación', 
                                                   f"¿Estás seguro de eliminar al usuario con UID: {uid}?",
                                                   QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
                if reply == QtWidgets.QMessageBox.Yes:
                    # Eliminar usuario utilizando el controlador
                    if self.controller.delete_user(uid):
                        QtWidgets.QMessageBox.information(self, "Eliminado", "Usuario eliminado correctamente.")
                        self.show_users()  # Actualizar la tabla de usuarios después de eliminar
                    else:
                        QtWidgets.QMessageBox.warning(self, "Error", "Hubo un problema al eliminar el usuario.")
        else:
            QtWidgets.QMessageBox.warning(self, "Error", "Por favor, seleccione una fila para eliminar.")
			


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mi_app = Viewdashboardstandar()
    mi_app.show()
    sys.exit(app.exec_())

import os

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QColor, QImage, QPainter
from PyQt5.QtWidgets import (
    QApplication,
    QGraphicsRectItem,
    QGraphicsScene,
    QGraphicsTextItem,
    QGraphicsView,
    QLabel,
    QMainWindow,
    QPushButton,
    QSizeGrip,
)
from PyQt5.uic import loadUi

from configuration.configuration_buttom import icon_configurate_top, icon_exit_program
from configuration.configuration_buttom_top import (
    control_bt_maximizar,
    control_bt_minimizar,
    control_bt_normal,
)
from configuration.configuration_config_theme import load_config
from configuration.configuration_delete_banner import delete_banner
from configuration.configuration_message import show_message
from configuration.configuration_window_move import mousePressEvent, window_move
from controller.controllerbusiness import BusinessController


class ZoomableGraphicsView(QGraphicsView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setDragMode(
            QGraphicsView.ScrollHandDrag
        )  # Permitir arrastrar con el mouse

    def wheelEvent(self, event):
        """Controlar el zoom con la rueda del mouse."""
        zoom_in_factor = 1.15
        zoom_out_factor = 1 / zoom_in_factor

        # Si se mueve hacia adelante, hacer zoom in, si no, zoom out
        if event.angleDelta().y() > 0:
            zoom_factor = zoom_in_factor
        else:
            zoom_factor = zoom_out_factor

        # Aplicar el zoom
        self.scale(zoom_factor, zoom_factor)


class GainChart(QMainWindow):
    def __init__(self):
        super().__init__()

        self.theme = load_config(self)  # Lee la configuración al iniciar
        # Cargar el diseño desde el archivo .ui
        loadUi(
            f"design/admin/maingraphicgain{self.theme}.ui", self
        )  # Asegúrate de que el archivo esté en el mismo directorio

        icon_configurate_top(self)
        icon_exit_program(self)
        delete_banner(self)

        # Inicializar el QSizeGrip y establecer su tamaño
        self.gripSize = 16  # Define el tamaño del grip
        self.grip = QSizeGrip(self)  # Crea un QSizeGrip para el redimensionamiento
        self.grip.resize(self.gripSize, self.gripSize)  # Ajusta el tamaño del QSizeGrip

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
        self.btn_exit.clicked.connect(self.close_program)
        self.bt_maximizar.hide()

        # Vincular el ZoomableGraphicsView del diseño
        self.graphics_view = self.findChild(QGraphicsView, "graphics_view")

        # Configurar el gráfico con una escena
        self.scene = QGraphicsScene()
        self.graphics_view.setScene(self.scene)
        self.graphics_view.setDragMode(
            QGraphicsView.ScrollHandDrag
        )  # Arrastrar con el mouse

        # Conectar controlador de datos
        self.controller = BusinessController(self)

        # Obtener datos desde la base de datos y crear el gráfico
        business_data = self.controller.get_graphi()
        self.create_chart(business_data)

        # Agregar botones de zoom
        self.zoom_in_button = self.findChild(QPushButton, "zoom_in_button")
        self.zoom_out_button = self.findChild(QPushButton, "zoom_out_button")
        self.zoom_in_button.clicked.connect(lambda: self.zoom(1.15))
        self.zoom_out_button.clicked.connect(lambda: self.zoom(1 / 1.15))
        self.btn_export_image.clicked.connect(self.export_graphic_image)
        self.open_explore_file.clicked.connect(self.open_file_explorer)

    def close_program(self):
        QApplication.quit()

    def export_graphic_image(self):
        """Exporta el contenido del gráfico a una imagen."""

        name_file = self.name_imagetxt.text()
        # Crear un objeto QImage con las dimensiones de la escena
        rect = self.scene.sceneRect()
        image = QImage(int(rect.width()), int(rect.height()), QImage.Format_ARGB32)
        image.fill(Qt.transparent)  # Fondo transparente

        # Pintar la escena en el QImage
        painter = QPainter(image)
        self.scene.render(painter)
        painter.end()

        # Guardar la imagen en un archivo
        file_path = os.path.join(
            os.path.dirname(__file__), f"../../../img/graphic/{name_file}.png"
        )  # Cambia el nombre o ruta según tus necesidades
        if image.save(file_path):
            show_message("Información", "Exportado  Correctamente")
        else:
            show_message("Información", "Error")

    def open_file_explorer(self):
        """
        Abre el explorador de archivos en la ubicación especificada.
        """
        # Construir la ruta correctamente
        path = os.path.join(os.path.dirname(__file__), "../../../img/graphic")

        if os.path.exists(path):
            os.startfile(path)  # Abre el explorador de archivos (Solo en Windows)
        else:
            print("La ruta especificada no existe.")

    def zoom(self, factor):
        """Aplicar el zoom con los botones."""
        self.graphics_view.scale(factor, factor)

    def add_value_labels(self, max_value):
        """Agregar etiquetas de monto en el eje Y fuera de la escena."""
        num_labels = 10  # Número de etiquetas de monto a mostrar en el eje Y
        increment = max_value / num_labels
        y_offset = 400
        for i in range(num_labels + 1):
            value = i * increment
            value_label = QLabel(f"CP{value:.2f}")
            value_label.setAlignment(Qt.AlignRight)
            self.y_labels_layout.addWidget(value_label)
        # Añadir estiramiento al final para alinear las etiquetas de monto correctamente
        self.y_labels_layout.addStretch()

    def create_chart(self, business_data):
        """Crea un gráfico de barras en la escena usando los datos proporcionados desde la consulta de negocio."""

        # Extraer los datos necesarios del resultado de la consulta
        business_names = [row[0] for row in business_data]  # 'name'
        gains = [row[1] for row in business_data]  # 'gain'

        # Calcular el valor máximo para escalar las barras
        max_value = max(gains) if gains else 1
        num_labels = 10  # Número de etiquetas de monto en el eje Y
        increment = max_value / num_labels  # Incremento entre cada etiqueta de monto

        bar_width = 50
        spacing = 80
        x_offset = 80
        y_offset = 400
        chart_height = 300  # Altura máxima del gráfico

        # Agregar etiquetas de monto en el eje Y y líneas de fondo
        for i in range(num_labels + 1):
            value = i * increment
            y_position = y_offset - (value / max_value) * chart_height

            # Etiqueta del eje Y
            value_label = QGraphicsTextItem(f"CLP{value:.2f}")
            value_label.setDefaultTextColor(Qt.white)
            value_label.setPos(x_offset - 70, y_position - 10)
            self.scene.addItem(value_label)

            # Línea horizontal de fondo
            line = QGraphicsRectItem(
                x_offset, y_position, len(business_data) * (bar_width + spacing), 1
            )
            line.setBrush(QBrush(QColor("#E8E8E8")))
            line.setOpacity(1.0)
            self.scene.addItem(line)

        # Crear las barras para cada negocio
        for i, (name, gain) in enumerate(zip(business_names, gains)):
            x_position = x_offset + i * (bar_width + spacing)

            # Altura de la barra
            bar_height = (gain / max_value) * chart_height

            # Dibujar la barra del gain
            rect = QGraphicsRectItem(
                x_position,
                y_offset - bar_height,
                bar_width,
                bar_height,
            )
            rect.setBrush(QBrush(QColor("#4CAF50")))  # Verde para las ganancias
            self.scene.addItem(rect)

            # Etiquetas del eje X (nombre del negocio)
            text_item = QGraphicsTextItem(name)
            text_item.setDefaultTextColor(Qt.white)
            text_item.setPos(x_position + bar_width // 4, y_offset + 10)
            self.scene.addItem(text_item)

            # Etiquetas de valores encima de las barras
            value_item = QGraphicsTextItem(f"CLP{gain:.2f}")
            value_item.setDefaultTextColor(Qt.white)
            value_item.setPos(
                x_position,
                y_offset - bar_height - 25,
            )
            self.scene.addItem(value_item)


if __name__ == "__main__":
    app = QApplication([])
    window = GainChart()
    window.show()
    app.exec_()

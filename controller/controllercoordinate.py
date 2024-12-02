# controller_register.py

from PyQt5.QtWidgets import QMessageBox

from models.modelcoordinate import ModelCoordinate


class CoordinateController:
    def __init__(self, view):
        self.model = ModelCoordinate()
        self.view = view

    def register(self, address_id, uuid, lat, lon):
        self.model.register(address_id, uuid, lat, lon)

    def get(self):
        return self.model.get()

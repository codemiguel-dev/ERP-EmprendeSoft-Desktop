# controller_register.py

from PyQt5.QtWidgets import QMessageBox

from models.modelprovider import ModelProvider


class ProviderController:
    def __init__(self, view):
        self.model = ModelProvider()
        self.view = view

    def register(self, rut, name, email, fono, address, type_provider, image):
        self.model.register(rut, name, email, fono, address, type_provider, image)

    def get(self):
        return self.model.get()

    def update(self, uid, rut, name, email, fono, address, type_provider, image):
        return self.model.update(
            uid, rut, name, email, fono, address, type_provider, image
        )

    def delete(self, uid):
        return self.model.delete(uid)

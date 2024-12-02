# controller_register.py

from PyQt5.QtWidgets import QMessageBox

from models.modelclient import ModelClient


class ClientController:
    def __init__(self, view):
        self.model = ModelClient()
        self.view = view

    def register(self, name, lastname, email, fono, address, client_type, image):
        self.model.register(name, lastname, email, fono, address, client_type, image)

    def get(self):
        return self.model.get()

    def update_client(
        self, uid, name, lastname, email, fono, address, client_type, image
    ):
        return self.model.update(
            uid, name, lastname, email, fono, address, client_type, image
        )

    def delete_client(self, uid):
        return self.model.delete(uid)

# controller_register.py

from PyQt5.QtWidgets import QMessageBox

from models.modelsent import ModelSent


class SentController:
    def __init__(self, view):
        self.model = ModelSent()
        self.view = view

    def register(self, address, method, description, budget, status):
        self.model.register(address, method, description, budget, status)

    def get(self):
        return self.model.get()

    def update(self, uid, address, method, description, price_send, status):
        return self.model.update(uid, address, method, description, price_send, status)

    def delete(self, uid):
        return self.model.delete(uid)

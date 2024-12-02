# controller_register.py

from PyQt5.QtWidgets import QMessageBox

from models.modeladdress import ModelAddress


class AddressController:
    def __init__(self, view):
        self.model = ModelAddress()
        self.view = view

    def register(self, country, region, commune, description):
        self.model.register(country, region, commune, description)

    def get(self):
        return self.model.get()

    def update(self, uid, region, commune, address):
        return self.model.update(uid, region, commune, address)

    def delete_inventory(self, uid):
        return self.model.delete(uid)

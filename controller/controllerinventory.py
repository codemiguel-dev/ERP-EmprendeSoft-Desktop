# controller_register.py

from PyQt5.QtWidgets import QMessageBox

from models.modelinventory import ModelInventory


class InventoryController:
    def __init__(self, view):
        self.model = ModelInventory()
        self.view = view

    def register_inventory(
        self,
        name,
        category,
        stock,
        purchase_price,
        sale_price,
        total_purch,
        description,
        image,
    ):
        self.model.register(
            name,
            category,
            stock,
            purchase_price,
            sale_price,
            total_purch,
            description,
            image,
        )

    def get_inventory(self):
        return self.model.get_inventory()

    def update_inventory(
        self,
        uid,
        name,
        category,
        stock,
        purchase_price,
        sale_price,
        totalpurch,
        description,
        image,
    ):
        return self.model.update(
            uid,
            name,
            category,
            stock,
            purchase_price,
            sale_price,
            totalpurch,
            description,
            image,
        )

    def delete_inventory(self, uid):
        return self.model.delete(uid)

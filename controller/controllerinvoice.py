# controller_register.py

from PyQt5.QtWidgets import QMessageBox

from models.modelinvoice import ModelInvoice


class InvoiceController:
    def __init__(self, view):
        self.model = ModelInvoice()
        self.view = view

    def register(self, user, client, total, code):
        self.model.register(user, client, total, code)

    def register_item(self, product_id, product_quantity, product_total, code):
        self.model.register_item(product_id, product_quantity, product_total, code)

    def get_invoice_graph(self):
        return self.model.get_invoice_graph()

    def get_user(self, id_user):
        return self.model.get_user(id_user)

    def get(self):
        return self.model.get()

    def delete(self, uid):
        return self.model.delete(uid)

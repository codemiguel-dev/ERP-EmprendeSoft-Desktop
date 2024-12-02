# controller_register.py

from PyQt5.QtWidgets import QMessageBox

from models.modeltransaction import ModelTransaction


class TransactionController:
    def __init__(self, view):
        self.model = ModelTransaction()
        self.view = view

    def register(self, id_transaction, amount, type_transaction, entity, type_pay):
        self.model.register(id_transaction, amount, type_transaction, entity, type_pay)

    def get(self):
        return self.model.get()

    def update(self, uid, date, amount, type_transaction, entity, type_payment):
        return self.model.update(
            uid, date, amount, type_transaction, entity, type_payment
        )

    def delete(self, uid):
        return self.model.delete(uid)

    def get_transaction_graph(self):
        return self.model.get_transaction_graph()

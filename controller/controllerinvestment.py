# controller_register.py

from PyQt5.QtWidgets import QMessageBox

from models.modelinvestment import ModelInvestment


class InvestmentController:
    def __init__(self, view):
        self.model = ModelInvestment()
        self.view = view

    def register(self, types, amount, amount_end, yields, date):
        self.model.register(types, amount, amount_end, yields, date)

    def get(self):
        return self.model.get()

    def get_graphi(self):
        return self.model.get_graphi()

    def update(self, uid, types, amount, amount_end, yields, date_expiration):
        return self.model.update(
            uid, types, amount, amount_end, yields, date_expiration
        )

    def delete(self, uid):
        return self.model.delete(uid)

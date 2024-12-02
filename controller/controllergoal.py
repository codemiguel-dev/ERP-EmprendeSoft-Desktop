# controller_register.py

from PyQt5.QtWidgets import QMessageBox

from models.modelgoal import ModelGoal


class GoalController:
    def __init__(self, view):
        self.model = ModelGoal()
        self.view = view

    def register(self, business_id, name, description, status, start_date, end_date):
        self.model.register(
            business_id, name, description, status, start_date, end_date
        )

    def get(self):
        return self.model.get()

    def update(self, uid, name, descripcion, start_date, end_date):
        return self.model.update(uid, name, descripcion, start_date, end_date)

    def delete(self, uid):
        return self.model.delete(uid)

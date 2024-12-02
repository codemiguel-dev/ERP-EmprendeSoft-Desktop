# controller_register.py

from PyQt5.QtWidgets import QMessageBox

from models.modelemployee import ModelEmployee


class EmployeeController:
    def __init__(self, view):
        self.model = ModelEmployee()
        self.view = view

    def register(self, user_id, job):
        self.model.register(user_id, job)

    def get(self):
        return self.model.get()

    def update(self, uid, user_id, id_employee, job):
        return self.model.update(uid, user_id, id_employee, job)

    def delete(self, uid):
        return self.model.delete(uid)

# controller_register.py

from PyQt5.QtWidgets import QMessageBox

from models.modelreport import ModelReport


class ReportController:
    def __init__(self, view):
        self.model = ModelReport()
        self.view = view

    def register(self, id_user, name, type_report, description, file_name):
        self.model.register(id_user, name, type_report, description, file_name)

    def get(self):
        return self.model.get()

    def update(self, uid, name, descripcion, start_date, end_date):
        return self.model.update(uid, name, descripcion, start_date, end_date)

    def delete(self, uid):
        return self.model.delete(uid)

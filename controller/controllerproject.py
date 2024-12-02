# controller_register.py

from PyQt5.QtWidgets import QMessageBox

from models.modelproject import ModelProject


class ProjectController:
    def __init__(self, view):
        self.model = ModelProject()
        self.view = view

    def register(self, name, description, budget, status, type_project):
        self.model.register(name, description, budget, status, type_project)

    def get(self):
        return self.model.get()

    def update(self, uid, name, description, budget, status, type_project):
        return self.model.update(uid, name, description, budget, status, type_project)

    def delete(self, uid):
        return self.model.delete(uid)

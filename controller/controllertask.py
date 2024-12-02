# controller_register.py

from PyQt5.QtWidgets import QMessageBox

from models.modeltask import ModelTask


class TaskController:
    def __init__(self, view):
        self.model = ModelTask()
        self.view = view

    def register(self, user_id, name, description, status):
        self.model.register(user_id, name, description, status)

    def get(self):
        return self.model.get()

    def update(self, id_task, user_id, name, description, status):
        return self.model.update(id_task, user_id, name, description, status)

    def delete(self, id_task):
        return self.model.delete(id_task)

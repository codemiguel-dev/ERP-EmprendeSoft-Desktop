# controller_register.py

from PyQt5.QtWidgets import QMessageBox

from models.modeluser import ModelUser


class UserController:
    def __init__(self, view):
        self.model = ModelUser()
        self.view = view

    def register(self, name, email, fono, address, password, role, image):
        self.model.register(name, email, fono, address, password, role, image)

    def get_user(self):
        return self.model.get_user()

    def update_user(self, uid, name, password, email, fono, address, role, image):
        return self.model.update(uid, name, password, email, fono, address, role, image)

    def delete_user(self, uid):
        return self.model.delete(uid)

    def search_user(self, uid):
        return self.model.get_user_by_id(uid)

    def update_profile(self, uid, name, email, phone, password):
        return self.model.update_profile(uid, name, email, phone, password)

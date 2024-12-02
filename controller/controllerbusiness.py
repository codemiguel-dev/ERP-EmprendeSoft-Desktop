# controller_register.py

from PyQt5.QtWidgets import QMessageBox

from models.modelbusiness import ModelBusiness


class BusinessController:
    def __init__(self, view):
        self.model = ModelBusiness()
        self.view = view

    def register(
        self,
        address_id,
        name,
        image,
        legal_form,
        industry,
        registration_number,
        founding_date,
    ):
        self.model.register(
            address_id,
            name,
            image,
            legal_form,
            industry,
            registration_number,
            founding_date,
        )

    def register_gain(self, gain):
        self.model.register_gain(gain)

    def get_graphi(self):
        return self.model.get_graphi()

    def get(self):
        return self.model.get()

    def update(
        self,
        id_goal,
        name,
        num_legal,
        industry,
        num_register,
        date_founding,
        address,
        image,
    ):
        return self.model.update(
            id_goal,
            name,
            num_legal,
            industry,
            num_register,
            date_founding,
            address,
            image,
        )

    def delete(self, uid):
        return self.model.delete(uid)

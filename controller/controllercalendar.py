# controller_register.py

from PyQt5.QtWidgets import QMessageBox

from models.modelcalendar import ModelCalendar


class CalendarController:
    def __init__(self, view):
        self.model = ModelCalendar()
        self.view = view

    def register(self, employee, start_time, end_time, horary):
        self.model.register(employee, start_time, end_time, horary)

    def get(self):
        return self.model.get()

    def update(self, uid, employee, start_time, end_time, horary):
        return self.model.update(uid, employee, start_time, end_time, horary)

    def delete(self, uid):
        return self.model.delete(uid)

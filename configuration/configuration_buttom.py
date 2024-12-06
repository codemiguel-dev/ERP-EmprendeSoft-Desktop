# configuraciones_gui.py
from PyQt5.QtGui import QIcon


def icon_configurate_manager(self):
    self.btn_icon.setIcon(QIcon("img/icon.png"))
    self.btn_add.setIcon(QIcon("img/add.png"))
    self.btn_update.setIcon(QIcon("img/update.png"))
    self.btn_delete.setIcon(QIcon("img/delete.png"))
    self.btn_get.setIcon(QIcon("img/update_table.png"))


def icon_configurate_top(self):
    self.bt_minimizar.setIcon(QIcon("img/minus.svg"))
    self.bt_restaurar.setIcon(QIcon("img/chevron-up.svg"))
    self.bt_maximizar.setIcon(QIcon("img/chevron-down.svg"))
    self.bt_cerrar.setIcon(QIcon("img/x.svg"))


def icon_configurate_exit_session(self):
    self.bt_exit_session.setIcon(QIcon("img/exit_session.svg"))


def icon_exit_program(self):
    self.btn_exit.setIcon(QIcon("img/power-off-svgrepo-com.svg"))


def icon_excel(self):
    self.btn_excel.setIcon(QIcon("img/excel.png"))

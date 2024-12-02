def control_bt_minimizar(self):
    self.showMinimized()


def control_bt_normal(self):
    self.showNormal()
    self.bt_restaurar.hide()
    self.bt_maximizar.show()


def control_bt_maximizar(self):
    self.showMaximized()
    self.bt_maximizar.hide()
    self.bt_restaurar.show()

import sys
import random
import functools

from PySide6.QtGui import QPixmap, QImage, QColor, QRegularExpressionValidator, QIntValidator, QDoubleValidator
from PySide6.QtWidgets import QMainWindow, QApplication, QGraphicsScene, QGraphicsPixmapItem, QDialog
from PySide6.QtCore import QElapsedTimer, QRegularExpression, QThread, Signal, QLocale
from camera_parameters_dialog import Ui_CameraDataDialog


class CameraDataDialog(QDialog):
    def __init__(self, parent):  # camera_position_x, camera_position_y, camera_position_z, field_of_view
        super(CameraDataDialog, self).__init__()
        self.ui = Ui_CameraDataDialog()
        self.ui.setupUi(self)

        # Set validations
        validation = QDoubleValidator(decimals=2)
        validation.setNotation(QDoubleValidator.Notation.StandardNotation)
        validation.setLocale(QLocale(QLocale.English))
        self.ui.position_x_line.setValidator(validation)
        self.ui.position_y_line.setValidator(validation)
        self.ui.position_z_line.setValidator(validation)
        self.ui.field_of_view_line.setValidator(validation)

        # data value
        self._camera_position_x: float = 0.0
        self._camera_position_y: float = 0.0
        self._camera_position_z: float = 0.0
        self._field_of_view: float = 90.0

        # connections
        self.ui.accept_button.clicked.connect(self.accept_button_clicked)

    def accept_button_clicked(self):
        self._camera_position_x = float(self.ui.position_x_line.text())
        self._camera_position_y = float(self.ui.position_y_line.text())
        self._camera_position_z = float(self.ui.position_z_line.text())
        self._field_of_view = float(self.ui.field_of_view_line.text())
        self.close()

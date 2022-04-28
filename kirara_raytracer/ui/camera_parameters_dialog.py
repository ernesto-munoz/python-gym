# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'camera_parameters_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.3.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_CameraDataDialog(object):
    def setupUi(self, CameraDataDialog):
        if not CameraDataDialog.objectName():
            CameraDataDialog.setObjectName(u"CameraDataDialog")
        CameraDataDialog.resize(218, 132)
        self.verticalLayout = QVBoxLayout(CameraDataDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(CameraDataDialog)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.position_x_line = QLineEdit(CameraDataDialog)
        self.position_x_line.setObjectName(u"position_x_line")
        self.position_x_line.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.position_x_line.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_2.addWidget(self.position_x_line)

        self.position_y_line = QLineEdit(CameraDataDialog)
        self.position_y_line.setObjectName(u"position_y_line")
        self.position_y_line.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.position_y_line.setFrame(True)
        self.position_y_line.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.position_y_line.setClearButtonEnabled(False)

        self.horizontalLayout_2.addWidget(self.position_y_line)

        self.position_z_line = QLineEdit(CameraDataDialog)
        self.position_z_line.setObjectName(u"position_z_line")
        self.position_z_line.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.position_z_line.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_2.addWidget(self.position_z_line)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_6 = QLabel(CameraDataDialog)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_6.addWidget(self.label_6)

        self.field_of_view_line = QLineEdit(CameraDataDialog)
        self.field_of_view_line.setObjectName(u"field_of_view_line")
        self.field_of_view_line.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.field_of_view_line.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_6.addWidget(self.field_of_view_line)


        self.verticalLayout.addLayout(self.horizontalLayout_6)

        self.accept_button = QPushButton(CameraDataDialog)
        self.accept_button.setObjectName(u"accept_button")

        self.verticalLayout.addWidget(self.accept_button)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.retranslateUi(CameraDataDialog)

        QMetaObject.connectSlotsByName(CameraDataDialog)
    # setupUi

    def retranslateUi(self, CameraDataDialog):
        CameraDataDialog.setWindowTitle(QCoreApplication.translate("CameraDataDialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("CameraDataDialog", u"Position", None))
        self.position_x_line.setText(QCoreApplication.translate("CameraDataDialog", u"0.0", None))
        self.position_y_line.setText(QCoreApplication.translate("CameraDataDialog", u"0.0", None))
        self.position_z_line.setText(QCoreApplication.translate("CameraDataDialog", u"0.0", None))
        self.label_6.setText(QCoreApplication.translate("CameraDataDialog", u"FOV", None))
        self.field_of_view_line.setText(QCoreApplication.translate("CameraDataDialog", u"90.0", None))
        self.accept_button.setText(QCoreApplication.translate("CameraDataDialog", u"Accept", None))
    # retranslateUi


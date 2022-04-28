# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'render_view_window.ui'
##
## Created by: Qt User Interface Compiler version 6.3.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QLabel,
    QLineEdit, QMainWindow, QMenu, QMenuBar,
    QProgressBar, QPushButton, QSizePolicy, QSpacerItem,
    QStatusBar, QVBoxLayout, QWidget)

from viewport_graphics_view import ViewportGraphicsView
import render_view_window_rc

class Ui_RenderViewWindow(object):
    def setupUi(self, RenderViewWindow):
        if not RenderViewWindow.objectName():
            RenderViewWindow.setObjectName(u"RenderViewWindow")
        RenderViewWindow.resize(1197, 706)
        self.centralwidget = QWidget(RenderViewWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.camera_parameters_button = QPushButton(self.centralwidget)
        self.camera_parameters_button.setObjectName(u"camera_parameters_button")
        icon = QIcon()
        icon.addFile(u":/images/resources/camera_icon.png", QSize(), QIcon.Normal, QIcon.Off)
        self.camera_parameters_button.setIcon(icon)

        self.horizontalLayout.addWidget(self.camera_parameters_button)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.resolution_combo_box = QComboBox(self.centralwidget)
        self.resolution_combo_box.addItem("")
        self.resolution_combo_box.addItem("")
        self.resolution_combo_box.addItem("")
        self.resolution_combo_box.addItem("")
        self.resolution_combo_box.addItem("")
        self.resolution_combo_box.addItem("")
        self.resolution_combo_box.setObjectName(u"resolution_combo_box")

        self.horizontalLayout.addWidget(self.resolution_combo_box)

        self.resolution_width_line = QLineEdit(self.centralwidget)
        self.resolution_width_line.setObjectName(u"resolution_width_line")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.resolution_width_line.sizePolicy().hasHeightForWidth())
        self.resolution_width_line.setSizePolicy(sizePolicy)
        self.resolution_width_line.setMinimumSize(QSize(0, 0))

        self.horizontalLayout.addWidget(self.resolution_width_line)

        self.x_label = QLabel(self.centralwidget)
        self.x_label.setObjectName(u"x_label")
        self.x_label.setEnabled(True)

        self.horizontalLayout.addWidget(self.x_label)

        self.resolution_height_line = QLineEdit(self.centralwidget)
        self.resolution_height_line.setObjectName(u"resolution_height_line")
        sizePolicy.setHeightForWidth(self.resolution_height_line.sizePolicy().hasHeightForWidth())
        self.resolution_height_line.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.resolution_height_line)

        self.render_button = QPushButton(self.centralwidget)
        self.render_button.setObjectName(u"render_button")
        self.render_button.setAutoFillBackground(False)
        icon1 = QIcon()
        icon1.addFile(u":/images/resources/icons8-play-64.png", QSize(), QIcon.Normal, QIcon.Off)
        self.render_button.setIcon(icon1)

        self.horizontalLayout.addWidget(self.render_button)

        self.horizontalLayout.setStretch(1, 10)

        self.horizontalLayout_2.addLayout(self.horizontalLayout)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.viewport_graphics_view = ViewportGraphicsView(self.centralwidget)
        self.viewport_graphics_view.setObjectName(u"viewport_graphics_view")

        self.verticalLayout.addWidget(self.viewport_graphics_view)

        self.render_progress_bar = QProgressBar(self.centralwidget)
        self.render_progress_bar.setObjectName(u"render_progress_bar")
        self.render_progress_bar.setValue(24)

        self.verticalLayout.addWidget(self.render_progress_bar)

        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 40)
        RenderViewWindow.setCentralWidget(self.centralwidget)
        self.menu_bar = QMenuBar(RenderViewWindow)
        self.menu_bar.setObjectName(u"menu_bar")
        self.menu_bar.setGeometry(QRect(0, 0, 1197, 22))
        self.menuFile = QMenu(self.menu_bar)
        self.menuFile.setObjectName(u"menuFile")
        RenderViewWindow.setMenuBar(self.menu_bar)
        self.status_bar = QStatusBar(RenderViewWindow)
        self.status_bar.setObjectName(u"status_bar")
        RenderViewWindow.setStatusBar(self.status_bar)

        self.menu_bar.addAction(self.menuFile.menuAction())

        self.retranslateUi(RenderViewWindow)

        QMetaObject.connectSlotsByName(RenderViewWindow)
    # setupUi

    def retranslateUi(self, RenderViewWindow):
        RenderViewWindow.setWindowTitle(QCoreApplication.translate("RenderViewWindow", u"Render View", None))
        self.camera_parameters_button.setText("")
        self.resolution_combo_box.setItemText(0, QCoreApplication.translate("RenderViewWindow", u"Custom", None))
        self.resolution_combo_box.setItemText(1, QCoreApplication.translate("RenderViewWindow", u"854 - 480", None))
        self.resolution_combo_box.setItemText(2, QCoreApplication.translate("RenderViewWindow", u"1024 - 576", None))
        self.resolution_combo_box.setItemText(3, QCoreApplication.translate("RenderViewWindow", u"1280 - 720", None))
        self.resolution_combo_box.setItemText(4, QCoreApplication.translate("RenderViewWindow", u"1920 - 1080", None))
        self.resolution_combo_box.setItemText(5, QCoreApplication.translate("RenderViewWindow", u"2560 - 1440", None))

        self.resolution_width_line.setText(QCoreApplication.translate("RenderViewWindow", u"64", None))
        self.x_label.setText(QCoreApplication.translate("RenderViewWindow", u"x", None))
        self.resolution_height_line.setText(QCoreApplication.translate("RenderViewWindow", u"64", None))
        self.render_button.setText("")
        self.menuFile.setTitle(QCoreApplication.translate("RenderViewWindow", u"File", None))
    # retranslateUi


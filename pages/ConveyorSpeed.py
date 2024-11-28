# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ConveyorSpeed.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

import sys
import os
from time import sleep
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtSql import QSqlDatabase, QSqlQuery


direction_in = "CW"
speed_in = 0


class Ui_SpeedWindow(object):

    # database connect 
    def db_connect(self):
        db_path = "/home/rekinsa/Documents/conveyorITERAv1/db/conveyordb"

        if not os.path.exists(db_path):
            print(f"Database file does not exist at: {db_path}")
            return None

        print(f"Database file found: {db_path}")

        # Initialize the database connection if not already done
        if not QSqlDatabase.contains("speed_connection"):
            self.db = QSqlDatabase.addDatabase("QSQLITE", "speed_connection")
            self.db.setDatabaseName(db_path)
        else:
            self.db = QSqlDatabase.database("speed_connection")

        # Attempt to open the database
        if not self.db.open():
            print(f"Failed to open database: {self.db.lastError().text()}")
            return None

        print("Database connected successfully!")
        return self.db

    def close_connection(self):
        if self.db and self.db.isOpen():
            self.db.close()
            print("Database connection closed.")
        else:
            print("No open database connection to close.")

    def db_insert(self):
        
        try:
            conn = self.db_connect()

            if conn:
                direction_v = str(self.DirValue.text())
                speed_v = int(self.SpeedValue.text())

                print(f"Direction: {direction_v}, Speed: {speed_v}")

                if speed_v and direction_v:
                    query = QSqlQuery(conn)

                    if not query.exec_("BEGIN TRANSACTION;"):
                        print("Error starting transaction:", query.lastError().text())

                    # Correct query syntax
                    insert = "INSERT INTO Speed (Direction, Speed) VALUES (?, ?)"
                    query.prepare(insert)
                    query.addBindValue(direction_v)
                    query.addBindValue(speed_v)

                    if query.exec_():
                        query.exec_("COMMIT;")
                        print("Data inserted successfully.")
                        # self.DirValue.clear()
                        # self.SpeedValue.clear()
                        query.finish()
                    else:
                        print("Error executing query:", query.lastError().text())

                    
                else:
                    print("No valid data to insert")
            else:
                print("Failed to connect to the database.")
        except Exception as e:
            print(f"Error: {e}")
            sleep(1)
        finally:
            self.close_connection()

    def btn_cw(self):
        global direction_in
        direction_in = "CW"
        self.DirValue.setText("CW")

    def btn_ccw(self):
        global direction_in
        direction_in = "CCW"
        self.DirValue.setText("CCW")

    def btn_up_speed(self):
        global speed_in

        if speed_in >= 0 and speed_in < 100:
            speed_in += 5 
            self.SpeedValue.setText(str(speed_in))

    def btn_down_speed(self):
        global speed_in
        if speed_in > 0 and speed_in <= 100:
            speed_in -= 5 
            self.SpeedValue.setText(str(speed_in))

    def center(self, window):
        screen = QtWidgets.QDesktopWidget().screenGeometry()
        size = window.geometry()
        x = (screen.width() - size.width()) // 2
        y = (screen.height() - size.height()) // 2
        window.move(x, y)

    def openMonitoringdWindow(self):
        from Conveyor1 import Ui_MonitoringWindow

        self.SpeedWindow.close() 
        sleep(0.1)

        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_MonitoringWindow()
        self.ui.setupUi(self.window)
        self.ui.center(self.window)
        self.window.show()

    def setupUi(self, SpeedWindow):
        SpeedWindow.setObjectName("SpeedWindow")
        SpeedWindow.resize(1024, 530)

        self.SpeedWindow = SpeedWindow

        self.centralwidget = QtWidgets.QWidget(SpeedWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox_Speed2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_Speed2.setGeometry(QtCore.QRect(450, 10, 451, 271))
        self.groupBox_Speed2.setObjectName("groupBox_Speed2")
        self.SpeedGraph2 = QtWidgets.QWidget(self.groupBox_Speed2)
        self.SpeedGraph2.setGeometry(QtCore.QRect(0, 20, 451, 301))
        self.SpeedGraph2.setStyleSheet("background-color: rgb(61, 56, 70);")
        self.SpeedGraph2.setObjectName("SpeedGraph2")
        self.groupBoxMenu = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBoxMenu.setGeometry(QtCore.QRect(910, 10, 101, 501))
        self.groupBoxMenu.setObjectName("groupBoxMenu")

        self.BtnMonitoring = QtWidgets.QPushButton(self.groupBoxMenu)
        self.BtnMonitoring.setGeometry(QtCore.QRect(10, 30, 80, 115))
        font = QtGui.QFont()
        font.setKerning(True)
        self.BtnMonitoring.setFont(font)
        self.BtnMonitoring.setAutoFillBackground(False)
        self.BtnMonitoring.setStyleSheet("background-color: rgb(143, 240, 164);")
        self.BtnMonitoring.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../icons/icons8-monitoring-100.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.BtnMonitoring.setIcon(icon)
        self.BtnMonitoring.setIconSize(QtCore.QSize(50, 50))
        self.BtnMonitoring.setShortcut("")
        self.BtnMonitoring.setCheckable(False)
        self.BtnMonitoring.setObjectName("BtnMonitoring")

        self.BtnMonitoring.clicked.connect(self.openMonitoringdWindow)

        self.ExitBtn = QtWidgets.QPushButton(self.groupBoxMenu)
        self.ExitBtn.setGeometry(QtCore.QRect(10, 390, 80, 101))
        self.ExitBtn.setStyleSheet("background-color: rgb(246, 97, 81);")
        self.ExitBtn.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("../icons/icons8-exit-100.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ExitBtn.setIcon(icon1)
        self.ExitBtn.setIconSize(QtCore.QSize(50, 50))
        self.ExitBtn.setObjectName("ExitBtn")

        # self.ExitBtn.clicked.connect(SpeedWindow.close)
        self.ExitBtn.clicked.connect(self.pop_up_exit)

        self.groupBoxSpeed2_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBoxSpeed2_2.setGeometry(QtCore.QRect(450, 290, 451, 221))
        self.groupBoxSpeed2_2.setObjectName("groupBoxSpeed2_2")
        self.labelSpeed = QtWidgets.QLabel(self.groupBoxSpeed2_2)
        self.labelSpeed.setGeometry(QtCore.QRect(0, 20, 451, 201))
        font = QtGui.QFont()
        font.setFamily("Sans Serif")
        font.setPointSize(50)
        font.setBold(True)
        font.setWeight(75)
        self.labelSpeed.setFont(font)
        self.labelSpeed.setFocusPolicy(QtCore.Qt.NoFocus)
        self.labelSpeed.setAlignment(QtCore.Qt.AlignCenter)
        self.labelSpeed.setObjectName("labelSpeed")
        self.groupBoxSpeed2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBoxSpeed2.setGeometry(QtCore.QRect(10, 10, 421, 131))
        self.groupBoxSpeed2.setObjectName("groupBoxSpeed2")
        self.SpeedValue = QtWidgets.QLineEdit(self.groupBoxSpeed2)
        self.SpeedValue.setGeometry(QtCore.QRect(10, 30, 201, 91))
        font = QtGui.QFont()
        font.setFamily("Sans Serif")
        font.setPointSize(30)
        font.setBold(True)
        font.setWeight(75)

        self.SpeedValue.setFont(font)
        self.SpeedValue.setAlignment(QtCore.Qt.AlignCenter)
        self.SpeedValue.setObjectName("SpeedValue")

        self.BtnUpSpeed = QtWidgets.QPushButton(self.groupBoxSpeed2)
        self.BtnUpSpeed.setGeometry(QtCore.QRect(220, 30, 88, 91))
        self.BtnUpSpeed.setText("")

        self.BtnUpSpeed.clicked.connect(self.btn_up_speed)

        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("../icons/icons8-up-100.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.BtnUpSpeed.setIcon(icon2)
        self.BtnUpSpeed.setIconSize(QtCore.QSize(50, 50))
        self.BtnUpSpeed.setObjectName("BtnUpSpeed")
        self.BtnDownSpeed = QtWidgets.QPushButton(self.groupBoxSpeed2)
        self.BtnDownSpeed.setGeometry(QtCore.QRect(320, 30, 88, 91))
        self.BtnDownSpeed.setText("")

        self.BtnDownSpeed.clicked.connect(self.btn_down_speed)

        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("../icons/icons8-down-arrow-100.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.BtnDownSpeed.setIcon(icon3)
        self.BtnDownSpeed.setIconSize(QtCore.QSize(50, 50))
        self.BtnDownSpeed.setObjectName("BtnDownSpeed")

        self.groupBoxDirection = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBoxDirection.setGeometry(QtCore.QRect(10, 150, 421, 131))
        self.groupBoxDirection.setObjectName("groupBoxDirection")
        self.DirValue = QtWidgets.QLineEdit(self.groupBoxDirection)
        self.DirValue.setGeometry(QtCore.QRect(10, 30, 201, 91))
        font = QtGui.QFont()
        font.setFamily("Sans Serif")
        font.setPointSize(30)
        font.setBold(True)
        font.setWeight(75)
        self.DirValue.setFont(font)
        self.DirValue.setAlignment(QtCore.Qt.AlignCenter)
        self.DirValue.setObjectName("DirValue")

        self.BtnCCW = QtWidgets.QPushButton(self.groupBoxDirection)
        self.BtnCCW.setGeometry(QtCore.QRect(220, 30, 88, 91))
        self.BtnCCW.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("../icons/icons8-left-arrow-100.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.BtnCCW.setIcon(icon4)
        self.BtnCCW.setIconSize(QtCore.QSize(50, 50))
        self.BtnCCW.setObjectName("BtnCCW")

        self.BtnCCW.clicked.connect(self.btn_ccw)

        self.BtnCW = QtWidgets.QPushButton(self.groupBoxDirection)
        self.BtnCW.setGeometry(QtCore.QRect(320, 30, 88, 91))
        self.BtnCW.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("../icons/icons8-right-arrow-100.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.BtnCW.setIcon(icon5)
        self.BtnCW.setIconSize(QtCore.QSize(50, 50))
        self.BtnCW.setObjectName("BtnCW")

        self.BtnCW.clicked.connect(self.btn_cw)

        self.BtnSave = QtWidgets.QPushButton(self.centralwidget)
        self.BtnSave.setGeometry(QtCore.QRect(10, 450, 431, 61))
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("../icons/icons8-save-100.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.BtnSave.setIcon(icon6)
        self.BtnSave.setIconSize(QtCore.QSize(30, 30))
        self.BtnSave.setObjectName("BtnSave")

        # self.BtnSave.clicked.connect(self.db_insert)
        self.BtnSave.clicked.connect(self.pop_up_save)

        SpeedWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(SpeedWindow)
        QtCore.QMetaObject.connectSlotsByName(SpeedWindow)

    def retranslateUi(self, SpeedWindow):
        global speed_in
        global direction_in
        _translate = QtCore.QCoreApplication.translate
        SpeedWindow.setWindowTitle(_translate("SpeedWindow", "Controls - Speed"))
        self.groupBox_Speed2.setTitle(_translate("SpeedWindow", "Speed Graph"))
        self.groupBoxMenu.setTitle(_translate("SpeedWindow", "Menu"))
        self.groupBoxSpeed2_2.setTitle(_translate("SpeedWindow", "Speed"))
        self.labelSpeed.setText(_translate("SpeedWindow", "20Rpm"))
        self.groupBoxSpeed2.setTitle(_translate("SpeedWindow", "Speed"))
        self.SpeedValue.setText(_translate("SpeedWindow", str(speed_in)))
        self.groupBoxDirection.setTitle(_translate("SpeedWindow", "Direction"))
        self.DirValue.setText(_translate("SpeedWindow", direction_in))
        self.BtnSave.setText(_translate("SpeedWindow", "    Save"))

    def pop_up_save(self):
        msg = QMessageBox()
        msg.setWindowTitle("Info")
        msg.setText("Save data ?")
        msg.setInformativeText("Are you sure?")
        msg.setIcon(QMessageBox.Question)
        msg.resize(600, 400)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        msg.setDefaultButton(QMessageBox.Yes)

        # msg.buttonClicked.connect(self.db_insert)   

        x = msg.exec_()

        if x == QMessageBox.Yes:
            self.db_insert()
            print("yes")
        else:
            print("canceled")

    def pop_up_exit(self):
        msg = QMessageBox()
        msg.setWindowTitle("Info")
        msg.setText("Exit ?")
        msg.setInformativeText("Are you sure?")
        msg.setIcon(QMessageBox.Question)
        msg.resize(600, 400)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        msg.setDefaultButton(QMessageBox.Yes)

        # msg.buttonClicked.connect(TempWindow.close)

        x = msg.exec_()

        if x == QMessageBox.Yes:
            self.SpeedWindow.close()
            print("yes")
        else:
            print("canceled")


if __name__ == "__main__":
    while True:
        app = QtWidgets.QApplication(sys.argv)
        SpeedWindow = QtWidgets.QMainWindow()
        ui = Ui_SpeedWindow()
        ui.setupUi(SpeedWindow)
        ui.center(SpeedWindow)
        ui.db_connect()
        SpeedWindow.show()
        sys.exit(app.exec_())


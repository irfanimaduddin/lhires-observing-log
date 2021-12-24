from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *

from lhires_log import Ui_MainWindow
from function import GetFunction, MsgFunction

import pandas as pd
import sys

class Main_Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(Main_Window, self).__init__(parent)
        self.setupUi(self)

        self.data = pd.DataFrame(columns=['utctime', 'datatype', 'objname', 'filename', 'bin', 'exptime', 'N', 'ambtemp', 'ambhum', 'skycond', 'comment'])
        GetFunction.gettable(self)

        self.datatype_form.activated.connect(lambda: self.checked_datatype_value())      
        self.nightmode_check.stateChanged.connect(lambda: self.checked_nightmode())      

        self.startlog_button.clicked[bool].connect(lambda: self.clicked_start_button())
        self.updatelog_button.clicked[bool].connect(lambda: self.clicked_update_button())
        self.savelog_button.clicked[bool].connect(lambda: self.clicked_endsave_button())
        self.resetlog_button.clicked[bool].connect(lambda: self.clicked_reset_button())
        self.closewindow_button.clicked.connect(lambda: self.clicked_close_button())

    def closeEvent(self, event):
        result = QMessageBox.question(self, "Confirm Exit...", "Are you sure you want to exit?", QMessageBox.Yes| QMessageBox.No, QMessageBox.No)
        event.ignore()
        if result == QMessageBox.Yes:
            if self.data.empty:
                event.accept()
            elif (self.data['datatype'][0] == 'Start') & (self.data['datatype'][len(self.data)-1] != 'End'):
                MsgFunction.notsaved()
    
    def clicked_start_button(self):
        if self.feature_form.text() == '':
            MsgFunction.emptyfeature()
        elif self.observer_form.toPlainText() == '':
            MsgFunction.emptyobserver()
        else:
            confirm_msg = QMessageBox()
            confirm_msg.setWindowTitle("Confirmation Box.")
            confirm_msg.setText("Are you sure want to start the logger?")
            confirm_msg.setIcon(QMessageBox.Question)
            confirm_msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            confirm_msg.setDefaultButton(QMessageBox.No)
            x = confirm_msg.exec_()
            if x == QMessageBox.Yes:
                GetFunction.getstart(self)
            else:
                pass                

    def clicked_update_button(self):
        if self.datatype_form.currentIndex() == 0:
            if self.filename_form.text() == '':
                MsgFunction.emptyfilename()
            elif self.objname_form.text() == '':
                MsgFunction.emptyobject()
            else:
                confirm_msg = QMessageBox()
                confirm_msg.setWindowTitle("Confirmation Box.")
                confirm_msg.setText("Are you sure want to update the log?")
                confirm_msg.setIcon(QMessageBox.Question)
                confirm_msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                confirm_msg.setDefaultButton(QMessageBox.No)
                x = confirm_msg.exec_()
                if x == QMessageBox.Yes:
                    GetFunction.getupdate(self)
                else:
                    pass
        else:
            if self.filename_form.text() == '':
                MsgFunction.emptyfilename()
            else:
                confirm_msg = QMessageBox()
                confirm_msg.setWindowTitle("Confirmation Box.")
                confirm_msg.setText("Are you sure want to update the log?")
                confirm_msg.setIcon(QMessageBox.Question)
                confirm_msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                confirm_msg.setDefaultButton(QMessageBox.No)
                x = confirm_msg.exec_()
                if x == QMessageBox.Yes:
                    self.objname_form.setText('')
                    GetFunction.getupdate(self)
                else:
                    pass

    def clicked_endsave_button(self):
        if self.feature_form.text() == '':
            MsgFunction.emptyfeature()
        elif self.observer_form.toPlainText() == '':
            MsgFunction.emptyobserver()
        else:
            confirm_msg = QMessageBox()
            confirm_msg.setWindowTitle("Confirmation Box.")
            confirm_msg.setText("Are you sure want to end and save the log?")
            confirm_msg.setIcon(QMessageBox.Question)
            confirm_msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            confirm_msg.setDefaultButton(QMessageBox.No)
            x = confirm_msg.exec_()
            if x == QMessageBox.Yes:
                GetFunction.getendsave(self)
            else:
                pass
            
    def clicked_reset_button(self):
        confirm_msg = QMessageBox()
        confirm_msg.setWindowTitle("Warning!")
        confirm_msg.setText("Are you sure want to reset the log?")
        confirm_msg.setIcon(QMessageBox.Warning)
        confirm_msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        confirm_msg.setDefaultButton(QMessageBox.No)
        x = confirm_msg.exec_()
        if x == QMessageBox.Yes:
            GetFunction.getreset(self)
        else:
            pass

    def clicked_close_button(self):
        if self.data.empty:
            QApplication.quit()
        elif (self.data['datatype'][0] == 'Start') & (self.data['datatype'][len(self.data)-1] != 'End'):
            MsgFunction.notsaved()
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Information")
            msg.setText("Thank you for using the software.")
            msg.setIcon(QMessageBox.Information)
            msg.setStandardButtons(QMessageBox.Ok)
            msg.setDefaultButton(QMessageBox.Ok)
            x = msg.exec_()
            QApplication.quit()

    def checked_datatype_value(self):
        if self.datatype_form.currentIndex() == 0:
            self.objname_form.setEnabled(True)
        else:
            self.objname_form.setEnabled(False)
    
    def checked_nightmode(self):
        if self.nightmode_check.isChecked():
            dark_palette = QtGui.QPalette()
            dark_palette.setColor(QtGui.QPalette.Window, QtGui.QColor(53, 53, 53))
            dark_palette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.white)
            dark_palette.setColor(QtGui.QPalette.Base, QtGui.QColor(35, 35, 35))
            dark_palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(53, 53, 53))
            dark_palette.setColor(QtGui.QPalette.ToolTipBase, QtGui.QColor(25, 25, 25))
            dark_palette.setColor(QtGui.QPalette.ToolTipText, QtCore.Qt.white)
            dark_palette.setColor(QtGui.QPalette.Text, QtCore.Qt.white)
            dark_palette.setColor(QtGui.QPalette.Button, QtGui.QColor(53, 53, 53))
            dark_palette.setColor(QtGui.QPalette.ButtonText, QtCore.Qt.white)
            dark_palette.setColor(QtGui.QPalette.BrightText, QtCore.Qt.red)
            dark_palette.setColor(QtGui.QPalette.Link, QtGui.QColor(42, 130, 218))
            dark_palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(42, 130, 218))
            dark_palette.setColor(QtGui.QPalette.HighlightedText, QtGui.QColor(35, 35, 35))
            dark_palette.setColor(QtGui.QPalette.Active, QtGui.QPalette.Button, QtGui.QColor(53, 53, 53))
            dark_palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, QtCore.Qt.darkGray)
            dark_palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, QtCore.Qt.darkGray)
            dark_palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.Text, QtCore.Qt.darkGray)
            dark_palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.Light, QtGui.QColor(53, 53, 53))
            QApplication.setPalette(dark_palette)
        else:
            QApplication.setPalette(self.default_palette)


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    MainWindow = Main_Window()

    icon = QtGui.QIcon("logo.ico")
    icon.addPixmap(QtGui.QPixmap("logo.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    tray = QSystemTrayIcon()
    tray.setIcon(icon)
    tray.setToolTip("LHIRES Telescope Data Logger")
    tray.setVisible(True)

    MainWindow.show()

    sys.exit(app.exec_())

if __name__ == '__main__': main()
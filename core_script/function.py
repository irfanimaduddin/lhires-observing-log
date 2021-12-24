from PyQt5 import QtCore
from PyQt5.QtWidgets import *

import numpy as np
import pandas as pd
import re

class pandasModel(QtCore.QAbstractTableModel):

    def __init__(self, data):
        QtCore.QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parnet=None):
        return self._data.shape[1]

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if index.isValid():
            if role == QtCore.Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self._data.columns[col]
        return None


class GetFunction():
    def gettable(self):
        self.model = pandasModel(self.data)
        self.tableview.setModel(self.model)

    def getstart(self):
        self.datatype_form.setEnabled(True)
        lambda: self.datatype_form.setCurrentIndex(0)
        self.objname_form.setEnabled(True)
        self.filename_form.setEnabled(True)
        self.bin_form.setEnabled(True)
        self.exptime_form.setEnabled(True)
        self.nexp_form.setEnabled(True)
        self.updatelog_button.setEnabled(True)
        self.savelog_button.setEnabled(True)
        self.resetlog_button.setEnabled(True)
        self.startlog_button.setEnabled(False)

        utctime_value  = pd.Timestamp.utcnow().strftime('%H:%M:%S')
        groove_value   = self.groove_form.currentText()
        micro_setting_value = np.round(self.micro_setting_form.value(), 2)
        feature_value  = self.feature_form.text()
        observer_value = self.observer_form.toPlainText()
        ccdtemp_value  = np.round(self.ccdtemp_form.value(), 2)
        lamp_value     = self.lamp_form.currentText()
        datatype_value = 'Start'
        objname_value  = ''
        filename_value = ''
        bin_value      = ''
        exptime_value  = ''
        nexp_value    = ''
        ambtemp_value  = np.round(self.ambtemp_form.value(), 2)
        ambhum_value   = np.round(self.ambhum_form.value(), 2)
        skycond_value  = self.skycond_form.currentText()
        comment_value  = self.comment_form.text()

        self.general = [groove_value, micro_setting_value, feature_value, observer_value, ccdtemp_value, lamp_value]
        self.data_append  = [utctime_value, datatype_value, objname_value, filename_value, bin_value, exptime_value, nexp_value, ambtemp_value, ambhum_value, skycond_value, comment_value]
        self.data_app_ser = pd.Series(self.data_append, index=self.data.columns)
        self.data  = self.data.append(self.data_app_ser, ignore_index=True)
        GetFunction.gettable(self)

    def getupdate(self):
        utctime_value  = pd.Timestamp.utcnow().strftime('%H:%M:%S')
        datatype_value = self.datatype_form.currentText()
        objname_value  = self.objname_form.text()
        filename_value = self.filename_form.text()
        bin_value      = self.bin_form.currentText()
        exptime_value  = np.round(self.exptime_form.value(), 2)
        nexp_value     = int(self.nexp_form.value())
        ambtemp_value  = np.round(self.ambtemp_form.value(), 2)
        ambhum_value   = np.round(self.ambhum_form.value(), 2)
        skycond_value  = self.skycond_form.currentText()
        comment_value  = self.comment_form.text()

        self.data_append  = [utctime_value, datatype_value, objname_value, filename_value, bin_value, exptime_value, nexp_value, ambtemp_value, ambhum_value, skycond_value, comment_value]
        self.data_app_ser = pd.Series(self.data_append, index=self.data.columns)
        self.data  = self.data.append(self.data_app_ser, ignore_index=True)
        GetFunction.gettable(self)

        self.comment_form.setText('')
        self.objname_form.setText('')
        self.filename_form.setText('')
        self.exptime_form.setValue(0.)
        self.nexp_form.setValue(1)

    def getendsave(self):
        utctime_value  = pd.Timestamp.utcnow().strftime('%H:%M:%S')
        groove_value   = self.groove_form.currentText()
        micro_setting_value = np.round(self.micro_setting_form.value(), 2)
        feature_value  = self.feature_form.text()
        observer_value = self.observer_form.toPlainText()
        ccdtemp_value  = np.round(self.ccdtemp_form.value(), 2)
        lamp_value     = self.lamp_form.currentText()
        datatype_value = 'End'
        objname_value  = ''
        filename_value = ''
        bin_value      = ''
        exptime_value  = ''
        nexp_value    = ''
        ambtemp_value  = np.round(self.ambtemp_form.value(), 2)
        ambhum_value   = np.round(self.ambhum_form.value(), 2)
        skycond_value  = self.skycond_form.currentText()
        comment_value  = self.comment_form.text()
        
        if observer_value.find(r"[\t\n\d,']+") == -1:
            res = re.split(r"[\t\n\d,']+", observer_value)
            observer_value = ', '.join(res)
        else:
            observer_value = observer_value

        self.general = [groove_value, micro_setting_value, feature_value, observer_value, ccdtemp_value, lamp_value]
        self.data_append  = [utctime_value, datatype_value, objname_value, filename_value, bin_value, exptime_value, nexp_value, ambtemp_value, ambhum_value, skycond_value, comment_value]
        self.data_app_ser = pd.Series(self.data_append, index=self.data.columns)
        self.data  = self.data.append(self.data_app_ser, ignore_index=True)

        logdate = pd.Timestamp.utcnow().strftime('%Y%m%d')
        tomorrow = pd.Timestamp.utcnow() + pd.Timedelta(1, unit='day')
        tomorrow_date = tomorrow.strftime('%d')
        logfilename = f"{logdate}{tomorrow_date} - Log Pengamatan"
        name = QFileDialog.getSaveFileName(self, 'Save File', directory=f"C:/Users/User/Desktop/{logfilename}", filter='*.csv')
        if(name[0] == ''):
            pass
        else:
            GetFunction.gettable(self)

            datelog = pd.Timestamp.utcnow().strftime('%a, %b %d %Y')
            #Create a new Logbook file
            file = open(name[0], "w")
            file.write("############################################################################################################\n")
            file.write('                                    10" LHIRES TELESCOPE OBSERVATION LOG                                      \n')
            file.write("\n by: Irfan Imaduddin \n version: 2.0 \n contact: irfanimaduddin@gmail.com\n")
            file.write("============================================================================================================\n\n")
            #Save location and telescope parameters to logbook file
            file.write(f"Date of Observation: {datelog} \t\t\t\t\t\t\t\t\t\tObserver(s): {observer_value} \n")
            file.write("Observation location: Rumah Teleskop GOTO, Bosscha Observatory \n")
            file.write("- Longitude (deg): 107.61677 E \n- Latitude (deg): 6.82472 S \n- Altitude: 1327 m \n\n")
            file.write('10" LHIRES Telescope f/9.8\n')
            file.write('- OTA: Meade 10" f/9.8 (D = 254mm, F = 2500mm)\n')
            file.write(f"- Spectrograph: LHIRES III, centered on {feature_value} (micrometer= {micro_setting_value} mm, {groove_value})\n")
            file.write(f"- Comparison lamp: {lamp_value}\n")
            file.write(f"- CCD: SBIG ST-402ME \t T= {ccdtemp_value} °C\n")
            file.write("- Slit viewer: ZWO ASI120MM-S\n")
            file.write("\n\n")
            self.data.to_csv(file, sep=' ', index = False)
            file.close()

    def getreset(self):
        self.groove_form.setCurrentIndex(0)
        self.micro_setting_form.setValue(9.)
        self.feature_form.setText('')
        self.observer_form.setText('')
        self.ccdtemp_form.setValue(-10.)
        self.ambtemp_form.setValue(20.)
        self.ambhum_form.setValue(50.)
        self.skycond_form.setCurrentIndex(0)
        self.comment_form.setText('')
        self.datatype_form.setEnabled(False)
        self.datatype_form.setCurrentIndex(0)
        self.objname_form.setEnabled(False)
        self.objname_form.setText('')
        self.filename_form.setEnabled(False)
        self.filename_form.setText('')
        self.bin_form.setEnabled(False)
        self.bin_form.setCurrentIndex(0)
        self.exptime_form.setEnabled(False)
        self.exptime_form.setValue(0.)
        self.nexp_form.setEnabled(False)
        self.nexp_form.setValue(1)
        self.updatelog_button.setEnabled(False)
        self.savelog_button.setEnabled(False)
        self.resetlog_button.setEnabled(False)
        self.startlog_button.setEnabled(True)

        self.general = pd.DataFrame(columns=['groove', 'micro', 'feature', 'observer', 'ccdtemp'])
        self.data = pd.DataFrame(columns=['utctime', 'datatype', 'objname', 'filename', 'bin', 'exptime', 'N', 'ambtemp', 'ambhum', 'skycond', 'comment'])
        self.model = pandasModel(self.data)
        self.tableview.setModel(self.model)


class MsgFunction():
    def emptyfeature():
        msg = QMessageBox()
        msg.setWindowTitle("Error Found!")
        msg.setText("You haven't input the spectral feature.")
        msg.setIcon(QMessageBox.Critical)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setDefaultButton(QMessageBox.Ok)
        x = msg.exec_()

    def emptyobserver():
        msg = QMessageBox()
        msg.setWindowTitle("Error Found!")
        msg.setText("You haven't input observer name(s).")
        msg.setIcon(QMessageBox.Information)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setDefaultButton(QMessageBox.Ok)
        x = msg.exec_()

    def emptyfilename():
        msg = QMessageBox()
        msg.setWindowTitle("Error Found!")
        msg.setText("File name is empty.")
        msg.setIcon(QMessageBox.Critical)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setDefaultButton(QMessageBox.Ok)
        x = msg.exec_()
    
    def emptyobject():
        msg = QMessageBox()
        msg.setWindowTitle("Error Found!")
        msg.setText("Object name is empty.")
        msg.setIcon(QMessageBox.Critical)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setDefaultButton(QMessageBox.Ok)
        x = msg.exec_()
    
    def notsaved():
        msg = QMessageBox()
        msg.setWindowTitle("Error Found!")
        msg.setText("You haven't save the log file.")
        msg.setIcon(QMessageBox.Critical)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setDefaultButton(QMessageBox.Ok)
        x = msg.exec_()
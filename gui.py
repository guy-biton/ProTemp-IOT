import os
#from sqlite3.dbapi2 import Date
import sys
import random
# pip install pyqt5-tools
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from matplotlib.pyplot import get
BASE_PATH = os.path.abspath(os.path.dirname(__file__))
from init import *
from agent import Mqtt_client
import time
from icecream import ic
from datetime import datetime
import data_acq as da
import winsound
import winsound

import logging

# Gets or creates a logger
logger = logging.getLogger(__name__)

# set log level
logger.setLevel(logging.WARNING)

# define file handler and set formatter
file_handler = logging.FileHandler('logfile_gui.log')
formatter    = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
file_handler.setFormatter(formatter)

# add file handler to logger
logger.addHandler(file_handler)

# Logs
# Logs

def play_alarm_sound():
    try:
        winsound.Beep(1000, 500)
    except:
        pass


global WatMet
WatMet=True
def time_format():
    return f'{datetime.now()}  GUI|> '
ic.configureOutput(prefix=time_format)
ic.configureOutput(includeContext=False) # use True for including script file context file
# Creating Client name - should be unique
global clientname
r=random.randrange(1,10000) # for creating unique client ID
clientname="IOT_clientId-nXLMZeDcjH"+str(r)

def check(fnk):
    try:
        rz=fnk
    except:
        rz='NA'
    return rz

class MC(Mqtt_client):
    def __init__(self):
        super().__init__()
    def on_message(self, client, userdata, msg):
            global WatMet
            topic=msg.topic
            m_decode=str(msg.payload.decode("utf-8","ignore"))
            ic("message from:"+topic, m_decode)
            if 'Room_1' in topic:
                mainwin.airconditionDock.update_temp_Room(check(m_decode.split('Temperature: ')[1].split(' Humidity: ')[0]))
            if 'Common' in topic:
                mainwin.airconditionDock.update_temp_Room(check(m_decode.split('Temperature: ')[1].split(' Humidity: ')[0]))
            if 'Home' in topic:
                if WatMet:
                    mainwin.graphsDock.update_electricity_meter(check(m_decode.split('Electricity: ')[1].split(' Water: ')[0]))
                    WatMet = False
                else:
                    mainwin.graphsDock.update_water_meter(check(m_decode.split(' Water: ')[1]))
                    WatMet = True
            if 'alarm' in topic:
                mainwin.statusDock.update_mess_win(da.timestamp()+': ' + m_decode)
                if 'ALARM' in m_decode or 'WARNING' in m_decode:
                    play_alarm_sound()
            if 'Warehouse_Zone_A' in topic:
                temp_val = check(m_decode.split('Temperature: ')[1])
                mainwin.statusDock.vaccineTemp.setText(temp_val)


                try:
                    if float(temp_val) > -15: # Thaw Risk
                        mainwin.statusDock.vaccineTemp.setStyleSheet("color: red; font-weight: bold; font-size: 14px; background-color: #ffcccc;")
                    else:
                        mainwin.statusDock.vaccineTemp.setStyleSheet("color: blue; font-weight: bold; font-size: 14px;")
                except:
                    pass

            if 'Warehouse_Zone_B' in topic:
                mainwin.statusDock.foodTemp.setText(check(m_decode.split('Temperature: ')[1]))
            if 'Warehouse_Main' in topic:

                try:
                    temp = check(m_decode.split('Temperature: ')[1].split(' Humidity: ')[0])
                    hum = check(m_decode.split(' Humidity: ')[1])
                    mainwin.statusDock.ambientTemp.setText(temp)
                    mainwin.statusDock.ambientHum.setText(hum)
                except: pass
            if 'Power_Station' in topic:
                # From: Main_Power Electricity: 1.45
                try:
                    val = check(m_decode.split('Electricity: ')[1])
                    mainwin.statusDock.powerUsage.setText(val)
                except: pass
            if 'Warehouse_Backup' in topic:
                # Set temperature to: ON
                if 'Set temperature to:' in m_decode:
                    val = m_decode.split('Set temperature to: ')[1]
                    mainwin.statusDock.backupStatus.setText(val)



class ConnectionDock(QDockWidget):
    """Main """
    def __init__(self,mc):
        QDockWidget.__init__(self)
        self.mc = mc
        self.topic = comm_topic+'#'
        self.mc.set_on_connected_to_form(self.on_connected)
        self.eHostInput=QLineEdit()
        self.eHostInput.setInputMask('999.999.999.999')
        self.eHostInput.setText(broker_ip)
        self.ePort=QLineEdit()
        self.ePort.setValidator(QIntValidator())
        self.ePort.setMaxLength(4)
        self.ePort.setText(broker_port)
        self.eClientID=QLineEdit()
        global clientname
        self.eClientID.setText(clientname)
        self.eConnectButton=QPushButton("Connect", self)
        self.eConnectButton.setToolTip("click me to connect")
        self.eConnectButton.clicked.connect(self.on_button_connect_click)
        self.eConnectButton.setStyleSheet("background-color: red")

        self.eTopicInput = QLineEdit()
        self.eTopicInput.setText("pr/Smart/#")
        self.eTopicInput.setPlaceholderText("Topic Filter (e.g. #)")

        formLayot=QFormLayout()
        formLayot.addRow("Host",self.eHostInput )
        formLayot.addRow("Port",self.ePort )
        formLayot.addRow("Topic", self.eTopicInput)
        formLayot.addRow("",self.eConnectButton)
        widget = QWidget(self)
        widget.setLayout(formLayot)
        self.setTitleBarWidget(widget)
        self.setWidget(widget)
        self.setWindowTitle("Connect")

    def on_connected(self):
        self.eConnectButton.setStyleSheet("background-color: green")
        self.eConnectButton.setText('Connected')
        self.mc.subscribe_to(self.eTopicInput.text())

    def on_button_connect_click(self):
        self.mc.set_broker(self.eHostInput.text())
        self.mc.set_port(int(self.ePort.text()))
        self.mc.set_clientName(self.eClientID.text())
        self.mc.connect_to()
        self.mc.start_listening()

class StatusDock(QDockWidget):
    """Status """
    def __init__(self,mc):
        QDockWidget.__init__(self)
        self.mc = mc
        self.eRecMess=QTextEdit()
        self.eSubscribeButton = QPushButton("Subscribe",self)
        self.eSubscribeButton.clicked.connect(self.on_button_subscribe_click)

        self.eTestAlarmButton = QPushButton("TEST ALARM", self)
        self.eTestAlarmButton.clicked.connect(self.on_test_alarm_click)
        self.eTestAlarmButton.setStyleSheet("background-color: orange")

        # --- Vaccine Unit Section ---
        self.gbVaccine = QGroupBox("Vaccine Storage (Zone A)")
        self.gbVaccine.setStyleSheet("QGroupBox { font-weight: bold; border: 1px solid gray; border-radius: 5px; margin-top: 10px; } QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 3px 0 3px; }")
        v_layout = QFormLayout()
        self.vaccineTemp = QLabel("NA")
        self.vaccineTemp.setStyleSheet("color: blue; font-weight: bold; font-size: 14px;")
        v_layout.addRow("Temperature (°C):", self.vaccineTemp)
        self.gbVaccine.setLayout(v_layout)

        # --- Food Unit Section ---
        self.gbFood = QGroupBox("Food Storage (Zone B)")
        self.gbFood.setStyleSheet("QGroupBox { font-weight: bold; border: 1px solid gray; border-radius: 5px; margin-top: 10px; } QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 3px 0 3px; }")
        f_layout = QFormLayout()
        self.foodTemp = QLabel("NA")
        self.foodTemp.setStyleSheet("color: green; font-weight: bold; font-size: 14px;")
        f_layout.addRow("Temperature (°C):", self.foodTemp)
        self.gbFood.setLayout(f_layout)

        # --- Ambient Section ---
        self.gbAmbient = QGroupBox("Warehouse Ambient (Main)")
        self.gbAmbient.setStyleSheet("QGroupBox { font-weight: bold; border: 1px solid gray; border-radius: 5px; margin-top: 10px; } QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 3px 0 3px; }")
        a_layout = QFormLayout()
        self.ambientTemp = QLabel("NA")
        self.ambientHum = QLabel("NA")
        a_layout.addRow("Temperature (°C):", self.ambientTemp)
        a_layout.addRow("Humidity (%):", self.ambientHum)
        self.gbAmbient.setLayout(a_layout)

        # --- Power & Systems Section ---
        self.gbPower = QGroupBox("Power & Systems")
        self.gbPower.setStyleSheet("QGroupBox { font-weight: bold; border: 1px solid gray; border-radius: 5px; margin-top: 10px; } QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 3px 0 3px; }")
        p_layout = QFormLayout()
        self.powerUsage = QLabel("NA")
        self.powerUsage.setStyleSheet("color: red; font-weight: bold;")
        self.backupStatus = QLabel("OFF")
        self.backupStatus.setStyleSheet("color: green; font-weight: bold;")
        p_layout.addRow("Main Power (kW):", self.powerUsage)
        p_layout.addRow("Backup Cooler:", self.backupStatus)
        self.gbPower.setLayout(p_layout)

        # --- Main Layout ---
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.gbVaccine)
        mainLayout.addWidget(self.gbFood)
        mainLayout.addWidget(self.gbAmbient)
        mainLayout.addWidget(self.gbPower)

        # General Status
        self.wifi = QLabel("Normal")
        self.wifi.setStyleSheet("color: green")
        self.door = QLabel("Closed")
        self.door.setStyleSheet("color: green")

        gen_layout = QFormLayout()
        gen_layout.addRow("WI-Fi status:", self.wifi)
        gen_layout.addRow("Main Door:", self.door)
        mainLayout.addLayout(gen_layout)

        mainLayout.addWidget(QLabel("Alarm Messages:"))
        mainLayout.addWidget(self.eRecMess)
        mainLayout.addWidget(self.eSubscribeButton)
        mainLayout.addWidget(self.eTestAlarmButton)

        widget = QWidget(self)
        widget.setLayout(mainLayout)
        self.setTitleBarWidget(widget)
        self.setWidget(widget)
        self.setWindowTitle("ProTemp IOT Monitor")

    def on_button_subscribe_click(self):
        self.mc.subscribe_to(comm_topic+'alarm')
        self.eSubscribeButton.setStyleSheet("background-color: green")

    # create function that update text in received message window
    def update_mess_win(self,text):
        self.eRecMess.append(text)

    def on_button_publish_click(self):
        self.mc.publish_to(self.ePublisherTopic.text(), self.eMessageBox.toPlainText())
        self.ePublishButton.setStyleSheet("background-color: yellow")

    def on_test_alarm_click(self):
        play_alarm_sound()
        self.update_mess_win(da.timestamp() + ": TEST ALARM TRIGGERED")

# GraphsDock and PlotDock removed


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        # Init of Mqtt_client class
        # self.mc=Mqtt_client()
        self.mc=MC()
        # general GUI settings
        self.setUnifiedTitleAndToolBarOnMac(True)
        # set up main window
        self.setGeometry(30, 100, 800, 600)
        self.setWindowTitle('ProTemp IOT GUI')
        # Init QDockWidget objects
        self.connectionDock = ConnectionDock(self.mc)
        self.statusDock = StatusDock(self.mc)
        self.addDockWidget(Qt.TopDockWidgetArea, self.connectionDock)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.statusDock)

        # Auto-connect
        QTimer.singleShot(1000, self.connectionDock.on_button_connect_click)


if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        mainwin = MainWindow()
        mainwin.show()
        app.exec_()

    except:
        logger.exception("GUI Crash!")

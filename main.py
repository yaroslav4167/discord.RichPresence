from PyQt5 import QtCore, QtGui, QtWidgets, uic

from pypresence import Presence
from configmanager import ConfigManager
from rpcmanager import RPCManager
import os


class Ui_MainWindow(QtWidgets.QMainWindow):
    connected = False
    RPC = RPCManager()

    def __init__(self):
        self.config = ConfigManager()
        super(Ui_MainWindow, self).__init__()  # Call the inherited classes __init__ method
        file_from = self.resource_path('mainUI.ui')
        uic.loadUi(file_from, self)  # Load the .ui file
        self.show()  # Show the GUI

    def start_rpc(self):
        status = self.RPC.connect(self.lineEdit.text())
        self.statusLabel.setText(status)
        buttons_list = [{"label": "❤ Qiwi", "url": "https://qiwi.com/n/YAROSLAVIK"},
                        {"label": "❤ Co-fi", "url": "https://ko-fi.com/yaroslavik"}]
        if self.RPC.connected:
            self.RPC.RPC.update(details="You can support me", buttons=buttons_list)  # Set the presence
            print('Updated!')
        return

    def stop_rpc(self):
        status = self.RPC.disconnect()
        self.statusLabel.setText(status)

    def toggle_autostart(self):
        curr_state = bool(self.checkBox_autostart.isChecked())
        self.config.set('start_after_launch', curr_state)

    def setup_ui(self):
        self.startButton.clicked.connect(lambda: self.start_rpc())
        self.stopButton.clicked.connect(lambda: self.stop_rpc())
        self.checkBox_autostart.toggled.connect(lambda: self.toggle_autostart())
        self.lineEdit.setText(str(self.config.get('application_id')))
        autostart = bool(self.config.get('start_after_launch'))
        self.checkBox_autostart.setChecked(autostart)
        if autostart:
            self.start_rpc()

    def closeEvent(self, event):
        print('CLOSED')
        if self.RPC.connected:
            self.RPC.disconnect()
        event.accept()

    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = Ui_MainWindow()
    MainWindow.setup_ui()
    MainWindow.show()
    sys.exit(app.exec_())

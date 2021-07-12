from PyQt5 import QtCore, QtGui, QtWidgets, uic, Qt
from PyQt5.QtCore import QEvent

from pypresence import Presence
from configmanager import ConfigManager
from rpcmanager import RPCManager
import os


class MainUI(QtWidgets.QMainWindow):
    connected = False
    RPC = RPCManager()

    def __init__(self):
        self.force_close = False
        self.config = ConfigManager()
        super(MainUI, self).__init__()  # Call the inherited classes __init__ method
        main_ui = self.resource_path('mainUI.ui')
        uic.loadUi(main_ui, self)  # Load the .ui file
        self.show()  # Show the GUI
        self.icon_image = QtGui.QIcon(self.resource_path('icon.svg'))
        # Plasma 5 don't show swg icons
        self.icon_image = QtGui.QIcon(self.icon_image.pixmap(128, 128))
        self.setWindowIcon(self.icon_image)

        # Init tray icon
        self.tray_icon = QtWidgets.QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.icon_image) # self.style().standardIcon(QtWidgets.QStyle.SP_ArrowUp)
        self.tray_icon.activated.connect(self.click_tray_icon)

        # Init basic methods on tray
        show_action = QtWidgets.QAction("Show", self)
        quit_action = QtWidgets.QAction("Exit", self)
        hide_action = QtWidgets.QAction("Hide", self)
        show_action.triggered.connect(self.show)
        hide_action.triggered.connect(self.hide)
        quit_action.triggered.connect(self.exit_app)
        tray_menu = QtWidgets.QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def click_tray_icon(self, i_reason):
        if i_reason == QtCore.Qt.LeftArrow:
            self.show()
            self.activateWindow()

    def exit_app(self):
        self.force_close = True
        self.close()

    def start_rpc(self):
        status = self.RPC.connect(self.lineEdit.text())
        self.statusLabel.setText(status)
        buttons_list = [{"label": "❤ Qiwi", "url": "https://qiwi.com/n/YAROSLAVIK"},
                        {"label": "❤ Co-fi", "url": "https://ko-fi.com/yaroslavik"}]
        if self.RPC.connected:
            self.RPC.update(details="You can support me", buttons=buttons_list)  # Set the presence
            print('Updated!')
        return

    def stop_rpc(self):
        status = self.RPC.disconnect()
        self.statusLabel.setText(status)

    def toggle_autostart(self):
        curr_state = bool(self.checkBox_autostart.isChecked())
        self.config.set('start_after_launch', curr_state)

    def toggle_start_in_tray(self):
        curr_state = bool(self.checkBox_startInTray.isChecked())
        self.config.set('start_in_tray', curr_state)

    def setup_ui(self):
        self.startButton.clicked.connect(self.start_rpc)
        self.stopButton.clicked.connect(self.stop_rpc)
        self.checkBox_autostart.toggled.connect(self.toggle_autostart)
        self.checkBox_startInTray.toggled.connect(self.toggle_start_in_tray)
        self.lineEdit.setText(str(self.config.get('application_id')))
        autostart = bool(self.config.get('start_after_launch'))
        self.checkBox_autostart.setChecked(autostart)
        start_in_tray = bool(self.config.get('start_in_tray'))
        self.checkBox_startInTray.setChecked(start_in_tray)
        if autostart:
            self.start_rpc()
        if start_in_tray:
            self.hide()

    def closeEvent(self, event):
        if bool(self.config.get('start_in_tray')) and self.force_close is False:
            print('HIDDEN IN TRAY')
            self.hide()
            event.ignore()
        else:
            if self.RPC.connected:
                self.RPC.disconnect()
            print('CLOSED')
            event.accept()

    # def changeEvent(self, event):
    #     if event.type() == QEvent.WindowStateChange:
    #         if self.isMinimized():
    #             print("WindowMinimized")
    #             #self.hide()

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
    MainWindow = MainUI()
    MainWindow.setup_ui()
    # MainWindow.show() Its realize on setup_ui method
    sys.exit(app.exec_())

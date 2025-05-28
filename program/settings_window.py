from PyQt5 import QtWidgets
#from resources.settings import Settings
from program.themes import Themes
from core.xmlEt import loadCFG as xl

class SettingsWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setFixedSize(300, 200)
        self.setStyleSheet(Themes.DARK_MODE)
        self.config = xl()  # Instantiate loadCFG
        self.init_ui()

    def init_ui(self):
        layout = QtWidgets.QVBoxLayout()

        self.close_on_tray_checkbox = QtWidgets.QCheckBox("Keep running in system tray")
        self.close_on_tray_checkbox.setChecked(self.config.get('closeOnTray') == 'true')
        self.close_on_tray_checkbox.stateChanged.connect(self.toggle_close_on_tray)
        layout.addWidget(self.close_on_tray_checkbox)

        self.run_as_admin_checkbox = QtWidgets.QCheckBox("Run as administrator")
        self.run_as_admin_checkbox.setChecked(self.config.get('runAsAdmin') == 'true')
        self.run_as_admin_checkbox.stateChanged.connect(self.toggle_run_as_admin)
        layout.addWidget(self.run_as_admin_checkbox)

        self.minimizeAtLaunch_checkbox = QtWidgets.QCheckBox("Minimize at launch")
        self.minimizeAtLaunch_checkbox.setChecked(self.config.get('minimizeAtLaunch') == 'true')
        self.minimizeAtLaunch_checkbox.stateChanged.connect(self.minimizeAtLaunch)
        layout.addWidget(self.minimizeAtLaunch_checkbox)
        

        close_button = QtWidgets.QPushButton("Close")
        close_button.setStyleSheet(Themes.BUTTON_STYLE)
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button)

        self.setLayout(layout)

    def toggle_close_on_tray(self, state):
        new_value = 'true' if state == QtWidgets.QCheckBox.isChecked or state == 2 else 'false'
        self.config.set('closeOnTray', new_value)
        

    def toggle_run_as_admin(self, state):
        new_value = 'true' if state == QtWidgets.QCheckBox.isChecked or state == 2 else 'false'
        self.config.set('runAsAdmin', new_value)

    def minimizeAtLaunch(self, state):
        new_value = 'true' if state == QtWidgets.QCheckBox.isChecked or state == 2 else 'false'
        self.config.set('minimizeAtLaunch', new_value)    
        

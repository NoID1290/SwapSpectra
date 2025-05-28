from PyQt5 import QtWidgets, QtGui, QtCore
from core.executor import run_gsync_command
from core.registry import read_status, update_status_in_registry
from core.logger import setup_logging
from core.ckGpu import GPUname
from resources.settings import Settings
from program.themes import Themes

import logging





class GSyncToggleApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.gswdll = Settings.EXECUTABLE_PATH
        self.init_ui()
        setup_logging()
        self.checkNV()
        self.detect_current_status()
        
        

    def init_ui(self):
        self.setWindowTitle(Settings.APP_TITLE)
        self.setFixedSize(Settings.WINDOW_WIDTH, Settings.WINDOW_HEIGHT)
        self.setWindowIcon(QtGui.QIcon(Settings.ICON_PATH))
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # Title Bar
        title_label = QtWidgets.QLabel(Settings.MAIN_TITLE)
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        title_label.setStyleSheet(Themes.TITLE_STYLE)
        main_layout.addWidget(title_label)

        # Status Label
        self.status_label = QtWidgets.QLabel("Current Status: Detecting...")
        self.status_label.setAlignment(QtCore.Qt.AlignCenter)
        self.status_label.setStyleSheet(Themes.STATUS_STYLE)
        main_layout.addWidget(self.status_label)

        # Buttons
        button_layout = QtWidgets.QHBoxLayout()
        button_off = QtWidgets.QPushButton(Settings.BUTTON_OFF_TEXT)
        button_off.setStyleSheet(Themes.BUTTON_STYLE)
        button_off.clicked.connect(lambda: self.run_command(0))
        button_layout.addWidget(button_off)

        button_on = QtWidgets.QPushButton(Settings.BUTTON_ON_TEXT)
        button_on.setStyleSheet(Themes.BUTTON_STYLE)
        button_on.clicked.connect(lambda: self.run_command(2))
        button_layout.addWidget(button_on)
        main_layout.addLayout(button_layout)

        # Log Viewer
        self.log_viewer = QtWidgets.QTextEdit()
        self.log_viewer.setReadOnly(True)
        self.log_viewer.setStyleSheet(Themes.LOG_STYLE)
        #self.log_viewer.setPlaceholderText("Log messages will appear here...")
        main_layout.addWidget(self.log_viewer)

        # Spacer and copyright label
        main_layout.addStretch()
        copyright_label = QtWidgets.QLabel(Settings.COPYRIGHT_TEXT)
        copyright_label.setAlignment(QtCore.Qt.AlignCenter)
        copyright_label.setStyleSheet(Themes.COPYRIGHT_STYLE)
        main_layout.addWidget(copyright_label)

        self.setLayout(main_layout)
        self.apply_dark_mode()
        self.center_window()
        
        
    def logInfo(self, log):
        """Log a message to the console log viewer and log file."""
        self.log_viewer.append(log)
        logging.info(log)



    def checkNV(self):
        nvST = 0  # Default state for NVIDIA hardware detection
        if "NVIDIA" in GPUname:
            self.logInfo("NVIDIA Hardware detected")
            nvST = 1
        else:
            self.logInfo("No NVIDIA Hardware detected")
        
        return nvST


    def detect_current_status(self):
        try:
            self.logInfo (f"GPU Model: {GPUname}")    
            status = read_status()
            self.update_status(2 if status == "ON" else 0)
            self.logInfo (f"Detected G-SYNC status: {status}")
        except FileNotFoundError:
            self.status_label.setVisible(False)
            self.logInfo ("Error: Status file not found.")
        except Exception as e:
            self.status_label.setText("Current Status: Error")
            self.status_label.setStyleSheet(Themes.ERROR_STYLE)
            self.status_label.setVisible(True)
            self.logInfo(f"Error detecting status: {e}")
         
    def run_command(self, option):
        success, message = run_gsync_command(self.gswdll, option)
        if success:
            self.update_status(option)
            update_status_in_registry(option)
            QtWidgets.QMessageBox.information(self, "Success", message)
            self.logInfo(f"Command executed successfully: {message}")
        else:
            QtWidgets.QMessageBox.critical(self, "Error", message)
            self.logInfo(f"Command execution failed: {message}")

    def update_status(self, option):
        status_text = "ON" if option == 2 else "OFF"
        color = "lightgreen" if option == 2 else "red"
        self.status_label.setText(f"Current Status: G-SYNC {status_text}")
        self.status_label.setStyleSheet(f"font-size: 16px; font-weight: bold; color: {color};")
        #self.logInfo(f"Status updated to G-SYNC {status_text}")

    def apply_dark_mode(self):
        self.setStyleSheet(Themes.DARK_MODE)

    def center_window(self):
        screen = QtGui.QGuiApplication.primaryScreen()
        center_point = screen.geometry().center()
        qr = self.frameGeometry()
        qr.moveCenter(center_point)
        self.move(qr.topLeft())

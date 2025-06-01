from PyQt5 import QtWidgets, QtGui, QtCore
from core.executor import run_gsync_command
from core.registry import read_status, update_status_in_registry, read_dlss_overlay_status, update_dlss_overlay_in_registry
from core.logger import setup_logging
from core.ckGpu import GPUname
from core.nvgxswap import update_nvngx
from core.nvapi_init import initialize_nvapi
from resources.settings import Settings, format_text
from program.themes import Themes
from program.settings_window import SettingsWindow
from core.elevation import is_admin, elevate




import logging
import time


# Main application class for G-SYNC Toggle - Order run is important
class GSyncToggleApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.gswdll = Settings.EXECUTABLE_PATH
        setup_logging()
        self.init_ui()
        self.checkNV()
        self.init_nvapi()
        self.checkGvLib()
        self.detect_current_status()
        self.detect_dlss_overlay_status()
        
    def init_ui(self):  # Initialize the UI components
        self.setWindowTitle(Settings.APP_TITLE)
        self.setFixedSize(Settings.WINDOW_WIDTH, Settings.WINDOW_HEIGHT)
        self.setWindowIcon(QtGui.QIcon(Settings.ICON_PATH))
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # Widgets and layout setup organization
        self.add_title_bar(main_layout)
        self.add_status_label(main_layout)
        self.add_dlss_overlay_label(main_layout)
        self.add_dlssSwap_label(main_layout)
        self.add_buttons(main_layout)
        self.add_log_viewer(main_layout)
        self.add_footer(main_layout)
        self.add_settings_button(main_layout)
        self.setLayout(main_layout)
        self.apply_dark_mode()
        self.show()
        self.center_window()

    def add_title_bar(self, layout):
        title_label = QtWidgets.QLabel(Settings.MAIN_TITLE)
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        title_label.setStyleSheet(Themes.TITLE_STYLE)
        layout.addWidget(title_label)

    def add_status_label(self, layout):
        self.status_label = QtWidgets.QLabel("Current Status: Detecting...")
        self.status_label.setAlignment(QtCore.Qt.AlignCenter)
        self.status_label.setStyleSheet(Themes.STATUS_STYLE)
        layout.addWidget(self.status_label)

    def add_dlss_overlay_label(self, layout):
        self.dlss_overlay_label = QtWidgets.QLabel("DLSS Overlay: Detecting...")
        self.dlss_overlay_label.setAlignment(QtCore.Qt.AlignCenter)
        self.dlss_overlay_label.setStyleSheet(Themes.STATUS_STYLE)
        layout.addWidget(self.dlss_overlay_label)

    def add_dlssSwap_label(self, layout):
        self.dlssSwap_label = QtWidgets.QLabel("DLSS Swap: Detecting...")
        self.dlssSwap_label.setAlignment(QtCore.Qt.AlignCenter)
        self.dlssSwap_label.setStyleSheet(Themes.STATUS_STYLE)
        layout.addWidget(self.dlssSwap_label)        

    def add_buttons(self, layout):
        button_layout = QtWidgets.QHBoxLayout()
        
        button_off = QtWidgets.QPushButton(Settings.BUTTON_OFF_TEXT)
        button_off.setStyleSheet(Themes.BUTTON_STYLE)
        button_off.clicked.connect(lambda: self.run_command(0))
        button_layout.addWidget(button_off)

        button_on = QtWidgets.QPushButton(Settings.BUTTON_ON_TEXT)
        button_on.setStyleSheet(Themes.BUTTON_STYLE)
        button_on.clicked.connect(lambda: self.run_command(2))
        button_layout.addWidget(button_on)

        refresh_button = QtWidgets.QPushButton(Settings.BUTTON_REFRESH_TEXT)
        refresh_button.setStyleSheet(Themes.BUTTON_STYLE)
        refresh_button.clicked.connect(self.runRefreshWhenOn)
        if read_status() == "OFF":
            refresh_button.setEnabled(False)
        else:
            refresh_button.setEnabled(True)
        button_layout.addWidget(refresh_button)

        dlss_overlay_on = QtWidgets.QPushButton(Settings.DLSS_ON_TEXT)
        dlss_overlay_on.setStyleSheet(Themes.BUTTON_STYLE)
        dlss_overlay_on.clicked.connect(lambda: self.update_dlss_overlay_status(1))
        dlss_overlay_on.clicked.connect(lambda: update_dlss_overlay_in_registry(1))
        button_layout.addWidget(dlss_overlay_on)

        dlss_overlay_off = QtWidgets.QPushButton(Settings.DLSS_OFF_TEXT)
        dlss_overlay_off.setStyleSheet(Themes.BUTTON_STYLE)
        dlss_overlay_off.clicked.connect(lambda: self.update_dlss_overlay_status(0))
        dlss_overlay_off.clicked.connect(lambda: update_dlss_overlay_in_registry(0))    
        button_layout.addWidget(dlss_overlay_off)

        if not is_admin():
            dlss_overlay_on.setEnabled(False)
            dlss_overlay_off.setEnabled(False)
            dlss_overlay_on.setStyleSheet("background-color: gray; color: white;")
            dlss_overlay_off.setStyleSheet("background-color: gray; color: white;")

        dlssswap_button = QtWidgets.QPushButton(Settings.DLSS_SWAP_TEXT)
        dlssswap_button.setStyleSheet(Themes.BUTTON_STYLE)
        dlssswap_button.clicked.connect(self.show_dlss_swap_dialog)
        button_layout.addWidget(dlssswap_button)

        layout.addLayout(button_layout)

    def add_log_viewer(self, layout):
        self.log_viewer = QtWidgets.QTextEdit()
        self.log_viewer.setReadOnly(True)
        self.log_viewer.setStyleSheet(Themes.LOG_STYLE)
        layout.addWidget(self.log_viewer)

    def add_footer(self, layout):
        layout.addStretch()
        copyright_label = QtWidgets.QLabel(format_text.cpVbuild)
        copyright_label.setAlignment(QtCore.Qt.AlignCenter)
        copyright_label.setStyleSheet(Themes.COPYRIGHT_STYLE)
        layout.addWidget(copyright_label)

    def add_settings_button(self, layout):
        settings_layout = QtWidgets.QHBoxLayout()

        settings_button = QtWidgets.QPushButton("Settings")
        settings_button.setStyleSheet(Themes.BUTTON_STYLE)
        settings_button.clicked.connect(self.open_settings)

        restartinAdmin = QtWidgets.QPushButton("Restart in Admin Mode")
        restartinAdmin.setStyleSheet(Themes.BUTTON_STYLE)
        restartinAdmin.clicked.connect(lambda: elevate())
        restartinAdmin.setEnabled(not is_admin())
        restartinAdmin.setStyleSheet(is_admin() and "background-color: gray; color: white;" or "background-color: lightgreen; color: black;")
        restartinAdmin.setToolTip("Restart the application with administrative privileges.")
        
        
        
        settings_layout.addWidget(settings_button)
        settings_layout.addStretch()
        settings_layout.addWidget(restartinAdmin)
        layout.addLayout(settings_layout)

    def open_settings(self):
        settings_dialog = SettingsWindow(self)
        settings_dialog.exec_()

    def toggle_close_on_tray(self, state):
        Settings.CLOSE_ON_TRAY = bool(state)

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

    def checkGvLib(self):  # Check if GvLib is available
        try:
            import clr
            clr.AddReference("idsw-gvlib")
            from ReturnPresence import ReturnPresence  # type: ignore
            self.logInfo("GvLib found")
            readPresence = ReturnPresence.GetPresence()
            self.logInfo(f"{readPresence}")
            return True

        except ImportError as e:
            self.logInfo(f"Error loading GvLib: {e}")
            return False
    
    def init_nvapi(self):
        """Initialize the NVAPI wrapper library."""
        try:
            if initialize_nvapi():
                self.logInfo("NVAPI initialized successfully.")
            else:
                self.logInfo("NVAPI initialization failed.")
        except Exception as e:
            self.logInfo(f"Error initializing NVAPI: {e}")
            raise ImportError(f"Failed to initialize NVAPI: {e}")

    def detect_current_status(self):  # Detect the current G-SYNC status
        try:
            self.logInfo(f"GPU Model: {GPUname}")
            status = read_status()
            self.update_status(2 if status == "ON" else 0)
            self.logInfo(f"Detected G-SYNC status: {status}")
        except FileNotFoundError:
            self.status_label.setVisible(False)
            self.logInfo("Error: Status file not found.")
        except Exception as e:
            self.status_label.setText("Current Status: Error")
            self.status_label.setStyleSheet(Themes.ERROR_STYLE)
            self.status_label.setVisible(True)
            self.logInfo(f"Error detecting status: {e}")
            
    def detect_dlss_overlay_status(self):  # Detect the DLSS Overlay status
        try:
            dlss_overlay_status = read_dlss_overlay_status()
            self.update_dlss_overlay_status(1 if dlss_overlay_status == "ON" else 0)
            self.logInfo(f"Detected DLSS Overlay status: {dlss_overlay_status}")
        except FileNotFoundError:
            self.dlss_overlay_label.setVisible(False)
            self.logInfo("Error: DLSS Overlay status file not found.")
        except Exception as e:
            self.dlss_overlay_label.setText("DLSS Overlay: Error")
            self.dlss_overlay_label.setStyleSheet(Themes.ERROR_STYLE)
            self.dlss_overlay_label.setVisible(True)
            self.logInfo(f"Error detecting DLSS Overlay status: {e}")

    # Update the DLSS Overlay status label
    def update_dlss_overlay_status(self, option):
        status_text = Settings.TXT_TRUE if option == 1 else Settings.TXT_FALSE
        color = "lightgreen" if option == 1 else "red"
        self.dlss_overlay_label.setText(f"DLSS Overlay: {status_text}")
        self.dlss_overlay_label.setStyleSheet(f"font-size: 16px; font-weight: bold; color: {color};")

    def run_command(self, option):  # Run the G-SYNC command based on the option
        try:
            success, message = run_gsync_command(self.gswdll, option)
            if success:
                self.update_status(option)
                update_status_in_registry(option)
                QtWidgets.QMessageBox.information(self, "Success", message)
                self.logInfo(f"Command executed successfully: {message}")
                self.refresh_status_label()  # Refresh status label
            else:
                QtWidgets.QMessageBox.critical(self, "Error", message)
                self.logInfo(f"Command execution failed: {message}")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", str(e))
            self.logInfo(f"Exception during command execution: {e}")

    def runRefreshWhenOn(self):
        self.run_command(0)
        time.sleep(3)
        self.run_command(2)
        self.logInfo("Refreshed G-SYNC done!")
        run_gsync_command(self.gswdll, 2)
        self.logInfo("Refreshed G-SYNC done!")

    def refresh_status_label(self):
        """Refresh the status label."""
        status = read_status()
        self.update_status(2 if status == "ON" else 0)

    def refresh_dlss_overlay_label(self):
        """Refresh the DLSS overlay label."""
        dlss_overlay_status = read_dlss_overlay_status()
        self.update_dlss_overlay_status(1 if dlss_overlay_status == "ON" else 0)

    def update_status(self, option):
        status_text = "ON" if option == 2 else "OFF"
        color = "lightgreen" if option == 2 else "red"
        self.status_label.setText(f"Current Status: G-SYNC {status_text}")
        self.status_label.setStyleSheet(f"font-size: 16px; font-weight: bold; color: {color};")

    def apply_dark_mode(self):
        self.setStyleSheet(Themes.DARK_MODE)

    def center_window(self):
        screen = QtGui.QGuiApplication.primaryScreen()
        center_point = screen.geometry().center()
        qr = self.frameGeometry()
        qr.moveCenter(center_point)
        self.move(qr.topLeft())

    def show_dlss_swap_dialog(self):
        """Show file dialog for DLSS DLL selection and perform the swap."""
        file_dialog = QtWidgets.QFileDialog()
        file_dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        file_dialog.setNameFilter("DLSS DLL Files (nvngx_dlss*.dll);;All Files (*.*)")
        
        if file_dialog.exec_():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                dll_path = selected_files[0]
                self.perform_dlss_swap(dll_path)

    def perform_dlss_swap(self, dll_path: str):
        """Perform the DLSS DLL swap operation."""
        try:
            self.logInfo(f"Attempting to swap DLSS DLL: {dll_path}")
           
            """ 
            # Check if the application is running with administrator privileges
            # Uncomment this block if you want to enforce admin rights for the swap operation
            if not is_admin(): 
                QtWidgets.QMessageBox.warning(
                    self,
                    "Administrator Rights Required",
                    "This operation requires administrator privileges. Please restart the application as administrator."
                )
                return
            """
                
            if update_nvngx(dll_path):
                QtWidgets.QMessageBox.information(
                    self,
                    "Success",
                    "DLSS DLL swap completed successfully."
                )
                self.update_dlss_swap_status(True)
            else:
                QtWidgets.QMessageBox.critical(
                    self,
                    "Error",
                    "Failed to swap DLSS DLL. Check the logs for details."
                )
                self.update_dlss_swap_status(False)
        except Exception as e:
            self.logInfo(f"Error during DLSS swap: {e}")
            QtWidgets.QMessageBox.critical(
                self,
                "Error",
                f"An error occurred during DLSS swap: {str(e)}"
            )
            self.update_dlss_swap_status(False)

    def update_dlss_swap_status(self, success: bool):
        """Update the DLSS swap status label."""
        status_text = "Success" if success else "Failed"
        color = "lightgreen" if success else "red"
        self.dlssSwap_label.setText(f"DLSS Swap: {status_text}")
        self.dlssSwap_label.setStyleSheet(f"font-size: 16px; font-weight: bold; color: {color};")
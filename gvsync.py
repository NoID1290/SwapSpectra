"""
GvSync 1.1.0

MIT License

Copyright (c) 2024 NoID Softwork

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


from PyQt5 import QtWidgets, QtGui, QtCore
import subprocess
import sys
import os
import winreg as reg
import logging
import common


class GSyncToggleApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.executable_path = "gsyncwrapper-1.1.0-x86_64.dll"
        self.init_ui()
        self.init_logging()
        self.detect_current_status()

    def init_logging(self):
        logging.basicConfig(
            filename="gsyncwrapper.log",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
        )

    def init_ui(self):
        #windows settings
        self.setWindowTitle(common.project_title0)
        self.setFixedSize(common.wSizeH,common.wSizeV)
        self.setWindowIcon(QtGui.QIcon(common.icoP))
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint) #always stay on top

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # Title Bar
        title_bar_layout = QtWidgets.QHBoxLayout()
        title_label = QtWidgets.QLabel(common.main_title0)
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; color: white;")
        title_bar_layout.addWidget(title_label)
        main_layout.addLayout(title_bar_layout)

        # Status Label
        self.status_label = QtWidgets.QLabel("Current Status: Detecting...")
        self.status_label.setAlignment(QtCore.Qt.AlignCenter)
        self.status_label.setStyleSheet("font-size: 16px; font-weight: bold; color: lightgreen;")
        main_layout.addWidget(self.status_label)

        # Buttons
        button_layout = QtWidgets.QHBoxLayout()
        button_off = QtWidgets.QPushButton(common.gsOff)
        button_off.setStyleSheet(self.button_style())
        button_off.clicked.connect(lambda: self.run_command(0))
        button_layout.addWidget(button_off)

        button_on = QtWidgets.QPushButton(common.gsOn)
        button_on.setStyleSheet(self.button_style())
        button_on.clicked.connect(lambda: self.run_command(2))
        button_layout.addWidget(button_on)
        main_layout.addLayout(button_layout)

        
        # Change Executable Path (keeping this for later integration)
        #path_button = QtWidgets.QPushButton("Change Executable Path")
        #path_button.setStyleSheet(self.button_style())
        #path_button.clicked.connect(self.change_executable_path)
        #main_layout.addWidget(path_button)

        # Spacer and copyright label
        main_layout.addStretch()
        copyright_label = QtWidgets.QLabel(common.copyright0 + common.versionBuild)
        copyright_label.setAlignment(QtCore.Qt.AlignCenter)
        copyright_label.setStyleSheet("font-size: 12px; color: #999;")
        main_layout.addWidget(copyright_label)

        self.setLayout(main_layout)
        self.apply_dark_mode()  # Apply dark mode on startup
        self.center_window()

    def button_style(self):
        return """
            QPushButton {
                font-size: 14px;
                padding: 10px 20px;
                background-color: #555555;
                color: white;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #777777;
            }
            QPushButton:pressed {
                background-color: #444444;
            }
        """

    def apply_dark_mode(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #2B2B2B;
                color: white;
            }
            QLabel {
                color: white;
            }
            QPushButton {
                background-color: #555555;
                color: white;
            }
            QPushButton:hover {
                background-color: #777777;
            }
            QPushButton:pressed {
                background-color: #444444;
            }
        """)
        self.status_label.setStyleSheet("font-size: 16px; font-weight: bold; color: lightgreen;")

    def change_executable_path(self):
        path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Select GSync Toggle Executable", "", "Executables (*.exe)"
        )
        if path:
            self.executable_path = path
            QtWidgets.QMessageBox.information(self, "Path Changed", f"Path set to: {self.executable_path}")

    def detect_current_status(self):
        try:
            key_path = r"Software\NoID Softwork\GvSync"
            key = reg.OpenKey(reg.HKEY_CURRENT_USER, key_path, 0, reg.KEY_READ)
            status = reg.QueryValueEx(key, "GSyncStatus")[0]
            self.update_status(2 if status == "ON" else 0)
            reg.CloseKey(key)
        except FileNotFoundError:
            # Hide the status label if the status is unknown
            self.status_label.setVisible(False)
            logging.warning("Registry key not found.")
        except Exception as e:
            self.status_label.setText("Current Status: Error")
            self.status_label.setStyleSheet("font-size: 16px; font-weight: bold; color: red;")
            self.status_label.setVisible(True)  # Make sure it's visible in case of an error
            logging.error(f"Failed to detect current status: {e}")


    def run_command(self, option):
        if not os.path.exists(self.executable_path):
            QtWidgets.QMessageBox.critical(
                self, "Error", f"Executable not found: {self.executable_path}"
            )
            logging.error(f"Executable not found: {self.executable_path}")
            return

        try:
            result = subprocess.run(
                [self.executable_path, str(option)],
                capture_output=True,
                text=True,
                shell=True,
            )

            if result.returncode == 0:
                self.update_status(option)
                self.update_registry(option)
                QtWidgets.QMessageBox.information(
                    self, "Success", f"G-SYNC {'ON' if option == 2 else 'OFF'} applied!"
                )
                logging.info(f"G-SYNC {'ON' if option == 2 else 'OFF'} applied successfully.")
            else:
                QtWidgets.QMessageBox.critical(
                    self, "Error", f"Command failed: {result.stderr}"
                )
                logging.error(f"Command failed: {result.stderr}")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"An error occurred: {e}")
            logging.exception("An error occurred while running the command.")

    def update_status(self, option):
        self.status_label.setVisible(True)
        status_text = "ON" if option == 2 else "OFF"
        self.status_label.setText(f"Current Status: G-SYNC {status_text}")
        
        # Update the label color based on the status
        color = "lightgreen" if option == 2 else "red"
        self.status_label.setStyleSheet(f"font-size: 16px; font-weight: bold; color: {color};")

    def update_registry(self, option):
        try:
            key_path = r"Software\NoID Softwork\GvSync"
            key = reg.CreateKey(reg.HKEY_CURRENT_USER, key_path)

            reg.SetValueEx(key, "GSyncStatus", 0, reg.REG_SZ, "ON" if option == 2 else "OFF")
            reg.CloseKey(key)
            logging.info("Registry updated successfully.")
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Registry Error", f"Failed to update registry: {e}")
            logging.error(f"Failed to update registry: {e}")

    def center_window(self):
        screen = QtGui.QGuiApplication.primaryScreen()
        center_point = screen.geometry().center()
        qr = self.frameGeometry()
        qr.moveCenter(center_point)
        self.move(qr.topLeft())


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = GSyncToggleApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

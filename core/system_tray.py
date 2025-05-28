from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt
from program.main_W import GSyncToggleApp
from resources.settings import Settings

import sys


class GSyncToggleAppWithTray(GSyncToggleApp):
    def __init__(self):
        super().__init__()

        # Ensure the system tray is available
        if not QtWidgets.QSystemTrayIcon.isSystemTrayAvailable():
            QtWidgets.QMessageBox.critical(
                None, "Error", "System tray is not available. The application will exit."
            )
            sys.exit(1)

        # Create the system tray icon
        self.tray_icon = QtWidgets.QSystemTrayIcon(self)
        self.tray_icon.setIcon(QtGui.QIcon("gvico.ico"))

        # Create the menu for the system tray
        self.tray_menu = QtWidgets.QMenu()
        show_action = QtWidgets.QAction(QtGui.QIcon("show_icon.png"), "Show", self)
        settings_action = QtWidgets.QAction(QtGui.QIcon("settings_icon.png"), "Settings", self)
        about_action = QtWidgets.QAction(QtGui.QIcon("about_icon.png"), "About", self)
        exit_action = QtWidgets.QAction(QtGui.QIcon("exit_icon.png"), "Exit", self)

        # Connect the actions
        show_action.triggered.connect(self.show)
        settings_action.triggered.connect(self.open_settings)
        about_action.triggered.connect(self.show_about)
        exit_action.triggered.connect(self.exit_application)

        # Add actions to the menu
        self.tray_menu.addAction(show_action)
        self.tray_menu.addAction(settings_action)
        self.tray_menu.addAction(about_action)
        self.tray_menu.addSeparator()
        self.tray_menu.addAction(exit_action)

        # Assign the menu to the tray icon
        self.tray_icon.setContextMenu(self.tray_menu)
        self.tray_icon.activated.connect(self.on_tray_icon_activated)

        # Show the tray icon
        self.tray_icon.show()
        self.tray_icon.setToolTip("GSyncToggleApp - Click to open or right-click for options")

        # Ensure proper window flags for hiding
        self.setWindowFlags(self.windowFlags() | Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)

    def closeEvent(self, event):
        """Override the close event to hide the window instead of closing it."""
        if self.isVisible():
            event.ignore()
            self.hide()
            self.tray_icon.showMessage(
                "Application Minimized",
                "The application is running in the system tray. Right-click the tray icon to exit.",
                QtGui.QIcon("gvico.ico"),
                3000  # Duration in milliseconds
            )

    def on_tray_icon_activated(self, reason):
        """Handle interactions with the tray icon."""
        if reason == QtWidgets.QSystemTrayIcon.Trigger:  # Left-click to show the window
            self.showNormal()
            self.activateWindow()

    def exit_application(self):
        """Properly close the application."""
        self.tray_icon.hide()
        QtWidgets.QApplication.quit()

    def open_settings(self):
        """Open the settings window (placeholder)."""
        QtWidgets.QMessageBox.information(
            self, "Settings", "Settings window is under construction."
        )

    def show_about(self):
        """Show the about dialog."""
        QtWidgets.QMessageBox.about(
            self,
            Settings.APP_TITLE,
            Settings.COPYRIGHT_TEXT,
        )

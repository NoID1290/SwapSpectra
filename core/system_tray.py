from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt
from program.main_W import GSyncToggleApp
from resources.settings import Settings

from program.settings_window import SettingsWindow

import sys
import os
import logging
import core.xmlEt as xl

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


class GSyncToggleAppWithTray(GSyncToggleApp):
    def __init__(self):
        logging.debug("Initializing GSyncToggleAppWithTray")
        super().__init__()

        # Ensure the system tray is available
        if not QtWidgets.QSystemTrayIcon.isSystemTrayAvailable():
            logging.critical("System tray is not available. Exiting application.")
            QtWidgets.QMessageBox.critical(
                None, "Error", "System tray is not available. The application will exit."
            )
            sys.exit(1)

        # Initialize system tray icon
        self.init_tray_icon()

        # Ensure proper window flags for hiding
        self.setWindowFlags(
            self.windowFlags() | Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint
        )

    def init_tray_icon(self):
        """Initialize the system tray icon and menu."""
        logging.debug("Initializing system tray icon")
        icon_path = "gvico.ico"
        if not os.path.exists(icon_path):
            logging.warning(f"Tray icon '{icon_path}' not found. Using default icon.")
            QtWidgets.QMessageBox.warning(
                None, "Warning", f"Tray icon '{icon_path}' not found. Using default icon."
            )
            tray_icon = QtWidgets.QSystemTrayIcon(self)
            tray_icon.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_ComputerIcon))
        else:
            tray_icon = QtWidgets.QSystemTrayIcon(QtGui.QIcon(icon_path), self)

        # Create the tray menu
        tray_menu = self.create_tray_menu()

        # Assign the menu to the tray icon
        tray_icon.setContextMenu(tray_menu)
        tray_icon.activated.connect(self.on_tray_icon_activated)

        # Show the tray icon
        tray_icon.show()
        tray_icon.setToolTip(Settings.APP_TITLE)  # Tooltip overlay
        self.tray_icon = tray_icon

    def create_tray_menu(self):
        """Create and return the system tray menu."""
        logging.debug("Creating system tray menu")
        tray_menu = QtWidgets.QMenu()

        # Create actions
        show_action = QtWidgets.QAction("Show", self)
        settings_action = QtWidgets.QAction("Settings", self)
        about_action = QtWidgets.QAction("About", self)
        exit_action = QtWidgets.QAction("Exit", self)

        # Connect actions to methods
        show_action.triggered.connect(self.show)
        settings_action.triggered.connect(self.open_settings)
        about_action.triggered.connect(self.show_about)
        exit_action.triggered.connect(self.exit_application)

        # Add actions to the menu
        tray_menu.addAction(show_action)
        tray_menu.addAction(settings_action)
        tray_menu.addAction(about_action)
        tray_menu.addSeparator()
        tray_menu.addAction(exit_action)

        return tray_menu

    def closeEvent(self, event):
        """Override the close event to minimize to the system tray."""
        logging.debug("Handling close event")
        if xl.loadCFG().get('closeOnTray') == 'false':
            logging.debug("Close on tray is disabled. Exiting application.")
            event.accept()
            self.exit_application()
            self.tray_icon.hide()
        else:
            if self.isVisible():
                event.ignore()
                self.hide()
                self.tray_icon.showMessage(
                    "Application Minimized",
                    "The application is running in the system tray. Right-click the tray icon to manage.",
                    QtGui.QIcon("gvico.ico") if os.path.exists("gvico.ico") else None,
                    3000  # Duration in milliseconds
                )
    
    def minimizeIfNeeded(self):
            """Minimize the application if configured."""
            logging.debug("Checking if minimize at launch is needed")
            if xl.loadCFG().get('minimizeAtLaunch') == 'true':
                logging.debug("Minimizing application at launch")
                self.hide()
                self.tray_icon.showMessage(
                    "Application Minimized",
                    "The application is running in the system tray. Right-click the tray icon to manage.",
                    QtGui.QIcon("gvico.ico") if os.path.exists("gvico.ico") else None,
                    3000  # Duration in milliseconds
            )
                        

    def on_tray_icon_activated(self, reason):
        """Handle interactions with the tray icon."""
        logging.debug(f"Tray icon activated with reason: {reason}")
        if reason == QtWidgets.QSystemTrayIcon.Trigger:  # Left-click to show the window
            self.showNormal()
            self.activateWindow()

    def exit_application(self):
        """Properly close the application."""
        logging.debug("Exiting application")
        self.tray_icon.hide()
        QtWidgets.QApplication.quit()

    def open_settings(self):
        """Open the settings window."""
        logging.debug("Opening settings window")
        settings_dialog = SettingsWindow(self)
        settings_dialog.exec_()

    def show_about(self):
        """Show the about dialog."""
        logging.debug("Showing about dialog")
        QtWidgets.QMessageBox.about(
            self,
            Settings.APP_TITLE,
            f"<b>{Settings.APP_TITLE}</b><br>{Settings.COPYRIGHT_TEXT}",
        )


        


# Run the application
if __name__ == "__main__":
    logging.debug("Starting application")
    app = QtWidgets.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)  # Ensure the app runs even when all windows are closed

    main_window = GSyncToggleAppWithTray()
    main_window.minimizeIfNeeded()  # Minimize the application at launch if configured
    main_window.show()

    sys.exit(app.exec_())

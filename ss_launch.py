from PyQt5 import QtWidgets
from core.system_tray import GSyncToggleAppWithTray
import sys
#$import resources.settings as id12
import core.elevation as id13
#import core.xmlEt as id14


class load():
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.uacElevate = id13.elevate_by_config()

def main():
    id13.elevate_by_config()  # Attempt elevation if configured and not admin
    app = QtWidgets.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)  # Ensure app stays running in the system tray
    window = GSyncToggleAppWithTray()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
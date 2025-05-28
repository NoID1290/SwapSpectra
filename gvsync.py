from PyQt5 import QtWidgets #, QtGui
#from PyQt5.QtCore import Qt
#from program.main_W import GSyncToggleApp
from core.system_tray import GSyncToggleAppWithTray
import sys



def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)  # Ensure app stays running in the system tray
    window = GSyncToggleAppWithTray()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

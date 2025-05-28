from PyQt5 import QtWidgets
from program.main_W import GSyncToggleApp
import sys

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = GSyncToggleApp()
    window.show()
    sys.exit(app.exec_())

if __name__ ==  "__main__":
    main()

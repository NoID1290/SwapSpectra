import sys
import pyuac
import core.xmlEt as xl


def is_admin():
    return pyuac.isUserAdmin()

def elevate_by_config():  # Attempt elevation if configured and not admin
    if xl.loadCFG().get('runAsAdmin') == 'true' and not is_admin():
        pyuac.runAsAdmin()
        sys.exit(0)  # Exit the current process to allow the elevated process to take over
    return True

def elevate():
    if not is_admin():
        pyuac.runAsAdmin()
        sys.exit(0)  # Exit the current process to allow the elevated process to take over
    return True



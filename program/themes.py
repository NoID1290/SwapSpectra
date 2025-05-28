class Themes:
    DARK_MODE = """
        QWidget {
            background-color: #121212;
            color: #ffffff;
            font-family: Arial, sans-serif;
        }
        QLineEdit, QTextEdit {
            background-color: #1e1e1e;
            border: 1px solid #333;
            padding: 5px;
            color: #ffffff;
        }
        QPushButton {
            background-color: #333333;
            color: white;
            padding: 10px;
            border: none;
            border-radius: 5px;
        }
        QPushButton:hover {
            background-color: #444444;
        }
        QPushButton:pressed {
            background-color: #555555;
        }
        QScrollBar:vertical {
            background: #2e2e2e;
            width: 10px;
        }
        QScrollBar::handle:vertical {
            background: #555555;
            min-height: 20px;
        }
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            background: none;
        }
    """
    TITLE_STYLE = "font-size: 18px; font-weight: bold; text-align: center; margin-bottom: 10px;"
    STATUS_STYLE = "font-size: 16px; text-align: center; margin-bottom: 10px;"
    BUTTON_STYLE = """
        QPushButton {
            background-color: #333333;
            color: white;
            padding: 10px;
            border: none;
            border-radius: 5px;
        }
        QPushButton:hover {
            background-color: #444444;
        }
        QPushButton:pressed {
            background-color: #555555;
        }
    """
    COPYRIGHT_STYLE = "font-size: 12px; color: gray; text-align: center; margin-top: 10px;"
    ERROR_STYLE = "font-size: 16px; font-weight: bold; color: red; text-align: center;"
    LOG_STYLE = "font-size: 10px; background-color: #1e1e1e; color: #ffffff; border: 1px solid #333; padding: 5px;"

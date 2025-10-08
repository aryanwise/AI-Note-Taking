def load_stylesheet():
    """Returns the full QSS stylesheet for the application."""
    return """
        #mainWidget {
            background-color: rgba(35, 35, 35, 0.92);
            border: 1px solid #444;
            border-radius: 12px;
        }
        #titleBar {
            background-color: #333;
            border-top-left-radius: 12px;
            border-top-right-radius: 12px;
            height: 35px;
        }
        QLabel {
            color: #EEE;
            font-family: Arial;
        }
        QTextEdit {
            background-color: #1E1E1E;
            color: #DDD;
            border-radius: 6px;
            border: 1px solid #444;
            font-size: 14px;
            padding: 5px;
        }
        QPushButton {
            background-color: #5C5C5C;
            color: #FFF;
            border: none;
            padding: 8px 16px;
            border-radius: 6px;
            font-weight: bold;
            font-family: Arial;
        }
        QPushButton:hover {
            background-color: #6C6C6C;
        }
        QPushButton:pressed {
            background-color: #4C4C4C;
        }
        QPushButton:disabled {
            background-color: #404040;
            color: #888;
        }
        #closeButton {
            font-size: 14px;
            font-weight: bold;
            padding: 0px 6px;
            border-radius: 10px;
            background-color: transparent;
        }
        #closeButton:hover {
            color: #FFF;
            background-color: #E81123;
        }
        QSplitter::handle {
            background: #444;
        }
        QSplitter::handle:horizontal {
            width: 1px;
        }
    """
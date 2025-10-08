import sys
from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QMouseEvent, QFont
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QTextEdit, QPushButton, QSplitter)

# Import the stylesheet function from our utils file
from app.utils.stylesheet import load_stylesheet

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.drag_pos = None

        # --- Basic Window Setup ---
        self.setWindowTitle("AI Note Taker")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize(750, 500)

        # --- Create and Set Layout ---
        # Using a central widget to hold the background style
        self.central_widget = QWidget(self)
        self.central_widget.setObjectName("mainWidget")
        
        # Main layout for the entire application
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # Build the UI components
        self._create_title_bar()
        self._create_content_area()

        # Set the central widget's layout, then set the main window's layout
        # This seems redundant but is necessary for the stylesheet to apply correctly
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0,0,0,0)
        root_layout.addWidget(self.central_widget)
        self.setLayout(root_layout)

        # Apply the styles from the separate file
        self.setStyleSheet(load_stylesheet())

    def _create_title_bar(self):
        """Creates the custom draggable title bar."""
        self.title_bar = QWidget()
        self.title_bar.setObjectName("titleBar")
        title_layout = QHBoxLayout(self.title_bar)
        title_layout.setContentsMargins(15, 0, 5, 0)
        
        title_label = QLabel("AI Note Taker")
        title_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        
        self.close_button = QPushButton("✕")
        self.close_button.setObjectName("closeButton")
        self.close_button.setFixedSize(28, 28)
        
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        title_layout.addWidget(self.close_button)
        
        self.main_layout.addWidget(self.title_bar)

    def _create_content_area(self):
        """Creates the main content area with text boxes and buttons."""
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(10, 10, 10, 10)

        # Splitter allows resizing panes
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        self.transcript_area = QTextEdit()
        self.transcript_area.setReadOnly(True)
        self.transcript_area.setPlaceholderText("Live transcript will appear here...")

        self.notes_area = QTextEdit()
        self.notes_area.setPlaceholderText("Connect to your backend to generate notes...")

        splitter.addWidget(self.transcript_area)
        splitter.addWidget(self.notes_area)
        splitter.setSizes([300, 450])

        # Control Buttons
        button_layout = QHBoxLayout()
        self.start_button = QPushButton("▶ Start")
        self.stop_button = QPushButton("■ Stop")
        
        button_layout.addStretch()
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        
        content_layout.addWidget(splitter)
        content_layout.addLayout(button_layout)
        
        self.main_layout.addWidget(content_widget, 1) # The '1' makes it stretch

        # --- UI LOGIC & CONNECTIONS ---
        self.close_button.clicked.connect(self.close)
        self.start_button.clicked.connect(self._on_start_clicked)
        self.stop_button.clicked.connect(self._on_stop_clicked)
        self._on_stop_clicked() # Set initial button state

    # --- UI Event Handlers (Internal Logic) ---
    def _on_start_clicked(self):
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.transcript_area.clear()
        self.notes_area.clear()
        self.transcript_area.setPlaceholderText("Listening for audio...")
        # Your backend's start function will be connected to this.

    def _on_stop_clicked(self):
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.transcript_area.setPlaceholderText("Click 'Start' to begin transcription.")
        # Your backend's stop function will be connected to this.

    # --- Public Methods (for your backend to call) ---
    def append_transcript_text(self, text):
        """Appends a chunk of text to the transcript area."""
        self.transcript_area.append(text)

    def update_notes_text(self, text):
        """Replaces the entire content of the notes area."""
        self.notes_area.setPlainText(text)

    # --- Window Dragging Logic ---
    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton and self.title_bar.underMouse():
            self.drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.drag_pos:
            self.move(event.globalPosition().toPoint() - self.drag_pos)

    def mouseReleaseEvent(self, event: QMouseEvent):
        self.drag_pos = None
import sys
from PySide6.QtWidgets import QApplication

from app.ui.main_window import MainWindow
from app.core.transcriber import Transcriber
from app.core.llm_handler import LLMHandler

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # 1. Create instances of all our components
    window = MainWindow()
    transcriber = Transcriber()
    llm_handler = LLMHandler()

    # --- 2. Connect the components with signals and slots ---

    # Connect UI controls to the Transcriber
    # When 'Start' is clicked, call the transcriber's start method.
    window.start_button.clicked.connect(transcriber.start)
    # When 'Stop' is clicked, call the transcriber's stop method.
    window.stop_button.clicked.connect(transcriber.stop)

    # Connect the Transcriber's output to the UI and the LLM Handler
    # When the transcriber emits new text...
    # ...append it to the UI's transcript area.
    transcriber.new_transcript_chunk.connect(window.append_transcript_text)
    # ...and also send it to the LLM handler for processing.
    transcriber.new_transcript_chunk.connect(llm_handler.process_text)

    # Connect the LLM Handler's output to the UI
    # When the LLM generates new notes...
    # ...update the UI's notes area with the new content.
    llm_handler.new_notes_generated.connect(window.update_notes_text)

    # --- 3. Show the UI and run the application ---
    window.show()
    sys.exit(app.exec())
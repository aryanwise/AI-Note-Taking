import ollama
from PySide6.QtCore import QObject, Signal

class LLMHandler(QObject):
    """
    Handles buffering text and interacting with the Ollama LLM to generate notes.
    """
    new_notes_generated = Signal(str)

    # --- Configuration ---
    BUFFER_WORD_LIMIT = 50 # Generate notes after collecting this many words.
    OLLAMA_MODEL = 'gemma3:270m' # The Ollama model to use.

    def __init__(self):
        super().__init__()
        self._text_buffer = []
        self._buffer_word_count = 0

    def process_text(self, text_chunk):
        """Public slot to receive text from the transcriber."""
        self._text_buffer.append(text_chunk)
        self._buffer_word_count += len(text_chunk.split())

        if self._buffer_word_count >= self.BUFFER_WORD_LIMIT:
            self.generate_notes_from_buffer()

    def generate_notes_from_buffer(self):
        """Generates notes from the current buffer and clears it."""
        if not self._text_buffer:
            return

        full_text = " ".join(self._text_buffer)
        
        # Clear the buffer immediately
        self._text_buffer.clear()
        self._buffer_word_count = 0
        
        print(f"Sending text to LLM: '{full_text[:100]}...'")

        try:
            # --- This is the prompt that generates the notes ---
            response = ollama.chat(
                model=self.OLLAMA_MODEL,
                messages=[
                    {
                        'role': 'system',
                        'content': 'You are an expert note-taking assistant. Your task is to summarize the following text into concise, clear bullet points. Focus on key topics, action items, and important names or figures.',
                    },
                    {
                        'role': 'user',
                        'content': full_text,
                    },
                ],
            )
            generated_notes = response['message']['content']
            self.new_notes_generated.emit(generated_notes)
            print("LLM generated new notes.")

        except Exception as e:
            error_message = f"Error connecting to Ollama: {e}"
            print(error_message)
            self.new_notes_generated.emit(f"NOTE: {error_message}")
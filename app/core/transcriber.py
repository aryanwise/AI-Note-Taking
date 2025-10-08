import sys
import sounddevice as sd
import numpy as np
import threading
from faster_whisper import WhisperModel
from PySide6.QtCore import QObject, Signal

class Transcriber(QObject):
    """
    Handles audio capture and speech-to-text transcription in a separate thread.
    Emits a signal with the transcribed text.
    """
    new_transcript_chunk = Signal(str)

    # --- Configuration ---
    MODEL_SIZE = "tiny.en"  # Fast and lightweight for an MVP. Can be "base.en", "small.en", etc.
    SAMPLE_RATE = 16000     # Whisper requires a 16kHz sample rate.
    CHUNK_SECONDS = 5       # Process audio in 5-second chunks. A good balance for real-time feel.
    
    def __init__(self):
        super().__init__()
        self._is_running = False
        self._thread = None
        
        try:
            print(f"Loading Whisper model: {self.MODEL_SIZE}...")
            # Using int8 for lower CPU usage, good for an MVP.
            self.model = WhisperModel(self.MODEL_SIZE, device="cpu", compute_type="int8")
            print("Whisper model loaded successfully.")
        except Exception as e:
            print(f"Error loading Whisper model: {e}")
            self.model = None

    def _audio_capture_thread(self):
        """The main loop for audio capture and transcription."""
        if not self.model:
            print("Cannot start transcription: Whisper model not loaded.")
            return

        # A buffer to hold incoming audio data
        audio_buffer = np.array([], dtype=np.float32)

        def audio_callback(indata, frames, time, status):
            nonlocal audio_buffer
            if status:
                print(status, file=sys.stderr)
            audio_buffer = np.append(audio_buffer, indata.flatten())

        try:
            stream = sd.InputStream(
                samplerate=self.SAMPLE_RATE,
                channels=1,
                dtype='float32',
                callback=audio_callback
            )
            stream.start()
            print("Audio stream started. Listening...")

            while self._is_running:
                chunk_size = self.SAMPLE_RATE * self.CHUNK_SECONDS
                if len(audio_buffer) >= chunk_size:
                    # Process the next chunk from the buffer
                    chunk_to_process = audio_buffer[:chunk_size]
                    audio_buffer = audio_buffer[chunk_size:]

                    # Transcribe the audio chunk
                    segments, _ = self.model.transcribe(chunk_to_process, beam_size=5)
                    
                    transcribed_text = "".join(seg.text for seg in segments).strip()
                    
                    if transcribed_text:
                        self.new_transcript_chunk.emit(transcribed_text)

                threading.Event().wait(0.1) # Prevent busy-waiting

            stream.stop()
            stream.close()
            print("Audio stream stopped.")
        except Exception as e:
            print(f"An error occurred in the audio stream: {e}")

    def start(self):
        """Starts the transcription process in a new thread."""
        if not self._is_running:
            self._is_running = True
            self._thread = threading.Thread(target=self._audio_capture_thread)
            self._thread.start()
            print("Transcription thread started.")

    def stop(self):
        """Stops the transcription process."""
        if self._is_running:
            self._is_running = False
            if self._thread:
                self._thread.join() # Wait for the thread to finish cleanly
            self._thread = None
            print("Transcription thread stopped.")
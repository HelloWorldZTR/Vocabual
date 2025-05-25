import threading
from playsound import playsound
import time
import os
import tempfile

class PlaysoundPlayer:
    def __init__(self):
        self._lock = threading.Lock()
        self._thread = None
        self._stop_event = threading.Event()
        self._current_file = None

    def play_raw(self, audio_data: bytes):
        with self._lock:
            self.stop()
            self._stop_event.clear()
            # Create a temporary file to hold the audio data
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
            print(f"[log] Playing audio from temporary file: {temp_file.name}")
            try:
                temp_file.write(audio_data)
                temp_file.close()
                # Remove the old file if it exists
                if self._current_file and os.path.exists(self._current_file):
                    os.remove(self._current_file)
                self._current_file = temp_file.name
                self._thread = threading.Thread(target=self._play_audio, args=(self._current_file,))
                self._thread.start()
            except Exception as e:
                print(f"[err] Error playing audio: {e}")


    def play(self, file_path: str):
        with self._lock:
            self.stop()
            self._stop_event.clear()
            self._current_file = file_path
            self._thread = threading.Thread(target=self._play_audio, args=(file_path,))
            self._thread.start()

    def stop(self):
        self._stop_event.set()
        if self._thread and self._thread.is_alive():
            self._thread.join()
        self._thread = None

    def _play_audio(self, file_path: str):
        try:
            # playsound is blocking, so we run it in a thread and kill the thread if needed
            # However, playsound does not support stopping playback natively.
            # This workaround is to play in a subprocess and kill it if needed.
            import subprocess
            import sys

            if sys.platform.startswith('win'):
                cmd = ['python', '-m', 'playsound', file_path]
            else:
                cmd = ['python3', '-m', 'playsound', file_path]

            proc = subprocess.Popen(cmd)
            while proc.poll() is None:
                if self._stop_event.is_set():
                    proc.terminate()
                    break
                time.sleep(0.1)
        except Exception as e:
            print(f"[err] Audio playback error: {e}")

    def __del__(self):
        self.stop()
        # Delete the temporary file if it exists
        if self._current_file and os.path.exists(self._current_file):
            os.remove(self._current_file)
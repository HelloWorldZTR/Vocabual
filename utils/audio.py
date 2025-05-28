import threading
import simpleaudio as sa
from pydub import AudioSegment
import io
import os

# root_dir = os.path.dirname(os.path.abspath(__file__))
# ffmpeg = os.path.join(root_dir, 'ffmpeg.exe')
# if not os.path.exists(ffmpeg):
#     print(f"[Error] ffmpeg.exe not found in {root_dir}. Please ensure ffmpeg is installed and available.")
# AudioSegment.converter = ffmpeg  # 设置ffmpeg路径
from pydub.utils import which
print(f"[Info] Using ffmpeg from: {which('ffmpeg')}")

class AudioPlayer:
    def __init__(self):
        self._play_obj = None
        self._lock = threading.Lock()

    def play_raw(self, mp3_bytes: bytes):
        def _play_thread(audio_data):
            with self._lock:
                if self._play_obj:
                    self._play_obj.stop()
                self._play_obj = sa.play_buffer(
                    audio_data.raw_data,
                    num_channels=audio_data.channels,
                    bytes_per_sample=audio_data.sample_width,
                    sample_rate=audio_data.frame_rate
                )

        try:
            # 使用 BytesIO 处理内存中的 MP3 数据
            mp3_io = io.BytesIO(mp3_bytes)
            audio_segment = AudioSegment.from_file(mp3_io,
                                                format="mp3", 
                                                parameters=["-analyzeduration", "1000000", "-probesize", "10000000"])\
                                                    .set_channels(2).set_sample_width(2).set_frame_rate(44100)
            thread = threading.Thread(target=_play_thread, args=(audio_segment,), daemon=True)
            thread.start()
        except Exception as e:
            print(f"[AudioPlayer] 播放失败: {e}")
    
    def play(self, mp3_path: str):
        print(f"[AudioPlayer] 播放音频: {mp3_path}")
        def _play_thread(audio_data):
            with self._lock:
                if self._play_obj:
                    self._play_obj.stop()
                self._play_obj = sa.play_buffer(
                    audio_data.raw_data,
                    num_channels=audio_data.channels,
                    bytes_per_sample=audio_data.sample_width,
                    sample_rate=audio_data.frame_rate
                )
        try:
            audio_segment = AudioSegment.from_file(mp3_path, format="mp3")
            threading.Thread(target=_play_thread, args=(audio_segment,), daemon=True).start()
        except Exception as e:
            try:
                audio_segment = AudioSegment.from_file(mp3_path, format="wav")
                threading.Thread(target=_play_thread, args=(audio_segment,), daemon=True).start()
            except Exception as e2:
                print("[AudioPlayer] 播放失败: ", e, e2)
        

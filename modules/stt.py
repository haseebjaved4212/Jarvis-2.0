"""
Speech-to-text module. Fully offline using faster-whisper.
Records a few seconds of audio from the mic and transcribes it to text.
"""

import importlib
import numpy as np
import tempfile
import wave
try:
    WhisperModel = importlib.import_module("faster_whisper").WhisperModel
except ImportError as exc:
    raise ImportError(
        "The 'faster-whisper' package is required. Install it with: "
        "pip install faster-whisper"
    ) from exc


try:
    sd = importlib.import_module("sounddevice")
except ImportError as exc:
    raise ImportError(
        "The 'sounddevice' package is required. Install it with: pip install sounddevice"
    ) from exc

# "base" is a good speed/accuracy tradeoff for a live assistant.
# Use "small" or "medium" if you have a decent GPU and want better accuracy.
MODEL_SIZE = "base"
SAMPLE_RATE = 16000

_model = None


def _get_model():
    global _model
    if _model is None:
        print("[STT] Loading Whisper model (first run may take a moment)...")
        _model = WhisperModel(MODEL_SIZE, device="cpu", compute_type="int8")
    return _model


def record_audio(duration=5, sample_rate=SAMPLE_RATE):
    """Records audio from the default microphone for `duration` seconds."""
    print(f"[STT] Listening for {duration}s...")
    audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype="int16")
    sd.wait()
    return audio


def transcribe(audio, sample_rate=SAMPLE_RATE):
    """Transcribes recorded audio to text using local Whisper."""
    model = _get_model()

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        with wave.open(tmp.name, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            wf.writeframes(audio.tobytes())

        segments, _ = model.transcribe(tmp.name, beam_size=5)
        text = " ".join(segment.text.strip() for segment in segments)

    return text.strip()


def listen_and_transcribe(duration=5):
    """Convenience wrapper: record then transcribe in one call."""
    audio = record_audio(duration)
    return transcribe(audio)
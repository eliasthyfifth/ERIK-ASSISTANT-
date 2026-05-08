import os
import numpy as np
import sounddevice as sd
from kokoro_onnx import Kokoro
import logging
from scipy.interpolate import interp1d
from .config import config

logger = logging.getLogger(__name__)

class TTSEngine:
    def __init__(self, model_path, voices_path):
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found: {model_path}")
        if not os.path.exists(voices_path):
            raise FileNotFoundError(f"Voices file not found: {voices_path}")
            
        logger.info(f"Loading Kokoro model from {model_path}")
        self.kokoro = Kokoro(model_path, voices_path)
        self.target_sample_rate = 44100  # More compatible rate
        self.output_device = config.get("voice.device_index")
        
        # Load custom voice if it exists
        self.custom_voice = None
        custom_path = config.get("voice.custom_voice_path")
        if custom_path and os.path.exists(custom_path):
            logger.info(f"Loading custom voice from {custom_path}")
            self.custom_voice = np.load(custom_path)

    def resample(self, audio, original_rate, target_rate):
        """Resamples audio using linear interpolation."""
        if original_rate == target_rate:
            return audio
        duration = len(audio) / original_rate
        time_old = np.linspace(0, duration, len(audio))
        time_new = np.linspace(0, duration, int(len(audio) * target_rate / original_rate))
        interpolator = interp1d(time_old, audio, kind='linear', fill_value="extrapolate")
        return interpolator(time_new).astype(np.float32)

    def speak(self, text, voice=None, speed=None, lang=None):
        if not text:
            return
            
        voice_key = voice or config.get("voice.default_voice", "af_heart")
        speed = speed or config.get("voice.speed", 1.1)
        lang = lang or config.get("voice.default_lang", "en-us")

        # Handle custom voice profile
        if voice_key == "custom" and self.custom_voice is not None:
            voice_to_use = self.custom_voice
        else:
            voice_to_use = voice_key

        logger.info(f"Speaking ({lang}, {voice_key}): {text}")
        
        try:
            samples, sample_rate = self.kokoro.create(
                text, 
                voice=voice_to_use, 
                speed=speed, 
                lang=lang
            )
            
            # Resample to target rate for better hardware compatibility
            resampled_audio = self.resample(samples, sample_rate, self.target_sample_rate)
            
            sd.play(resampled_audio, self.target_sample_rate, device=self.output_device)
            sd.wait()
        except Exception as e:
            logger.error(f"TTS Error: {e}")

_engine = None

def init_tts(model_path=None, voices_path=None):
    global _engine
    m_path = model_path or config.get("voice.model_path")
    v_path = voices_path or config.get("voice.voices_path")
    _engine = TTSEngine(m_path, v_path)

def speak(text, voice=None, speed=None, lang=None):
    if _engine:
        _engine.speak(text, voice, speed, lang)
    else:
        print(f"TTS Engine not initialized. Text: {text}")

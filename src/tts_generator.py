"""
Text-to-Speech modülü
Metni sese dönüştürür (ücretsiz/düşük maliyetli çözümler)
"""
import os
import pyttsx3
from gtts import gTTS
from pydub import AudioSegment
import tempfile
from typing import List, Dict

class TTSGenerator:
    def __init__(self, engine="gtts", language="tr", speed=150):
        self.engine = engine
        self.language = language
        self.speed = speed
        self.audio_dir = "audio"
        self.tts_engine = None
        
        # Klasör oluştur
        os.makedirs(self.audio_dir, exist_ok=True)
        
        # pyttsx3 için setup
        if engine == "pyttsx3":
            try:
                self.tts_engine = pyttsx3.init()
                self.tts_engine.setProperty('rate', speed)
                print("✓ pyttsx3 engine başlatıldı")
            except Exception as e:
                print(f"⚠ pyttsx3 başlatma hatası: {e}")
                print("🔄 gTTS'ye geçiliyor...")
                self.engine = "gtts"
    
    def generate_scene_audio(self, scene: Dict[str, str], output_filename: str) -> str:
        """Bir sahne için ses dosyası oluşturur"""
        text = scene['text']
        output_path = os.path.join(self.audio_dir, output_filename)
        
        if self.engine == "gtts":
            return self._generate_with_gtts(text, output_path)
        elif self.engine == "pyttsx3":
            return self._generate_with_pyttsx3(text, output_path)
        else:
            raise ValueError(f"Desteklenmeyen TTS engine: {self.engine}")
    
    def _generate_with_gtts(self, text: str, output_path: str) -> str:
        """Google TTS ile ses üretir (ücretsiz, internet gerekli)"""
        try:
            tts = gTTS(text=text, lang=self.language, slow=False)
            
            # Temporary file kullan
            with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_file:
                temp_path = temp_file.name
                tts.save(temp_path)
            
            # MP3'ü WAV'a dönüştür (video işleme için)
            audio = AudioSegment.from_mp3(temp_path)
            audio.export(output_path, format="wav")
            
            # Temp dosyayı sil
            os.unlink(temp_path)
            
            print(f"✓ Ses dosyası oluşturuldu: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"✗ gTTS hatası: {e}")
            # Fallback olarak pyttsx3 kullan
            return self._generate_with_pyttsx3(text, output_path)
    
    def _generate_with_pyttsx3(self, text: str, output_path: str) -> str:
        """pyttsx3 ile ses üretir (offline, ücretsiz)"""
        try:
            # Engine kontrolü
            if not hasattr(self, 'tts_engine') or self.tts_engine is None:
                self.tts_engine = pyttsx3.init()
                self.tts_engine.setProperty('rate', self.speed)
            
            # WAV formatında kaydet
            if not output_path.endswith('.wav'):
                output_path = output_path.replace('.mp3', '.wav')
            
            self.tts_engine.save_to_file(text, output_path)
            self.tts_engine.runAndWait()
            
            print(f"✓ Ses dosyası oluşturuldu (offline): {output_path}")
            return output_path
            
        except Exception as e:
            print(f"✗ pyttsx3 hatası: {e}")
            raise
    
    def generate_story_audio(self, scenes: List[Dict[str, str]], story_title: str) -> List[str]:
        """Tüm hikaye için ses dosyalarını oluşturur"""
        audio_files = []
        
        print(f"🎤 {story_title} için ses dosyaları oluşturuluyor...")
        
        # Kısa bir hikaye ID'si oluştur (dosya adı çok uzun olmasın - Windows limit 260 karakter)
        import hashlib
        story_hash = hashlib.md5(story_title.encode()).hexdigest()[:8]
        
        for i, scene in enumerate(scenes, 1):
            # Kısa dosya adı kullan
            filename = f"story_{story_hash}_scene_{i:02d}.wav"
            audio_path = self.generate_scene_audio(scene, filename)
            audio_files.append(audio_path)
        
        print(f"✓ {len(audio_files)} ses dosyası oluşturuldu")
        return audio_files
    
    def get_audio_duration(self, audio_path: str) -> float:
        """Ses dosyasının süresini döndürür"""
        try:
            audio = AudioSegment.from_wav(audio_path)
            return len(audio) / 1000.0  # millisecond to second
        except Exception as e:
            print(f"✗ Ses dosyası süresi alınamadı: {e}")
            return 5.0  # Varsayılan süre
    
    def combine_audio_files(self, audio_files: List[str], output_path: str, 
                          silence_duration: float = 1.0) -> str:
        """Ses dosyalarını birleştirir"""
        try:
            combined = AudioSegment.empty()
            silence = AudioSegment.silent(duration=silence_duration * 1000)
            
            for audio_file in audio_files:
                audio = AudioSegment.from_wav(audio_file)
                combined += audio + silence
            
            combined.export(output_path, format="wav")
            print(f"✓ Ses dosyaları birleştirildi: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"✗ Ses birleştirme hatası: {e}")
            raise
    
    def list_available_voices(self):
        """Mevcut sesleri listeler (pyttsx3 için)"""
        if self.engine == "pyttsx3":
            voices = self.tts_engine.getProperty('voices')
            print("Mevcut sesler:")
            for i, voice in enumerate(voices):
                print(f"{i}: {voice.name} - {voice.languages}")
        else:
            print("gTTS engine için ses seçenekleri:")
            print("- tr: Türkçe")
            print("- en: İngilizce")
            print("- de: Almanca")
            print("- fr: Fransızca")
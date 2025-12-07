"""
OpenAI TTS-1 HD API ile Text-to-Speech
Yüksek kaliteli, doğal sesli anlatım için OpenAI API kullanır
"""
import os
import hashlib
from typing import List, Dict
from openai import OpenAI
from pydub import AudioSegment

class OpenAITTSGenerator:
    def __init__(self, api_key: str, voice="alloy", language="tr", speed=1.0):
        """
        OpenAI TTS Generator
        
        Args:
            api_key: OpenAI API anahtarı
            voice: Ses seçeneği (alloy, echo, fable, onyx, nova, shimmer)
            language: Dil kodu (tr, en, vb.)
            speed: Konuşma hızı (0.25 - 4.0 arası, 1.0 normal)
        """
        self.client = OpenAI(api_key=api_key)
        self.voice = voice
        self.language = language
        self.speed = speed
        self.audio_dir = "audio"
        
        # Klasör oluştur
        os.makedirs(self.audio_dir, exist_ok=True)
        
        print(f"✓ OpenAI TTS-1 HD başlatıldı (ses: {voice}, hız: {speed})")
    
    def generate_scene_audio(self, scene: Dict[str, str], output_filename: str) -> str:
        """
        Bir sahne için ses dosyası oluşturur
        
        Args:
            scene: Sahne bilgisi (text içermeli)
            output_filename: Çıktı dosya adı
        
        Returns:
            Oluşturulan ses dosyasının yolu
        """
        text = scene['text']
        output_path = os.path.join(self.audio_dir, output_filename)
        
        try:
            # OpenAI TTS-1 HD ile ses üret
            response = self.client.audio.speech.create(
                model="tts-1-hd",  # Yüksek kalite model
                voice=self.voice,
                input=text,
                speed=self.speed
            )
            
            # MP3 olarak kaydet
            mp3_path = output_path.replace('.wav', '.mp3')
            response.stream_to_file(mp3_path)
            
            # MP3'ü WAV'a dönüştür (video işleme için)
            audio = AudioSegment.from_mp3(mp3_path)
            audio.export(output_path, format="wav")
            
            # MP3'ü sil
            os.unlink(mp3_path)
            
            print(f"✓ OpenAI TTS ses dosyası oluşturuldu: {output_filename}")
            return output_path
            
        except Exception as e:
            print(f"✗ OpenAI TTS hatası: {e}")
            raise
    
    def generate_story_audio(self, scenes: List[Dict[str, str]], story_title: str) -> List[str]:
        """
        Tüm hikaye için ses dosyalarını oluşturur
        
        Args:
            scenes: Sahne listesi
            story_title: Hikaye başlığı
        
        Returns:
            Oluşturulan ses dosyalarının yol listesi
        """
        audio_files = []
        
        print(f"🎤 OpenAI TTS-1 HD ile {story_title} seslendiriliyor...")
        print(f"   Ses: {self.voice} | Hız: {self.speed}")
        
        # Kısa bir hikaye ID'si oluştur (dosya adı çok uzun olmasın)
        story_hash = hashlib.md5(story_title.encode()).hexdigest()[:8]
        
        for i, scene in enumerate(scenes, 1):
            # Kısa dosya adı kullan
            filename = f"story_{story_hash}_scene_{i:02d}.wav"
            
            print(f"   [{i}/{len(scenes)}] Sahne {i} seslendiriliyor...")
            audio_path = self.generate_scene_audio(scene, filename)
            audio_files.append(audio_path)
        
        print(f"✓ {len(audio_files)} OpenAI TTS ses dosyası oluşturuldu")
        return audio_files
    
    def get_audio_duration(self, audio_path: str) -> float:
        """Ses dosyasının süresini döndürür (saniye)"""
        try:
            audio = AudioSegment.from_wav(audio_path)
            return len(audio) / 1000.0  # millisecond to second
        except Exception as e:
            print(f"✗ Ses dosyası süresi alınamadı: {e}")
            return 5.0  # Varsayılan süre
    
    def combine_audio_files(self, audio_files: List[str], output_path: str, 
                          silence_duration: float = 1.0) -> str:
        """
        Ses dosyalarını birleştirir
        
        Args:
            audio_files: Ses dosya yolları listesi
            output_path: Çıktı dosya yolu
            silence_duration: Sahneler arasındaki sessizlik süresi (saniye)
        
        Returns:
            Birleştirilmiş ses dosyasının yolu
        """
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
    
    @staticmethod
    def list_available_voices():
        """Mevcut sesleri listeler"""
        voices = {
            "alloy": "Dengeli, nötr kadın sesi (varsayılan)",
            "echo": "Erkek sesi, güçlü ve net",
            "fable": "İngiliz aksanlı erkek sesi, hikaye anlatımı için ideal",
            "onyx": "Derin erkek sesi, otoriter",
            "nova": "Genç kadın sesi, canlı ve enerji dolu",
            "shimmer": "Yumuşak kadın sesi, sakin ve profesyonel"
        }
        
        print("\n🎙️ OpenAI TTS-1 HD Ses Seçenekleri:")
        print("─" * 60)
        for voice_id, description in voices.items():
            print(f"  {voice_id:10s} - {description}")
        print("─" * 60)
        print("\n💡 Türkçe hikayeler için öneriler:")
        print("  • nova: Çocuk hikayeleri için canlı ve eğlenceli")
        print("  • fable: Klasik masal anlatımı için")
        print("  • shimmer: Sakin, yumuşak anlatım için")
        print()

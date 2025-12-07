"""
Render.com Background Worker - 7/24 Çalışan Hikaye İşleme Sistemi
"""

import os
import sys
import time
import json
import logging
from pathlib import Path
from datetime import datetime
import traceback

# Logging ayarları
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Telegram bildirimleri için (opsiyonel)
TELEGRAM_ENABLED = bool(os.getenv('TELEGRAM_BOT_TOKEN'))
if TELEGRAM_ENABLED:
    import requests

class TelegramNotifier:
    """Telegram üzerinden bildirim gönderir"""
    
    def __init__(self):
        self.bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.chat_id = os.getenv('TELEGRAM_CHAT_ID')
        self.enabled = bool(self.bot_token and self.chat_id)
    
    def send(self, message):
        """Mesaj gönder"""
        if not self.enabled:
            return
        
        try:
            url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
            data = {
                'chat_id': self.chat_id,
                'text': message,
                'parse_mode': 'HTML'
            }
            requests.post(url, data=data, timeout=10)
            logger.info(f"Telegram bildirimi gönderildi: {message[:50]}...")
        except Exception as e:
            logger.error(f"Telegram hatası: {e}")

class RenderWorker:
    """Render.com'da 7/24 çalışan worker"""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.stories_dir = self.base_dir / "stories"
        self.videos_dir = self.base_dir / "videos"
        self.progress_file = self.base_dir / "render_progress.json"
        
        # Klasörleri oluştur
        self.stories_dir.mkdir(exist_ok=True)
        self.videos_dir.mkdir(exist_ok=True)
        
        # Telegram
        self.telegram = TelegramNotifier()
        
        # İlerleme durumu
        self.progress = self.load_progress()
        
        logger.info("✅ RenderWorker başlatıldı!")
        self.telegram.send("🚀 <b>YouTube Story Worker Başlatıldı!</b>\n\nHikaye klasörü izleniyor...")
    
    def load_progress(self):
        """İlerleme dosyasını yükle"""
        if self.progress_file.exists():
            with open(self.progress_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            'completed': [],
            'failed': [],
            'last_check': None,
            'total_processed': 0
        }
    
    def save_progress(self):
        """İlerlemeyi kaydet"""
        with open(self.progress_file, 'w', encoding='utf-8') as f:
            json.dump(self.progress, f, ensure_ascii=False, indent=2)
    
    def get_pending_stories(self):
        """İşlenmemiş hikayeleri bul"""
        all_stories = list(self.stories_dir.glob('*.txt'))
        completed = set(self.progress['completed'])
        pending = [s for s in all_stories if s.stem not in completed]
        return sorted(pending)
    
    def process_story(self, story_file):
        """Tek bir hikayeyi işle"""
        story_name = story_file.stem
        
        logger.info(f"🎬 İşleniyor: {story_name}")
        self.telegram.send(f"🎬 <b>Yeni Hikaye İşleniyor</b>\n\n📝 {story_name}")
        
        try:
            # Ana modülleri import et
            from config.config import Config
            from src.story_processor import StoryProcessor
            from src.openai_tts_generator import OpenAITTSGenerator
            from src.multi_image_generator import MultiImageGenerator
            from src.character_manager import CharacterManager
            from src.video_creator import VideoCreator
            
            start_time = time.time()
            
            # 1. Hikaye işleme
            logger.info("📖 Hikaye işleniyor...")
            story_processor = StoryProcessor(
                stories_dir=str(self.stories_dir),
                deepseek_api_key=Config.DEEPSEEK_API_KEY
            )
            
            story_text = story_processor.load_story(story_file.name)
            story_title = story_processor.get_story_title(story_text)
            scenes = story_processor.split_into_scenes(story_text)
            
            logger.info(f"✓ {len(scenes)} sahne oluşturuldu")
            
            # 2. TTS oluştur
            logger.info("🎤 Sesler oluşturuluyor...")
            tts_generator = OpenAITTSGenerator(
                api_key=Config.OPENAI_API_KEY,
                voice=Config.OPENAI_TTS_VOICE,
                language=Config.TTS_LANGUAGE,
                speed=Config.OPENAI_TTS_SPEED
            )
            audio_files = tts_generator.generate_story_audio(scenes, story_title)
            logger.info(f"✓ {len(audio_files)} ses dosyası")
            
            # 3. Görseller oluştur
            logger.info("🖼️ Görseller oluşturuluyor...")
            char_manager = CharacterManager()
            
            if hasattr(story_processor, 'ai_response') and story_processor.ai_response:
                char_manager.extract_characters(story_processor.ai_response)
            
            image_generator = MultiImageGenerator(
                hf_token=Config.HUGGINGFACE_API_KEY,
                replicate_token=Config.REPLICATE_API_KEY,
                use_free_alternative=Config.USE_FREE_IMAGES_ONLY
            )
            image_generator.character_manager = char_manager
            
            image_files = image_generator.generate_story_images(scenes, story_title)
            logger.info(f"✓ {len(image_files)} görsel")
            
            # 4. Video oluştur
            logger.info("🎥 Video oluşturuluyor...")
            video_creator = VideoCreator(str(self.videos_dir))
            video_path = video_creator.create_story_video(
                scenes=scenes,
                image_files=image_files,
                audio_files=audio_files,
                story_title=story_title
            )
            
            if video_path and Path(video_path).exists():
                elapsed = time.time() - start_time
                file_size = Path(video_path).stat().st_size / (1024*1024)
                
                # İlerlemeyi kaydet
                self.progress['completed'].append(story_name)
                self.progress['total_processed'] += 1
                self.save_progress()
                
                # Başarı bildirimi
                message = (
                    f"✅ <b>Video Hazır!</b>\n\n"
                    f"📝 {story_title}\n"
                    f"📊 {file_size:.1f} MB\n"
                    f"🎬 {len(scenes)} sahne\n"
                    f"⏱️ {int(elapsed//60)} dakika {int(elapsed%60)} saniye"
                )
                self.telegram.send(message)
                logger.info(f"✅ Başarılı: {story_name}")
                
                # Temizlik
                try:
                    video_creator.cleanup_temp_files()
                except:
                    pass
                
                return True
            else:
                raise Exception("Video dosyası oluşturulamadı")
        
        except Exception as e:
            error_msg = str(e)
            error_trace = traceback.format_exc()
            
            # Hata kaydı
            self.progress['failed'].append({
                'story': story_name,
                'error': error_msg,
                'timestamp': datetime.now().isoformat()
            })
            self.save_progress()
            
            # Hata bildirimi
            self.telegram.send(
                f"❌ <b>Hata!</b>\n\n"
                f"📝 {story_name}\n"
                f"⚠️ {error_msg[:200]}"
            )
            logger.error(f"❌ Hata: {story_name}\n{error_trace}")
            return False
    
    def run(self):
        """Ana döngü - sürekli yeni hikaye kontrol et"""
        check_interval = int(os.getenv('STORIES_CHECK_INTERVAL', 300))  # 5 dakika
        
        logger.info(f"🔄 Ana döngü başladı (kontrol: {check_interval}s)")
        
        iteration = 0
        while True:
            try:
                iteration += 1
                logger.info(f"\n{'='*60}")
                logger.info(f"🔍 Kontrol #{iteration} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                logger.info(f"{'='*60}")
                
                # Yeni hikayeleri bul
                pending = self.get_pending_stories()
                
                if pending:
                    logger.info(f"📚 {len(pending)} yeni hikaye bulundu!")
                    
                    for story_file in pending:
                        self.process_story(story_file)
                        
                        # Her hikaye sonrası 30 saniye bekle (API koruması)
                        if len(pending) > 1:
                            logger.info("⏳ 30 saniye bekleniyor...")
                            time.sleep(30)
                else:
                    logger.info("📭 Yeni hikaye yok")
                
                # İlerleme güncelle
                self.progress['last_check'] = datetime.now().isoformat()
                self.save_progress()
                
                # Özet bilgi
                logger.info(f"\n📊 ÖZET:")
                logger.info(f"   ✅ Tamamlanan: {len(self.progress['completed'])}")
                logger.info(f"   ❌ Hatalı: {len(self.progress['failed'])}")
                logger.info(f"   ⏳ Bir sonraki kontrol: {check_interval}s sonra")
                
                # Bekle
                time.sleep(check_interval)
                
            except KeyboardInterrupt:
                logger.info("\n\n⚠️ Worker durduruldu (Ctrl+C)")
                self.telegram.send("⚠️ <b>Worker Durduruldu</b>")
                break
            
            except Exception as e:
                logger.error(f"❌ Ana döngü hatası: {e}")
                logger.error(traceback.format_exc())
                
                # Hata durumunda 60 saniye bekle
                time.sleep(60)

if __name__ == "__main__":
    logger.info("🚀 Render.com Worker başlatılıyor...")
    
    # API anahtarlarını kontrol et
    required_keys = ['OPENAI_API_KEY', 'DEEPSEEK_API_KEY', 'REPLICATE_API_KEY']
    missing_keys = [key for key in required_keys if not os.getenv(key)]
    
    if missing_keys:
        logger.error(f"❌ Eksik API anahtarları: {', '.join(missing_keys)}")
        logger.error("Render.com dashboard'dan Environment Variables ekleyin!")
        sys.exit(1)
    
    logger.info("✅ Tüm API anahtarları mevcut")
    
    # Worker'ı başlat
    worker = RenderWorker()
    worker.run()

"""
Render.com Cron Job - Günlük/Saatlik Otomatik Hikaye İşleme
"""

import os
import sys
import json
import logging
from pathlib import Path
from datetime import datetime
import traceback

# Logging ayarları
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Telegram bildirimleri
TELEGRAM_ENABLED = bool(os.getenv('TELEGRAM_BOT_TOKEN'))
if TELEGRAM_ENABLED:
    import requests

class TelegramNotifier:
    """Telegram bildirim sistemi"""
    
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
            logger.info(f"✅ Telegram bildirimi gönderildi")
        except Exception as e:
            logger.error(f"❌ Telegram hatası: {e}")

class CronWorker:
    """Render.com Cron Job - Her çalıştığında yeni hikayeleri işler"""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.stories_dir = self.base_dir / "stories"
        self.videos_dir = self.base_dir / "videos"
        self.progress_file = self.base_dir / "cron_progress.json"
        
        # Klasörleri oluştur
        self.stories_dir.mkdir(exist_ok=True)
        self.videos_dir.mkdir(exist_ok=True)
        
        # Telegram
        self.telegram = TelegramNotifier()
        
        # İlerleme durumu
        self.progress = self.load_progress()
        
        logger.info("="*70)
        logger.info("🔄 CRON JOB BAŞLATILDI")
        logger.info(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("="*70)
    
    def load_progress(self):
        """İlerleme dosyasını yükle"""
        if self.progress_file.exists():
            with open(self.progress_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            'completed': [],
            'failed': [],
            'last_run': None,
            'total_runs': 0,
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
        
        logger.info(f"\n🎬 İŞLENİYOR: {story_name}")
        logger.info("-" * 70)
        
        self.telegram.send(
            f"🎬 <b>Yeni Hikaye İşleniyor</b>\n\n"
            f"📝 {story_name}\n"
            f"🕐 {datetime.now().strftime('%H:%M')}"
        )
        
        try:
            # Modülleri import et
            from config.config import Config
            from src.story_processor import StoryProcessor
            from src.openai_tts_generator import OpenAITTSGenerator
            from src.multi_image_generator import MultiImageGenerator
            from src.character_manager import CharacterManager
            from src.video_creator import VideoCreator
            
            import time
            start_time = time.time()
            
            # 1. Hikaye işleme
            logger.info("📖 1. Hikaye işleniyor...")
            story_processor = StoryProcessor(
                stories_dir=str(self.stories_dir),
                deepseek_api_key=Config.DEEPSEEK_API_KEY
            )
            
            story_text = story_processor.load_story(story_file.name)
            story_title = story_processor.get_story_title(story_text)
            scenes = story_processor.split_into_scenes(story_text)
            
            logger.info(f"   ✓ Hikaye: {story_title}")
            logger.info(f"   ✓ {len(scenes)} sahne oluşturuldu")
            
            # 2. TTS oluştur
            logger.info("\n🎤 2. Sesler oluşturuluyor...")
            tts_generator = OpenAITTSGenerator(
                api_key=Config.OPENAI_API_KEY,
                voice=Config.OPENAI_TTS_VOICE,
                language=Config.TTS_LANGUAGE,
                speed=Config.OPENAI_TTS_SPEED
            )
            audio_files = tts_generator.generate_story_audio(scenes, story_title)
            logger.info(f"   ✓ {len(audio_files)} ses dosyası")
            
            # 3. Görseller
            logger.info("\n🖼️ 3. Görseller oluşturuluyor...")
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
            logger.info(f"   ✓ {len(image_files)} görsel")
            
            # 4. Video
            logger.info("\n🎥 4. Video oluşturuluyor...")
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
                video_info = video_creator.get_video_info(video_path)
                
                # İlerleme kaydet
                self.progress['completed'].append(story_name)
                self.progress['total_processed'] += 1
                self.save_progress()
                
                # Başarı bildirimi
                logger.info(f"\n✅ BAŞARILI: {story_name}")
                logger.info(f"📁 Video: {video_path}")
                logger.info(f"📊 Boyut: {file_size:.1f} MB")
                logger.info(f"⏱️  Süre: {int(elapsed//60)}dk {int(elapsed%60)}sn")
                
                self.telegram.send(
                    f"✅ <b>Video Hazır!</b>\n\n"
                    f"📝 {story_title}\n"
                    f"📊 {file_size:.1f} MB\n"
                    f"🎬 {len(scenes)} sahne\n"
                    f"⏱️ {int(elapsed//60)}dk {int(elapsed%60)}sn"
                )
                
                # Temizlik
                try:
                    video_creator.cleanup_temp_files()
                except:
                    pass
                
                return True
            else:
                raise Exception("Video oluşturulamadı")
        
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
            
            logger.error(f"\n❌ HATA: {story_name}")
            logger.error(f"Mesaj: {error_msg}")
            logger.error(f"Trace:\n{error_trace}")
            
            self.telegram.send(
                f"❌ <b>Hata!</b>\n\n"
                f"📝 {story_name}\n"
                f"⚠️ {error_msg[:150]}"
            )
            
            return False
    
    def run(self):
        """Ana işlem - yeni hikayeleri işle"""
        try:
            # Run sayacı
            self.progress['total_runs'] += 1
            self.progress['last_run'] = datetime.now().isoformat()
            
            # Yeni hikayeleri bul
            pending = self.get_pending_stories()
            
            logger.info(f"\n📊 DURUM:")
            logger.info(f"   🔍 Run #{self.progress['total_runs']}")
            logger.info(f"   📚 Bekleyen hikaye: {len(pending)}")
            logger.info(f"   ✅ Tamamlanan: {len(self.progress['completed'])}")
            logger.info(f"   ❌ Hatalı: {len(self.progress['failed'])}")
            
            if not pending:
                logger.info("\n📭 Yeni hikaye yok, bekleniyor...")
                self.telegram.send(
                    f"📭 <b>Cron Job Çalıştı</b>\n\n"
                    f"🔍 Run #{self.progress['total_runs']}\n"
                    f"📚 Yeni hikaye yok\n"
                    f"✅ Toplam işlenen: {len(self.progress['completed'])}"
                )
                self.save_progress()
                return
            
            # Hikayeleri işle
            logger.info(f"\n🚀 {len(pending)} HİKAYE İŞLENECEK\n")
            
            success_count = 0
            fail_count = 0
            
            for i, story_file in enumerate(pending, 1):
                logger.info(f"\n{'='*70}")
                logger.info(f"İLERLEME: [{i}/{len(pending)}] {story_file.stem}")
                logger.info(f"{'='*70}")
                
                result = self.process_story(story_file)
                if result:
                    success_count += 1
                else:
                    fail_count += 1
                
                # Her hikaye arası 30 saniye (API koruması)
                if i < len(pending):
                    logger.info("\n⏳ 30 saniye bekleniyor...")
                    import time
                    time.sleep(30)
            
            # Özet
            logger.info(f"\n\n{'='*70}")
            logger.info(f"🎉 CRON JOB TAMAMLANDI!")
            logger.info(f"{'='*70}")
            logger.info(f"✅ Başarılı: {success_count}")
            logger.info(f"❌ Hatalı: {fail_count}")
            logger.info(f"📊 Toplam tamamlanan: {len(self.progress['completed'])}")
            logger.info(f"{'='*70}\n")
            
            # Özet bildirimi
            self.telegram.send(
                f"🎉 <b>Cron Job Tamamlandı</b>\n\n"
                f"✅ Başarılı: {success_count}\n"
                f"❌ Hatalı: {fail_count}\n"
                f"📊 Toplam: {len(self.progress['completed'])}"
            )
            
            self.save_progress()
            
        except Exception as e:
            logger.error(f"\n❌ FATAL ERROR: {e}")
            logger.error(traceback.format_exc())
            
            self.telegram.send(
                f"🔥 <b>Kritik Hata!</b>\n\n"
                f"⚠️ {str(e)[:200]}"
            )
            
            sys.exit(1)

if __name__ == "__main__":
    # API kontrolü
    required_keys = ['OPENAI_API_KEY', 'DEEPSEEK_API_KEY', 'REPLICATE_API_KEY']
    missing = [k for k in required_keys if not os.getenv(k)]
    
    if missing:
        logger.error(f"❌ Eksik API anahtarları: {', '.join(missing)}")
        sys.exit(1)
    
    logger.info("✅ API anahtarları OK")
    
    # Worker'ı çalıştır
    worker = CronWorker()
    worker.run()
    
    logger.info("\n✨ Cron job başarıyla tamamlandı!")
    sys.exit(0)

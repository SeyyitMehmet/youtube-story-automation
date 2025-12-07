#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
YouTube Story Automation - Ana Program
Hikayeleri otomatik olarak videoya dönüştürür ve YouTube'a yükler
"""

import os
import sys
import shutil
from colorama import init, Fore, Style
from config.config import Config
from src.story_processor import StoryProcessor
from src.tts_generator import TTSGenerator
from src.openai_tts_generator import OpenAITTSGenerator
from src.image_generator import ImageGenerator

# Video creator - conditional import
try:
    from src.video_creator import VideoCreator
    VIDEO_CREATOR_AVAILABLE = True
except ImportError:
    VIDEO_CREATOR_AVAILABLE = False
    print("⚠ VideoCreator modülü kullanılamaz (MoviePy kurulu değil)")

try:
    from src.youtube_uploader import YouTubeUploader  
    YOUTUBE_UPLOADER_AVAILABLE = True
except ImportError:
    YOUTUBE_UPLOADER_AVAILABLE = False

# Colorama'yı başlat (Windows için renkli konsol)
init(autoreset=True)

def print_banner():
    """Program başlığını yazdırır"""
    banner = f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║           🎬 YouTube Hikaye Otomasyonu 🎬                   ║
║                                                              ║
║     AI destekli hikaye anlatım video üretimi                ║
║     Kibritçi Kız hikayesi -> YouTube video                  ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""
    print(banner)

def print_step(step_num, total_steps, description):
    """Adım numarasını yazdırır"""
    print(f"\n{Fore.YELLOW}[{step_num}/{total_steps}] {description}{Style.RESET_ALL}")

def cleanup_folders():
    """Video oluşturma öncesi klasörleri temizler"""
    folders = ['audio', 'images', 'videos']
    print(f"\n{Fore.CYAN}🗑️  Klasörler temizleniyor...{Style.RESET_ALL}")
    
    for folder in folders:
        folder_path = os.path.join(os.getcwd(), folder)
        if os.path.exists(folder_path):
            try:
                # Klasördeki tüm dosyaları sil
                for filename in os.listdir(folder_path):
                    file_path = os.path.join(folder_path, filename)
                    try:
                        if os.path.isfile(file_path) or os.path.islink(file_path):
                            os.unlink(file_path)
                        elif os.path.isdir(file_path):
                            shutil.rmtree(file_path)
                    except Exception as e:
                        print(f"{Fore.RED}   ⚠️  {filename} silinirken hata: {e}{Style.RESET_ALL}")
                
                print(f"{Fore.GREEN}   ✓ {folder}/ klasörü temizlendi{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}   ✗ {folder}/ temizlenirken hata: {e}{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}   ⓘ {folder}/ klasörü bulunamadı{Style.RESET_ALL}")

    print("─" * 60)

def create_story_video(story_filename="kibritci_kiz.txt", upload_to_youtube=False):
    """Ana video oluşturma fonksiyonu"""
    
    print_banner()
    
    # Klasörleri temizle (her çalıştırmada yeni başla)
    cleanup_folders()
    
    try:
        # 1. Hikaye işleme
        print_step(1, 6, "📚 Hikaye yükleniyor ve işleniyor")
        
        story_processor = StoryProcessor(
            stories_dir=Config.STORIES_DIR,
            deepseek_api_key=Config.DEEPSEEK_API_KEY
        )
        story_text = story_processor.load_story(story_filename)
        story_title = story_processor.get_story_title(story_text)
        scenes = story_processor.split_into_scenes(story_text)
        
        print(f"✓ Hikaye: {Fore.GREEN}{story_title}{Style.RESET_ALL}")
        print(f"✓ {len(scenes)} sahne oluşturuldu")
        
        # 2. Ses dosyaları oluşturma
        print_step(2, 6, "🎤 Ses dosyaları oluşturuluyor (TTS)")
        
        # TTS Engine seçimi
        if Config.TTS_ENGINE == "openai":
            # OpenAI TTS-1 HD kullan
            if not Config.OPENAI_API_KEY:
                print(f"{Fore.RED}✗ OPENAI_API_KEY bulunamadı! .env dosyasını kontrol edin.{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}🔄 Yedek TTS (gtts) kullanılıyor...{Style.RESET_ALL}")
                tts_generator = TTSGenerator(
                    engine="gtts",
                    language=Config.TTS_LANGUAGE,
                    speed=Config.TTS_SPEED
                )
            else:
                tts_generator = OpenAITTSGenerator(
                    api_key=Config.OPENAI_API_KEY,
                    voice=Config.OPENAI_TTS_VOICE,
                    language=Config.TTS_LANGUAGE,
                    speed=Config.OPENAI_TTS_SPEED
                )
        else:
            # Klasik TTS (gtts veya pyttsx3) kullan
            tts_generator = TTSGenerator(
                engine=Config.TTS_ENGINE,
                language=Config.TTS_LANGUAGE,
                speed=Config.TTS_SPEED
            )
        
        audio_files = tts_generator.generate_story_audio(scenes, story_title)
        print(f"✓ {len(audio_files)} ses dosyası oluşturuldu")
        
        # 3. Görsel oluşturma
        print_step(3, 6, "🎨 Görseller oluşturuluyor")
        
        from src.multi_image_generator import MultiImageGenerator
        from src.character_manager import CharacterManager
        
        # Karakter yöneticisini başlat
        char_manager = CharacterManager()
        
        # AI'dan gelen karakterleri çıkar (eğer varsa)
        if hasattr(story_processor, 'ai_response') and story_processor.ai_response:
            characters = char_manager.extract_characters(story_processor.ai_response)
            if characters:
                print(f"\n{Fore.CYAN}👥 Karakter Tutarlılığı Sistemi Aktif{Style.RESET_ALL}")
                print(char_manager.get_all_character_info())
        
        image_generator = MultiImageGenerator(
            hf_token=Config.HUGGINGFACE_API_KEY,
            replicate_token=Config.REPLICATE_API_KEY,
            use_free_alternative=Config.USE_FREE_IMAGES_ONLY
        )
        
        # Karakter yöneticisini image generator'a bağla
        image_generator.character_manager = char_manager
        
        # API'leri test et
        print("🔍 Resim API'leri test ediliyor...")
        api_results = image_generator.test_all_apis()
        
        working_apis = [api for api, status in api_results.items() if status]
        if working_apis:
            print(f"✓ Çalışan API'ler: {', '.join(working_apis)}")
        else:
            print("⚠ Hiçbir ücretli API çalışmıyor, ücretsiz seçenekler kullanılacak")
        
        image_files = image_generator.generate_story_images(scenes, story_title)
        print(f"✓ {len(image_files)} görsel oluşturuldu")
        
        # 4. Video oluşturma (MoviePy gerekli)
        if VIDEO_CREATOR_AVAILABLE:
            print_step(4, 6, "🎬 Video birleştiriliyor")
            
            video_creator = VideoCreator(Config.VIDEOS_DIR)
            video_path = video_creator.create_story_video(
                scenes=scenes,
                image_files=image_files,
                audio_files=audio_files,
                story_title=story_title
            )
            
            # Video bilgilerini göster
            video_info = video_creator.get_video_info(video_path)
            print(f"✅ Video oluşturuldu: {Fore.GREEN}{video_path}{Style.RESET_ALL}")
            print(f"📊 Süre: {video_info.get('duration', 0):.1f} saniye")
            print(f"📏 Boyut: {video_info.get('size', 'Bilinmiyor')}")
            print(f"💾 Dosya boyutu: {video_info.get('filesize', 0) / (1024*1024):.1f} MB")
            
            # 5. Önizleme oluşturma
            print_step(5, 6, "👀 Önizleme oluşturuluyor")
            
            try:
                preview_path = video_creator.create_preview_video(video_path, duration=30)
                print(f"✓ Önizleme: {preview_path}")
            except Exception as e:
                print(f"⚠ Önizleme oluşturulamadı: {e}")
            
            final_step = 6
            
        else:
            print_step(4, 4, "⏭ Video oluşturma atlandı (MoviePy kurulu değil)")
            print("💡 FFmpeg kurup MoviePy'yi yükledikten sonra video oluşturabilirsiniz")
            print("📁 Ses ve görsel dosyaları hazır:")
            
            for i, (audio, image) in enumerate(zip(audio_files, image_files), 1):
                print(f"   Sahne {i}: {os.path.basename(audio)} + {os.path.basename(image)}")
            
            video_path = None
            final_step = 4
        
        # Temizlik
        if VIDEO_CREATOR_AVAILABLE:
            try:
                video_creator.cleanup_temp_files()
            except:
                pass
        
        # Başarı mesajı
        print(f"\n{Fore.GREEN}🎉 İşlem tamamlandı!{Style.RESET_ALL}")
        
        if video_path:
            print(f"📁 Video dosyası: {video_path}")
            print(f"🔗 Yerel önizleme için video player ile açabilirsiniz")
        else:
            print(f"📁 Ses dosyaları: audio/ klasöründe")
            print(f"� Görsel dosyaları: images/ klasöründe")
            print(f"� MoviePy kurulduğunda bunlardan video oluşturulabilir")
        
        return video_path or "ses_ve_görsel_hazır"
        
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}❌ İşlem kullanıcı tarafından iptal edildi{Style.RESET_ALL}")
        return None
    except Exception as e:
        print(f"\n{Fore.RED}❌ Hata oluştu: {e}{Style.RESET_ALL}")
        return None

def setup_environment():
    """Çevre değişkenlerini ve API anahtarlarını kontrol eder"""
    print(f"{Fore.CYAN}🔧 Sistem kontrolleri{Style.RESET_ALL}")
    print("─" * 40)
    
    # API anahtarları kontrolü
    if Config.DEEPSEEK_API_KEY:
        print(f"✓ DeepSeek API key: {'*' * 20}...")
    else:
        print("⚠ DeepSeek API key tanımlanmamış (.env dosyasına DEEPSEEK_API_KEY ekleyin)")
    
    if Config.YOUTUBE_CLIENT_ID:
        print(f"✓ YouTube Client ID: {'*' * 20}...")
    else:
        print("⚠ YouTube credentials tanımlanmamış (isteğe bağlı)")
    
    # Klasör yapısı kontrolü
    required_dirs = [Config.STORIES_DIR, Config.AUDIO_DIR, Config.IMAGES_DIR, Config.VIDEOS_DIR]
    for dir_path in required_dirs:
        if os.path.exists(dir_path):
            print(f"✓ Klasör mevcut: {dir_path}")
        else:
            os.makedirs(dir_path, exist_ok=True)
            print(f"✓ Klasör oluşturuldu: {dir_path}")
    
    print()

def show_menu():
    """Ana menüyü gösterir"""
    menu = f"""
{Fore.CYAN}📋 Ana Menü{Style.RESET_ALL}
─────────────

1. 🎬 Kibritçi Kız videosunu oluştur
2.  Sistem kontrolü
3. 🧪 API testleri  
4. ❌ Çıkış

"""
    print(menu)

def run_api_tests():
    """API testlerini çalıştırır"""
    print(f"{Fore.CYAN}🧪 API Testleri{Style.RESET_ALL}")
    print("─" * 40)
    
    # TTS testleri
    print("🎤 TTS Testleri...")
    print("─" * 40)
    
    # 1. OpenAI TTS-1 HD testi
    if Config.OPENAI_API_KEY:
        print("\n1️⃣  OpenAI TTS-1 HD Test...")
        try:
            openai_tts = OpenAITTSGenerator(
                api_key=Config.OPENAI_API_KEY,
                voice=Config.OPENAI_TTS_VOICE,
                speed=Config.OPENAI_TTS_SPEED
            )
            test_scene = {
                'text': 'Merhaba, ben OpenAI TTS-1 HD sistemi. Bu bir test mesajıdır.',
                'scene_number': 1
            }
            audio_path = openai_tts.generate_scene_audio(test_scene, 'test_openai_tts.wav')
            if os.path.exists(audio_path):
                print(f"{Fore.GREEN}✓ OpenAI TTS-1 HD çalışıyor{Style.RESET_ALL}")
                print(f"  Ses: {Config.OPENAI_TTS_VOICE} | Hız: {Config.OPENAI_TTS_SPEED}")
                print(f"  Test dosyası: {audio_path}")
                # Test dosyasını silme - dinlemek için bırak
            else:
                print(f"{Fore.RED}❌ OpenAI TTS-1 HD başarısız{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}❌ OpenAI TTS-1 HD hatası: {e}{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}⚠  OpenAI API key tanımlanmamış (.env dosyasına OPENAI_API_KEY ekleyin){Style.RESET_ALL}")
    
    # 2. Klasik TTS (gtts) testi
    print("\n2️⃣  Klasik TTS (gTTS) Test...")
    try:
        tts = TTSGenerator(engine="gtts")
        test_scene = {
            'text': 'Bu bir test mesajıdır. Klasik TTS sistemi.',
            'scene_number': 1
        }
        audio_path = tts.generate_scene_audio(test_scene, 'test_gtts.wav')
        if os.path.exists(audio_path):
            print(f"{Fore.GREEN}✓ gTTS çalışıyor{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}❌ gTTS başarısız{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}❌ gTTS hatası: {e}{Style.RESET_ALL}")
    
    # Resim API testleri
    print("\n🎨 Resim API Testleri...")
    try:
        from src.multi_image_generator import MultiImageGenerator
        
        img_gen = MultiImageGenerator(
            hf_token=Config.HUGGINGFACE_API_KEY,
            replicate_token=Config.REPLICATE_API_KEY
        )
        
        api_results = img_gen.test_all_apis()
        
        for api_name, status in api_results.items():
            status_text = "✓ Çalışıyor" if status else "❌ Çalışmıyor"
            print(f"  {api_name.title()}: {status_text}")
        
        # Test görseli oluştur
        test_scene = {
            'scene_number': 1,
            'image_prompt': 'A beautiful fairy tale scene with magical lighting'
        }
        image_path = img_gen.generate_scene_image(test_scene, 'api_test_image.jpg')
        if os.path.exists(image_path):
            print("✓ Test görseli başarıyla oluşturuldu")
            os.remove(image_path)  # Test dosyasını sil
        
    except Exception as e:
        print(f"❌ Resim API test hatası: {e}")
    
    # DeepSeek Chat API testi (hikaye analizi)
    if Config.DEEPSEEK_API_KEY:
        print("\n� DeepSeek Chat API Test...")
        try:
            from src.deepseek_processor import DeepSeekProcessor
            
            deepseek = DeepSeekProcessor(Config.DEEPSEEK_API_KEY)
            if deepseek.test_connection():
                print("✓ DeepSeek Chat API çalışıyor")
            else:
                print("❌ DeepSeek Chat API başarısız")
        except Exception as e:
            print(f"❌ DeepSeek Chat API hatası: {e}")
    
    # YouTube API testi (geçici olarak devre dışı)
    # if Config.YOUTUBE_CLIENT_ID:
    #     print("\n📤 YouTube API Test...")
    #     try:
    #         uploader = YouTubeUploader(
    #             client_id=Config.YOUTUBE_CLIENT_ID,
    #             client_secret=Config.YOUTUBE_CLIENT_SECRET
    #         )
    #         if uploader.test_api_connection():
    #             print("✓ YouTube API çalışıyor")
    #         else:
    #             print("❌ YouTube API başarısız")
    #     except Exception as e:
    #         print(f"❌ YouTube API hatası: {e}")
    
    print("\n💡 Not: YouTube entegrasyonu şu an devre dışı (en son aşamada aktif edilecek)")

def main():
    """Ana program"""
    setup_environment()
    
    while True:
        show_menu()
        
        try:
            choice = input(f"{Fore.YELLOW}Seçiminizi yapın (1-4): {Style.RESET_ALL}").strip()
            
            if choice == "1":
                print("\n🎬 Video oluşturuluyor...")
                result = create_story_video(upload_to_youtube=False)
                if result:
                    input(f"\n{Fore.GREEN}✅ Devam etmek için Enter'a basın...{Style.RESET_ALL}")
            
            elif choice == "2":
                setup_environment()
                input(f"\n{Fore.GREEN}✅ Devam etmek için Enter'a basın...{Style.RESET_ALL}")
            
            elif choice == "3":
                run_api_tests()
                input(f"\n{Fore.GREEN}✅ Devam etmek için Enter'a basın...{Style.RESET_ALL}")
            
            elif choice == "4":
                print(f"\n{Fore.GREEN}👋 Görüşmek üzere!{Style.RESET_ALL}")
                break
            
            else:
                print(f"{Fore.RED}❌ Geçersiz seçim! Lütfen 1-4 arası bir sayı girin.{Style.RESET_ALL}")
                
        except KeyboardInterrupt:
            print(f"\n\n{Fore.GREEN}👋 Program sonlandırıldı.{Style.RESET_ALL}")
            break
        except Exception as e:
            print(f"{Fore.RED}❌ Hata: {e}{Style.RESET_ALL}")
            input("Devam etmek için Enter'a basın...")

if __name__ == "__main__":
    main()
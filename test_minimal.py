#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Minimal Demo - Sadece temel fonksiyonları test eder
"""

import os
import sys
from colorama import init, Fore, Style

# Colorama'yı başlat
init(autoreset=True)

def test_story_and_image():
    """Hikaye ve görsel testi"""
    print(f"{Fore.CYAN}🧪 Minimal Test - Hikaye + Görsel{Style.RESET_ALL}")
    print("=" * 50)
    
    try:
        # 1. Hikaye işleme
        print("📚 Hikaye yükleniyor...")
        sys.path.append('.')
        from src.story_processor import StoryProcessor
        
        processor = StoryProcessor("stories")
        story_text = processor.load_story("kibritci_kiz.txt")
        story_title = processor.get_story_title(story_text)
        scenes = processor.split_into_scenes(story_text)
        
        print(f"✓ Hikaye: {story_title}")
        print(f"✓ Sahne sayısı: {len(scenes)}")
        
        # 2. Görsel oluşturma (sadece 1 sahne)
        print("\n🎨 Test görseli oluşturuluyor...")
        from src.image_generator import ImageGenerator
        
        img_gen = ImageGenerator(use_free_alternative=True)
        test_scene = scenes[0]  # İlk sahne
        
        image_path = img_gen.generate_scene_image(test_scene, "test_minimal.jpg")
        
        if os.path.exists(image_path):
            size = os.path.getsize(image_path) / 1024
            print(f"✓ Görsel oluşturuldu: {image_path} ({size:.1f} KB)")
        
        # 3. gTTS testi (internet bağlantısı varsa)
        print("\n🎤 gTTS testi...")
        try:
            from gtts import gTTS
            import tempfile
            
            test_text = "Bu bir test mesajıdır."
            tts = gTTS(text=test_text, lang='tr', slow=False)
            
            with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_file:
                temp_path = temp_file.name
                tts.save(temp_path)
            
            if os.path.exists(temp_path):
                size = os.path.getsize(temp_path) / 1024
                print(f"✓ gTTS çalışıyor: test dosyası ({size:.1f} KB)")
                os.unlink(temp_path)
            
        except Exception as e:
            print(f"⚠ gTTS test hatası: {e}")
        
        print(f"\n{Fore.GREEN}✅ Minimal test başarılı!{Style.RESET_ALL}")
        print("🔧 Temel sistem çalışıyor. MoviePy kurulduğunda video üretimi de çalışacak.")
        
        return True
        
    except Exception as e:
        print(f"❌ Test hatası: {e}")
        return False

def show_next_steps():
    """Sonraki adımları göster"""
    print(f"\n{Fore.YELLOW}📋 Sonraki Adımlar:{Style.RESET_ALL}")
    print("1. 🎬 MoviePy kurulumu için:")
    print("   - FFmpeg'i sisteminize kurun")
    print("   - pip install moviepy komutu ile tekrar deneyin")
    print()
    print("2. 🔑 API Anahtarları (.env dosyası):")
    print("   - DEEPSEEK_API_KEY: Gelişmiş görseller için")
    print("   - YOUTUBE_CLIENT_ID/SECRET: YouTube yükleme için")
    print()
    print("3. 🚀 Kullanım:")
    print("   - python main.py (tam özellikli program)")
    print("   - python demo.py (basit test)")

def main():
    """Ana fonksiyon"""
    print(f"{Fore.GREEN}🎬 YouTube Story Automation{Style.RESET_ALL}")
    print("Minimal Test Sürümü\n")
    
    success = test_story_and_image()
    
    if success:
        show_next_steps()
    else:
        print(f"{Fore.RED}❌ Test başarısız{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
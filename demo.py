#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Basit Demo - MoviePy olmadan temel fonksiyonları test eder
"""

import os
import sys
from colorama import init, Fore, Style

# Colorama'yı başlat
init(autoreset=True)

def demo_story_processing():
    """Hikaye işleme demo"""
    print(f"{Fore.CYAN}=== 📚 Hikaye İşleme Demo ==={Style.RESET_ALL}")
    
    try:
        sys.path.append('.')
        from src.story_processor import StoryProcessor
        
        processor = StoryProcessor("stories")
        story_text = processor.load_story("kibritci_kiz.txt")
        story_title = processor.get_story_title(story_text)
        scenes = processor.split_into_scenes(story_text)
        
        print(f"✓ Hikaye başlığı: {Fore.GREEN}{story_title}{Style.RESET_ALL}")
        print(f"✓ Sahne sayısı: {len(scenes)}")
        print()
        
        for i, scene in enumerate(scenes, 1):
            print(f"{Fore.YELLOW}Sahne {i}:{Style.RESET_ALL}")
            print(f"  Metin: {scene['text'][:100]}...")
            print(f"  Süre: {scene['duration']:.1f} saniye")
            print(f"  Görsel: {scene['image_prompt'][:80]}...")
            print()
        
        return scenes, story_title
        
    except Exception as e:
        print(f"❌ Hata: {e}")
        return None, None

def demo_tts(scenes, story_title):
    """TTS demo"""
    print(f"{Fore.CYAN}=== 🎤 TTS Demo ==={Style.RESET_ALL}")
    
    if not scenes:
        print("❌ Sahne verisi yok")
        return []
    
    try:
        from src.tts_generator import TTSGenerator
        
        # Offline TTS kullan (internet bağlantısı sorunu olabilir)
        tts = TTSGenerator(engine="pyttsx3", language="tr", speed=150)
        
        print("🎤 Ses dosyaları oluşturuluyor...")
        
        # Sadece ilk 2 sahne için test
        test_scenes = scenes[:2]
        audio_files = []
        
        for i, scene in enumerate(test_scenes, 1):
            print(f"  Sahne {i} seslendiriliyor...")
            filename = f"test_scene_{i:02d}.wav"
            
            try:
                audio_path = tts.generate_scene_audio(scene, filename)
                audio_files.append(audio_path)
                print(f"  ✓ {filename} oluşturuldu")
            except Exception as e:
                print(f"  ❌ Ses oluşturma hatası: {e}")
        
        print(f"✓ {len(audio_files)} ses dosyası oluşturuldu")
        return audio_files
        
    except Exception as e:
        print(f"❌ TTS Hatası: {e}")
        return []

def demo_image_generation(scenes, story_title):
    """Görsel üretimi demo"""
    print(f"{Fore.CYAN}=== 🎨 Görsel Üretimi Demo ==={Style.RESET_ALL}")
    
    if not scenes:
        print("❌ Sahne verisi yok")
        return []
    
    try:
        from src.image_generator import ImageGenerator
        
        # Ücretsiz alternatif kullan
        img_gen = ImageGenerator(use_free_alternative=True)
        
        print("🎨 Görseller oluşturuluyor...")
        
        # Sadece ilk 2 sahne için test
        test_scenes = scenes[:2]
        image_files = []
        
        for i, scene in enumerate(test_scenes, 1):
            print(f"  Sahne {i} görseli oluşturuluyor...")
            filename = f"test_scene_{i:02d}.jpg"
            
            try:
                image_path = img_gen.generate_scene_image(scene, filename)
                image_files.append(image_path)
                print(f"  ✓ {filename} oluşturuldu")
            except Exception as e:
                print(f"  ❌ Görsel oluşturma hatası: {e}")
        
        print(f"✓ {len(image_files)} görsel oluşturuldu")
        return image_files
        
    except Exception as e:
        print(f"❌ Görsel Hatası: {e}")
        return []

def show_file_info(audio_files, image_files):
    """Dosya bilgilerini göster"""
    print(f"{Fore.CYAN}=== 📁 Oluşturulan Dosyalar ==={Style.RESET_ALL}")
    
    print("🎵 Ses Dosyaları:")
    for audio_file in audio_files:
        if os.path.exists(audio_file):
            size = os.path.getsize(audio_file) / 1024
            print(f"  ✓ {audio_file} ({size:.1f} KB)")
        else:
            print(f"  ❌ {audio_file} (bulunamadı)")
    
    print("\n🖼 Görsel Dosyaları:")
    for image_file in image_files:
        if os.path.exists(image_file):
            size = os.path.getsize(image_file) / 1024
            print(f"  ✓ {image_file} ({size:.1f} KB)")
        else:
            print(f"  ❌ {image_file} (bulunamadı)")

def main():
    """Ana demo fonksiyonu"""
    print(f"{Fore.GREEN}🎬 YouTube Story Automation - Demo{Style.RESET_ALL}")
    print("=" * 60)
    print("MoviePy kurulum sorunu nedeniyle video oluşturma atlandı.")
    print("Ses ve görsel üretimi test ediliyor...\n")
    
    # 1. Hikaye işleme
    scenes, story_title = demo_story_processing()
    
    if not scenes:
        print("❌ Hikaye işleme başarısız, demo sonlandırılıyor.")
        return
    
    # 2. Ses üretimi
    audio_files = demo_tts(scenes, story_title)
    
    # 3. Görsel üretimi
    image_files = demo_image_generation(scenes, story_title)
    
    # 4. Dosya bilgileri
    if audio_files or image_files:
        show_file_info(audio_files, image_files)
    
    # Sonuç
    print(f"\n{Fore.GREEN}✅ Demo tamamlandı!{Style.RESET_ALL}")
    print(f"🔧 MoviePy kurulumu tamamlandığında video oluşturma da çalışacak.")
    print(f"📁 Oluşturulan dosyalar audio/ ve images/ klasörlerinde")

if __name__ == "__main__":
    main()
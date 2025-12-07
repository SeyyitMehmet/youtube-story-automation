#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Basit Test - Core fonksiyonları test eder
"""

import os
import sys

def test_story_processor():
    """Hikaye işleme testi"""
    print("=== Hikaye İşleme Testi ===")
    
    try:
        # Direct import
        sys.path.append('.')
        from src.story_processor import StoryProcessor
        
        processor = StoryProcessor("stories")
        story_text = processor.load_story("kibritci_kiz.txt")
        story_title = processor.get_story_title(story_text)
        scenes = processor.split_into_scenes(story_text)
        
        print(f"✓ Hikaye başlığı: {story_title}")
        print(f"✓ Sahne sayısı: {len(scenes)}")
        
        for i, scene in enumerate(scenes[:2], 1):
            print(f"  Sahne {i}: {scene['text'][:60]}...")
            print(f"  Süre: {scene['duration']:.1f}s")
            print(f"  Görsel prompt: {scene['image_prompt'][:80]}...")
            print()
        
        return True
        
    except Exception as e:
        print(f"❌ Hata: {e}")
        return False

def test_tts():
    """TTS testi"""
    print("=== TTS Testi ===")
    
    try:
        # Test gTTS
        from gtts import gTTS
        print("✓ gTTS modülü yüklendi")
        
        # Test pyttsx3
        import pyttsx3
        print("✓ pyttsx3 modülü yüklendi")
        
        return True
        
    except Exception as e:
        print(f"❌ TTS Hatası: {e}")
        return False

def test_image_generation():
    """Görsel üretimi testi"""
    print("=== Görsel Üretimi Testi ===")
    
    try:
        from PIL import Image, ImageDraw, ImageFont
        print("✓ Pillow modülü yüklendi")
        
        # Basit test görseli oluştur
        image = Image.new('RGB', (100, 100), (255, 0, 0))
        draw = ImageDraw.Draw(image)
        draw.text((10, 10), "Test", fill=(255, 255, 255))
        
        test_path = "test_image.jpg"
        image.save(test_path)
        
        if os.path.exists(test_path):
            print("✓ Test görseli oluşturuldu")
            os.remove(test_path)
            return True
        
    except Exception as e:
        print(f"❌ Görsel Hatası: {e}")
        return False

def test_basic_apis():
    """Temel API'ları test et"""
    print("=== API Testleri ===")
    
    try:
        import requests
        print("✓ Requests modülü yüklendi")
        
        # Test internet bağlantısı
        response = requests.get("https://httpbin.org/ip", timeout=5)
        if response.status_code == 200:
            print("✓ İnternet bağlantısı çalışıyor")
        
        return True
        
    except Exception as e:
        print(f"❌ API Hatası: {e}")
        return False

def main():
    """Ana test fonksiyonu"""
    print("🧪 YouTube Story Automation - Basit Test")
    print("=" * 50)
    
    results = []
    
    # Testleri çalıştır
    results.append(("Hikaye İşleme", test_story_processor()))
    results.append(("TTS", test_tts()))
    results.append(("Görsel Üretimi", test_image_generation()))
    results.append(("API'lar", test_basic_apis()))
    
    # Sonuçları göster
    print("\n" + "=" * 50)
    print("📊 TEST SONUÇLARI")
    print("=" * 50)
    
    passed = 0
    for test_name, result in results:
        status = "✅ BAŞARILI" if result else "❌ BAŞARISIZ"
        print(f"{test_name:20}: {status}")
        if result:
            passed += 1
    
    print(f"\nToplam: {passed}/{len(results)} test başarılı")
    
    if passed == len(results):
        print("🎉 Tüm temel testler başarılı! Sistem hazır.")
    else:
        print("⚠ Bazı testler başarısız. Kurulum kontrol edilmeli.")

if __name__ == "__main__":
    main()
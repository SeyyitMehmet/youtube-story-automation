#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Yeni API Sistemi Demo - DeepSeek + Çoklu Resim API'leri Test
"""

import os
import sys
from colorama import init, Fore, Style

# Colorama'yı başlat
init(autoreset=True)

def test_deepseek_story_analysis():
    """DeepSeek ile hikaye analizi testi"""
    print(f"{Fore.CYAN}=== 🧠 DeepSeek Hikaye Analizi ==={Style.RESET_ALL}")
    
    try:
        sys.path.append('.')
        from config.config import Config
        from src.deepseek_processor import DeepSeekProcessor
        from src.story_processor import StoryProcessor
        
        if not Config.DEEPSEEK_API_KEY:
            print("⚠ DeepSeek API key tanımlanmamış (.env dosyasında)")
            return False
        
        # Hikaye yükle
        with open('stories/kibritci_kiz.txt', 'r', encoding='utf-8') as f:
            story_text = f.read()
        
        # DeepSeek ile analiz
        deepseek = DeepSeekProcessor(Config.DEEPSEEK_API_KEY)
        
        print("🔍 DeepSeek bağlantısı test ediliyor...")
        if deepseek.test_connection():
            print("✅ DeepSeek Chat API çalışıyor")
        else:
            print("❌ DeepSeek Chat API çalışmıyor")
            return False
        
        print("🤖 Hikaye AI ile analiz ediliyor...")
        ai_result = deepseek.analyze_story_with_ai(story_text)
        
        if ai_result:
            print(f"✅ AI Analizi Başarılı!")
            print(f"📖 Başlık: {ai_result['story_title']}")
            print(f"🎬 Sahne Sayısı: {ai_result['total_scenes']}")
            print(f"⏱ Toplam Süre: {ai_result['total_estimated_duration']} saniye")
            print(f"🎯 Hedef Kitle: {ai_result['target_audience']}")
            
            print(f"\n📋 Sahne Detayları:")
            for scene in ai_result['scenes'][:3]:  # İlk 3 sahne
                print(f"  Sahne {scene['scene_number']}: {scene['text'][:60]}...")
                print(f"    Süre: {scene['duration']}s | Ruh Hali: {scene.get('mood', 'N/A')}")
                print(f"    Görsel: {scene['image_prompt'][:80]}...")
                print()
            
            return True
        else:
            print("❌ AI analizi başarısız")
            return False
            
    except Exception as e:
        print(f"❌ Hata: {e}")
        return False

def test_multi_image_apis():
    """Çoklu resim API'lerini test et"""
    print(f"{Fore.CYAN}=== 🎨 Çoklu Resim API Testi ==={Style.RESET_ALL}")
    
    try:
        sys.path.append('.')
        from config.config import Config
        from src.multi_image_generator import MultiImageGenerator
        
        # Yeni çoklu API generator
        img_gen = MultiImageGenerator(
            hf_token=Config.HUGGINGFACE_API_KEY,
            use_free_alternative=Config.USE_FREE_IMAGES_ONLY
        )
        
        print("🔍 Tüm resim API'leri test ediliyor...")
        api_results = img_gen.test_all_apis()
        
        print("📊 API Durum Raporu:")
        for api_name, status in api_results.items():
            status_icon = "✅" if status else "❌"
            print(f"  {status_icon} {api_name.title()}: {'Çalışıyor' if status else 'Çalışmıyor'}")
        
        # Test görseli oluştur
        print("\n🎨 Test görseli oluşturuluyor...")
        test_scene = {
            'scene_number': 1,
            'image_prompt': 'A magical fairy tale scene with a little girl and glowing matches, cinematic lighting, detailed illustration'
        }
        
        image_path = img_gen.generate_scene_image(test_scene, 'new_api_test.jpg')
        
        if os.path.exists(image_path):
            size = os.path.getsize(image_path) / 1024
            print(f"✅ Test görseli oluşturuldu: {image_path} ({size:.1f} KB)")
            
            # API öncelik sırasını göster
            print(f"📋 API Öncelik Sırası: {' → '.join(img_gen.api_priority)}")
            return True
        else:
            print("❌ Test görseli oluşturulamadı")
            return False
            
    except Exception as e:
        print(f"❌ Hata: {e}")
        return False

def test_full_integration():
    """Tam entegrasyon testi - DeepSeek analizi + resim üretimi"""
    print(f"{Fore.CYAN}=== 🔗 Tam Entegrasyon Testi ==={Style.RESET_ALL}")
    
    try:
        sys.path.append('.')
        from config.config import Config
        from src.story_processor import StoryProcessor
        from src.multi_image_generator import MultiImageGenerator
        
        # 1. AI destekli hikaye işleme
        print("📚 Hikaye AI ile işleniyor...")
        story_processor = StoryProcessor(
            stories_dir="stories",
            deepseek_api_key=Config.DEEPSEEK_API_KEY
        )
        
        story_text = story_processor.load_story("kibritci_kiz.txt")
        story_title = story_processor.get_story_title(story_text)
        scenes = story_processor.split_into_scenes(story_text)
        
        print(f"✅ Hikaye: {story_title}")
        print(f"✅ {len(scenes)} sahne oluşturuldu")
        
        # AI tarafından geliştirilmiş mi kontrol et
        ai_enhanced = any(scene.get('enhanced_by_ai', False) for scene in scenes)
        if ai_enhanced:
            print("🤖 Sahneler AI ile geliştirildi")
        
        # 2. İlk sahne için görsel üret
        print("\n🎨 İlk sahne için AI görseli oluşturuluyor...")
        
        img_gen = MultiImageGenerator(
            hf_token=Config.HUGGINGFACE_API_KEY,
            use_free_alternative=Config.USE_FREE_IMAGES_ONLY
        )
        
        first_scene = scenes[0]
        image_path = img_gen.generate_scene_image(first_scene, 'integration_test_scene1.jpg')
        
        if os.path.exists(image_path):
            size = os.path.getsize(image_path) / 1024
            print(f"✅ Görsel oluşturuldu: {image_path} ({size:.1f} KB)")
            print(f"🎬 Sahne: {first_scene['text'][:80]}...")
            print(f"🎨 Prompt: {first_scene['image_prompt'][:80]}...")
            
            return True
        else:
            print("❌ Görsel oluşturulamadı")
            return False
            
    except Exception as e:
        print(f"❌ Entegrasyon hatası: {e}")
        return False

def show_api_setup_guide():
    """API kurulum rehberi"""
    print(f"{Fore.YELLOW}📋 API Kurulum Rehberi{Style.RESET_ALL}")
    print("=" * 50)
    
    print("🤖 DeepSeek API (Hikaye Analizi):")
    print("   1. https://platform.deepseek.com/ adresine gidin")
    print("   2. Ücretsiz hesap oluşturun")
    print("   3. API key alın")
    print("   4. .env dosyasına DEEPSEEK_API_KEY=your_key_here ekleyin")
    print()
    
    print("🎨 Resim Üretimi API'leri:")
    print()
    
    print("   🆓 Hugging Face (KULLANILIYOR - Günde 1000 ücretsiz):")
    print("      1. https://huggingface.co/settings/tokens")
    print("      2. Read token oluşturun")
    print("      3. .env: HUGGINGFACE_API_KEY=your_token")
    print()
    
    print("   🆓 Pollinations.ai (Backup - Tamamen ücretsiz):")
    print("      - API key gerekmez, otomatik kullanılır")
    print("      - Hugging Face başarısız olursa kullanılır")

def main():
    """Ana demo fonksiyonu"""
    print(f"{Fore.GREEN}🚀 YouTube Story Automation - Yeni API Sistemi Demo{Style.RESET_ALL}")
    print("=" * 60)
    
    results = []
    
    # 1. DeepSeek hikaye analizi
    results.append(("DeepSeek Hikaye Analizi", test_deepseek_story_analysis()))
    
    # 2. Çoklu resim API'leri
    results.append(("Çoklu Resim API'leri", test_multi_image_apis()))
    
    # 3. Tam entegrasyon
    results.append(("Tam Entegrasyon", test_full_integration()))
    
    # Sonuçları göster
    print(f"\n{Fore.CYAN}📊 Test Sonuçları{Style.RESET_ALL}")
    print("=" * 40)
    
    passed = 0
    for test_name, result in results:
        status = f"{Fore.GREEN}✅ BAŞARILI{Style.RESET_ALL}" if result else f"{Fore.RED}❌ BAŞARISIZ{Style.RESET_ALL}"
        print(f"{test_name:25}: {status}")
        if result:
            passed += 1
    
    print(f"\nToplam: {passed}/{len(results)} test başarılı")
    
    if passed == len(results):
        print(f"\n{Fore.GREEN}🎉 Tüm testler başarılı! Sistem hazır.{Style.RESET_ALL}")
    elif passed >= 1:
        print(f"\n{Fore.YELLOW}⚠ Bazı testler başarılı. API key'leri kontrol edin.{Style.RESET_ALL}")
        show_api_setup_guide()
    else:
        print(f"\n{Fore.RED}❌ Hiçbir test başarılı olmadı.{Style.RESET_ALL}")
        show_api_setup_guide()

if __name__ == "__main__":
    main()
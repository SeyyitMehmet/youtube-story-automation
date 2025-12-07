#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hızlı API Testi - DeepSeek + Hugging Face
"""

import os
import sys
from colorama import init, Fore, Style

init(autoreset=True)

def quick_api_test():
    """Hızlı API testleri"""
    print(f"{Fore.GREEN}🚀 Hızlı API Testi{Style.RESET_ALL}")
    print("=" * 40)
    
    try:
        sys.path.append('.')
        from config.config import Config
        
        # API key'leri kontrol et
        print("🔑 API Key Kontrolü:")
        
        if Config.DEEPSEEK_API_KEY and Config.DEEPSEEK_API_KEY != "your_api_key_here":
            print(f"✅ DeepSeek: {'*' * 20}...{Config.DEEPSEEK_API_KEY[-4:]}")
        else:
            print("❌ DeepSeek: Tanımlanmamış")
        
        if Config.HUGGINGFACE_API_KEY and Config.HUGGINGFACE_API_KEY != "your_huggingface_token_here":
            print(f"✅ Hugging Face: {'*' * 20}...{Config.HUGGINGFACE_API_KEY[-4:]}")
        else:
            print("❌ Hugging Face: Tanımlanmamış")
        
        print()
        
        # DeepSeek Chat API testi
        if Config.DEEPSEEK_API_KEY:
            print("🧠 DeepSeek Chat API Test...")
            try:
                from src.deepseek_processor import DeepSeekProcessor
                
                deepseek = DeepSeekProcessor(Config.DEEPSEEK_API_KEY)
                if deepseek.test_connection():
                    print("✅ DeepSeek Chat API çalışıyor")
                else:
                    print("❌ DeepSeek Chat API çalışmıyor")
            except Exception as e:
                print(f"❌ DeepSeek test hatası: {e}")
        
        # Hugging Face API testi
        if Config.HUGGINGFACE_API_KEY:
            print("\n🎨 Hugging Face API Test...")
            try:
                from src.multi_image_generator import MultiImageGenerator
                
                img_gen = MultiImageGenerator(hf_token=Config.HUGGINGFACE_API_KEY)
                
                # API prioritylerini göster
                print(f"📋 API Öncelik Sırası: {' → '.join(img_gen.api_priority)}")
                
                # API testleri
                api_results = img_gen.test_all_apis()
                
                for api_name, status in api_results.items():
                    status_text = "✅ Çalışıyor" if status else "❌ Çalışmıyor" 
                    print(f"  {api_name.title()}: {status_text}")
                
                # Test görseli oluştur
                print("\n🎨 Test görseli oluşturuluyor...")
                test_scene = {
                    'scene_number': 1,
                    'image_prompt': 'A beautiful winter scene with a little girl, snow falling, warm lighting, fairy tale style'
                }
                
                image_path = img_gen.generate_scene_image(test_scene, 'quick_test.jpg')
                
                if os.path.exists(image_path):
                    size = os.path.getsize(image_path) / 1024
                    print(f"✅ Test görseli oluşturuldu: {image_path} ({size:.1f} KB)")
                    return True
                else:
                    print("❌ Test görseli oluşturulamadı")
                    return False
                    
            except Exception as e:
                print(f"❌ Hugging Face test hatası: {e}")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Genel test hatası: {e}")
        return False

def main():
    result = quick_api_test()
    
    if result:
        print(f"\n{Fore.GREEN}🎉 API testleri başarılı!{Style.RESET_ALL}")
        print("📋 Sonraki adım: python main.py ile tam sistemi çalıştırın")
    else:
        print(f"\n{Fore.RED}❌ API testlerinde sorun var{Style.RESET_ALL}")
        print("🔧 .env dosyasındaki API key'leri kontrol edin")

if __name__ == "__main__":
    main()
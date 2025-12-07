#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setup Script - Sistem kurulumu ve kontrolleri
"""

import os
import sys
import subprocess
import platform
from colorama import init, Fore, Style

# Colorama'yı başlat
init(autoreset=True)

def print_header():
    """Başlık yazdır"""
    print(f"{Fore.CYAN}")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "    🎬 YouTube Story Automation - Setup    ".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "═" * 58 + "╝")
    print(f"{Style.RESET_ALL}")

def check_python():
    """Python sürümünü kontrol et"""
    print(f"{Fore.YELLOW}🐍 Python Kontrolü{Style.RESET_ALL}")
    print("─" * 30)
    
    version = sys.version_info
    print(f"Python Sürümü: {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python sürümü uygun (3.8+ gerekli)")
        return True
    else:
        print(f"❌ Python 3.8+ gerekli (mevcut: {version.major}.{version.minor})")
        return False

def check_venv():
    """Virtual environment kontrolü"""
    print(f"\n{Fore.YELLOW}📦 Virtual Environment{Style.RESET_ALL}")
    print("─" * 30)
    
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Virtual environment aktif")
        return True
    else:
        print("⚠ Virtual environment tespit edilemedi")
        return False

def check_packages():
    """Gerekli paketleri kontrol et"""
    print(f"\n{Fore.YELLOW}📚 Python Paketleri{Style.RESET_ALL}")
    print("─" * 30)
    
    required_packages = [
        'requests', 'python-dotenv', 'gTTS', 'Pillow', 
        'colorama', 'pyttsx3', 'pydub'
    ]
    
    optional_packages = [
        'moviepy', 'opencv-python', 'google-auth'
    ]
    
    missing_required = []
    missing_optional = []
    
    # Gerekli paketler
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            missing_required.append(package)
    
    # İsteğe bağlı paketler
    for package in optional_packages:
        try:
            if package == 'moviepy':
                import moviepy.editor
            elif package == 'opencv-python':
                import cv2
            elif package == 'google-auth':
                import google.auth
            print(f"✅ {package} (isteğe bağlı)")
        except ImportError:
            print(f"⚠ {package} (isteğe bağlı)")
            missing_optional.append(package)
    
    return missing_required, missing_optional

def check_ffmpeg():
    """FFmpeg kontrolü"""
    print(f"\n{Fore.YELLOW}🎬 FFmpeg Kontrolü{Style.RESET_ALL}")
    print("─" * 30)
    
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            print(f"✅ FFmpeg kurulu: {version_line}")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    print("❌ FFmpeg bulunamadı")
    print("\n📋 FFmpeg Kurulum Talimatları:")
    
    system = platform.system().lower()
    if 'windows' in system:
        print("  Windows için:")
        print("  1. https://ffmpeg.org/download.html adresinden indirin")
        print("  2. ZIP dosyasını çıkarın")
        print("  3. ffmpeg.exe'yi PATH'e ekleyin")
        print("  4. Alternatif: chocolatey ile 'choco install ffmpeg'")
    elif 'darwin' in system:
        print("  macOS için:")
        print("  brew install ffmpeg")
    else:
        print("  Linux için:")
        print("  sudo apt install ffmpeg  # Ubuntu/Debian")
        print("  sudo yum install ffmpeg  # RHEL/CentOS")
    
    return False

def check_directories():
    """Gerekli klasörleri kontrol et"""
    print(f"\n{Fore.YELLOW}📁 Klasör Yapısı{Style.RESET_ALL}")
    print("─" * 30)
    
    required_dirs = ['stories', 'audio', 'images', 'videos', 'config', 'src']
    
    for directory in required_dirs:
        if os.path.exists(directory):
            print(f"✅ {directory}/")
        else:
            os.makedirs(directory, exist_ok=True)
            print(f"✅ {directory}/ (oluşturuldu)")

def check_config():
    """Konfigürasyon dosyalarını kontrol et"""
    print(f"\n{Fore.YELLOW}⚙ Konfigürasyon{Style.RESET_ALL}")
    print("─" * 30)
    
    # .env dosyası
    if os.path.exists('.env'):
        print("✅ .env dosyası mevcut")
        
        # API anahtarları kontrolü
        try:
            from dotenv import load_dotenv
            load_dotenv()
            
            deepseek_key = os.getenv('DEEPSEEK_API_KEY', '')
            youtube_id = os.getenv('YOUTUBE_CLIENT_ID', '')
            
            if deepseek_key and deepseek_key != 'your_deepseek_api_key_here':
                print("✅ DeepSeek API key tanımlı")
            else:
                print("⚠ DeepSeek API key tanımlanmamış (isteğe bağlı)")
            
            if youtube_id and youtube_id != 'your_youtube_client_id_here':
                print("✅ YouTube API credentials tanımlı")
            else:
                print("⚠ YouTube API credentials tanımlanmamış (isteğe bağlı)")
                
        except ImportError:
            print("⚠ python-dotenv kurulu değil")
    else:
        print("⚠ .env dosyası bulunamadı")
    
    # Hikaye dosyası
    if os.path.exists('stories/kibritci_kiz.txt'):
        print("✅ Kibritçi Kız hikayesi mevcut")
    else:
        print("❌ Hikaye dosyası bulunamadı")

def run_test():
    """Basit sistem testi çalıştır"""
    print(f"\n{Fore.YELLOW}🧪 Sistem Testi{Style.RESET_ALL}")
    print("─" * 30)
    
    try:
        # Test minimal functionality
        sys.path.append('.')
        
        # Hikaye işleme
        from src.story_processor import StoryProcessor
        processor = StoryProcessor("stories")
        story_text = processor.load_story("kibritci_kiz.txt")
        scenes = processor.split_into_scenes(story_text)
        print(f"✅ Hikaye işleme: {len(scenes)} sahne")
        
        # Görsel üretimi
        from src.image_generator import ImageGenerator
        img_gen = ImageGenerator(use_free_alternative=True)
        print("✅ Görsel üretimi hazır")
        
        # TTS
        from gtts import gTTS
        print("✅ gTTS hazır")
        
        return True
        
    except Exception as e:
        print(f"❌ Test hatası: {e}")
        return False

def install_missing_packages(missing_packages):
    """Eksik paketleri kur"""
    if not missing_packages:
        return True
    
    print(f"\n{Fore.YELLOW}📦 Eksik Paketler Kuruluyor{Style.RESET_ALL}")
    print("─" * 30)
    
    for package in missing_packages:
        print(f"Kuruluyor: {package}")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
            print(f"✅ {package} kuruldu")
        except subprocess.CalledProcessError:
            print(f"❌ {package} kurulum hatası")
            return False
    
    return True

def main():
    """Ana setup fonksiyonu"""
    print_header()
    
    print("Bu script sisteminizi YouTube Story Automation için hazırlar.\n")
    
    # Kontroller
    checks = []
    checks.append(("Python", check_python()))
    checks.append(("Virtual Environment", check_venv()))
    
    # Paket kontrolü
    missing_required, missing_optional = check_packages()
    if missing_required:
        install_choice = input(f"\n{Fore.YELLOW}Eksik paketler kurulsun mu? (y/N): {Style.RESET_ALL}")
        if install_choice.lower() in ['y', 'yes', 'evet', 'e']:
            success = install_missing_packages(missing_required)
            checks.append(("Gerekli Paketler", success))
        else:
            checks.append(("Gerekli Paketler", False))
    else:
        checks.append(("Gerekli Paketler", True))
    
    checks.append(("FFmpeg", check_ffmpeg()))
    
    # Dosya/klasör kontrolleri
    check_directories()
    check_config()
    
    # Test
    test_result = run_test()
    checks.append(("Sistem Testi", test_result))
    
    # Sonuçlar
    print(f"\n{Fore.CYAN}📊 KURULUM RAPORU{Style.RESET_ALL}")
    print("═" * 40)
    
    passed = 0
    for check_name, result in checks:
        status = f"{Fore.GREEN}✅ BAŞARILI{Style.RESET_ALL}" if result else f"{Fore.RED}❌ BAŞARISIZ{Style.RESET_ALL}"
        print(f"{check_name:20}: {status}")
        if result:
            passed += 1
    
    print(f"\nToplam: {passed}/{len(checks)} kontrol başarılı")
    
    if passed == len(checks):
        print(f"\n{Fore.GREEN}🎉 Sistem hazır! python main.py ile başlayabilirsiniz.{Style.RESET_ALL}")
    elif passed >= len(checks) - 1:  # FFmpeg hariç hepsi tamam
        print(f"\n{Fore.YELLOW}⚠ Sistem neredeyse hazır. FFmpeg kurulduğunda video üretimi de çalışacak.{Style.RESET_ALL}")
        print("Şu an için ses ve görsel üretimi çalışıyor.")
    else:
        print(f"\n{Fore.RED}❌ Kurulum tamamlanamadı. Hataları giderin ve tekrar deneyin.{Style.RESET_ALL}")
    
    input(f"\n{Fore.CYAN}Enter'a basarak çıkın...{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
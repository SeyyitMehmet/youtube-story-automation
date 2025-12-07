#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TEST SCRIPT - Sadece ilk 2 sahneyi kullanarak hızlı test
Ana sistemi değiştirmeden test yapabilmek için
"""

import os
import sys
from colorama import init, Fore, Style
from config.config import Config
from src.story_processor import StoryProcessor
from src.openai_tts_generator import OpenAITTSGenerator
from src.video_creator import VideoCreator
from src.multi_image_generator import MultiImageGenerator
from src.character_manager import CharacterManager

init(autoreset=True)

def test_2_scenes():
    """Sadece ilk 2 sahneyi test et"""
    
    print(f"\n{Fore.CYAN}🧪 TEST MODU - Sadece 2 Sahne{Style.RESET_ALL}\n")
    
    try:
        # 1. Hikayeyi yükle ve sahnelere böl
        print(f"{Fore.YELLOW}[1/4] 📚 Hikaye yükleniyor...{Style.RESET_ALL}")
        story_processor = StoryProcessor(
            stories_dir=Config.STORIES_DIR,
            deepseek_api_key=Config.DEEPSEEK_API_KEY
        )
        story_text = story_processor.load_story("kibritci_kiz.txt")
        story_title = story_processor.get_story_title(story_text)
        all_scenes = story_processor.split_into_scenes(story_text)
        
        # SADECE İLK 2 SAHNEYİ AL
        scenes = all_scenes[:2]
        print(f"✓ Toplam {len(all_scenes)} sahne bulundu")
        print(f"✓ Test için ilk {len(scenes)} sahne kullanılıyor\n")
        
        # Sahneleri göster
        for scene in scenes:
            print(f"{Fore.CYAN}Sahne {scene['scene_number']}:{Style.RESET_ALL}")
            print(f"  Metin: {scene['text'][:100]}...")
            print(f"  Görsel Prompt: {scene['image_prompt'][:80]}...\n")
        
        # 2. Ses dosyaları oluştur
        print(f"{Fore.YELLOW}[2/4] 🎤 Ses dosyaları oluşturuluyor...{Style.RESET_ALL}")
        
        if Config.OPENAI_API_KEY:
            tts_generator = OpenAITTSGenerator(
                api_key=Config.OPENAI_API_KEY,
                voice=Config.OPENAI_TTS_VOICE,
                language=Config.TTS_LANGUAGE,
                speed=Config.OPENAI_TTS_SPEED
            )
        else:
            print(f"{Fore.RED}✗ OPENAI_API_KEY bulunamadı!{Style.RESET_ALL}")
            return
        
        audio_files = tts_generator.generate_story_audio(scenes, story_title)
        print(f"✓ {len(audio_files)} ses dosyası oluşturuldu\n")
        
        # 3. Görseller oluştur
        print(f"{Fore.YELLOW}[3/4] 🎨 Görseller oluşturuluyor...{Style.RESET_ALL}")
        
        char_manager = CharacterManager()
        
        # AI'dan karakterleri çıkar
        if hasattr(story_processor, 'ai_response') and story_processor.ai_response:
            characters = char_manager.extract_characters(story_processor.ai_response)
            if characters:
                print(f"{Fore.CYAN}👥 Karakter sistemi aktif{Style.RESET_ALL}")
                print(char_manager.get_all_character_info())
        
        image_generator = MultiImageGenerator(
            hf_token=Config.HUGGINGFACE_API_KEY,
            replicate_token=Config.REPLICATE_API_KEY,
            use_free_alternative=Config.USE_FREE_IMAGES_ONLY
        )
        image_generator.character_manager = char_manager
        
        image_files = image_generator.generate_story_images(scenes, story_title)
        print(f"✓ {len(image_files)} görsel oluşturuldu\n")
        
        # 4. Video oluştur
        print(f"{Fore.YELLOW}[4/4] 🎬 Video birleştiriliyor...{Style.RESET_ALL}")
        
        video_creator = VideoCreator(Config.VIDEOS_DIR)
        video_path = video_creator.create_story_video(
            scenes=scenes,
            image_files=image_files,
            audio_files=audio_files,
            story_title=f"{story_title}_TEST_2_SCENES"
        )
        
        video_info = video_creator.get_video_info(video_path)
        
        print(f"\n{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}✅ TEST BAŞARILI!{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
        print(f"\n📹 Video: {video_path}")
        print(f"⏱️  Süre: {video_info.get('duration', 0):.1f} saniye")
        print(f"💾 Boyut: {video_info.get('filesize', 0) / (1024*1024):.1f} MB\n")
        print(f"{Fore.CYAN}💡 Sistem çalışıyor! Ana kodu (main.py) kullanarak 15 sahne üretebilirsiniz.{Style.RESET_ALL}\n")
        
    except Exception as e:
        print(f"\n{Fore.RED}❌ Hata: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_2_scenes()

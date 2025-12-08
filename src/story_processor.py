"""
Hikaye işleme modülü
Hikayeleri parçalara ayırır ve sahne bazında düzenler
DeepSeek AI ile güçlendirilmiş analiz
"""
import re
import os
from typing import List, Dict, Optional
from .deepseek_processor import DeepSeekProcessor

class StoryProcessor:
    def __init__(self, stories_dir: str = "stories", deepseek_api_key: str = ""):
        self.stories_dir = stories_dir
        self.deepseek_processor = DeepSeekProcessor(deepseek_api_key)
        self.use_ai_analysis = bool(deepseek_api_key)
        self.ai_response = None  # AI yanıtını sakla (karakter bilgileri için)
    
    def load_story(self, filename: str) -> str:
        """Hikaye dosyasını yükler"""
        filepath = os.path.join(self.stories_dir, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                return file.read().strip()
        except FileNotFoundError:
            raise FileNotFoundError(f"Hikaye dosyası bulunamadı: {filepath}")
    
    def split_into_scenes(self, story_text: str) -> Optional[List[Dict[str, str]]]:
        """Hikayeyi sahnelere böler - AI destekli (AI zorunlu)"""
        
        # AI ile analiz et
        if self.use_ai_analysis:
            print("🤖 DeepSeek AI ile hikaye analizi yapılıyor...")
            ai_result = self.deepseek_processor.analyze_story_with_ai(story_text)
            
            if ai_result and 'scenes' in ai_result:
                print(f"✅ AI analizi başarılı: {len(ai_result['scenes'])} sahne")
                # AI yanıtını sakla (karakter bilgileri için)
                self.ai_response = ai_result
                return ai_result['scenes']
            else:
                print("⚠ AI analizi başarısız...")
        
        # AI çalışmazsa None döndür (detaylı hata mesajı ile)
        return self._manual_scene_splitting(story_text)
    
    def _manual_scene_splitting(self, story_text: str) -> Optional[List[Dict[str, str]]]:
        """AI çalışmazsa uyarı ver ve None döndür"""
        
        print("\n" + "="*70)
        print("❌ HATA: DeepSeek AI analizi çalışmadı!")
        print("="*70)
        print("\n📋 Olası Nedenler:")
        print("   1. DEEPSEEK_API_KEY eksik veya hatalı")
        print("   2. DeepSeek API sunucusu yanıt vermiyor")
        print("   3. API rate limit aşıldı")
        print("   4. Model parametreleri hatalı (max_tokens, vb.)")
        print("\n🔧 Çözümler:")
        print("   • Colab Secrets'da DEEPSEEK_API_KEY'i kontrol edin")
        print("   • DeepSeek API durumu: https://status.deepseek.com/")
        print("   • API anahtarınızı yenileyin: https://platform.deepseek.com/")
        print("\n⚠️  Manuel prompt sistemi devre dışı - AI zorunludur!")
        print("="*70 + "\n")
        
        return None
    
    def _estimate_duration(self, text: str) -> float:
        """Metne göre tahmini ses süresi (saniye)"""
        word_count = len(text.split())
        # Ortalama 150 kelime/dakika
        duration = (word_count / 150) * 60
        return max(3.0, min(duration, 10.0))  # 3-10 saniye arası
    
    def _generate_image_prompt(self, text: str, scene_number: int) -> str:
        """Metin için görsel üretim prompt'u oluşturur"""
        # Temel görsel stilleri
        base_style = "fairy tale illustration, cinematic lighting, detailed, beautiful"
        
        # Scene-specific prompts (Kibritçi Kız için)
        scene_prompts = {
            1: "A little girl selling matches on a cold winter street, snow falling, warm street lamp light",
            2: "A little girl lighting a match, seeing a warm stove in the match light, magical glow",
            3: "A magical dining table with delicious food appearing in match light, fantasy scene",
            4: "A beautiful Christmas tree with lights and decorations, magical holiday scene",
            5: "A grandmother's spirit reaching out to a little girl, heavenly light, peaceful scene",
            6: "A peaceful morning scene, people finding the little girl, soft winter light"
        }
        
        # Varsayılan prompt
        if scene_number in scene_prompts:
            prompt = scene_prompts[scene_number]
        else:
            # Metinden anahtar kelimeler çıkar
            keywords = self._extract_keywords(text)
            prompt = f"A scene showing {', '.join(keywords)}"
        
        return f"{prompt}, {base_style}"
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Metinden anahtar kelimeler çıkarır"""
        # Türkçe için temel anahtar kelimeler
        keywords = []
        
        keyword_mapping = {
            'soğuk': 'cold winter',
            'kış': 'winter',
            'kibrit': 'match',
            'kız': 'little girl',
            'soba': 'warm stove',
            'yemek': 'food',
            'masa': 'table',
            'ağaç': 'tree',
            'büyükanne': 'grandmother',
            'gülümseme': 'smile'
        }
        
        text_lower = text.lower()
        for turkish, english in keyword_mapping.items():
            if turkish in text_lower:
                keywords.append(english)
        
        return keywords[:3]  # En fazla 3 anahtar kelime
    
    def get_story_title(self, story_text: str) -> str:
        """Hikaye başlığını döndürür"""
        lines = story_text.strip().split('\n')
        return lines[0].strip() if lines else "Bilinmeyen Hikaye"
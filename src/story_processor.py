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
    
    def split_into_scenes(self, story_text: str) -> List[Dict[str, str]]:
        """Hikayeyi sahnelere böler - AI destekli veya manuel"""
        
        # Önce AI ile analiz etmeyi dene
        if self.use_ai_analysis:
            print("🤖 DeepSeek AI ile hikaye analizi yapılıyor...")
            ai_result = self.deepseek_processor.analyze_story_with_ai(story_text)
            
            if ai_result and 'scenes' in ai_result:
                print(f"✅ AI analizi başarılı: {len(ai_result['scenes'])} sahne")
                # AI yanıtını sakla (karakter bilgileri için)
                self.ai_response = ai_result
                return ai_result['scenes']
            else:
                print("⚠ AI analizi başarısız, manuel işleme geçiliyor...")
        
        # Manuel işleme (fallback)
        return self._manual_scene_splitting(story_text)
    
    def _manual_scene_splitting(self, story_text: str) -> List[Dict[str, str]]:
        """Manuel sahne bölme - 20 sahneye böl, orijinal metni kullan"""
        
        # Hikayeyi 20 eşit parçaya böl
        total_chars = len(story_text)
        chars_per_scene = total_chars // 20
        
        scenes = []
        for i in range(20):
            start_char = i * chars_per_scene
            
            # Son sahne için tüm kalan metni al
            if i == 19:
                end_char = total_chars
            else:
                # Cümle sonunda bitir (nokta, soru işareti, ünlem)
                end_char = start_char + chars_per_scene
                
                # Önce cümle sonunu bul
                sentence_end = end_char
                for j in range(end_char, min(end_char + 200, total_chars)):
                    if story_text[j] in '.!?':
                        sentence_end = j + 1
                        break
                
                # Eğer çok uzaksa, en azından kelime sınırında kes
                if sentence_end - end_char > 100:
                    # Kelime sınırı bul (boşluk, virgül, noktalama)
                    for j in range(end_char, min(end_char + 50, total_chars)):
                        if story_text[j] in ' \n\t,;:':
                            end_char = j + 1
                            break
                else:
                    end_char = sentence_end
            
            scene_text = story_text[start_char:end_char].strip()
            
            scene = {
                'scene_number': i + 1,
                'text': scene_text,
                'start_char': start_char,
                'end_char': end_char,
                'image_prompt': self._generate_image_prompt(scene_text, i + 1),
                'characters': []
            }
            scenes.append(scene)
        
        print(f"📊 Manuel bölme: 20 sahne oluşturuldu (kelime sınırlarında kesildi)")
        return scenes
    
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
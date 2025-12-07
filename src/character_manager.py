"""
Karakter Tutarlılığı Yönetimi
Her hikaye için tutarlı karakter tanımları oluşturur ve yönetir
"""
import hashlib
from typing import List, Dict, Optional

class CharacterManager:
    def __init__(self):
        self.characters = {}
        self.character_templates = {}
        
    def extract_characters(self, ai_response: Dict) -> Dict[str, str]:
        """
        AI yanıtından ana karakterleri çıkarır
        
        Args:
            ai_response: DeepSeek'ten gelen JSON yanıt
            
        Returns:
            {character_name: visual_description} dictionary
        """
        characters = {}
        
        # AI'dan gelen karakter listesi
        if 'main_characters' in ai_response:
            for char in ai_response['main_characters']:
                name = char.get('name', '')
                description = char.get('description', '')
                if name and description:
                    characters[name] = description
                    print(f"✓ Karakter: {name} - {description[:50]}...")
        
        self.characters = characters
        return characters
    
    def create_character_seed(self, character_name: str) -> str:
        """
        Her karakter için benzersiz ama tutarlı bir seed oluşturur
        
        Args:
            character_name: Karakter adı
            
        Returns:
            Karakter için tutarlı seed string
        """
        # Karakter adından deterministic seed oluştur
        hash_obj = hashlib.md5(character_name.encode())
        seed = int(hash_obj.hexdigest()[:8], 16) % 1000000
        return str(seed)
    
    def enhance_prompt_with_character_consistency(self, 
                                                   scene_prompt: str, 
                                                   scene_characters: List[str]) -> str:
        """
        Sahne prompt'una karakter tutarlılığı için ek bilgiler ekler
        
        Args:
            scene_prompt: Orijinal sahne prompt'u
            scene_characters: Sahnedeki karakterler listesi
            
        Returns:
            Geliştirilmiş prompt (karakter tutarlılığı ile)
        """
        if not scene_characters or not self.characters:
            return scene_prompt
        
        # Karakterlerin detaylı tanımlarını ekle
        character_descriptions = []
        for char_name in scene_characters:
            if char_name in self.characters:
                desc = self.characters[char_name]
                character_descriptions.append(f"{char_name}: {desc}")
        
        if character_descriptions:
            # Prompt'a karakter tanımlarını ekle
            character_section = " | ".join(character_descriptions)
            enhanced_prompt = f"{scene_prompt}. Characters: {character_section}"
            
            # Tutarlılık için ek anahtar kelimeler
            enhanced_prompt += ", consistent character design, same appearance, character continuity"
            
            return enhanced_prompt
        
        return scene_prompt
    
    def create_character_reference_string(self, character_name: str) -> str:
        """
        Karakter için referans string oluşturur (FLUX için)
        
        Args:
            character_name: Karakter adı
            
        Returns:
            Karakter referans string'i
        """
        if character_name not in self.characters:
            return ""
        
        description = self.characters[character_name]
        seed = self.create_character_seed(character_name)
        
        # FLUX için optimize edilmiş format
        return f"[CHAR:{character_name}:{seed}] {description}"
    
    def get_all_character_info(self) -> str:
        """Tüm karakterlerin bilgisini döndürür"""
        if not self.characters:
            return "Henüz karakter tanımlanmadı"
        
        info = "📋 Tanımlı Karakterler:\n"
        info += "─" * 50 + "\n"
        
        for name, description in self.characters.items():
            seed = self.create_character_seed(name)
            info += f"• {name}\n"
            info += f"  Tanım: {description}\n"
            info += f"  Seed: {seed}\n\n"
        
        return info
    
    def save_character_templates(self, story_title: str):
        """Karakter şablonlarını saklar (gelecekte kullanım için)"""
        self.character_templates[story_title] = self.characters.copy()
        print(f"✓ {len(self.characters)} karakter şablonu kaydedildi")
    
    def load_character_templates(self, story_title: str) -> bool:
        """Önceden kaydedilmiş karakter şablonlarını yükler"""
        if story_title in self.character_templates:
            self.characters = self.character_templates[story_title].copy()
            print(f"✓ {len(self.characters)} karakter şablonu yüklendi")
            return True
        return False


class FluxConsistentCharacterHelper:
    """
    FLUX Schnell için karakter tutarlılığı yardımcı sınıfı
    """
    
    @staticmethod
    def create_consistent_prompt(base_prompt: str, 
                                 character_name: str,
                                 character_description: str,
                                 seed: str) -> str:
        """
        FLUX için tutarlı karakter prompt'u oluşturur
        
        Teknik: 
        - Aynı seed kullanımı
        - Detaylı karakter tanımı
        - Tutarlılık anahtar kelimeleri
        """
        consistent_prompt = (
            f"{base_prompt}. "
            f"Main character: {character_description}. "
            f"Character consistency is critical, same person, identical features, "
            f"recognizable appearance, character reference: {character_name}_{seed}"
        )
        
        return consistent_prompt
    
    @staticmethod
    def get_consistency_tips() -> str:
        """Karakter tutarlılığı için ipuçları döndürür"""
        return """
🎨 Karakter Tutarlılığı İpuçları:

1. **Detaylı Tanım**: Saç rengi, göz rengi, kıyafet, yaş vb.
   Örnek: "young girl, blonde hair in braids, blue eyes, red hood and cape"

2. **Anahtar Kelimeler**: 
   - "same character"
   - "consistent appearance" 
   - "character continuity"
   - "identical features"

3. **Seed Kullanımı**: Her karakter için aynı seed

4. **Referans Sistemi**: "character reference: [name]_[seed]"

5. **Stil Tutarlılığı**: Aynı art style kullanın
   Örnek: "digital art, consistent style, same artist"
"""

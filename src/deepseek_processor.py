"""
DeepSeek Chat API entegrasyonu
Hikaye analizi ve sahne bölme için AI kullanır
"""
import requests
import json
from typing import List, Dict, Optional

class DeepSeekProcessor:
    def __init__(self, api_key: str = ""):
        self.api_key = api_key
        self.chat_api_url = "https://api.deepseek.com/v1/chat/completions"
        
    def analyze_story_with_ai(self, story_text: str) -> Dict[str, any]:
        """DeepSeek ile hikayeyi analiz eder ve sahne önerileri alır"""
        
        if not self.api_key:
            print("⚠ DeepSeek API key yok, manuel işleme kullanılıyor")
            return None
        
        prompt = f"""
Aşağıdaki Türkçe hikayeyi analiz et ve 15 sahneye böl. Her sahne için:
- Orijinal hikayeden başlangıç ve bitiş karakteri (character index)
- Görsel prompt (İngilizce, AI image generation için)
- Karakter tanımı (tutarlılık için)

ÖNEMLİ: 
1. Ses seslendirmesi için ORİJİNAL HİKAYE METNİ kullanılacak!
2. "start_char" ve "end_char" ile orijinal metinden hangi bölümün okunacağını belirt
3. Tam olarak 20 sahne oluştur
4. Her sahne yaklaşık eşit uzunlukta olsun
5. ÖNEMLI: Sahneleri MUTLAKA kelime sınırında kes! Kelimeler yarım kalmasın.
   Örnek YANLIŞ: "aca" | "ba" ✗
   Örnek DOĞRU: "acaba" | "sonraki kelime" ✓
6. Tercihen cümle sonlarında (.!?) bitir, yoksa en azından boşluk/virgülde kes

KARAKTER TUTARLILIĞI: Ana karakterler için tutarlı fiziksel tanım kullan.
Örnek: "young girl with red hood, blonde hair, blue eyes, innocent face"
Her sahnede AYNI karakter tanımını kullan!

Hikaye (Toplam {len(story_text)} karakter):
{story_text}

JSON formatında yanıt ver:
{{
    "story_title": "Kısa hikaye başlığı",
    "main_characters": [
        {{"name": "Karakter Adı", "description": "Consistent visual description"}}
    ],
    "scenes": [
        {{
            "scene_number": 1,
            "start_char": 0,
            "end_char": 250,
            "image_prompt": "English visual prompt with consistent character description",
            "characters": ["Ana karakterler listesi"]
        }}
    ]
}}

Sadece JSON yanıt ver!
"""
        
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                "model": "deepseek-chat",
                "messages": [
                    {
                        "role": "system", 
                        "content": "Sen bir hikaye analiz uzmanısın. Hikayeleri kısa sahnelere böler ve sadece JSON yanıt verirsin."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.5,  # Daha tutarlı yanıt için düşürüldü
                "max_tokens": 4000,  # Uzun hikayeler için artırıldı
                "stream": False
            }
            
            # Timeout'u artır: bağlantı 30s, okuma 180s (3 dakika)
            print("⏳ DeepSeek AI'dan yanıt bekleniyor (bu biraz zaman alabilir)...")
            response = requests.post(
                self.chat_api_url, 
                headers=headers, 
                json=payload, 
                timeout=(30, 180)  # (connect timeout, read timeout)
            )
            response.raise_for_status()
            
            result = response.json()
            ai_response = result['choices'][0]['message']['content']
            
            # JSON extract et
            try:
                # JSON kısmını bul ve parse et
                json_start = ai_response.find('{')
                json_end = ai_response.rfind('}') + 1
                
                if json_start == -1 or json_end == 0:
                    print(f"⚠ JSON bulunamadı. Response: {ai_response[:300]}...")
                    return None
                
                json_str = ai_response[json_start:json_end]
                parsed_data = json.loads(json_str)
                
                # Sahne sayısını hesapla ve orijinal metni ekle
                scene_count = len(parsed_data.get('scenes', []))
                
                # Her sahneye orijinal metin bölümünü ekle
                for scene in parsed_data.get('scenes', []):
                    start_char = scene.get('start_char', 0)
                    end_char = scene.get('end_char', len(story_text))
                    scene['text'] = story_text[start_char:end_char].strip()
                
                print(f"✅ DeepSeek ile hikaye analizi tamamlandı")
                print(f"📊 {scene_count} sahne oluşturuldu (orijinal metin bölümleri eklendi)")
                
                return parsed_data
                
            except json.JSONDecodeError as e:
                print(f"⚠ DeepSeek JSON parse hatası: {e}")
                print(f"Raw response ilk 300 karakter: {ai_response[:300]}...")
                return None
                
        except requests.exceptions.Timeout:
            print(f"❌ DeepSeek API timeout (180 saniye aşıldı)")
            print(f"💡 Hikaye çok uzun olabilir, manuel işleme kullanılacak")
            return None
            
        except requests.exceptions.RequestException as e:
            print(f"❌ DeepSeek API bağlantı hatası: {e}")
            return None
            
        except Exception as e:
            print(f"❌ DeepSeek API hatası: {e}")
            return None
    
    def enhance_scene_descriptions(self, scenes: List[Dict]) -> List[Dict]:
        """Mevcut sahnelerin açıklamalarını DeepSeek ile geliştirir"""
        
        if not self.api_key:
            return scenes
        
        enhanced_scenes = []
        
        for scene in scenes:
            try:
                prompt = f"""
Bu sahne için daha iyi bir görsel açıklama yaz:

Sahne metni: {scene['text']}
Mevcut açıklama: {scene.get('image_prompt', '')}

Lütfen sinematik, detaylı ve AI görsel üretimi için optimize edilmiş İngilizce bir prompt yaz.
Stil: cinematic, storytelling, fairy tale illustration, detailed, beautiful lighting

Sadece görsel açıklamayı ver, başka açıklama ekleme.
"""
                
                headers = {
                    'Authorization': f'Bearer {self.api_key}',
                    'Content-Type': 'application/json'
                }
                
                payload = {
                    "model": "deepseek-chat",
                    "messages": [
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.8,
                    "max_tokens": 200
                }
                
                response = requests.post(self.chat_api_url, headers=headers, json=payload, timeout=15)
                
                if response.status_code == 200:
                    result = response.json()
                    enhanced_prompt = result['choices'][0]['message']['content'].strip()
                    
                    # Enhanced scene'i oluştur
                    enhanced_scene = scene.copy()
                    enhanced_scene['image_prompt'] = enhanced_prompt
                    enhanced_scene['enhanced_by_ai'] = True
                    enhanced_scenes.append(enhanced_scene)
                    
                    print(f"✅ Sahne {scene.get('scene_number', '?')} görsel açıklaması geliştirildi")
                else:
                    enhanced_scenes.append(scene)
                    
            except Exception as e:
                print(f"⚠ Sahne {scene.get('scene_number', '?')} geliştirme hatası: {e}")
                enhanced_scenes.append(scene)
        
        return enhanced_scenes
    
    def test_connection(self) -> bool:
        """DeepSeek Chat API bağlantısını test eder"""
        if not self.api_key:
            return False
        
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                "model": "deepseek-chat",
                "messages": [
                    {"role": "user", "content": "Merhaba, bu bir test mesajıdır."}
                ],
                "max_tokens": 50
            }
            
            response = requests.post(self.chat_api_url, headers=headers, json=payload, timeout=10)
            
            if response.status_code == 200:
                print("✅ DeepSeek Chat API çalışıyor")
                return True
            else:
                print(f"❌ DeepSeek Chat API hatası: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ DeepSeek Chat API test hatası: {e}")
            return False
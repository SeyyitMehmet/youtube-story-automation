"""
Replicate API ile görsel üretimi
FLUX ve SDXL modelleri desteklenir
"""
import os
import time
import requests
import replicate
from typing import Optional
from PIL import Image
from io import BytesIO

class ReplicateImageGenerator:
    def __init__(self, api_key: str):
        """
        Replicate görsel üretici
        
        Args:
            api_key: Replicate API anahtarı
        """
        self.api_key = api_key
        os.environ["REPLICATE_API_TOKEN"] = api_key
        
        # En iyi modeller (kalite/hız/fiyat dengesi)
        self.models = {
            "flux-schnell": "black-forest-labs/flux-schnell",  # Hızlı, ucuz, kaliteli
            "flux-dev": "black-forest-labs/flux-dev",  # Daha yüksek kalite
            "flux-2-dev": "black-forest-labs/flux-2-dev",  # FLUX 2.0 - multi-reference support
            "flux-2-pro": "black-forest-labs/flux-2-pro",  # FLUX 2.0 Pro - en kaliteli
            "flux-dev-lora": "black-forest-labs/flux-dev-lora",  # LoRA desteği
            "sdxl": "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
        }
        
        # Varsayılan model (flux-schnell en iyi seçim)
        self.default_model = "flux-schnell"
        
        # Karakter referans görselleri (FLUX-2 multi-reference için)
        self.character_references = {}  # {character_name: image_path}
        
    def generate_image(self, prompt: str, output_path: str, 
                      model: str = None, width: int = 1024, height: int = 1024,
                      max_retries: int = 3) -> str:
        """
        Prompt'tan görsel üretir (rate limit retry ile)
        
        Args:
            prompt: İngilizce görsel açıklaması
            output_path: Kaydedilecek dosya yolu
            model: Kullanılacak model (flux-schnell, flux-dev, sdxl)
            width: Görsel genişliği
            height: Görsel yüksekliği
            max_retries: Maksimum deneme sayısı (rate limit için)
            
        Returns:
            str: Oluşturulan görsel dosya yolu
        """
        model_name = model or self.default_model
        model_id = self.models.get(model_name, self.models["flux-schnell"])
        
        for attempt in range(max_retries):
            try:
                if attempt > 0:
                    print(f"🔄 Deneme {attempt + 1}/{max_retries}...")
                
                print(f"🎨 Replicate {model_name} ile görsel üretiliyor...")
                
                # Flux modelleri için input
                if "flux" in model_name:
                    input_params = {
                        "prompt": prompt,
                        "aspect_ratio": "16:9",  # YouTube için ideal
                        "output_format": "jpg",
                        "output_quality": 90
                    }
                # SDXL için input
                else:
                    input_params = {
                        "prompt": prompt,
                        "width": width,
                        "height": height,
                        "num_outputs": 1,
                        "quality": 90
                    }
                
                # API çağrısı
                output = replicate.run(model_id, input=input_params)
                
                # Output URL'den görseli indir
                if isinstance(output, list):
                    image_url = output[0]
                else:
                    image_url = output
                
                # Görseli indir
                response = requests.get(image_url, timeout=30)
                response.raise_for_status()
                
                # PIL ile aç ve kaydet
                image = Image.open(BytesIO(response.content))
                
                # 1920x1080'e resize et
                image = image.resize((1920, 1080), Image.Resampling.LANCZOS)
                image.save(output_path, 'JPEG', quality=95)
                
                print(f"✓ Replicate ile görsel oluşturuldu: {output_path}")
                return output_path
                
            except Exception as e:
                error_str = str(e)
                
                # Rate limit hatası kontrolü
                if "429" in error_str or "throttled" in error_str.lower():
                    # Rate limit süresini bul (örn: "resets in ~8s")
                    import re
                    match = re.search(r'resets in ~?(\d+)s', error_str)
                    wait_time = int(match.group(1)) if match else 10
                    
                    if attempt < max_retries - 1:
                        print(f"⏳ Rate limit! {wait_time} saniye bekleniyor...")
                        time.sleep(wait_time + 2)  # +2 saniye güvenlik payı
                        continue
                    else:
                        print(f"✗ Rate limit - maksimum deneme sayısına ulaşıldı")
                        raise
                else:
                    # Diğer hatalar için direkt raise
                    print(f"✗ Replicate hatası: {e}")
                    raise
        
        raise Exception("Replicate görsel üretimi başarısız")
    
    def generate_image_with_character_reference(self, prompt: str, output_path: str,
                                                 reference_image_path: str,
                                                 character_strength: float = 0.8,
                                                 max_retries: int = 3) -> str:
        """
        FLUX-2 Dev ile karakter referanslı görsel üretir (YÜKSEK TUTARLILIK)
        
        Args:
            prompt: Sahne açıklaması
            output_path: Çıktı dosya yolu
            reference_image_path: Referans karakter görseli yolu
            character_strength: Karakter benzerlik gücü (0.0-1.0)
            max_retries: Maksimum deneme sayısı
            
        Returns:
            str: Oluşturulan görsel dosya yolu
        """
        model_id = self.models["flux-2-dev"]  # FLUX 2.0 multi-reference destekli
        
        for attempt in range(max_retries):
            try:
                if attempt > 0:
                    print(f"🔄 Deneme {attempt + 1}/{max_retries}...")
                
                print(f"🎭 FLUX-2 Dev ile karakter referanslı görsel üretiliyor...")
                
                # Referans görseli base64'e çevir (FLUX-2 formatı)
                import base64
                with open(reference_image_path, 'rb') as f:
                    reference_base64 = base64.b64encode(f.read()).decode()
                
                input_params = {
                    "prompt": f"{prompt}, consistent character, same appearance, character reference",
                    "reference_images": [reference_base64],  # Multi-reference support
                    "reference_strength": character_strength,  # Karakter tutarlılığı
                    "aspect_ratio": "16:9",
                    "output_format": "jpg",
                    "output_quality": 90,
                    "num_outputs": 1
                }
                
                # API çağrısı
                output = replicate.run(model_id, input=input_params)
                
                # Output URL'den görseli indir
                if isinstance(output, list):
                    image_url = output[0]
                else:
                    image_url = output
                
                # Görseli indir
                response = requests.get(image_url, timeout=30)
                response.raise_for_status()
                
                # PIL ile aç ve kaydet
                image = Image.open(BytesIO(response.content))
                image = image.resize((1920, 1080), Image.Resampling.LANCZOS)
                image.save(output_path, 'JPEG', quality=95)
                
                print(f"✓ FLUX-2 ile tutarlı görsel oluşturuldu: {output_path}")
                return output_path
                
            except Exception as e:
                error_str = str(e)
                
                # Rate limit hatası kontrolü
                if "429" in error_str or "throttled" in error_str.lower():
                    import re
                    match = re.search(r'resets in ~?(\d+)s', error_str)
                    wait_time = int(match.group(1)) if match else 10
                    
                    if attempt < max_retries - 1:
                        print(f"⏳ Rate limit! {wait_time} saniye bekleniyor...")
                        time.sleep(wait_time + 2)
                        continue
                    else:
                        print(f"✗ Rate limit - maksimum deneme sayısına ulaşıldı")
                        raise
                else:
                    print(f"✗ FLUX-2 hatası: {e}")
                    raise
        
        raise Exception("FLUX-2 görsel üretimi başarısız")
    
    def set_character_reference(self, character_name: str, image_path: str):
        """Karakter için referans görseli saklar"""
        self.character_references[character_name] = image_path
        print(f"✓ Karakter referansı kaydedildi: {character_name} -> {image_path}")
    
    def get_character_reference(self, character_name: str) -> Optional[str]:
        """Karakter referans görselini döndürür"""
        return self.character_references.get(character_name)
    
    def test_api(self) -> bool:
        """API'nin çalışıp çalışmadığını test eder"""
        try:
            # Basit bir test prompt
            output = replicate.run(
                self.models["flux-schnell"],
                input={
                    "prompt": "a beautiful sunset over mountains",
                    "aspect_ratio": "16:9",
                    "output_format": "jpg"
                }
            )
            return True if output else False
        except Exception as e:
            print(f"Replicate test hatası: {e}")
            return False
    
    def get_model_info(self, model_name: str = None) -> dict:
        """Model bilgilerini döndürür"""
        model_name = model_name or self.default_model
        
        info = {
            "flux-schnell": {
                "name": "FLUX Schnell",
                "speed": "Çok Hızlı (1-4 saniye)",
                "quality": "Yüksek",
                "cost": "~$0.003/image",
                "recommended": True
            },
            "flux-dev": {
                "name": "FLUX Dev",
                "speed": "Orta (5-10 saniye)",
                "quality": "Çok Yüksek",
                "cost": "~$0.025/image",
                "recommended": False
            },
            "sdxl": {
                "name": "Stable Diffusion XL",
                "speed": "Orta (5-8 saniye)",
                "quality": "Yüksek",
                "cost": "~$0.008/image",
                "recommended": False
            }
        }
        
        return info.get(model_name, info["flux-schnell"])

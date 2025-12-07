"""
Çoklu AI Görsel Üretimi Modülü
Replicate, Hugging Face ve Pollinations.ai desteği
"""
import os
import requests
import json
import time
import base64
from PIL import Image, ImageDraw, ImageFont
from typing import List, Dict, Optional
import tempfile
import io

class MultiImageGenerator:
    def __init__(self, hf_token: str = "", replicate_token: str = "", use_free_alternative: bool = True):
        self.hf_token = hf_token
        self.replicate_token = replicate_token
        self.use_free_alternative = use_free_alternative
        self.images_dir = "images"
        
        # API URLs
        self.hf_api_url = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
        self.pollinations_api_url = "https://image.pollinations.ai/prompt"
        
        # Replicate generator
        self.replicate_generator = None
        if replicate_token:
            try:
                from src.replicate_image_generator import ReplicateImageGenerator
                self.replicate_generator = ReplicateImageGenerator(replicate_token)
            except Exception as e:
                print(f"⚠ Replicate yüklenemedi: {e}")
        
        # Klasör oluştur
        os.makedirs(self.images_dir, exist_ok=True)
        
        # API öncelik sırası
        self.api_priority = self._determine_api_priority()
        
        # Rate limit kontrolü için son istek zamanı
        self.last_replicate_request_time = 0
        
        # Karakter yöneticisi (dışarıdan atanacak)
        self.character_manager = None
        
        # Hibrit IP-Adapter sistemi
        self.use_ip_adapter = True  # IP-Adapter kullan
        self.first_scene_images = {}  # {character_name: first_scene_image_path}
        
        # Config'den rate limit ayarlarını al
        try:
            from config.config import Config
            self.replicate_delay = Config.REPLICATE_RATE_LIMIT_DELAY
        except:
            self.replicate_delay = 12  # Varsayılan: 12 saniye (6 istek/dakika için güvenli)
    
    def _determine_api_priority(self) -> List[str]:
        """Kullanılabilir API'leri öncelik sırasına göre listeler"""
        available_apis = []
        
        # Replicate en öncelikli (en kaliteli)
        if self.replicate_generator:
            available_apis.append("replicate")
        
        if self.hf_token and not self.use_free_alternative:
            available_apis.append("huggingface")
        
        # Ücretsiz seçenekler
        available_apis.append("pollinations")
        available_apis.append("placeholder")  # Son çare
        
        return available_apis
    
    def generate_scene_image(self, scene: Dict[str, str], output_filename: str) -> str:
        """Bir sahne için görsel oluşturur - çoklu API desteği + HIBRIT IP-Adapter"""
        prompt = scene['image_prompt']
        output_path = os.path.join(self.images_dir, output_filename)
        scene_number = scene.get('scene_number', 1)
        
        # Karakter tutarlılığı ekle (Seviye 1: Prompt-based)
        if self.character_manager and 'characters' in scene:
            scene_characters = scene.get('characters', [])
            prompt = self.character_manager.enhance_prompt_with_character_consistency(
                prompt, 
                scene_characters
            )
            print(f"🎭 Karakter tutarlılığı eklendi: {', '.join(scene_characters)}")
        
        # API'leri sırayla dene
        for api_name in self.api_priority:
            try:
                print(f"🎨 {api_name.title()} ile deneniyor...")
                
                if api_name == "replicate":
                    # HIBRIT SISTEM: Sadece USE_IP_ADAPTER=True ise IP-Adapter kullan
                    try:
                        from config.config import Config
                        use_ip_adapter = Config.USE_IP_ADAPTER
                    except:
                        use_ip_adapter = False
                    
                    if use_ip_adapter and scene_number > 1 and self.first_scene_images:
                        # Seviye 2: IP-Adapter/FLUX-2 (referans görselli)
                        return self._generate_with_replicate_ip_adapter(
                            prompt, output_path, scene
                        )
                    else:
                        # Normal FLUX Schnell
                        result = self._generate_with_replicate(prompt, output_path)
                        
                        # İlk sahne görselini kaydet (gelecekte IP-Adapter için)
                        if scene_number == 1 and 'characters' in scene:
                            for char in scene['characters']:
                                self.first_scene_images[char] = result
                                print(f"📸 İlk sahne görseli kaydedildi: {char}")
                        
                        return result
                        
                elif api_name == "huggingface":
                    return self._generate_with_huggingface(prompt, output_path)
                elif api_name == "pollinations":
                    return self._generate_with_pollinations(prompt, output_path)
                elif api_name == "placeholder":
                    return self._generate_placeholder_image(prompt, output_path, scene['scene_number'])
                    
            except Exception as e:
                print(f"⚠ {api_name.title()} hatası: {e}")
                continue
        
        # Hiç biri çalışmazsa placeholder
        return self._generate_placeholder_image(prompt, output_path, scene['scene_number'])
    
    def _generate_with_replicate(self, prompt: str, output_path: str) -> str:
        """Replicate API ile görsel üretir (FLUX Schnell) - Rate limit korumalı"""
        if not self.replicate_generator:
            raise Exception("Replicate generator bulunamadı")
        
        # Rate limit kontrolü - istekler arası bekleme
        current_time = time.time()
        time_since_last_request = current_time - self.last_replicate_request_time
        
        if time_since_last_request < self.replicate_delay:
            wait_time = self.replicate_delay - time_since_last_request
            print(f"⏳ Rate limit koruması: {wait_time:.1f} saniye bekleniyor...")
            time.sleep(wait_time)
        
        # Prompt'u optimize et
        enhanced_prompt = f"{prompt}, cinematic, high quality, detailed, professional photography"
        
        # Görseli üret
        result = self.replicate_generator.generate_image(
            prompt=enhanced_prompt,
            output_path=output_path,
            model="flux-schnell"  # En hızlı ve ucuz
        )
        
        # Son istek zamanını güncelle
        self.last_replicate_request_time = time.time()
        
        return result
    
    def _generate_with_replicate_ip_adapter(self, prompt: str, output_path: str, 
                                            scene: Dict[str, str]) -> str:
        """
        FLUX-2 Dev ile karakter tutarlı görsel üretir (SEVIYE 2: YÜKSEK TUTARLILIK)
        İlk sahne görselini referans alarak %90+ tutarlılık sağlar
        
        NOT: Şu an USE_IP_ADAPTER=False olduğu için bu metod çağrılmayacak
        """
        if not self.replicate_generator:
            raise Exception("Replicate generator bulunamadı")
        
        # Rate limit kontrolü
        current_time = time.time()
        time_since_last_request = current_time - self.last_replicate_request_time
        
        if time_since_last_request < self.replicate_delay:
            wait_time = self.replicate_delay - time_since_last_request
            print(f"⏳ Rate limit koruması: {wait_time:.1f} saniye bekleniyor...")
            time.sleep(wait_time)
        
        # Ana karakteri bul
        scene_characters = scene.get('characters', [])
        if not scene_characters:
            # Karakter yoksa normal mod
            return self._generate_with_replicate(prompt, output_path)
        
        main_character = scene_characters[0]  # İlk karakter ana karakter
        reference_image = self.first_scene_images.get(main_character)
        
        if not reference_image or not os.path.exists(reference_image):
            # Referans yoksa normal mod
            print(f"⚠ {main_character} için referans görsel bulunamadı, normal mod kullanılıyor")
            return self._generate_with_replicate(prompt, output_path)
        
        # Prompt'u optimize et
        enhanced_prompt = f"{prompt}, same character as reference, consistent appearance, identical features"
        
        print(f"🎭 FLUX-2 ile {main_character} tutarlılığı sağlanıyor...")
        print(f"   Referans: {reference_image}")
        
        try:
            # FLUX-2 Dev multi-reference ile üret
            result = self.replicate_generator.generate_image_with_character_reference(
                prompt=enhanced_prompt,
                output_path=output_path,
                reference_image_path=reference_image,
                character_strength=0.85  # Yüksek tutarlılık
            )
        except Exception as e:
            # FLUX-2 başarısız olursa normal FLUX kullan
            print(f"⚠ FLUX-2 hatası, normal FLUX Schnell kullanılıyor: {e}")
            return self._generate_with_replicate(prompt, output_path)
        
        # Son istek zamanını güncelle
        self.last_replicate_request_time = time.time()
        
        return result
    
    def _generate_with_huggingface(self, prompt: str, output_path: str) -> str:
        """Hugging Face Inference API ile görsel üretir"""
        headers = {
            'Authorization': f'Bearer {self.hf_token}',
            'Content-Type': 'application/json'
        }
        
        # Prompt'u optimize et
        enhanced_prompt = f"{prompt}, high quality, detailed, cinematic lighting, 4k"
        
        payload = {
            "inputs": enhanced_prompt,
            "parameters": {
                "negative_prompt": "blurry, low quality, distorted, ugly, bad anatomy",
                "num_inference_steps": 25,
                "guidance_scale": 7.5,
                "width": 1024,
                "height": 768
            }
        }
        
        response = requests.post(self.hf_api_url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        
        # Resmi kaydet
        with open(output_path, 'wb') as f:
            f.write(response.content)
        
        print(f"✓ Hugging Face ile görsel oluşturuldu: {output_path}")
        return output_path
    
    def _generate_with_together(self, prompt: str, output_path: str) -> str:
        """Together AI ile görsel üretir"""
        headers = {
            'Authorization': f'Bearer {self.together_key}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            "model": "stabilityai/stable-diffusion-xl-base-1.0",
            "prompt": f"{prompt}, high quality, detailed, cinematic",
            "width": 1024,
            "height": 768,
            "steps": 20,
            "n": 1
        }
        
        response = requests.post(self.together_api_url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        
        result = response.json()
        image_url = result['data'][0]['url']
        
        # Görseli indir
        image_response = requests.get(image_url, timeout=30)
        image_response.raise_for_status()
        
        with open(output_path, 'wb') as f:
            f.write(image_response.content)
        
        print(f"✓ Together AI ile görsel oluşturuldu: {output_path}")
        return output_path
    
    def _generate_with_stability(self, prompt: str, output_path: str) -> str:
        """Stability AI ile görsel üretir"""
        headers = {
            'Authorization': f'Bearer {self.stability_key}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            "text_prompts": [
                {
                    "text": f"{prompt}, masterpiece, best quality, detailed",
                    "weight": 1
                },
                {
                    "text": "blurry, bad quality, distorted, ugly",
                    "weight": -1
                }
            ],
            "cfg_scale": 7,
            "height": 768,
            "width": 1024,
            "samples": 1,
            "steps": 20
        }
        
        response = requests.post(self.stability_api_url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        
        result = response.json()
        image_data = result['artifacts'][0]['base64']
        
        # Base64'ü decode et ve kaydet
        image_bytes = base64.b64decode(image_data)
        with open(output_path, 'wb') as f:
            f.write(image_bytes)
        
        print(f"✓ Stability AI ile görsel oluşturuldu: {output_path}")
        return output_path
    
    def _generate_with_pollinations(self, prompt: str, output_path: str) -> str:
        """Pollinations.ai ile görsel üretir (ücretsiz)"""
        # URL parametrelerini hazırla
        enhanced_prompt = f"{prompt}, cinematic, high quality, detailed"
        params = {
            "width": 1024,
            "height": 768,
            "seed": -1,  # Random seed
            "model": "flux"  # En iyi model
        }
        
        # URL oluştur
        url = f"{self.pollinations_api_url}/{requests.utils.quote(enhanced_prompt)}"
        
        response = requests.get(url, params=params, timeout=60)
        response.raise_for_status()
        
        # Görseli kaydet
        with open(output_path, 'wb') as f:
            f.write(response.content)
        
        print(f"✓ Pollinations.ai ile görsel oluşturuldu: {output_path}")
        return output_path
    
    def _generate_placeholder_image(self, prompt: str, output_path: str, scene_number: int) -> str:
        """Placeholder görsel oluşturur (son çare)"""
        try:
            # 1024x768 boyutunda görsel oluştur
            width, height = 1024, 768
            
            # Sahne numarasına göre renk gradyanı
            colors = [
                (25, 25, 112),    # Midnight Blue
                (72, 61, 139),    # Dark Slate Blue  
                (106, 90, 205),   # Slate Blue
                (147, 112, 219),  # Medium Purple
                (138, 43, 226),   # Blue Violet
                (75, 0, 130)      # Indigo
            ]
            
            color_index = (scene_number - 1) % len(colors)
            base_color = colors[color_index]
            
            # Görsel oluştur
            image = Image.new('RGB', (width, height), base_color)
            draw = ImageDraw.Draw(image)
            
            # Gradient efekti
            for y in range(height):
                alpha = y / height
                r = int(base_color[0] * (1 - alpha) + 255 * alpha * 0.3)
                g = int(base_color[1] * (1 - alpha) + 255 * alpha * 0.3)
                b = int(base_color[2] * (1 - alpha) + 255 * alpha * 0.3)
                
                draw.line([(0, y), (width, y)], fill=(r, g, b))
            
            # Sahne numarasını ekle
            try:
                font = ImageFont.truetype("arial.ttf", 80)
            except:
                font = ImageFont.load_default()
            
            scene_text = f"Sahne {scene_number}"
            
            # Metin boyutunu hesapla
            text_bbox = draw.textbbox((0, 0), scene_text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            
            # Metni ortala
            x = (width - text_width) // 2
            y = (height - text_height) // 2 - 50
            
            # Gölge efekti
            draw.text((x + 3, y + 3), scene_text, fill=(0, 0, 0), font=font)
            draw.text((x, y), scene_text, fill=(255, 255, 255), font=font)
            
            # Prompt'u alt kısma ekle
            prompt_lines = self._wrap_text(prompt[:100], 60)
            try:
                small_font = ImageFont.truetype("arial.ttf", 24)
            except:
                small_font = ImageFont.load_default()
            
            y_offset = height - 150
            for line in prompt_lines[:3]:  # En fazla 3 satır
                line_bbox = draw.textbbox((0, 0), line, font=small_font)
                line_width = line_bbox[2] - line_bbox[0]
                x_line = (width - line_width) // 2
                
                # Gölge
                draw.text((x_line + 2, y_offset + 2), line, fill=(0, 0, 0), font=small_font)
                draw.text((x_line, y_offset), line, fill=(200, 200, 200), font=small_font)
                y_offset += 35
            
            # Görseli kaydet
            image.save(output_path, 'JPEG', quality=95)
            print(f"✓ Placeholder görsel oluşturuldu: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"✗ Placeholder görsel oluşturma hatası: {e}")
            raise
    
    def _wrap_text(self, text: str, width: int) -> List[str]:
        """Metni belirtilen genişlikte satırlara böler"""
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            current_line.append(word)
            if len(' '.join(current_line)) > width:
                if len(current_line) > 1:
                    current_line.pop()
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    lines.append(word)
                    current_line = []
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines
    
    def generate_story_images(self, scenes: List[Dict[str, str]], story_title: str) -> List[str]:
        """Tüm hikaye için görselleri oluşturur"""
        image_files = []
        
        print(f"🎨 {story_title} için görseller oluşturuluyor...")
        print(f"📋 Kullanılacak API sırası: {' → '.join(self.api_priority)}")
        
        # Kısa bir hikaye ID'si oluştur (dosya adı çok uzun olmasın - Windows limit 260 karakter)
        import hashlib
        story_hash = hashlib.md5(story_title.encode()).hexdigest()[:8]
        
        for i, scene in enumerate(scenes, 1):
            # Kısa dosya adı kullan
            filename = f"story_{story_hash}_scene_{i:02d}.jpg"
            
            try:
                image_path = self.generate_scene_image(scene, filename)
                image_files.append(image_path)
                
                # API rate limiting için kısa bekleme
                time.sleep(1)
                
            except Exception as e:
                print(f"✗ Sahne {i} görseli oluşturulamadı: {e}")
                # Son çare placeholder
                fallback_path = os.path.join(self.images_dir, filename)
                self._generate_placeholder_image(scene['image_prompt'], fallback_path, i)
                image_files.append(fallback_path)
        
        print(f"✅ {len(image_files)} görsel oluşturuldu")
        return image_files
    
    def test_all_apis(self) -> Dict[str, bool]:
        """Tüm API'leri test eder"""
        test_results = {}
        
        if self.replicate_generator:
            test_results["replicate"] = self._test_replicate()
        
        if self.hf_token:
            test_results["huggingface"] = self._test_huggingface()
        
        test_results["pollinations"] = self._test_pollinations()
        
        return test_results
    
    def _test_replicate(self) -> bool:
        """Replicate API test"""
        try:
            return self.replicate_generator.test_api()
        except:
            return False
    
    def _test_huggingface(self) -> bool:
        """Hugging Face API test"""
        try:
            headers = {'Authorization': f'Bearer {self.hf_token}'}
            response = requests.post(
                self.hf_api_url,
                headers=headers,
                json={"inputs": "test"},
                timeout=10
            )
            return response.status_code == 200
        except:
            return False
    
    def _test_pollinations(self) -> bool:
        """Pollinations.ai test"""
        try:
            response = requests.get(f"{self.pollinations_api_url}/test", timeout=10)
            return response.status_code == 200
        except:
            return False
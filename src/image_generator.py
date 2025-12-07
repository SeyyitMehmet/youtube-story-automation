"""
AI Görsel üretimi modülü
DeepSeek API ve ücretsiz alternatiflerle görsel üretir
"""
import os
import requests
import json
from PIL import Image, ImageDraw, ImageFont
from typing import List, Dict, Optional
import tempfile
import time

class ImageGenerator:
    def __init__(self, api_key: str = "", api_url: str = "", use_free_alternative: bool = True):
        self.api_key = api_key
        self.api_url = api_url
        self.use_free_alternative = use_free_alternative
        self.images_dir = "images"
        
        # Klasör oluştur
        os.makedirs(self.images_dir, exist_ok=True)
    
    def generate_scene_image(self, scene: Dict[str, str], output_filename: str) -> str:
        """Bir sahne için görsel oluşturur"""
        prompt = scene['image_prompt']
        output_path = os.path.join(self.images_dir, output_filename)
        
        # DeepSeek API'yi dene
        if self.api_key and not self.use_free_alternative:
            try:
                return self._generate_with_deepseek(prompt, output_path)
            except Exception as e:
                print(f"⚠ DeepSeek API hatası: {e}")
                print("🔄 Ücretsiz alternatife geçiliyor...")
        
        # Ücretsiz alternatif: Placeholder görsel + metin
        return self._generate_placeholder_image(prompt, output_path, scene['scene_number'])
    
    def _generate_with_deepseek(self, prompt: str, output_path: str) -> str:
        """DeepSeek API ile görsel üretir"""
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'prompt': prompt,
            'size': '1920x1080',
            'quality': 'standard',
            'n': 1
        }
        
        try:
            response = requests.post(self.api_url, headers=headers, json=payload)
            response.raise_for_status()
            
            result = response.json()
            image_url = result['data'][0]['url']
            
            # Görseli indir
            image_response = requests.get(image_url)
            image_response.raise_for_status()
            
            with open(output_path, 'wb') as f:
                f.write(image_response.content)
            
            print(f"✓ DeepSeek ile görsel oluşturuldu: {output_path}")
            return output_path
            
        except Exception as e:
            raise Exception(f"DeepSeek API hatası: {e}")
    
    def _generate_placeholder_image(self, prompt: str, output_path: str, scene_number: int) -> str:
        """Placeholder görsel oluşturur (ücretsiz alternatif)"""
        try:
            # 1920x1080 boyutunda görsel oluştur
            width, height = 1920, 1080
            
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
                # Sistem fontunu kullanmaya çalış
                font = ImageFont.truetype("arial.ttf", 120)
            except:
                # Varsayılan font
                font = ImageFont.load_default()
            
            scene_text = f"Sahne {scene_number}"
            
            # Metin boyutunu hesapla
            text_bbox = draw.textbbox((0, 0), scene_text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            
            # Metni ortala
            x = (width - text_width) // 2
            y = (height - text_height) // 2 - 100
            
            # Gölge efekti
            draw.text((x + 3, y + 3), scene_text, fill=(0, 0, 0), font=font)
            draw.text((x, y), scene_text, fill=(255, 255, 255), font=font)
            
            # Prompt'u alt kısma ekle
            prompt_lines = self._wrap_text(prompt, 80)
            try:
                small_font = ImageFont.truetype("arial.ttf", 32)
            except:
                small_font = ImageFont.load_default()
            
            y_offset = height - 200
            for line in prompt_lines[:4]:  # En fazla 4 satır
                line_bbox = draw.textbbox((0, 0), line, font=small_font)
                line_width = line_bbox[2] - line_bbox[0]
                x_line = (width - line_width) // 2
                
                # Gölge
                draw.text((x_line + 2, y_offset + 2), line, fill=(0, 0, 0), font=small_font)
                draw.text((x_line, y_offset), line, fill=(200, 200, 200), font=small_font)
                y_offset += 40
            
            # Görseli kaydet
            image.save(output_path, 'JPEG', quality=95)
            print(f"✓ Placeholder görsel oluşturuldu: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"✗ Placeholder görsel oluşturma hatası: {e}")
            # Son çare: Tek renkli görsel
            return self._generate_solid_image(output_path, base_color, scene_number)
    
    def _generate_solid_image(self, output_path: str, color: tuple, scene_number: int) -> str:
        """Tek renkli görsel oluşturur (son çare)"""
        try:
            image = Image.new('RGB', (1920, 1080), color)
            draw = ImageDraw.Draw(image)
            
            # Sadece sahne numarası
            text = f"Sahne {scene_number}"
            font = ImageFont.load_default()
            
            text_bbox = draw.textbbox((0, 0), text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            
            x = (1920 - text_width) // 2
            y = (1080 - text_height) // 2
            
            draw.text((x, y), text, fill=(255, 255, 255), font=font)
            
            image.save(output_path, 'JPEG')
            print(f"✓ Basit görsel oluşturuldu: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"✗ Görsel oluşturma başarısız: {e}")
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
                time.sleep(0.5)
                
            except Exception as e:
                print(f"✗ Sahne {i} görseli oluşturulamadı: {e}")
                # Varsayılan görsel oluştur
                fallback_path = os.path.join(self.images_dir, filename)
                self._generate_solid_image(fallback_path, (50, 50, 100), i)
                image_files.append(fallback_path)
        
        print(f"✓ {len(image_files)} görsel oluşturuldu")
        return image_files
    
    def test_deepseek_api(self) -> bool:
        """DeepSeek API'nin çalışıp çalışmadığını test eder"""
        if not self.api_key:
            print("❌ DeepSeek API key tanımlanmamış")
            return False
        
        test_prompt = "A simple test image"
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'prompt': test_prompt,
            'size': '512x512',
            'n': 1
        }
        
        try:
            response = requests.post(self.api_url, headers=headers, json=payload, timeout=10)
            if response.status_code == 200:
                print("✓ DeepSeek API çalışıyor")
                return True
            else:
                print(f"❌ DeepSeek API hatası: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ DeepSeek API bağlantı hatası: {e}")
            return False
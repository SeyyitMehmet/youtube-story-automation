"""
Video oluşturma modülü
Ses ve görselleri birleştirerek video oluşturur
"""
import os
import tempfile
from typing import List, Dict, Tuple

# MoviePy 2.x import syntax
from moviepy import (
    VideoFileClip, ImageClip, AudioFileClip,
    TextClip, ColorClip, CompositeVideoClip,
    concatenate_videoclips, concatenate_audioclips,
    CompositeAudioClip
)

class VideoCreator:
    def __init__(self, output_dir: str = "videos"):
        self.output_dir = output_dir
        self.temp_dir = tempfile.mkdtemp()
        
        # Klasörleri oluştur
        os.makedirs(output_dir, exist_ok=True)
    
    def create_scene_video(self, image_path: str, audio_path: str, 
                          scene_duration: float = None):
        """Bir sahne için video klip oluşturur"""
        try:
            # Ses dosyasını yükle
            audio_clip = AudioFileClip(audio_path)
            
            # SES DOSYASININ GERÇEK SÜRESİNİ KULLAN (AI'nin önerdiği süre değil!)
            visual_duration = audio_clip.duration
            
            # Görseli yükle ve video klip haline getir (MoviePy 2.x syntax)
            image_clip = ImageClip(image_path).with_duration(visual_duration)
            
            # Görseli 1920x1080'e boyutlandır
            image_clip = image_clip.resized((1920, 1080))
            
            # Zoom efekti ekle (Ken Burns efekti)
            image_clip = self._apply_zoom_effect(image_clip, visual_duration)
            
            # Ses ve görüntüyü birleştir (MoviePy 2.x syntax)
            video_clip = image_clip.with_audio(audio_clip)
            
            print(f"✓ Sahne video klipi oluşturuldu: ses={visual_duration:.1f}s, görsel={visual_duration:.1f}s")
            return video_clip
            
        except Exception as e:
            print(f"✗ Sahne video klip hatası: {e}")
            raise
            raise
    
    def create_story_video(self, scenes: List[Dict[str, str]], 
                          image_files: List[str], audio_files: List[str], 
                          story_title: str) -> str:
        """Tüm hikaye için video oluşturur"""
        
        print(f"🎬 {story_title} için video oluşturuluyor...")
        
        if len(scenes) != len(image_files) or len(scenes) != len(audio_files):
            raise ValueError("Sahne, görsel ve ses dosyası sayıları eşleşmiyor!")
        
        video_clips = []
        
        try:
            # Her sahne için video klip oluştur
            for i, (scene, image_file, audio_file) in enumerate(zip(scenes, image_files, audio_files)):
                print(f"📹 Sahne {i+1}/{len(scenes)} işleniyor...")
                
                # Süreyi verme! Ses dosyasının gerçek süresi kullanılacak
                clip = self.create_scene_video(
                    image_path=image_file,
                    audio_path=audio_file,
                    scene_duration=None  # Ses dosyasının gerçek süresini kullan
                )
                video_clips.append(clip)
            
            # Tüm klipleri birleştir
            print("🔗 Video klipleri birleştiriliyor...")
            final_video = concatenate_videoclips(video_clips, method="compose")
            
            # Başlık ve bitiş ekranları kaldırıldı (hata veriyordu)
            # final_video = self._add_title_and_credits(final_video, story_title)
            
            # Fon müziği ekle
            final_video = self._add_background_music(final_video, volume=0.05)
            
            # Video dosyasını kaydet - KISA DOSYA ADI (Windows 260 karakter limiti)
            import hashlib
            story_hash = hashlib.md5(story_title.encode()).hexdigest()[:8]
            output_filename = f"story_{story_hash}.mp4"
            output_path = os.path.join(self.output_dir, output_filename)
            
            print(f"💾 Video kaydediliyor: {output_filename}")
            
            # Video export ayarları (optimize edilmiş)
            final_video.write_videofile(
                output_path,
                fps=24,
                codec='libx264',
                audio_codec='aac',
                temp_audiofile=os.path.join(self.temp_dir, 'temp-audio.m4a'),
                remove_temp=True,
                preset='medium',  # Hız vs kalite dengesi
                ffmpeg_params=['-crf', '23']  # Kalite ayarı (18-28 arası)
            )
            
            # Klipleri temizle
            for clip in video_clips:
                clip.close()
            final_video.close()
            
            print(f"✅ Video başarıyla oluşturuldu: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"✗ Video oluşturma hatası: {e}")
            # Klipleri temizle
            for clip in video_clips:
                try:
                    clip.close()
                except:
                    pass
            raise
    
    def _apply_zoom_effect(self, clip, duration):
        """Görsele zoom efekti uygular (Ken Burns efekti)"""
        try:
            import random
            
            # Rastgele zoom yönü seç (zoom-in veya zoom-out)
            zoom_type = random.choice(['in', 'out'])
            
            if zoom_type == 'in':
                # Zoom-in: Normal boyuttan başla, yakınlaş
                start_scale = 1.0
                end_scale = 1.3
            else:
                # Zoom-out: Yakından başla, uzaklaş
                start_scale = 1.3
                end_scale = 1.0
            
            def zoom_effect(get_frame, t):
                """Her frame için zoom uygula"""
                # Zamanla ölçeği değiştir (linear interpolation)
                progress = t / duration
                current_scale = start_scale + (end_scale - start_scale) * progress
                
                frame = get_frame(t)
                h, w = frame.shape[:2]
                
                # Yeni boyutları hesapla
                new_h, new_w = int(h * current_scale), int(w * current_scale)
                
                # Görüntüyü yeniden boyutlandır
                from PIL import Image
                img = Image.fromarray(frame)
                img_resized = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
                
                # Merkeze göre kırp
                left = (new_w - w) // 2
                top = (new_h - h) // 2
                img_cropped = img_resized.crop((left, top, left + w, top + h))
                
                import numpy as np
                return np.array(img_cropped)
            
            # Efekti uygula
            clip = clip.transform(zoom_effect)
            print(f"  ✓ Zoom efekti uygulandı: {zoom_type}")
            return clip
            
        except Exception as e:
            print(f"  ⚠ Zoom efekti uygulanamadı: {e}")
            return clip
    
    def _add_title_and_credits(self, main_video, story_title: str):
        """Video'ya başlık ve bitiş ekranları ekler"""
        try:
            # Başlık ekranı oluştur
            title_clip = self._create_title_screen(story_title, duration=3)
            
            # Bitiş ekranı oluştur
            credits_clip = self._create_credits_screen(duration=3)
            
            # Tüm klipleri birleştir
            full_video = concatenate_videoclips([title_clip, main_video, credits_clip])
            
            return full_video
            
        except Exception as e:
            print(f"⚠ Başlık/bitiş ekranı eklenemedi: {e}")
            return main_video
    
    def _create_title_screen(self, title: str, duration: float = 3):
        """Başlık ekranı oluşturur"""
        try:
            # Siyah arka plan (MoviePy 2.x syntax)
            title_clip = ColorClip(size=(1920, 1080), color=(0, 0, 0)).with_duration(duration)
            
            # Başlık metni (MoviePy 2.x syntax)
            title_text = TextClip(
                text=title,
                font_size=80,
                color='white',
                font='Arial-Bold'
            ).with_position('center').with_duration(duration)
            
            # Alt yazı
            subtitle_text = TextClip(
                text="Yapay Zeka ile Hikaye Anlatımı",
                font_size=40,
                color='lightgray',
                font='Arial'
            ).with_position(('center', 0.7), relative=True).with_duration(duration)
            
            # Tüm elementleri birleştir
            title_screen = CompositeVideoClip([title_clip, title_text, subtitle_text])
            
            return title_screen
            
        except Exception as e:
            print(f"⚠ Başlık ekranı oluşturulamadı: {e}")
            # Basit siyah ekran döndür
            return ColorClip(size=(1920, 1080), color=(0, 0, 0)).with_duration(duration)
    
    def _create_credits_screen(self, duration: float = 3):
        """Bitiş ekranı oluşturur"""
        try:
            # Koyu mavi arka plan (MoviePy 2.x syntax)
            credits_clip = ColorClip(size=(1920, 1080), color=(25, 25, 50)).with_duration(duration)
            
            # Teşekkür metni
            thanks_text = TextClip(
                text="Dinlediğiniz İçin Teşekkürler!",
                font_size=60,
                color='white',
                font='Arial-Bold'
            ).with_position('center').with_duration(duration)
            
            # Alt bilgi
            info_text = TextClip(
                text="Bu video AI teknolojileri ile oluşturulmuştur\n🎨 Görseller: AI Generated\n🎤 Ses: TTS\n🎬 Video: Otomatik",
                font_size=30,
                color='lightblue',
                font='Arial'
            ).with_position(('center', 0.75), relative=True).with_duration(duration)
            
            # Tüm elementleri birleştir
            credits_screen = CompositeVideoClip([credits_clip, thanks_text, info_text])
            
            return credits_screen
            
        except Exception as e:
            print(f"⚠ Bitiş ekranı oluşturulamadı: {e}")
            # Basit renkli ekran döndür
            return ColorClip(size=(1920, 1080), color=(25, 25, 50)).with_duration(duration)
    
    def _add_background_music(self, video_clip, volume: float = 0.05):
        """Video'ya fon müziği ekler (rastgele seçim)"""
        try:
            import random
            import glob
            
            # musics/ klasöründeki tüm .mp3 dosyalarını bul
            music_files = glob.glob(os.path.join("musics", "*.mp3"))
            
            if not music_files:
                print(f"⚠ musics/ klasöründe hiç müzik dosyası bulunamadı!")
                return video_clip
            
            # Rastgele bir müzik seç
            background_music_path = random.choice(music_files)
            music_name = os.path.basename(background_music_path)
            
            print(f"🎵 Fon müziği ekleniyor: {music_name} (ses seviyesi: %{int(volume*100)})")
            
            # Fon müziğini yükle
            bg_music = AudioFileClip(background_music_path)
            
            # Müziği video süresi kadar döngüye al (loop)
            if bg_music.duration < video_clip.duration:
                # Müzik kısaysa, döngüye al
                loops_needed = int(video_clip.duration / bg_music.duration) + 1
                bg_music = concatenate_audioclips([bg_music] * loops_needed)
            
            # Müziği video süresi kadar kes
            bg_music = bg_music.subclipped(0, video_clip.duration)
            
            # Ses seviyesini ayarla (%5)
            bg_music = bg_music.with_volume_scaled(volume)
            
            # Orijinal ses ile fon müziğini birleştir
            if video_clip.audio:
                final_audio = CompositeAudioClip([video_clip.audio, bg_music])
                video_clip = video_clip.with_audio(final_audio)
            else:
                video_clip = video_clip.with_audio(bg_music)
            
            print("✓ Fon müziği başarıyla eklendi")
            return video_clip
            
        except Exception as e:
            print(f"⚠ Fon müziği eklenemedi: {e}")
            return video_clip
    
    def get_video_info(self, video_path: str) -> Dict[str, any]:
        """Video dosyası hakkında bilgi döndürür"""
        try:
            video = VideoFileClip(video_path)
            info = {
                'duration': video.duration,
                'fps': video.fps,
                'size': video.size,
                'filename': os.path.basename(video_path),
                'filesize': os.path.getsize(video_path),
                'format': os.path.splitext(video_path)[1]
            }
            video.close()
            return info
        except Exception as e:
            print(f"✗ Video bilgisi alınamadı: {e}")
            return {}
    
    def create_preview_video(self, video_path: str, start_time: float = 0, 
                           duration: float = 30) -> str:
        """Video'dan önizleme klipi oluşturur"""
        try:
            video = VideoFileClip(video_path)
            
            # Önizleme klipini kes (MoviePy 2.x syntax)
            preview = video.subclipped(start_time, min(start_time + duration, video.duration))
            
            # Önizleme dosyasını kaydet
            preview_filename = f"preview_{os.path.basename(video_path)}"
            preview_path = os.path.join(self.output_dir, preview_filename)
            
            preview.write_videofile(
                preview_path,
                fps=24,
                codec='libx264',
                preset='fast'
            )
            
            video.close()
            preview.close()
            
            print(f"✓ Önizleme oluşturuldu: {preview_path}")
            return preview_path
            
        except Exception as e:
            print(f"✗ Önizleme oluşturma hatası: {e}")
            raise
    
    def cleanup_temp_files(self):
        """Geçici dosyaları temizler"""
        try:
            import shutil
            shutil.rmtree(self.temp_dir, ignore_errors=True)
            print("✓ Geçici dosyalar temizlendi")
        except Exception as e:
            print(f"⚠ Geçici dosya temizleme hatası: {e}")
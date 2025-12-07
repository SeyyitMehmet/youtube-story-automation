# 🎬 YouTube Hikaye Otomasyonu

AI destekli otomatik hikaye anlatım video üretim sistemi. Metinsel hikayeleri sesli anlatım ve görseller ile videoya dönüştürür.

## 🌟 Özellikler

- 📚 **Hikaye İşleme**: Metinsel hikayeleri sahnelere böler (AI destekli)
- 🎤 **Sesli Anlatım**: 
  - **OpenAI TTS-1 HD**: Yüksek kaliteli, doğal seslendirme (6 farklı ses)
  - **gTTS**: Ücretsiz Google TTS
  - **pyttsx3**: Offline TTS
- 🎨 **AI Görseller**: 
  - **Replicate (FLUX Schnell)**: Yüksek kaliteli görseller
  - **Pollinations.ai**: Ücretsiz alternatif
  - **DeepSeek**: Hikaye analizi ve sahne oluşturma
- 🎬 **Video Üretimi**: 
  - MoviePy ile profesyonel montaj
  - Ken Burns zoom efektleri
  - Fon müziği desteği
  - Otomatik klasör temizleme
- 📤 **YouTube Entegrasyonu**: Otomatik video yükleme (isteğe bağlı)
- 💰 **Esnek Maliyet**: Ücretsiz ve premium API seçenekleri

## 🚀 Hızlı Başlangıç

### 1. Kurulum

```bash
# Repository'i klonlayın
git clone <repo-url>
cd youtube-story-automation

# Python bağımlılıklarını kurun
pip install -r requirements.txt
```

### 2. API Anahtarları

`.env` dosyasını düzenleyin:

```env
# DeepSeek API (hikaye analizi için - gerekli)
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxx

# OpenAI API (TTS-1 HD seslendirme - isteğe bağlı)
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxx

# Replicate API (FLUX Schnell görseller - isteğe bağlı)
REPLICATE_API_KEY=r8_xxxxxxxxxxxxxxxx

# YouTube API (otomatik yükleme için - isteğe bağlı)
YOUTUBE_CLIENT_ID=your_client_id_here
YOUTUBE_CLIENT_SECRET=your_client_secret_here
```

**API Kullanım Kılavuzları:**
- 📖 [OpenAI TTS-1 HD Kullanımı](docs/OPENAI_TTS_KULLANIMI.md)
- 📖 [DeepSeek API Kurulumu](docs/DEEPSEEK_SETUP.md)
- 📖 [Replicate API Kullanımı](docs/REPLICATE_SETUP.md)

### 3. Çalıştırma

```bash
python main.py
```

## 📋 Kullanım

### Menü Seçenekleri

1. **Video Oluştur (Yerel)**: Sadece video dosyası oluşturur
2. **Video Oluştur + YouTube**: Video oluşturur ve YouTube'a yükler
3. **Sistem Kontrolü**: Klasörler ve ayarları kontrol eder
4. **API Testleri**: Tüm API'leri test eder

### Örnek: Kibritçi Kız Hikayesi

Program varsayılan olarak `stories/kibritci_kiz.txt` dosyasındaki hikayeyi işler. Kendi hikayenizi eklemek için:

1. `stories/` klasörüne hikaye dosyanızı ekleyin
2. `main.py`'de dosya adını değiştirin veya fonksiyonu kendi dosyanızla çağırın

## 🛠 Teknik Detaylar

### Proje Yapısı

```
youtube-story-automation/
├── stories/           # Hikaye dosyaları
├── audio/            # Üretilen ses dosyaları
├── images/           # Üretilen görseller
├── videos/           # Son video dosyaları
├── src/              # Ana kod modülleri
│   ├── story_processor.py    # Hikaye işleme
│   ├── tts_generator.py      # Ses üretimi
│   ├── image_generator.py    # Görsel üretimi
│   ├── video_creator.py      # Video montajı
│   └── youtube_uploader.py   # YouTube yükleme
├── config/           # Konfigürasyon
├── main.py          # Ana program
└── requirements.txt # Python bağımlılıkları
```

### Teknolojiler

- **Python 3.8+**
- **TTS**: gTTS (ücretsiz) / pyttsx3 (offline)
- **Video**: MoviePy + FFmpeg
- **Görsel**: Pillow + DeepSeek API
- **YouTube**: Google APIs

## 💰 Maliyet Analizi

### Ücretsiz Seçenekler
- **TTS**: gTTS (Google) - Ücretsiz
- **Görseller**: Placeholder görseller - Ücretsiz
- **Video**: MoviePy + FFmpeg - Ücretsiz

### Ücretli Seçenekler (İsteğe Bağlı)
- **DeepSeek API**: ~$0.002 per görsel
- **YouTube API**: Ücretsiz (quota limiti var)

### Örnek Maliyet (5 dakikalık video)
- Ücretsiz yöntem: **$0**
- AI görselli yöntem: **~$0.012** (6 görsel)

## 🔧 Konfigürasyon

`config/config.py` dosyasında tüm ayarları özelleştirebilirsiniz:

```python
# TTS Ayarları
TTS_ENGINE = "gtts"  # veya "pyttsx3"
TTS_LANGUAGE = "tr"
TTS_SPEED = 150

# Video Ayarları
VIDEO_WIDTH = 1920
VIDEO_HEIGHT = 1080
VIDEO_FPS = 24

# Görsel Ayarları
IMAGE_STYLE = "cinematic, storytelling, fairy tale illustration"
```

## 📚 API Kurulumları

### DeepSeek API
1. [DeepSeek Platform](https://platform.deepseek.com/) hesabı oluşturun
2. API key alın
3. `.env` dosyasına ekleyin

### YouTube API
1. [Google Cloud Console](https://console.cloud.google.com/) projesine gidin
2. YouTube Data API v3'ü etkinleştirin
3. OAuth2 credentials oluşturun
4. Client ID ve Secret'ı `.env` dosyasına ekleyin

## 🐛 Sorun Giderme

### Yaygın Hatalar

**FFmpeg Hatası**:
```bash
# Windows
# FFmpeg'i indirin ve PATH'e ekleyin

# Linux/Mac
sudo apt install ffmpeg  # Ubuntu
brew install ffmpeg      # macOS
```

**Python Modül Hatası**:
```bash
pip install -r requirements.txt
```

**TTS Hatası**:
- İnternet bağlantısını kontrol edin (gTTS için)
- Offline için `TTS_ENGINE = "pyttsx3"` kullanın

### Log Dosyaları

Program çalışırken renkli çıktılar verir:
- ✅ Başarılı işlemler
- ⚠ Uyarılar
- ❌ Hatalar

## 🤝 Katkıda Bulunma

1. Fork edin
2. Feature branch oluşturun (`git checkout -b feature/YeniOzellik`)
3. Commit edin (`git commit -am 'Yeni özellik eklendi'`)
4. Push edin (`git push origin feature/YeniOzellik`)
5. Pull Request oluşturun

## 📄 Lisans

Bu proje MIT lisansı altında yayınlanmıştır.

## 🎯 Gelecek Özellikler

- [ ] Çoklu hikaye batch işleme
- [ ] Farklı AI görsel servisler (DALL-E, Midjourney)
- [ ] Çoklu ses seçenekleri
- [ ] Video efektleri ve geçişler
- [ ] Subtitle/altyazı desteği
- [ ] Çoklu dil desteği
- [ ] Web arayüzü

## 📞 İletişim

Sorularınız için:
- Issues açın
- Pull request gönderin
- Dokümantasyonu inceleyin

---

🎬 **Happy Storytelling!** 🎬
# 🎬 YouTube Hikaye Otomasyonu

**AI destekli otomatik hikaye-video dönüştürme sistemi.**

Metinsel hikayeleri profesyonel sesli anlatım ve AI görselleri ile otomatik videoya dönüştürür.

---

## 🎯 Ne Yapar?

```
📝 Hikaye (.txt) → 🎬 Video (.mp4)
```

**Örnek:** "Kibritçi Kız" hikayesini yüklersiniz → 5-10 dakikalık profesyonel video oluşturur.

---

## ⚡ Hızlı Başlangıç (Google Colab)

**En Kolay Yol:** Google Colab ile tarayıcıdan çalıştırın!

1. **Notebook'u açın:** [youtube_automation_full.ipynb](./youtube_automation_full.ipynb)
2. **Google Colab'da aç** → "Open in Colab" butonuna tıklayın
3. **API anahtarlarını ekle** (OpenAI, DeepSeek, Replicate)
4. **Run All** yap → Bilgisayarı kapat, işlem devam eder! ☕

**Detaylı adımlar notebook içinde.**

---

## 🎨 Özellikler

### ✨ AI Destekli İşlem Akışı

```
1. 📖 Hikaye Analizi (DeepSeek AI)
   → Hikayeyi otomatik sahnelere böler
   → Karakterleri ve ortamları tanımlar
   → Her sahne için prompt oluşturur

2. 🎤 Sesli Anlatım (OpenAI TTS-1 HD)
   → Profesyonel Türkçe ses
   → Doğal tonlama
   → 6 farklı ses seçeneği

3. 🖼️ Görsel Üretimi (Replicate FLUX)
   → Her sahne için AI görsel
   → Karakter tutarlılığı
   → 1920x1080 çözünürlük

4. 🎥 Video Montajı (MoviePy)
   → Ken Burns zoom efektleri
   → Fon müziği desteği
   → Otomatik senkronizasyon
```

---

## 📊 Üretilen Video Özellikleri

**Örnek Çıktı (5 sahneli hikaye):**

| Özellik | Değer |
|---------|-------|
| **Çözünürlük** | 1920x1080 (Full HD) |
| **FPS** | 24 fps |
| **Sahne Sayısı** | 5-8 sahne (hikayeye göre) |
| **Görsel/Sahne** | 1 AI üretimi görsel |
| **Ses** | OpenAI TTS-1 HD (Türkçe) |
| **Video Süresi** | 5-10 dakika (metin uzunluğuna göre) |
| **Dosya Boyutu** | ~40-60 MB |
| **Efektler** | Ken Burns zoom, cross-fade geçişleri |
| **Müzik** | Opsiyonel fon müziği |

**Maliyet (hikaye başına):**
- OpenAI TTS: ~$0.50
- Replicate FLUX: ~$0.015 (5 görsel)
- **Toplam: ~$0.52/hikaye**

---

## 💻 Yerel Bilgisayarda Çalıştırma (Opsiyonel)

### Kurulum

```bash
# Repository'i klonlayın
git clone https://github.com/SeyyitMehmet/youtube-story-automation.git
cd youtube-story-automation

# Virtual environment oluşturun
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Paketleri kurun
pip install -r requirements.txt
```

### API Anahtarlarını Ayarlayın

`.env.example` dosyasını `.env` olarak kopyalayın ve API anahtarlarınızı ekleyin:

```env
DEEPSEEK_API_KEY=sk-...
OPENAI_API_KEY=sk-proj-...
REPLICATE_API_KEY=r8_...
```

### Çalıştırın

```bash
python main.py
```

---

## 📁 Proje Yapısı

```
youtube-story-automation/
├── src/                          # Ana modüller
│   ├── story_processor.py        # DeepSeek ile hikaye analizi
│   ├── openai_tts_generator.py   # OpenAI TTS-1 HD
│   ├── multi_image_generator.py  # FLUX görsel üretimi
│   ├── character_manager.py      # Karakter tutarlılığı
│   └── video_creator.py          # MoviePy video montajı
│
├── config/                       # Ayarlar
│   ├── config.example.py         # Örnek config
│   └── config.py                 # Gerçek config (gitignore)
│
├── stories/                      # Hikaye dosyaları (.txt)
├── audio/                        # Üretilen sesler (temp)
├── images/                       # Üretilen görseller (temp)
├── videos/                       # Üretilen videolar
├── musics/                       # Fon müzikleri
│
├── main.py                       # Yerel çalıştırma scripti
├── youtube_automation_full.ipynb # Google Colab notebook
├── requirements.txt              # Python paketleri
├── .env.example                  # Örnek environment variables
└── README.md                     # Bu dosya
```

---

## 🔑 Gerekli API Anahtarları

### DeepSeek API (Hikaye Analizi)
- **Nereden:** https://platform.deepseek.com/api_keys
- **Maliyet:** Ücretsiz deneme kredisi
- **Kullanım:** Hikayeyi sahnelere böler, karakter analizi

### OpenAI API (Sesli Anlatım)
- **Nereden:** https://platform.openai.com/api-keys
- **Maliyet:** ~$15/milyon karakter (TTS-1 HD)
- **Kullanım:** Profesyonel Türkçe ses üretimi

### Replicate API (Görsel Üretimi)
- **Nereden:** https://replicate.com/account/api-tokens
- **Maliyet:** ~$0.003/görsel (FLUX Schnell)
- **Kullanım:** AI ile hikaye görselleri

---

## 📊 Performans & Süre

**5 sahneli bir hikaye için:**

| İşlem | Süre | Maliyet |
|-------|------|---------|
| Hikaye analizi (DeepSeek) | ~30 saniye | $0.001 |
| Ses üretimi (OpenAI TTS) | ~2 dakika | $0.50 |
| Görseller (Replicate FLUX) | ~5 dakika | $0.015 |
| Video montajı (MoviePy) | ~3 dakika | Ücretsiz |
| **TOPLAM** | **~10-12 dakika** | **~$0.52** |

**10 hikaye işleme:**
- Toplam süre: ~2 saat
- Toplam maliyet: ~$5.20

---

## 🆘 Sorun Giderme

### "No module named 'pyttsx3'" hatası
- Google Colab'da normal, pyttsx3 Windows'a özeldir
- Sistem otomatik OpenAI TTS kullanır

### MoviePy import hatası
```bash
pip install moviepy==2.2.1
```

### API rate limit
- `config.py` içinde `REPLICATE_RATE_LIMIT_DELAY` değerini artırın

### Video oluşmuyor
- FFmpeg kurulu mu kontrol edin: `ffmpeg -version`
- Windows: https://ffmpeg.org/download.html

---

## 📝 Lisans

MIT License - Detaylar için `LICENSE` dosyasına bakın.

---

## 🙏 Teşekkürler

- OpenAI (TTS-1 HD API)
- DeepSeek (Hikaye analizi)
- Replicate (FLUX modelleri)
- MoviePy (Video işleme)

---

**Made with ❤️ and AI**

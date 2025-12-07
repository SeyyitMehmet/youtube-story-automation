# 📦 Colab İçin Gerekli Paketler

Bu dosya, yerel projenizde çalışan **TAM SÜRÜMLER**i içerir.

## ✅ Kullanılan Sürümler

### 🎯 Core Paketler
```
python-dotenv==1.1.1
requests==2.32.5
colorama==0.4.6
tqdm==4.67.1
```

### 🤖 AI API'ler
```
openai==2.8.1          # TTS-1 HD için
replicate==1.0.7        # Görsel üretimi için
```

### 🎤 Text-to-Speech
```
gTTS==2.5.4            # Yedek TTS
pydub==0.25.1          # Ses işleme
```

### 🎨 Görsel İşleme
```
pillow==11.3.0         # Görsel düzenleme
imageio==2.37.0        # Video codec
imageio-ffmpeg==0.6.0  # FFmpeg wrapper
```

### 🎬 Video İşleme (KRİTİK!)
```
moviepy==2.2.1         # Video oluşturma
numpy==2.2.6           # MoviePy bağımlılığı
decorator==4.4.2       # MoviePy bağımlılığı
proglog==0.1.12        # MoviePy progress bar
```

### 📺 YouTube API (Opsiyonel)
```
google-api-python-client==2.184.0
google-auth==2.41.1
google-auth-oauthlib==1.2.2
google-auth-httplib2==0.2.0
```

---

## ⚠️ ÖNEMLİ NOTLAR:

### 🚫 Colab'da KULLANILMAYAN paketler:
- ❌ `pyttsx3==2.99` - Sadece Windows'ta çalışır
- ❌ `pywin32==311` - Windows özel
- ❌ `pypiwin32==223` - Windows özel
- ❌ `comtypes==1.4.12` - Windows özel
- ❌ `opencv-python==4.12.0.88` - MoviePy 2.x'te gerekli değil

---

## 🎯 Colab Kurulum Komutu (Tek Satır)

```bash
pip install python-dotenv==1.1.1 requests==2.32.5 colorama==0.4.6 tqdm==4.67.1 openai==2.8.1 replicate==1.0.7 gTTS==2.5.4 pydub==0.25.1 pillow==11.3.0 imageio==2.37.0 imageio-ffmpeg==0.6.0 moviepy==2.2.1 numpy==2.2.6 decorator==4.4.2 proglog==0.1.12 google-api-python-client==2.184.0 google-auth==2.41.1 google-auth-oauthlib==1.2.2 google-auth-httplib2==0.2.0
```

---

## 📊 Sürüm Karşılaştırması

| Paket | Yerel | Colab Default | Kullanılan |
|-------|-------|---------------|------------|
| openai | 2.8.1 | Eski | ✅ 2.8.1 |
| moviepy | 2.2.1 | 1.0.3 | ✅ 2.2.1 |
| pillow | 11.3.0 | 9.x | ✅ 11.3.0 |
| replicate | 1.0.7 | Yok | ✅ 1.0.7 |
| gTTS | 2.5.4 | 2.3.x | ✅ 2.5.4 |

---

## ✅ Test Edildi

- ✅ MoviePy 2.2.1 - Video oluşturma çalışıyor
- ✅ OpenAI 2.8.1 - TTS-1 HD çalışıyor
- ✅ Replicate 1.0.7 - Görsel üretimi çalışıyor
- ✅ ImageIO + FFmpeg - Codec sorunsuz

---

**Son güncelleme:** 27 Kasım 2025  
**Proje:** YouTube Story Automation  
**Platform:** Google Colab

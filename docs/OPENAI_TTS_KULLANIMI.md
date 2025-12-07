# OpenAI TTS-1 HD Kullanım Kılavuzu

## 🎤 OpenAI TTS-1 HD Nedir?

OpenAI'ın en yüksek kaliteli Text-to-Speech API'si. Doğal, akıcı ve profesyonel sesli anlatım sağlar.

### ✨ Özellikler
- **Yüksek Kalite**: TTS-1 HD modeli (en kaliteli)
- **Doğal Sesler**: 6 farklı ses karakteri
- **Hız Kontrolü**: 0.25x - 4.0x hız ayarı
- **Çok Dilli**: Türkçe dahil 50+ dil desteği
- **Hızlı**: 1-2 saniyede ses üretimi

### 💰 Fiyatlandırma
- **TTS-1 HD**: $0.015 / 1000 karakter
- Örnek: 5000 karakterlik hikaye = ~$0.075 (yaklaşık 2.5 TL)

---

## 🚀 Kurulum

### 1. OpenAI API Key Alma

1. [platform.openai.com](https://platform.openai.com/) adresine gidin
2. Hesap oluşturun veya giriş yapın
3. **API Keys** bölümüne gidin
4. **Create new secret key** butonuna tıklayın
5. Anahtarı kopyalayın (bir daha göremezsiniz!)

### 2. API Key'i .env Dosyasına Ekleme

`.env` dosyasını açın ve şu satırı güncelleyin:

```env
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxx
```

### 3. Paket Kurulumu

OpenAI paketi otomatik kuruldu. Eğer sorun olursa:

```bash
.\.venv\Scripts\python.exe -m pip install openai
```

---

## ⚙️ Yapılandırma

### config/config.py Ayarları

```python
# TTS Engine Seçimi
TTS_ENGINE = "openai"  # "openai", "gtts" veya "pyttsx3"

# OpenAI TTS-1 HD Ayarları
OPENAI_TTS_VOICE = "nova"  # Ses karakteri
OPENAI_TTS_SPEED = 1.0     # Konuşma hızı (0.25-4.0)
```

### 🎙️ Ses Karakterleri

| Ses | Karakter | Kullanım Alanı |
|-----|----------|----------------|
| **alloy** | Dengeli, nötr kadın | Genel amaçlı anlatım |
| **echo** | Erkek, güçlü | Otoriter anlatımlar |
| **fable** | İngiliz aksanlı erkek | Klasik masal anlatımı ⭐ |
| **onyx** | Derin erkek | Dramatik hikayeler |
| **nova** | Canlı kadın | Çocuk hikayeleri ⭐⭐⭐ |
| **shimmer** | Yumuşak kadın | Sakin, yatıştırıcı anlatım ⭐ |

**Türkçe hikayeler için öneriler:**
- 🌟 **En İyi**: `nova` - Canlı ve eğlenceli
- 📖 **Masal**: `fable` - Klasik anlatım
- 😌 **Sakin**: `shimmer` - Yumuşak ses

### ⚡ Hız Ayarları

```python
OPENAI_TTS_SPEED = 0.75  # Yavaş (anlaşılır)
OPENAI_TTS_SPEED = 1.0   # Normal (varsayılan) ⭐
OPENAI_TTS_SPEED = 1.25  # Hızlı (dinamik)
OPENAI_TTS_SPEED = 1.5   # Çok hızlı
```

---

## 📝 Kullanım

### Video Oluşturma ile Kullanım

1. `.env` dosyasına API key'inizi ekleyin
2. `config/config.py` dosyasında `TTS_ENGINE = "openai"` yapın
3. Ses karakterini seçin: `OPENAI_TTS_VOICE = "nova"`
4. Programı çalıştırın:

```bash
.\.venv\Scripts\python.exe main.py
```

5. Menüden **1. 🎬 Kibritçi Kız videosunu oluştur** seçin

### API Testi

Menüden **3. 🧪 API testleri** seçin:

```
🎤 TTS Testleri...
─────────────────────────────────────────

1️⃣  OpenAI TTS-1 HD Test...
✓ OpenAI TTS-1 HD başlatıldı (ses: nova, hız: 1.0)
✓ OpenAI TTS ses dosyası oluşturuldu: test_openai_tts.wav
✓ OpenAI TTS-1 HD çalışıyor
  Ses: nova | Hız: 1.0
  Test dosyası: audio\test_openai_tts.wav
```

Test dosyasını dinleyerek ses kalitesini kontrol edebilirsiniz.

---

## 🔄 TTS Engine Değiştirme

### OpenAI TTS → gTTS (Ücretsiz)

`config/config.py`:
```python
TTS_ENGINE = "gtts"
```

### OpenAI TTS → pyttsx3 (Offline)

`config/config.py`:
```python
TTS_ENGINE = "pyttsx3"
```

### Otomatik Yedekleme

Eğer OpenAI API key yoksa veya hata olursa, sistem otomatik olarak `gtts`'ye geçer:

```
✗ OPENAI_API_KEY bulunamadı! .env dosyasını kontrol edin.
🔄 Yedek TTS (gtts) kullanılıyor...
```

---

## 💡 İpuçları

### 1. Maliyet Optimizasyonu

- **5 sahne**: ~$0.03-0.05 (1.5 TL)
- **10 sahne**: ~$0.08-0.12 (3 TL)
- Sahne sayısını azaltmak maliyeti düşürür

### 2. Kalite Artırma

```python
OPENAI_TTS_VOICE = "nova"   # Canlı anlatım
OPENAI_TTS_SPEED = 0.9      # Biraz yavaşlat (net anlaşılır)
```

### 3. Ses Karşılaştırması

Her ses için test yapın:

```python
# test_voices.py
voices = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
for voice in voices:
    OPENAI_TTS_VOICE = voice
    # API test menüsünü çalıştır
```

### 4. Türkçe Optimizasyonu

OpenAI TTS otomatik dil algılar. Türkçe metinler için ekstra ayar gerekmez.

---

## ❓ Sorun Giderme

### "OPENAI_API_KEY bulunamadı"

✅ `.env` dosyasını kontrol edin:
```env
OPENAI_API_KEY=sk-proj-...
```

✅ API key'in doğru kopyalandığından emin olun (başında/sonunda boşluk olmamalı)

### "API key geçersiz" hatası

✅ [platform.openai.com/api-keys](https://platform.openai.com/api-keys) adresinden yeni key alın

✅ Eski key'lerin silinmiş olabileceğini kontrol edin

### "Kredi yetersiz" hatası

✅ [platform.openai.com/account/billing](https://platform.openai.com/account/billing) adresinden bakiye ekleyin

✅ Minimum $5 eklemeniz önerilir

### Ses dosyası oluşmuyor

✅ `audio/` klasörünü kontrol edin

✅ Test menüsünden OpenAI TTS testini çalıştırın

✅ Hata mesajını okuyun ve logları kontrol edin

---

## 📊 Maliyet Hesaplama

### Karakter Sayısı Tahminleri

- **Kibritçi Kız hikayesi**: ~1800 karakter
- **10 sahne** × **180 karakter/sahne** = 1800 karakter
- **Maliyet**: 1800 × $0.015 / 1000 = **~$0.027** (0.90 TL)

### Video Başına Ortalama Maliyet

| Sahne Sayısı | Karakter | Maliyet (USD) | Maliyet (TL) |
|--------------|----------|---------------|--------------|
| 5 sahne | ~900 | $0.014 | 0.45 TL |
| 10 sahne | ~1800 | $0.027 | 0.90 TL |
| 15 sahne | ~2700 | $0.041 | 1.35 TL |
| 20 sahne | ~3600 | $0.054 | 1.80 TL |

💰 **$5 kredi ile**: ~185 video oluşturabilirsiniz (10 sahne/video)

---

## 🎯 Karşılaştırma

| Özellik | OpenAI TTS-1 HD | gTTS | pyttsx3 |
|---------|-----------------|------|---------|
| **Kalite** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| **Doğallık** | Çok yüksek | Orta | Düşük |
| **Hız** | Çok hızlı | Orta | Hızlı |
| **Maliyet** | $0.015/1000 char | Ücretsiz | Ücretsiz |
| **İnternet** | Gerekli | Gerekli | Gerekmez |
| **Türkçe** | Mükemmel | İyi | Kötü |

**Sonuç**: OpenAI TTS-1 HD profesyonel kalite için ideal, gTTS test için yeterli, pyttsx3 offline çalışma için.

---

## 📚 Ek Kaynaklar

- [OpenAI TTS Dokumentasyon](https://platform.openai.com/docs/guides/text-to-speech)
- [OpenAI Fiyatlandırma](https://openai.com/pricing)
- [Ses Örnekleri](https://platform.openai.com/docs/guides/text-to-speech/voice-options)

---

## 🆘 Destek

Sorun yaşarsanız:
1. API test menüsünü çalıştırın
2. Hata mesajlarını kontrol edin
3. `.env` dosyasındaki API key'i doğrulayın
4. OpenAI hesap bakiyenizi kontrol edin

**İyi seslendirmeler! 🎤✨**

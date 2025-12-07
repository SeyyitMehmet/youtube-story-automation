# 🚀 Render.com Deployment Rehberi

Bu rehber projenizi Render.com'da 7/24 çalışır hale getirmenizi sağlar.

---

## 📋 Ön Hazırlık

### Gereksinimler:
- ✅ GitHub hesabı (kodlar yüklü olmalı)
- ✅ Render.com hesabı (ücretsiz: https://render.com)
- ✅ API anahtarları hazır:
  - OpenAI API Key
  - DeepSeek API Key
  - Replicate API Key
- ✅ Telegram Bot (opsiyonel ama önerilen)

---

## 1️⃣ Render.com'da Hesap Oluşturun

1. **https://render.com** adresine gidin
2. **"Get Started"** butonuna tıklayın
3. **GitHub ile giriş yapın** (önerilen)
4. GitHub hesabınızı bağlayın

---

## 2️⃣ Yeni Cron Job Oluşturun

### Adım 1: Yeni Servis Ekleyin

1. Render.com Dashboard'da **"New +"** butonuna tıklayın
2. **"Cron Job"** seçin ⚠️ (Background Worker DEĞİL!)
3. GitHub repository'nizi seçin:
   - **Repository:** `SeyyitMehmet/youtube-story-automation`
   - **Branch:** `main`

### Adım 2: Servis Ayarları

| Alan | Değer |
|------|-------|
| **Name** | `youtube-story-cron` |
| **Region** | Frankfurt (Türkiye için en yakın) |
| **Branch** | `main` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `python cron_worker.py` |
| **Schedule** | `0 */6 * * *` (Her 6 saatte bir) |

### Adım 3: Çalışma Zamanlaması

**Schedule** için cron formatı:

| Zamanlama | Cron Kodu | Açıklama |
|-----------|-----------|----------|
| Her 6 saatte bir | `0 */6 * * *` | 00:00, 06:00, 12:00, 18:00 |
| Her 3 saatte bir | `0 */3 * * *` | Her 3 saatte |
| Her 1 saatte | `0 * * * *` | Her saat başı |
| Günde 1 kez | `0 0 * * *` | Gece yarısı |
| Günde 3 kez | `0 9,15,21 * * *` | 09:00, 15:00, 21:00 |

**Önerim:** `0 */6 * * *` (günde 4 kez - yeterli)

### Adım 4: Plan Seçin

- **✅ FREE PLAN** (Otomatik seçili)
- ✅ Tamamen ücretsiz
- ✅ Sınırsız çalıştırma
- ✅ 512 MB RAM

---

## 3️⃣ Environment Variables Ekleyin

**Önemli:** API anahtarlarını Render.com'a eklemelisiniz!

### Dashboard'da:

1. **"Environment"** sekmesine gidin
2. **"Add Environment Variable"** butonuna tıklayın
3. Şu değişkenleri **tek tek** ekleyin:

| Key | Value (Kendi anahtarlarınız) |
|-----|------------------------------|
| `OPENAI_API_KEY` | `sk-proj-...` |
| `DEEPSEEK_API_KEY` | `sk-...` |
| `REPLICATE_API_KEY` | `r8_...` |
| `TELEGRAM_BOT_TOKEN` | `123456789:ABC...` (opsiyonel) |
| `TELEGRAM_CHAT_ID` | `987654321` (opsiyonel) |
| `STORIES_CHECK_INTERVAL` | `300` (5 dakika) |

### ⚠️ Önemli Notlar:

- API anahtarlarını **tırnak içine almayın**
- Başında/sonunda **boşluk bırakmayın**
- Her satıra **sadece 1 anahtar** ekleyin

---

## 4️⃣ Deploy Edin!

1. **"Create Web Service"** butonuna tıklayın
2. Render.com otomatik olarak:
   - ✅ Kodları GitHub'dan çeker
   - ✅ Paketleri kurar (`requirements.txt`)
   - ✅ Worker'ı başlatır (`render_worker.py`)

### Deployment Süreci:

```
🔄 Deploying... (2-3 dakika)
  → Cloning repository
  → Installing dependencies
  → Starting worker
✅ Live
```

---

## 5️⃣ İlk Hikayeyi Yükleyin

### Render.com Shell Kullanarak:

1. Dashboard'da **"Shell"** sekmesine gidin
2. Şu komutları çalıştırın:

```bash
# stories/ klasörüne git
cd stories

# Örnek hikaye oluştur
cat > test_hikaye.txt << 'EOF'
Bir varmış bir yokmuş, evvel zaman içinde...
(hikayenizin devamı)
EOF

# Dosyayı kontrol et
ls -la
```

### Veya GitHub'dan:

1. Local bilgisayarınızda `stories/` klasörüne `.txt` dosyası ekleyin
2. Git ile yükleyin:

```bash
git add stories/yeni_hikaye.txt
git commit -m "Yeni hikaye eklendi"
git push
```

3. Render.com otomatik deploy eder (2-3 dakika)

---

## 6️⃣ Logları İzleyin

### Dashboard'da:

1. **"Logs"** sekmesine gidin
2. Canlı logları göreceksiniz:

```
✅ RenderWorker başlatıldı!
🔄 Ana döngü başladı (kontrol: 300s)
🔍 Kontrol #1 - 2025-12-07 14:30:00
📚 1 yeni hikaye bulundu!
🎬 İşleniyor: test_hikaye
📖 Hikaye işleniyor...
✓ 5 sahne oluşturuldu
🎤 Sesler oluşturuluyor...
✓ 5 ses dosyası
🖼️ Görseller oluşturuluyor...
✓ 5 görsel
🎥 Video oluşturuluyor...
✅ Başarılı: test_hikaye
```

---

## 7️⃣ Videoları İndirin

### Render.com Shell'den:

```bash
# videos/ klasörüne git
cd videos

# Videoları listele
ls -lh *.mp4

# Video indirmek için (tarayıcıda açılır)
cat kibritci_kiz_video.mp4 | base64
```

### Daha Kolay: Google Drive Entegrasyonu

**Gelecek güncellemede eklenecek:**
- Worker otomatik olarak videoları Google Drive'a yükleyecek
- Siz sadece Drive'dan indireceksiniz

---

## 🔄 Otomatik Güncellemeler

Render.com **otomatik deploy** özelliği aktif:

1. Local'de kod değiştirin
2. `git push` yapın
3. Render.com otomatik günceller (2-3 dakika)

### Manuel Deploy:

Dashboard'da **"Manual Deploy"** → **"Deploy latest commit"**

---

## 💰 Maliyet

### Render.com (Ücretsiz Plan):
- ✅ 750 saat/ay (31 gün x 24 saat = 744 saat)
- ✅ Yeterli! 7/24 çalışabilir

### API Maliyetleri:
- OpenAI TTS: ~$0.50/hikaye
- Replicate FLUX: ~$0.015/hikaye
- **Toplam: ~$0.52/hikaye**

### 10 Hikaye/Ay:
- Render.com: **$0** (ücretsiz)
- API'ler: **~$5.20**
- **Toplam: ~$5.20/ay**

---

## ⚠️ Sorun Giderme

### "Worker durdu" hatası:
- Logları kontrol edin
- API anahtarları doğru mu?
- Environment Variables eksiksiz mi?

### "Deployment failed" hatası:
- `requirements.txt` dosyası GitHub'da mı?
- Python sürümü uyumlu mu? (3.11)

### "No stories found" uyarısı:
- `stories/` klasörü boş
- Shell'den yeni hikaye ekleyin

### Worker sürekli restart oluyor:
- Logları inceleyin (hata mesajı var mı?)
- API rate limit aşıldı mı?
- `STORIES_CHECK_INTERVAL` değerini artırın (örn: 600)

---

## 🎉 Tamamlandı!

Artık sisteminiz **7/24 çalışıyor!**

1. ✅ GitHub'a hikaye (.txt) yükleyin
2. ✅ Render.com otomatik deploy eder
3. ✅ Worker hikayeyi işler
4. ✅ Video oluşur
5. ✅ Telegram'dan bildirim alırsınız

---

## 📚 Ek Kaynaklar

- Render.com Docs: https://render.com/docs
- GitHub Actions: https://docs.github.com/actions
- Telegram Bot API: https://core.telegram.org/bots/api

---

**Sorularınız için:** GitHub Issues kullanın

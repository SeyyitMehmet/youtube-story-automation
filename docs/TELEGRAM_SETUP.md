# 📱 Telegram Bot Kurulumu

Render.com'dan bildirim almak için Telegram botu oluşturun.

---

## 1️⃣ Telegram Bot Oluşturma

### Adım 1: BotFather ile Bot Oluşturun

1. Telegram'da **@BotFather** kullanıcısını açın
2. `/newbot` komutunu gönderin
3. Bot için isim girin: **YouTube Story Bot**
4. Bot için kullanıcı adı girin: **youtube_story_bot** (benzersiz olmalı)
5. BotFather size **API Token** verecek:
   ```
   123456789:ABCdefGHIjklMNOpqrsTUVwxyz
   ```
6. Bu token'ı **kaydedin!**

---

## 2️⃣ Chat ID Bulma

### Adım 2: Kendi Chat ID'nizi Öğrenin

1. Telegram'da **@userinfobot** kullanıcısını açın
2. **Herhangi bir mesaj** gönderin
3. Bot size **Chat ID**'nizi verecek:
   ```
   Your Chat ID: 987654321
   ```
4. Bu ID'yi **kaydedin!**

---

## 3️⃣ Render.com'a Ekleyin

Render.com Dashboard'da **Environment Variables** bölümüne ekleyin:

| Key | Value | Örnek |
|-----|-------|-------|
| `TELEGRAM_BOT_TOKEN` | BotFather'dan aldığınız token | `123456789:ABCdefGHI...` |
| `TELEGRAM_CHAT_ID` | userinfobot'tan aldığınız ID | `987654321` |

---

## 4️⃣ Test Edin

Worker başladığında Telegram'dan şu mesajı alacaksınız:

```
🚀 YouTube Story Worker Başlatıldı!

Hikaye klasörü izleniyor...
```

Her video bittiğinde:

```
✅ Video Hazır!

📝 Kibritçi Kız
📊 45.2 MB
🎬 5 sahne
⏱️ 12 dakika 34 saniye
```

---

## 🔕 Bildirimleri Kapatma

Eğer Telegram bildirimi istemiyorsanız:
- Render.com'dan `TELEGRAM_BOT_TOKEN` ve `TELEGRAM_CHAT_ID` değişkenlerini **silmeyin**
- Sadece **boş** bırakın
- Worker otomatik olarak bildirim göndermeyecek

---

## ⚠️ Sorun Giderme

### "Bot token geçersiz" hatası:
- Token'ı doğru kopyaladığınızdan emin olun
- Başında/sonunda boşluk olmamalı

### "Chat ID geçersiz" hatası:
- Chat ID sadece rakamlardan oluşmalı
- Tire (-) işareti olabilir: `-987654321`

### "Bildirim gelmiyor" hatası:
- Botunuzu **/start** komutuyla başlatın
- Bot size en az 1 kez mesaj göndermeli

---

**Artık her şey hazır!** 🎉

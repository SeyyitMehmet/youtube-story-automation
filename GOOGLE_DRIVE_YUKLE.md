# 📤 Google Drive'a Dosya Yükleme Rehberi

## 🎯 Amaç
Bilgisayarınızdaki proje dosyalarını Google Drive'a yükleyeceğiz.

---

## 📋 Adım Adım Talimatlar

### 1️⃣ Google Drive'ı Açın
1. Tarayıcınızda `https://drive.google.com` adresine gidin
2. Google hesabınızla giriş yapın
3. Ana ekranda olduğunuzdan emin olun

---

### 2️⃣ Ana Klasörü Oluşturun

**Yöntem 1: Sağ Tık Menüsü**
1. Boş bir alana **sağ tıklayın**
2. **"Yeni klasör"** seçin
3. Klasör adı: `YouTube_Automation` yazın
4. **"Oluştur"** butonuna tıklayın

**Yöntem 2: Sol Üst Buton**
1. Sol üstte **"Yeni"** butonuna tıklayın
2. **"Yeni klasör"** seçin
3. Klasör adı: `YouTube_Automation` yazın
4. **"Oluştur"** butonuna tıklayın

---

### 3️⃣ Alt Klasörleri Oluşturun

**YouTube_Automation klasörünün içine girin** (çift tık)

Şimdi 4 tane alt klasör oluşturun:

#### A) `src` klasörü
1. **Yeni klasör** → İsim: `src`
2. Klasörü açın
3. Bilgisayarınızdan bu dosyaları **SÜRÜKLE-BIRAK** yapın:
   - `c:\Users\sms\Desktop\aktif_pojeler\test_yotube\src\` klasöründeki TÜM dosyalar
   - ✅ `story_processor.py`
   - ✅ `openai_tts_generator.py`
   - ✅ `replicate_image_generator.py`
   - ✅ `video_creator.py`
   - ✅ `character_manager.py`
   - ✅ `deepseek_processor.py`
   - ✅ `image_generator.py`
   - ✅ `multi_image_generator.py`
   - ✅ `tts_generator.py`
   - ✅ `youtube_uploader.py`
   - ✅ `__init__.py`

#### B) `config` klasörü
1. Geri dönün (YouTube_Automation klasörüne)
2. **Yeni klasör** → İsim: `config`
3. Klasörü açın
4. Bilgisayarınızdan şunu yükleyin:
   - ✅ `c:\Users\sms\Desktop\aktif_pojeler\test_yotube\config\config.py`

#### C) `stories` klasörü
1. Geri dönün (YouTube_Automation klasörüne)
2. **Yeni klasör** → İsim: `stories`
3. Klasörü açın
4. **10 tane hikaye dosyası** hazırlayın ve buraya yükleyin:
   
   **Şu an elinizde var:**
   - ✅ `kibritci_kiz.txt`
   
   **9 tane daha hikaye ekleyin** (örnekler):
   - `kirmizi_baslikli_kiz.txt`
   - `uyuyan_guzel.txt`
   - `pamuk_prenses.txt`
   - `cinderella.txt`
   - `rapunzel.txt`
   - `alice_harikalar_diyarinda.txt`
   - `kurbaga_prens.txt`
   - `pinokyo.txt`
   - `hansel_gretel.txt`

#### D) `musics` klasörü
1. Geri dönün (YouTube_Automation klasörüne)
2. **Yeni klasör** → İsim: `musics`
3. Klasörü açın
4. Fon müziği dosyasını yükleyin:
   - Eğer varsa: `fon1.mp3`
   - Yoksa: Herhangi bir müzik dosyasını `fon1.mp3` olarak yeniden adlandırıp yükleyin

---

### 4️⃣ Kontrol Edin

YouTube_Automation klasörüne geri dönün ve şunu görmelisiniz:

```
📁 YouTube_Automation/
  ├─ 📁 src (11 dosya)
  ├─ 📁 config (1 dosya)
  ├─ 📁 stories (10 dosya)
  └─ 📁 musics (1 dosya)
```

Her klasörü tek tek açıp dosyaların yüklendiğini kontrol edin!

---

## 🎯 Hızlı Yükleme (Tüm Klasörü Bir Anda)

**Alternatif Yöntem:**

1. Bilgisayarınızda yeni bir klasör oluşturun:
   - Konum: Masaüstü
   - İsim: `YouTube_Automation`

2. İçine şu klasörleri kopyalayın:
   ```
   YouTube_Automation/
     ├─ src/     (test_yotube/src/ klasörünü kopyalayın)
     ├─ config/  (test_yotube/config/ klasörünü kopyalayın)
     ├─ stories/ (10 hikaye .txt dosyası ekleyin)
     └─ musics/  (fon1.mp3 ekleyin)
   ```

3. Tüm `YouTube_Automation` klasörünü Google Drive'a **sürükle-bırak** yapın!

4. Yükleme bitene kadar bekleyin (sağ altta ilerleme çubuğu görünür)

---

## ✅ Tamamlandı!

Artık Google Colab notebook'unu çalıştırabilirsiniz!

---

## 📸 Görsel Rehber (Adımlar)

### Sürükle-Bırak Nasıl Yapılır?

1. **Windows Gezgini**'ni açın (⊞ Win + E)
2. Şu konuma gidin: `c:\Users\sms\Desktop\aktif_pojeler\test_yotube\`
3. **Tarayıcıda** Google Drive'ı açın
4. **Pencereleri yan yana** koyun:
   - Sol taraf: Windows Gezgini
   - Sağ taraf: Google Drive (tarayıcı)
5. **Dosyayı tutun ve tarayıcıya sürükleyin**
6. **Bırakın** (yükleme otomatik başlar)

---

## 🆘 Sorun Giderme

### ❌ Dosya yüklenmiyor
- İnternet bağlantınızı kontrol edin
- Tarayıcıyı yenileyin (F5)
- Farklı tarayıcı deneyin (Chrome önerilir)

### ❌ Klasör ismi yanlış
- Klasöre sağ tık → **"Yeniden adlandır"**
- Tam olarak şöyle olmalı: `YouTube_Automation`
- Büyük/küçük harf önemli!

### ❌ Dosya eksik
- Her klasörü tek tek kontrol edin
- Eksik dosyaları tekrar yükleyin

---

**🎉 Hazırsınız! Şimdi Colab notebook'unu çalıştırabilirsiniz!**

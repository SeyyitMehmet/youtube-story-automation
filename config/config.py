import os
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

class Config:
    # DeepSeek API 
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
    
    # DeepSeek endpoints
    DEEPSEEK_CHAT_API_URL = "https://api.deepseek.com/v1/chat/completions"  # Hikaye analizi için
    DEEPSEEK_IMAGE_API_URL = "https://api.deepseek.com/v1/images/generations"  # Görsel üretimi için
    
    # AI analiz ayarları
    USE_AI_STORY_ANALYSIS = bool(DEEPSEEK_API_KEY)  # API key varsa AI kullan
    
    # OpenAI API
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    
    # Resim Üretimi API'leri
    HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY", "")
    REPLICATE_API_KEY = os.getenv("REPLICATE_API_KEY", "")
    
    # Resim üretimi ayarları (Replicate birincil - rate limit korumalı)
    IMAGE_API_PRIORITY = ["replicate", "pollinations", "placeholder"]
    USE_FREE_IMAGES_ONLY = False  # Replicate kullan
    
    # Replicate Rate Limit Ayarları ($5'dan az bakiye için)
    REPLICATE_RATE_LIMIT_DELAY = 12  # Her istek arasında 12 saniye bekle (6 istek/dakika için güvenli)
    REPLICATE_MAX_RETRIES = 5        # Maksimum 5 deneme
    
    # Karakter Tutarlılığı Ayarları (Hibrit Sistem)
    USE_IP_ADAPTER = False             # IP-Adapter şu an kullanılamıyor (model bulunamadı)
    IP_ADAPTER_STRENGTH = 0.85         # Karakter benzerlik gücü (0.0-1.0, yüksek = daha benzer)
    # Not: FLUX-2 Pro/Dev multi-reference desteği ile karakter tutarlılığı sağlanacak
    
    # YouTube API
    YOUTUBE_CLIENT_ID = os.getenv("YOUTUBE_CLIENT_ID", "")
    YOUTUBE_CLIENT_SECRET = os.getenv("YOUTUBE_CLIENT_SECRET", "")
    
    # TTS Ayarları
    TTS_ENGINE = "openai"  # "openai" (TTS-1 HD), "gtts" (ücretsiz), "pyttsx3" (offline)
    TTS_LANGUAGE = "tr"  # Türkçe
    TTS_SPEED = 150      # Konuşma hızı (gtts/pyttsx3 için)
    
    # OpenAI TTS-1 HD Ayarları
    OPENAI_TTS_VOICE = "nova"  # alloy, echo, fable, onyx, nova, shimmer
    OPENAI_TTS_SPEED = 1.0     # 0.25 - 4.0 arası (1.0 = normal)
    
    # Video Ayarları
    VIDEO_WIDTH = 1920
    VIDEO_HEIGHT = 1080
    VIDEO_FPS = 24
    VIDEO_DURATION_PER_SCENE = 5  # Her sahne için saniye
    
    # Dosya yolları
    STORIES_DIR = "stories"
    AUDIO_DIR = "audio"
    IMAGES_DIR = "images"
    VIDEOS_DIR = "videos"
    
    # Görsel üretimi ayarları
    IMAGE_STYLE = "cinematic, storytelling, fairy tale illustration"
    IMAGE_SIZE = "1920x1080"
    
    # YouTube upload ayarları
    YOUTUBE_TITLE_PREFIX = "Hikaye Anlatımı: "
    YOUTUBE_DESCRIPTION = """
    Bu video yapay zeka destekli hikaye anlatım sistemi ile oluşturulmuştur.
    
    📚 Hikaye: {story_title}
    🎨 Görseller: AI ile üretilmiştir
    🎤 Sesli anlatım: Türkçe TTS
    
    #hikaye #masallar #yapayزeka #storytelling
    """
    YOUTUBE_TAGS = ["hikaye", "masal", "çocuk hikayeleri", "Türkçe", "anlatım"]
    YOUTUBE_PRIVACY = "public"  # "private", "unlisted", "public"
import os
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

class Config:
    # ====================================================================
    # API ANAHTARLARI - .env dosyasından yüklenir
    # ====================================================================
    
    # DeepSeek API (Hikaye analizi için)
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
    
    # DeepSeek endpoints
    DEEPSEEK_CHAT_API_URL = "https://api.deepseek.com/v1/chat/completions"
    DEEPSEEK_IMAGE_API_URL = "https://api.deepseek.com/v1/images/generations"
    
    # AI analiz ayarları
    USE_AI_STORY_ANALYSIS = bool(DEEPSEEK_API_KEY)
    
    # OpenAI API (TTS için)
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    
    # Resim Üretimi API'leri
    HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY", "")
    REPLICATE_API_KEY = os.getenv("REPLICATE_API_KEY", "")
    
    # YouTube API
    YOUTUBE_CLIENT_ID = os.getenv("YOUTUBE_CLIENT_ID", "")
    YOUTUBE_CLIENT_SECRET = os.getenv("YOUTUBE_CLIENT_SECRET", "")
    
    # ====================================================================
    # UYGULAMA AYARLARI
    # ====================================================================
    
    # Resim üretimi ayarları
    IMAGE_API_PRIORITY = ["replicate", "pollinations", "placeholder"]
    USE_FREE_IMAGES_ONLY = False  # Replicate kullan
    
    # Replicate Rate Limit Ayarları
    REPLICATE_RATE_LIMIT_DELAY = 12  # Her istek arasında 12 saniye
    REPLICATE_MAX_RETRIES = 5
    
    # Karakter Tutarlılığı
    USE_IP_ADAPTER = False
    IP_ADAPTER_STRENGTH = 0.85
    
    # TTS Ayarları
    TTS_ENGINE = "openai"  # "openai", "gtts", "pyttsx3"
    TTS_LANGUAGE = "tr"
    TTS_SPEED = 150
    
    # OpenAI TTS-1 HD
    OPENAI_TTS_VOICE = "nova"  # alloy, echo, fable, onyx, nova, shimmer
    OPENAI_TTS_SPEED = 1.0     # 0.25 - 4.0
    
    # ====================================================================
    # KLASÖR YAPISI
    # ====================================================================
    
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    STORIES_DIR = os.path.join(BASE_DIR, "stories")
    AUDIO_DIR = os.path.join(BASE_DIR, "audio")
    IMAGES_DIR = os.path.join(BASE_DIR, "images")
    VIDEOS_DIR = os.path.join(BASE_DIR, "videos")
    MUSIC_DIR = os.path.join(BASE_DIR, "musics")
    
    # Video ayarları
    FPS = 24
    VIDEO_RESOLUTION = (1920, 1080)
    
    # Sahne süresi ayarları
    MIN_SCENE_DURATION = 3
    MAX_SCENE_DURATION = 15

"""
YouTube Story Automation System
AI destekli hikaye anlatım video üretimi
"""

__version__ = "1.0.0"
__author__ = "YouTube Story Automation"

from .story_processor import StoryProcessor
from .tts_generator import TTSGenerator
from .image_generator import ImageGenerator

try:
    from .video_creator import VideoCreator
    VIDEO_CREATOR_AVAILABLE = True
except ImportError:
    VIDEO_CREATOR_AVAILABLE = False
    print("⚠ VideoCreator modülü kullanılamaz (MoviePy kurulu değil)")

try:
    from .youtube_uploader import YouTubeUploader
    YOUTUBE_UPLOADER_AVAILABLE = True
except ImportError:
    YOUTUBE_UPLOADER_AVAILABLE = False
    print("⚠ YouTubeUploader modülü kullanılamaz")

__all__ = [
    'StoryProcessor',
    'TTSGenerator', 
    'ImageGenerator'
]

if VIDEO_CREATOR_AVAILABLE:
    __all__.append('VideoCreator')

if YOUTUBE_UPLOADER_AVAILABLE:
    __all__.append('YouTubeUploader')
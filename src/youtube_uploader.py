"""
YouTube yükleme modülü
YouTube API ile video yükleme
"""
import os
import json
from typing import Dict, Optional
import tempfile

# YouTube API imports (kurulduğunda çalışacak)
try:
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    from googleapiclient.http import MediaFileUpload
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    YOUTUBE_API_AVAILABLE = True
except ImportError:
    YOUTUBE_API_AVAILABLE = False
    print("⚠ YouTube API kütüphaneleri bulunamadı. pip install -r requirements.txt çalıştırın.")

class YouTubeUploader:
    def __init__(self, client_id: str = "", client_secret: str = "", 
                 credentials_file: str = "youtube_credentials.json"):
        self.client_id = client_id
        self.client_secret = client_secret
        self.credentials_file = credentials_file
        self.youtube_service = None
        
        # YouTube API scope'ları
        self.scopes = ['https://www.googleapis.com/auth/youtube.upload']
        
        if not YOUTUBE_API_AVAILABLE:
            print("❌ YouTube API kullanılamaz. Önce gerekli kütüphaneleri kurun.")
    
    def authenticate(self) -> bool:
        """YouTube API ile kimlik doğrulama"""
        if not YOUTUBE_API_AVAILABLE:
            return False
        
        try:
            creds = None
            
            # Mevcut token'ı kontrol et
            if os.path.exists(self.credentials_file):
                creds = Credentials.from_authorized_user_file(
                    self.credentials_file, self.scopes
                )
            
            # Token yoksa veya geçersizse yenile
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    # OAuth2 akışı
                    if not self.client_id or not self.client_secret:
                        print("❌ YouTube API credentials tanımlanmamış!")
                        print("Google Cloud Console'dan OAuth2 credentials alın:")
                        print("1. https://console.cloud.google.com/ adresine gidin")
                        print("2. YouTube Data API v3'ü etkinleştirin")
                        print("3. OAuth2 credentials oluşturun")
                        print("4. client_id ve client_secret'i config.py'ye ekleyin")
                        return False
                    
                    # Geçici client secrets dosyası oluştur
                    client_config = {
                        "installed": {
                            "client_id": self.client_id,
                            "client_secret": self.client_secret,
                            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                            "token_uri": "https://oauth2.googleapis.com/token",
                            "redirect_uris": ["http://localhost"]
                        }
                    }
                    
                    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                        json.dump(client_config, f)
                        temp_file = f.name
                    
                    try:
                        flow = InstalledAppFlow.from_client_secrets_file(
                            temp_file, self.scopes
                        )
                        creds = flow.run_local_server(port=0)
                    finally:
                        os.unlink(temp_file)
                
                # Credentials'ı kaydet
                with open(self.credentials_file, 'w') as token:
                    token.write(creds.to_json())
            
            # YouTube service oluştur
            self.youtube_service = build('youtube', 'v3', credentials=creds)
            print("✓ YouTube API kimlik doğrulaması başarılı")
            return True
            
        except Exception as e:
            print(f"❌ YouTube kimlik doğrulama hatası: {e}")
            return False
    
    def upload_video(self, video_path: str, title: str, description: str = "",
                    tags: list = None, privacy: str = "private") -> Optional[str]:
        """YouTube'a video yükler"""
        
        if not YOUTUBE_API_AVAILABLE:
            print("❌ YouTube API kullanılamaz")
            return None
        
        if not self.youtube_service:
            if not self.authenticate():
                return None
        
        if not os.path.exists(video_path):
            print(f"❌ Video dosyası bulunamadı: {video_path}")
            return None
        
        try:
            # Video metadata
            body = {
                'snippet': {
                    'title': title,
                    'description': description,
                    'tags': tags or [],
                    'categoryId': '24'  # Entertainment category
                },
                'status': {
                    'privacyStatus': privacy,
                    'selfDeclaredMadeForKids': False
                }
            }
            
            # Video dosyasını yükle
            print(f"📤 YouTube'a yükleniyor: {title}")
            print(f"📁 Dosya: {video_path}")
            print(f"🔒 Gizlilik: {privacy}")
            
            media = MediaFileUpload(
                video_path,
                chunksize=-1,  # Tek seferde yükle
                resumable=True,
                mimetype='video/mp4'
            )
            
            # Upload request
            request = self.youtube_service.videos().insert(
                part=','.join(body.keys()),
                body=body,
                media_body=media
            )
            
            response = None
            while response is None:
                try:
                    status, response = request.next_chunk()
                    if status:
                        print(f"📊 Yükleme durumu: {int(status.progress() * 100)}%")
                except HttpError as e:
                    if e.resp.status in [500, 502, 503, 504]:
                        # Yeniden denenebilir hatalar
                        print(f"⚠ Geçici hata, yeniden deneniyor: {e}")
                        continue
                    else:
                        raise
            
            if 'id' in response:
                video_id = response['id']
                video_url = f"https://www.youtube.com/watch?v={video_id}"
                print(f"✅ Video başarıyla yüklendi!")
                print(f"🔗 URL: {video_url}")
                print(f"🆔 Video ID: {video_id}")
                
                return video_url
            else:
                print(f"❌ Yükleme başarısız: {response}")
                return None
                
        except HttpError as e:
            print(f"❌ YouTube API hatası: {e}")
            return None
        except Exception as e:
            print(f"❌ Video yükleme hatası: {e}")
            return None
    
    def update_video_info(self, video_id: str, title: str = None, 
                         description: str = None, tags: list = None) -> bool:
        """Yüklenmiş videonun bilgilerini günceller"""
        
        if not self.youtube_service:
            if not self.authenticate():
                return False
        
        try:
            # Mevcut video bilgilerini al
            video_response = self.youtube_service.videos().list(
                part='snippet',
                id=video_id
            ).execute()
            
            if not video_response['items']:
                print(f"❌ Video bulunamadı: {video_id}")
                return False
            
            # Güncellenecek bilgileri hazırla
            snippet = video_response['items'][0]['snippet']
            
            if title:
                snippet['title'] = title
            if description:
                snippet['description'] = description
            if tags:
                snippet['tags'] = tags
            
            # Güncelleme request'i
            update_request = self.youtube_service.videos().update(
                part='snippet',
                body={
                    'id': video_id,
                    'snippet': snippet
                }
            )
            
            update_request.execute()
            print(f"✓ Video bilgileri güncellendi: {video_id}")
            return True
            
        except Exception as e:
            print(f"❌ Video güncelleme hatası: {e}")
            return False
    
    def get_upload_quota(self) -> Dict[str, any]:
        """YouTube API quota bilgilerini döndürür"""
        quota_info = {
            'daily_upload_limit': '6 saat video',
            'api_quota_limit': '10,000 units/gün',
            'upload_cost': '1600 units per video',
            'max_videos_per_day': '~6 video',
            'note': 'Quota limitleri hesap türüne göre değişebilir'
        }
        return quota_info
    
    def create_playlist(self, title: str, description: str = "", 
                       privacy: str = "private") -> Optional[str]:
        """YouTube'da playlist oluşturur"""
        
        if not self.youtube_service:
            if not self.authenticate():
                return None
        
        try:
            body = {
                'snippet': {
                    'title': title,
                    'description': description
                },
                'status': {
                    'privacyStatus': privacy
                }
            }
            
            request = self.youtube_service.playlists().insert(
                part=','.join(body.keys()),
                body=body
            )
            
            response = request.execute()
            playlist_id = response['id']
            
            print(f"✓ Playlist oluşturuldu: {title}")
            print(f"🆔 Playlist ID: {playlist_id}")
            
            return playlist_id
            
        except Exception as e:
            print(f"❌ Playlist oluşturma hatası: {e}")
            return None
    
    def add_video_to_playlist(self, playlist_id: str, video_id: str) -> bool:
        """Videoyu playlist'e ekler"""
        
        if not self.youtube_service:
            if not self.authenticate():
                return False
        
        try:
            body = {
                'snippet': {
                    'playlistId': playlist_id,
                    'resourceId': {
                        'kind': 'youtube#video',
                        'videoId': video_id
                    }
                }
            }
            
            request = self.youtube_service.playlistItems().insert(
                part='snippet',
                body=body
            )
            
            request.execute()
            print(f"✓ Video playlist'e eklendi: {video_id}")
            return True
            
        except Exception as e:
            print(f"❌ Playlist'e ekleme hatası: {e}")
            return False
    
    def test_api_connection(self) -> bool:
        """YouTube API bağlantısını test eder"""
        if not YOUTUBE_API_AVAILABLE:
            print("❌ YouTube API kütüphaneleri kurulmamış")
            return False
        
        if not self.authenticate():
            return False
        
        try:
            # Basit bir API çağrısı yap
            request = self.youtube_service.channels().list(
                part='snippet',
                mine=True
            )
            response = request.execute()
            
            if response.get('items'):
                channel_name = response['items'][0]['snippet']['title']
                print(f"✓ YouTube API bağlantısı başarılı")
                print(f"📺 Kanal: {channel_name}")
                return True
            else:
                print("❌ YouTube kanalı bulunamadı")
                return False
                
        except Exception as e:
            print(f"❌ YouTube API test hatası: {e}")
            return False
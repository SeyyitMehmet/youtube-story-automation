"""
🚀 Google Drive için Klasör Hazırlama

Bu script, Google Drive'a yüklenecek dosyaları hazırlar.
Masaüstünde 'YouTube_Automation' klasörü oluşturur.
"""

import os
import shutil
from pathlib import Path

# Renkli çıktı için
try:
    from colorama import init, Fore, Style
    init()
    GREEN = Fore.GREEN
    RED = Fore.RED
    YELLOW = Fore.YELLOW
    BLUE = Fore.BLUE
    RESET = Style.RESET_ALL
except:
    GREEN = RED = YELLOW = BLUE = RESET = ""

def create_colab_folder():
    """Google Drive için klasör yapısını oluştur"""
    
    print(f"\n{BLUE}{'='*70}{RESET}")
    print(f"{BLUE}🚀 Google Drive Klasör Hazırlama{RESET}")
    print(f"{BLUE}{'='*70}{RESET}\n")
    
    # Masaüstü yolu
    desktop = Path.home() / "Desktop"
    output_folder = desktop / "YouTube_Automation"
    
    # Mevcut proje klasörü
    project_root = Path(__file__).parent
    
    print(f"📂 Kaynak klasör: {project_root}")
    print(f"📦 Hedef klasör: {output_folder}\n")
    
    # Eski klasörü sil
    if output_folder.exists():
        print(f"{YELLOW}⚠️  Eski klasör bulundu, siliniyor...{RESET}")
        shutil.rmtree(output_folder)
    
    # Yeni klasör oluştur
    output_folder.mkdir(exist_ok=True)
    print(f"{GREEN}✓ Ana klasör oluşturuldu{RESET}\n")
    
    # Alt klasörler
    folders_to_create = {
        'src': project_root / 'src',
        'config': project_root / 'config',
        'stories': project_root / 'stories',
        'musics': project_root / 'musics'
    }
    
    stats = {
        'total': 0,
        'success': 0,
        'failed': 0
    }
    
    for folder_name, source_path in folders_to_create.items():
        dest_path = output_folder / folder_name
        
        print(f"📁 {folder_name:12} → ", end="")
        
        if source_path.exists():
            # Klasörü kopyala
            shutil.copytree(source_path, dest_path)
            
            # Dosya sayısını hesapla
            file_count = len([f for f in dest_path.rglob('*') if f.is_file()])
            stats['total'] += file_count
            stats['success'] += 1
            
            print(f"{GREEN}✓ {file_count} dosya kopyalandı{RESET}")
        else:
            print(f"{RED}✗ Kaynak klasör bulunamadı!{RESET}")
            stats['failed'] += 1
            
            # Boş klasör oluştur
            dest_path.mkdir(exist_ok=True)
            print(f"{YELLOW}  → Boş klasör oluşturuldu (manuel yükleme gerekli){RESET}")
    
    print(f"\n{BLUE}{'='*70}{RESET}")
    print(f"{GREEN}✅ HAZIR!{RESET}\n")
    print(f"📊 İstatistikler:")
    print(f"   - Toplam dosya: {stats['total']}")
    print(f"   - Başarılı klasör: {stats['success']}")
    print(f"   - Eksik klasör: {stats['failed']}")
    
    print(f"\n{BLUE}{'='*70}{RESET}")
    print(f"{YELLOW}📝 SONRAKI ADIMLAR:{RESET}\n")
    print(f"1. Masaüstündeki '{output_folder.name}' klasörünü açın")
    print(f"2. Eksik dosyaları manuel ekleyin:")
    
    # Eksik klasörleri kontrol et
    stories_count = len(list((output_folder / 'stories').glob('*.txt')))
    music_count = len(list((output_folder / 'musics').glob('*.mp3')))
    
    if stories_count < 10:
        print(f"   {RED}✗ stories/ → {10 - stories_count} hikaye daha ekleyin (.txt dosyası){RESET}")
    else:
        print(f"   {GREEN}✓ stories/ → {stories_count} hikaye hazır{RESET}")
    
    if music_count == 0:
        print(f"   {RED}✗ musics/ → fon1.mp3 müzik dosyası ekleyin{RESET}")
    else:
        print(f"   {GREEN}✓ musics/ → {music_count} müzik dosyası hazır{RESET}")
    
    print(f"\n3. TÜM '{output_folder.name}' klasörünü Google Drive'a yükleyin:")
    print(f"   → drive.google.com adresine gidin")
    print(f"   → Klasörü tarayıcıya sürükle-bırak yapın")
    print(f"   → MyDrive klasörünün içine yerleştirin")
    
    print(f"\n4. Google Colab notebook'unu açın ve çalıştırın!")
    
    print(f"\n{BLUE}{'='*70}{RESET}\n")
    
    # Klasörü aç
    try:
        os.startfile(output_folder)
        print(f"{GREEN}✓ Klasör otomatik açıldı!{RESET}\n")
    except:
        print(f"{YELLOW}⚠️  Klasörü manuel açın: {output_folder}{RESET}\n")

if __name__ == "__main__":
    try:
        create_colab_folder()
    except Exception as e:
        print(f"\n{RED}❌ HATA: {str(e)}{RESET}\n")
        import traceback
        traceback.print_exc()

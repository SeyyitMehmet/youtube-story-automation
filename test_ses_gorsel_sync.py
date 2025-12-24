#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ses-Görsel Senkronizasyon Test Scripti
Video'larınızda ses ve görsel süreleri kontrol eder
"""

import os
from pathlib import Path
from moviepy import VideoFileClip

def analyze_video_sync(video_path):
    """Bir videodaki sahne senkronizasyonunu analiz eder"""
    print(f"\n{'='*70}")
    print(f"🎬 Video Analizi: {Path(video_path).name}")
    print(f"{'='*70}\n")
    
    try:
        video = VideoFileClip(video_path)
        
        # Video bilgileri
        print(f"📊 GENEL BİLGİLER:")
        print(f"   ⏱️  Toplam Süre: {video.duration:.2f} saniye")
        print(f"   📏 Çözünürlük: {video.size[0]}x{video.size[1]}")
        print(f"   🎞️  FPS: {video.fps}")
        print(f"   🔊 Ses: {'Var ✅' if video.audio else 'Yok ❌'}")
        
        if video.audio:
            audio_duration = video.audio.duration
            video_duration = video.duration
            
            print(f"\n🎯 SENKRONIZASYON KONTROLÜ:")
            print(f"   Görsel Süresi: {video_duration:.2f}s")
            print(f"   Ses Süresi:    {audio_duration:.2f}s")
            
            diff = abs(video_duration - audio_duration)
            
            if diff < 0.1:
                print(f"   ✅ MÜKEMMEL! Fark: {diff:.3f}s (ihmal edilebilir)")
            elif diff < 0.5:
                print(f"   ✅ İYİ! Fark: {diff:.3f}s (kabul edilebilir)")
            elif diff < 1.0:
                print(f"   ⚠️  UYARI! Fark: {diff:.3f}s (fark edilebilir)")
            else:
                print(f"   ❌ PROBLEM! Fark: {diff:.3f}s (büyük uyumsuzluk)")
            
            # Senkronizasyon durumu
            sync_percentage = min(audio_duration, video_duration) / max(audio_duration, video_duration) * 100
            print(f"   📊 Senkronizasyon: %{sync_percentage:.1f}")
        
        video.close()
        print(f"\n{'='*70}\n")
        
    except Exception as e:
        print(f"❌ Hata: {e}\n")

def analyze_all_videos(videos_dir="videos"):
    """Tüm videoları analiz eder"""
    videos_path = Path(videos_dir)
    
    if not videos_path.exists():
        print(f"❌ '{videos_dir}' klasörü bulunamadı!")
        return
    
    video_files = list(videos_path.glob("*.mp4"))
    
    if not video_files:
        print(f"⚠️  '{videos_dir}' klasöründe hiç MP4 dosyası bulunamadı!")
        return
    
    print(f"\n{'='*70}")
    print(f"🔍 TOPLU VİDEO ANALİZİ")
    print(f"{'='*70}")
    print(f"📂 Klasör: {videos_dir}")
    print(f"📊 Toplam Video: {len(video_files)}")
    print(f"{'='*70}")
    
    results = []
    
    for video_file in sorted(video_files):
        analyze_video_sync(str(video_file))
        
        # Kısa rapor için bilgi topla
        try:
            video = VideoFileClip(str(video_file))
            if video.audio:
                diff = abs(video.duration - video.audio.duration)
                status = "✅" if diff < 0.5 else "⚠️" if diff < 1.0 else "❌"
                results.append({
                    'name': video_file.name,
                    'duration': video.duration,
                    'diff': diff,
                    'status': status
                })
            video.close()
        except:
            pass
    
    # Özet rapor
    if results:
        print(f"\n{'='*70}")
        print(f"📋 ÖZET RAPOR")
        print(f"{'='*70}\n")
        print(f"{'Durum':<6} {'Video':<30} {'Süre':<10} {'Uyumsuzluk'}")
        print(f"{'-'*70}")
        
        for r in results:
            print(f"{r['status']:<6} {r['name']:<30} {r['duration']:>6.1f}s   {r['diff']:>6.3f}s")
        
        # İstatistikler
        perfect = sum(1 for r in results if r['diff'] < 0.1)
        good = sum(1 for r in results if 0.1 <= r['diff'] < 0.5)
        warning = sum(1 for r in results if 0.5 <= r['diff'] < 1.0)
        problem = sum(1 for r in results if r['diff'] >= 1.0)
        
        print(f"\n{'='*70}")
        print(f"📊 İSTATİSTİKLER:")
        print(f"   ✅ Mükemmel (< 0.1s): {perfect}")
        print(f"   ✅ İyi (0.1-0.5s):    {good}")
        print(f"   ⚠️  Uyarı (0.5-1.0s):  {warning}")
        print(f"   ❌ Problem (> 1.0s):  {problem}")
        print(f"{'='*70}\n")

if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║        🎬 Ses-Görsel Senkronizasyon Test Aracı 🎬          ║
║                                                              ║
║  Video'larınızdaki ses ve görsel senkronizasyonunu          ║
║  kontrol eder ve raporlar                                   ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
""")
    
    # Tek bir video analizi için:
    # analyze_video_sync("videos/Kibritci_Kiz.mp4")
    
    # Tüm videolar için:
    analyze_all_videos("videos")

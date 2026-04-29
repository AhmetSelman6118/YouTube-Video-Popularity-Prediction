from api_handler import search_videos, get_bulk_video_details
import pandas as pd
import json
import os

def collect_diverse_data(keyword_list, max_per_keyword=50):
    """
    Verilen kelime listesi üzerinden arama yapar, mükerrer verileri temizler ve kaydeder.
    """
    all_video_data = []
    seen_ids = set() # Daha önce eklenen videoları takip etmek için

    print(f"🚀 Toplam {len(keyword_list)} farklı konu başlığı için veri toplama başlatıldı...")

    for query in keyword_list:
        print(f"🔍 '{query}' için aramalar çekiliyor...")
        try:
            # 1. Video ID'lerini bul
            video_ids = search_videos(query, max_results=max_per_keyword)

            # 2. Daha önce listede olmayan ID'leri ayıkla (Mükerrer veri kontrolü)
            new_ids = [vid for vid in video_ids if vid not in seen_ids]
            
            if not new_ids:
                print(f"ℹ️ '{query}' için yeni video bulunamadı (hepsi zaten listede).")
                continue
                
            # 3. Detayları çek
            raw_data = get_bulk_video_details(new_ids)
            
            all_video_data.extend(raw_data)
            seen_ids.update(new_ids) # Eklenen ID'leri kümeye ekle
            
            print(f"✅ '{query}' için {len(raw_data)} yeni video eklendi.")
            
        except Exception as e:
            print(f"⚠️ '{query}' araması sırasında bir pürüz çıktı: {e}")

    # 4. Klasör kontrolü
    os.makedirs("data/raw", exist_ok=True)

    # 5. Kaydetme işlemleri
    if all_video_data:
        # JSON Kayıt
        with open("data/raw/youtube_data.json", "w", encoding="utf-8") as f:
            json.dump(all_video_data, f, ensure_ascii=False, indent=4)
        
        # CSV Kayıt (Pandas)
        df = pd.DataFrame(all_video_data)
        df.to_csv("data/raw/youtube_data.csv", index=False, encoding="utf-8-sig")
        
        print("\n" + "="*40)
        print(f"📊 ÖZET: Toplam {len(df)} benzersiz video verisi başarıyla toplandı.")
        print(f"📂 Dosya Yolu: data/raw/youtube_data.csv")
        print("="*40)
    else:
        print("❌ Hiç veri toplanamadı. API anahtarını veya internetini kontrol etmelisin.")

if __name__ == "__main__":
    # Örnek Konu Listesi (Bunları projenin odağına göre değiştirebilirsin)
    target_keywords = [
        # AI & Future Tech
        "Generative AI Trends 2026", "Artificial General Intelligence News", 
        "Neurallink Brain Chip Update", "Humanoid Robots Boston Dynamics",
        "Autonomous Driving Tesla FSD", "Quantum Computing Breakthrough",
        
        # Coding & Software
        "Python 3.14 New Features", "Rust vs C++ Performance", 
        "Full Stack Developer Roadmap 2026", "Cyber Security Ethical Hacking",
        "Microservices Architecture Tutorial", "Cloud Native Engineering",
        
        # Science & Innovation
        "SpaceX Mars Mission Update", "James Webb Telescope Discoveries",
        "Nuclear Fusion Energy Progress", "Genetic Engineering CRISPR",
        "Renewable Energy Solutions 2026",
        
        # Gaming & Digital Trends
        "GTA VI Official Trailer News", "Unreal Engine 5.5 Tech Demo",
        "Virtual Reality Metaverse Gaming", "E-sports World Cup Highlights",
        
        # Business & Lifestyle
        "Stock Market Analysis AI Tech", "Cryptocurrency Future Outlook",
        "Minimalist Home Office Setup", "Smart City Infrastructure 2026"
    ]
    
    # 10 kelime x 50 video = Maksimum 500 video hedefi
    collect_diverse_data(target_keywords, max_per_keyword=50)
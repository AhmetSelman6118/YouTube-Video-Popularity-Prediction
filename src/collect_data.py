from api_handler import search_videos, get_bulk_video_details
import pandas as pd
import json
import os

def save_dataset(query, count=50):
    print(f"{query}' konusu için veri toplama başlatıldı...")
    
    video_ids = search_videos(query, max_results=count)
    
    raw_data = get_bulk_video_details(video_ids)
    
    os.makedirs("data/raw", exist_ok=True)
    
    with open("data/raw/youtube_data.json", "w", encoding="utf-8") as f:
        json.dump(raw_data, f, ensure_ascii=False, indent=4)
    print("JSON kaydedildi: data/raw/youtube_data.json")
    
    df = pd.DataFrame(raw_data)
    df.to_csv("data/raw/youtube_data.csv", index=False, encoding="utf-8-sig")
    print("CSV kaydedildi: data/raw/youtube_data.csv")
    
    print(f"\nToplam {len(df)} video verisi başarıyla depolandı.")

if __name__ == "__main__":
    save_dataset(query="Machine Learning Tutorial", count=50)
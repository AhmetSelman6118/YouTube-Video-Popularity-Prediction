import re
from src.api_handler import get_video_details

def extract_video_id(url):
    """
    YouTube linkinden Video ID'sini çıkaran Regex fonksiyonu.
    Desteklenen formatlar: youtube.com, youtu.be, youtube.com/embed/ vb.
    """
    pattern = r'(?:v=|\/)([0-9A-Za-z_-]{11}).*'
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    return None

def main():
    print("=== YouTube Video Bilgi Getirici ===")
    user_input = input("Lütfen YouTube video linkini yapıştırın: ")
    
    video_id = extract_video_id(user_input)
    
    if not video_id:
        print("❌ Hata: Geçerli bir YouTube ID'si bulunamadı. Lütfen linki kontrol edin.")
        return

    print(f"🔍 Video ID tespit edildi: {video_id}")
    print("⏳ Veriler API'den çekiliyor...")

    try:
        data = get_video_details(video_id)
        
        if data:
            print("\n" + "="*30)
            print(f"📌 BAŞLIK: {data['title']}")
            print(f"👁️ İZLENME: {int(data['views']):,}") # Binlik ayırıcı ekler
            print(f"👍 BEĞENİ: {int(data['likes']):,}")
            print(f"💬 YORUM : {int(data['comments']):,}")
            print(f"📅 TARİH : {data['published_at']}")
            print("="*30)
        else:
            print("❌ Video bulunamadı veya gizli.")

    except Exception as e:
        print(f"⚠️ Bir hata oluştu: {e}")

if __name__ == "__main__":
    main()
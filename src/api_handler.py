import os
import pandas as pd
import json
from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()

def get_youtube_client():
    api_key = os.getenv("YOUTUBE_API_KEY")
    return build("youtube", "v3", developerKey=api_key)

def search_videos(query, max_results=50):
    """
    Belirli bir kelimeyle arama yapar ve Video ID'lerini döndürür.
    """
    youtube = get_youtube_client()
    request = youtube.search().list(
        q=query,
        part="id",
        type="video",
        maxResults=max_results
    )
    response = request.execute()
    
    video_ids = [item['id']['videoId'] for item in response.get('items', [])]
    return video_ids

def get_video_details(video_id):
    """
    Tek bir video ID'sine göre detayları getirir. (main.py için gerekli)
    """
    youtube = get_youtube_client()
    request = youtube.videos().list(
        part="snippet,statistics",
        id=video_id
    )
    response = request.execute()

    if not response['items']:
        return None

    video_data = response['items'][0]
    return {
        "title": video_data['snippet']['title'],
        "views": video_data['statistics'].get('viewCount', 0),
        "likes": video_data['statistics'].get('likeCount', 0),
        "comments": video_data['statistics'].get('commentCount', 0),
        "published_at": video_data['snippet']['publishedAt']
    }

def get_bulk_video_details(video_ids):
    """
    Video ID'lerini alır; hem video istatistiklerini hem de 
    ilgili kanalın bilgilerini çekip birleştirir.
    """
    youtube = get_youtube_client()
    
    # 1. Adım: Videoların temel detaylarını ve istatistiklerini çek
    video_request = youtube.videos().list(
        part="snippet,statistics,contentDetails",
        id=",".join(video_ids)
    )
    video_response = video_request.execute()
    
    # 2. Adım: Bu videolara ait benzersiz Kanal ID'lerini listele
    # (Set kullanarak aynı kanalın bilgilerini tekrar tekrar istemiyoruz - Kota dostu!)
    channel_ids = list(set([item['snippet']['channelId'] for item in video_response.get('items', [])]))
    
    # 3. Adım: Kanalların abone ve toplam izlenme sayılarını çek (Toplu sorgu)
    channel_request = youtube.channels().list(
        part="statistics",
        id=",".join(channel_ids)
    )
    channel_response = channel_request.execute()
    
    # Kanal bilgilerini hızlıca bulabilmek için bir sözlük (map) oluşturalım
    channels_map = {
        item['id']: {
            "channel_subscribers": int(item['statistics'].get('subscriberCount', 0)),
            "channel_total_views": int(item['statistics'].get('viewCount', 0)),
            "channel_total_videos": int(item['statistics'].get('videoCount', 0))
        } for item in channel_response.get('items', [])
    }
    
    # 4. Adım: Video verileriyle kanal verilerini harmanla
    all_video_data = []
    for item in video_response.get('items', []):
        c_id = item['snippet']['channelId']
        # Kanala dair verileri al, bulamazsan varsayılan 0 ata
        c_stats = channels_map.get(c_id, {
            "channel_subscribers": 0, 
            "channel_total_views": 0, 
            "channel_total_videos": 0
        })
        
        data = {
            "video_id": item['id'],
            "title": item['snippet']['title'],
            "published_at": item['snippet']['publishedAt'],
            "category_id": item['snippet']['categoryId'],
            "duration": item['contentDetails']['duration'],
            "view_count": int(item['statistics'].get('viewCount', 0)),
            "like_count": int(item['statistics'].get('likeCount', 0)),
            "comment_count": int(item['statistics'].get('commentCount', 0)),
            # Kanal bilgileri yeni sütunlar olarak ekleniyor
            "channel_subscribers": c_stats["channel_subscribers"],
            "channel_total_views": c_stats["channel_total_views"],
            "channel_total_videos": c_stats["channel_total_videos"]
        }
        all_video_data.append(data)
    
    return all_video_data
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
    ID listesi verilen videoların detaylarını toplu halde çeker.
    """
    youtube = get_youtube_client()
    
    request = youtube.videos().list(
        part="snippet,statistics,contentDetails",
        id=",".join(video_ids)
    )
    response = request.execute()
    
    all_video_data = []
    for item in response.get('items', []):
        data = {
            "video_id": item['id'],
            "title": item['snippet']['title'],
            "published_at": item['snippet']['publishedAt'],
            "category_id": item['snippet']['categoryId'],
            "duration": item['contentDetails']['duration'],
            # BURASI KRİTİK: API'den gelen isimler viewCount, likeCount, commentCount şeklindedir.
            "view_count": int(item['statistics'].get('viewCount', 0)),
            "like_count": int(item['statistics'].get('likeCount', 0)),
            "comment_count": int(item['statistics'].get('commentCount', 0))
        }
        all_video_data.append(data)
    
    return all_video_data
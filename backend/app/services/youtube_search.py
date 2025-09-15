from googleapiclient.discovery import build
import os
from openai import OpenAI
from typing import List, Dict
import re
from datetime import datetime, timedelta

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY) if YOUTUBE_API_KEY and YOUTUBE_API_KEY != "your_youtube_api_key_here" else None

# Initialize OpenAI client only if API key is available
openai_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_key) if openai_key and openai_key != "your_openai_api_key_here" else None

async def search_youtube_influencers(query: str, max_results: int = 20) -> List[Dict]:
    """
    Search for YouTube channels based on query
    """
    try:
        if not youtube or not YOUTUBE_API_KEY or YOUTUBE_API_KEY == "your_youtube_api_key_here":
            print("YouTube API key not configured, returning mock data")
            return get_mock_influencers(query, max_results)
            
        request = youtube.search().list(
            part="snippet",
            type="channel",
            q=query,
            maxResults=max_results,
            order="relevance"
        )
        response = request.execute()
        
        results = []
        for item in response.get("items", []):
            results.append({
                "channel_id": item["snippet"]["channelId"],
                "name": item["snippet"]["channelTitle"],
                "description": item["snippet"]["description"],
                "thumbnail": item["snippet"]["thumbnails"].get("default", {}).get("url", "")
            })
        return results
    except Exception as e:
        print(f"YouTube search error: {e}")
        print("Falling back to mock data")
        return get_mock_influencers(query, max_results)

def get_mock_influencers(query: str, max_results: int) -> List[Dict]:
    """
    Return mock influencer data for demo purposes
    """
    mock_influencers = [
        {
            "channel_id": "UC_x5XG1OV2P6uZZ5FSM9Ttw",
            "name": "Tech Reviewer Pro",
            "description": "Professional tech reviews and gadget unboxings",
            "thumbnail": "https://via.placeholder.com/88x88/3B82F6/FFFFFF?text=TR"
        },
        {
            "channel_id": "UCBJycsmduvYEL83R_U4JriQ",
            "name": "Gadget Guru",
            "description": "Latest tech news, reviews, and tutorials",
            "thumbnail": "https://via.placeholder.com/88x88/10B981/FFFFFF?text=GG"
        },
        {
            "channel_id": "UCuAXFkgsw1L7xaCfnd5JJOw",
            "name": "Tech Unboxed",
            "description": "Unboxing and reviewing the latest technology products",
            "thumbnail": "https://via.placeholder.com/88x88/F59E0B/FFFFFF?text=TU"
        },
        {
            "channel_id": "UCBJycsmduvYEL83R_U4JriQ",
            "name": "Electronics Expert",
            "description": "In-depth electronics reviews and comparisons",
            "thumbnail": "https://via.placeholder.com/88x88/EF4444/FFFFFF?text=EE"
        },
        {
            "channel_id": "UC_x5XG1OV2P6uZZ5FSM9Ttw",
            "name": "Tech Lifestyle",
            "description": "How technology integrates into daily life",
            "thumbnail": "https://via.placeholder.com/88x88/8B5CF6/FFFFFF?text=TL"
        }
    ]
    
    return mock_influencers[:max_results]

async def analyze_influencer(channel_id: str) -> Dict:
    """
    Comprehensive analysis of a YouTube influencer
    """
    try:
        # Check if we're using mock data
        if not youtube or not YOUTUBE_API_KEY or YOUTUBE_API_KEY == "your_youtube_api_key_here":
            return get_mock_influencer_analysis(channel_id)
        
        # Get channel statistics
        channel_stats = get_channel_statistics(channel_id)
        if not channel_stats:
            return get_mock_influencer_analysis(channel_id)
        
        # Get recent videos for content analysis
        recent_videos = get_recent_videos(channel_id, max_results=10)
        
        # Analyze content categories and engagement
        content_analysis = analyze_content_categories(recent_videos)
        
        # Calculate engagement rate
        engagement_rate = calculate_engagement_rate(channel_stats, recent_videos)
        
        # Estimate CPM based on channel size and category
        cpm = estimate_cpm(channel_stats['subscriber_count'], content_analysis['categories'])
        
        # Analyze audience demographics using AI
        demographics = await analyze_audience_demographics(channel_stats, recent_videos)
        
        return {
            'name': channel_stats.get('title', ''),
            'title': channel_stats.get('title', ''),
            'description': channel_stats.get('description', ''),
            'subscriber_count': channel_stats.get('subscriber_count', 0),
            'view_count': channel_stats.get('view_count', 0),
            'video_count': channel_stats.get('video_count', 0),
            'avg_views': calculate_avg_views(recent_videos),
            'engagement_rate': engagement_rate,
            'cpm': cpm,
            'categories': content_analysis['categories'],
            'content_themes': content_analysis['themes'],
            'demographics': demographics,
            'upload_frequency': calculate_upload_frequency(recent_videos),
            'last_upload': get_last_upload_date(recent_videos)
        }
        
    except Exception as e:
        print(f"Influencer analysis error: {e}")
        return get_mock_influencer_analysis(channel_id)

def get_mock_influencer_analysis(channel_id: str) -> Dict:
    """
    Return mock influencer analysis data for demo purposes
    """
    import random
    
    # Generate realistic mock data
    subscriber_count = random.randint(10000, 1000000)
    avg_views = random.randint(5000, subscriber_count // 2)
    engagement_rate = random.uniform(0.02, 0.08)
    cpm = random.uniform(10, 25)
    
    categories = random.sample([
        'Technology', 'Gaming', 'Lifestyle', 'Beauty & Fashion', 
        'Food & Cooking', 'Health & Fitness'
    ], random.randint(1, 3))
    
    demographics = {
        "age_range": random.choice(["18-24", "25-34", "35-44", "45-54"]),
        "gender": random.choice(["Male", "Female", "Mixed"]),
        "interests": random.sample([
            "Technology", "Gaming", "Fashion", "Fitness", "Cooking", "Travel"
        ], random.randint(2, 4)),
        "income_level": random.choice(["Low", "Middle", "High"]),
        "location": random.choice(["US", "Europe", "Global"])
    }
    
    return {
        'name': f"Mock Influencer {channel_id[-4:]}",
        'title': f"Tech Channel {channel_id[-4:]}",
        'description': f"Professional tech reviews and gadget unboxings",
        'subscriber_count': subscriber_count,
        'view_count': subscriber_count * random.randint(5, 20),
        'video_count': random.randint(50, 500),
        'avg_views': avg_views,
        'engagement_rate': engagement_rate,
        'cpm': round(cpm, 2),
        'categories': categories,
        'content_themes': ['Reviews', 'Unboxing', 'Tutorials'],
        'demographics': demographics,
        'upload_frequency': random.choice(['Weekly', 'Bi-weekly', 'Daily']),
        'last_upload': '2024-01-15T10:30:00Z'
    }

def get_channel_statistics(channel_id: str) -> Dict:
    """Get basic channel statistics"""
    try:
        request = youtube.channels().list(
            part="statistics,snippet",
            id=channel_id
        )
        response = request.execute()
        
        if not response.get("items"):
            return {}
        
        item = response["items"][0]
        stats = item["statistics"]
        snippet = item["snippet"]
        
        return {
            'title': snippet.get('title', ''),
            'description': snippet.get('description', ''),
            'subscriber_count': int(stats.get('subscriberCount', 0)),
            'view_count': int(stats.get('viewCount', 0)),
            'video_count': int(stats.get('videoCount', 0))
        }
    except Exception as e:
        print(f"Channel stats error: {e}")
        return {}

def get_recent_videos(channel_id: str, max_results: int = 10) -> List[Dict]:
    """Get recent videos from channel"""
    try:
        # First, get the uploads playlist ID
        request = youtube.channels().list(
            part="contentDetails",
            id=channel_id
        )
        response = request.execute()
        
        if not response.get("items"):
            return []
        
        uploads_playlist_id = response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
        
        # Get videos from uploads playlist
        request = youtube.playlistItems().list(
            part="snippet,contentDetails",
            playlistId=uploads_playlist_id,
            maxResults=max_results
        )
        response = request.execute()
        
        videos = []
        for item in response.get("items", []):
            video_id = item["contentDetails"]["videoId"]
            snippet = item["snippet"]
            
            # Get video statistics
            video_stats = get_video_statistics(video_id)
            
            videos.append({
                'video_id': video_id,
                'title': snippet.get('title', ''),
                'description': snippet.get('description', ''),
                'published_at': snippet.get('publishedAt', ''),
                'view_count': video_stats.get('view_count', 0),
                'like_count': video_stats.get('like_count', 0),
                'comment_count': video_stats.get('comment_count', 0)
            })
        
        return videos
    except Exception as e:
        print(f"Recent videos error: {e}")
        return []

def get_video_statistics(video_id: str) -> Dict:
    """Get statistics for a specific video"""
    try:
        request = youtube.videos().list(
            part="statistics",
            id=video_id
        )
        response = request.execute()
        
        if not response.get("items"):
            return {}
        
        stats = response["items"][0]["statistics"]
        return {
            'view_count': int(stats.get('viewCount', 0)),
            'like_count': int(stats.get('likeCount', 0)),
            'comment_count': int(stats.get('commentCount', 0))
        }
    except Exception as e:
        print(f"Video stats error: {e}")
        return {}

def analyze_content_categories(videos: List[Dict]) -> Dict:
    """Analyze video content to determine categories and themes"""
    if not videos:
        return {'categories': [], 'themes': []}
    
    # Extract keywords from video titles and descriptions
    all_text = " ".join([v['title'] + " " + v['description'] for v in videos])
    
    # Simple keyword extraction (in a real implementation, you'd use more sophisticated NLP)
    keywords = re.findall(r'\b\w+\b', all_text.lower())
    
    # Common content categories
    categories = []
    themes = []
    
    # Technology
    if any(word in keywords for word in ['tech', 'review', 'unboxing', 'gadget', 'phone', 'laptop']):
        categories.append('Technology')
    
    # Beauty/Fashion
    if any(word in keywords for word in ['beauty', 'makeup', 'fashion', 'style', 'skincare']):
        categories.append('Beauty & Fashion')
    
    # Gaming
    if any(word in keywords for word in ['gaming', 'game', 'play', 'stream', 'gamer']):
        categories.append('Gaming')
    
    # Lifestyle
    if any(word in keywords for word in ['lifestyle', 'daily', 'vlog', 'life', 'routine']):
        categories.append('Lifestyle')
    
    # Food
    if any(word in keywords for word in ['food', 'cooking', 'recipe', 'restaurant', 'eat']):
        categories.append('Food & Cooking')
    
    return {
        'categories': categories if categories else ['General'],
        'themes': themes
    }

def calculate_engagement_rate(channel_stats: Dict, videos: List[Dict]) -> float:
    """Calculate average engagement rate from recent videos"""
    if not videos:
        return 0.0
    
    total_engagement = 0
    valid_videos = 0
    
    for video in videos:
        if video['view_count'] > 0:
            likes = video.get('like_count', 0)
            comments = video.get('comment_count', 0)
            engagement = (likes + comments) / video['view_count']
            total_engagement += engagement
            valid_videos += 1
    
    return total_engagement / valid_videos if valid_videos > 0 else 0.0

def calculate_avg_views(videos: List[Dict]) -> int:
    """Calculate average views per video"""
    if not videos:
        return 0
    
    total_views = sum(video['view_count'] for video in videos)
    return total_views // len(videos)

def estimate_cpm(subscriber_count: int, categories: List[str]) -> float:
    """Estimate CPM based on channel size and content category"""
    base_cpm = 15.0
    
    # Adjust based on subscriber count
    if subscriber_count > 1000000:  # 1M+
        base_cpm *= 1.5
    elif subscriber_count > 100000:  # 100K+
        base_cpm *= 1.2
    elif subscriber_count < 10000:  # <10K
        base_cpm *= 0.7
    
    # Adjust based on category
    if 'Technology' in categories:
        base_cpm *= 1.3
    elif 'Beauty & Fashion' in categories:
        base_cpm *= 1.1
    elif 'Gaming' in categories:
        base_cpm *= 0.9
    
    return round(base_cpm, 2)

def calculate_upload_frequency(videos: List[Dict]) -> str:
    """Calculate how often the channel uploads"""
    if len(videos) < 2:
        return "Unknown"
    
    # Calculate days between uploads
    dates = [datetime.fromisoformat(v['published_at'].replace('Z', '+00:00')) for v in videos]
    dates.sort(reverse=True)
    
    if len(dates) < 2:
        return "Unknown"
    
    avg_days = (dates[0] - dates[-1]).days / (len(dates) - 1)
    
    if avg_days < 1:
        return "Daily"
    elif avg_days < 7:
        return "Multiple times per week"
    elif avg_days < 14:
        return "Weekly"
    elif avg_days < 30:
        return "Bi-weekly"
    else:
        return "Monthly"

def get_last_upload_date(videos: List[Dict]) -> str:
    """Get the date of the last upload"""
    if not videos:
        return "Unknown"
    
    return videos[0].get('published_at', 'Unknown')

async def analyze_audience_demographics(channel_stats: Dict, videos: List[Dict]) -> Dict:
    """Use AI to analyze audience demographics based on content"""
    try:
        # Create a summary of content for AI analysis
        content_summary = f"Channel: {channel_stats.get('title', '')}\n"
        content_summary += f"Description: {channel_stats.get('description', '')}\n"
        content_summary += f"Recent video titles: {', '.join([v['title'] for v in videos[:5]])}\n"
        
        prompt = f"""
        Analyze this YouTube channel's content and estimate the audience demographics. Return a JSON response with:
        
        {{
            "age_range": "Primary age group (e.g., 18-24, 25-34, 35-44, etc.)",
            "gender": "Primary gender (e.g., Male, Female, Mixed)",
            "interests": ["interest1", "interest2", "interest3"],
            "income_level": "Estimated income level (e.g., Low, Middle, High)",
            "location": "Primary geographic location (e.g., US, Europe, Global)"
        }}
        
        Channel content:
        {content_summary}
        """
        
        if not client:
            return {
                "age_range": "25-34",
                "gender": "Mixed",
                "interests": ["Technology", "Gaming", "Lifestyle"],
                "income_level": "Middle",
                "location": "Global"
            }
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert in audience analysis and demographics. Analyze the provided YouTube channel content and estimate the audience demographics. Always return valid JSON format."
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        
        import json
        result = json.loads(response.choices[0].message.content)
        return result
        
    except Exception as e:
        print(f"Demographics analysis error: {e}")
        return {
            "age_range": "Unknown",
            "gender": "Unknown", 
            "interests": [],
            "income_level": "Unknown",
            "location": "Unknown"
        }

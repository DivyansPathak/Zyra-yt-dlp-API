import yt_dlp
from yt_dlp.utils import DownloadError
from typing import Dict, Any, Optional

def fetch_stream_data(url: str) -> Dict[str, Any]:
    """
    Extracts all video information for a given YouTube URL using yt-dlp.
    """
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            return ydl.extract_info(url, download=False)
    except (DownloadError, Exception) as e:
        print(f"An error occurred while fetching stream data: {e}")
        raise

def parse_stream_url(info: Dict[str, Any]) -> Optional[str]:
    """
    Parses the extracted video info to find the best audio-only stream URL.
    """
    if 'url' in info:
        return info['url']
    
    for f in info.get('formats', []):
        
        if f.get('acodec') != 'none' and f.get('vcodec') == 'none':
            return f.get('url')
            
    return None
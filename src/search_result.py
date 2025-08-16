from typing import List, Dict, Any
import yt_dlp
from yt_dlp.utils import DownloadError
from schema.ouput_schema import SongSearchResult

def fetch_youtube_data(query: str) -> List[Dict[str, Any]]:
    """
    Handles the logic of searching YouTube using yt-dlp.
    It's responsible for one thing: getting raw data from the source.
    """
    ydl_opts = {
        'noplaylist': True,
        'quiet': True,
        'default_search': 'ytsearch1',
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(query, download=False)
           
            return result.get('entries', [])
    except (DownloadError, Exception) as e:

        print(f"An error occurred while fetching from YouTube: {e}")
        raise

def parse_search_results(entries: List[Dict[str, Any]]) -> List[SongSearchResult]:
    """
    Handles the logic of transforming the raw YouTube data into our desired format.
    This function doesn't know where the data came from; it just knows how to parse it.
    """
    parsed_list = []
    for entry in entries:
        if entry:
            parsed_list.append(
                SongSearchResult(
                    name=entry.get('title', 'N/A'),
                    artist_name=entry.get('uploader', 'N/A'),
                    url=f"https://www.youtube.com/watch?v={entry.get('id')}",
                    thumbnail=entry.get('thumbnail', ''),
                    duration=int(entry.get('duration', 0))
                )
            )
    return parsed_list
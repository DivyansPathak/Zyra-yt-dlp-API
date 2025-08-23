from typing import List, Dict, Any
import yt_dlp
from yt_dlp.utils import DownloadError
from schema.ouput_schema import SongSearchResult
import json

def fetch_youtube_data(query: str) -> List[Dict[str, Any]]:
    """
    Handles the logic of searching YouTube using yt-dlp.
    It's responsible for one thing: getting raw data from the source.
    """
    search_query = f"ytsearch5:{query}"
    ydl_opts = {
        'noplaylist': True,
        'quiet': True,
        # 'default_search': 'ytsearch5',
        # 'skip_download': True,
        'extract_flat' : True,
        'force_generic_extractor': True
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(search_query, download=False)
            # print("--- Raw Data from yt-dlp ---")
            # print(json.dumps(result, indent=2))
            # print("----------------------------")
            return result.get('entries', [])
    except (DownloadError, Exception) as e:

        print(f"An error occurred while fetching from YouTube: {e}")
        raise

def parse_search_results(entries: List[Dict[str, Any]]) -> List[SongSearchResult]:
    """
    Handles the logic of transforming the raw YouTube data into our desired format.
    """
    parsed_list = []
    for entry in entries:
        # If the entry is invalid or empty, skip it.
        if not entry:
            continue

        # Now, process the valid entry.
        # Safely get duration: check if it exists before converting to int
        duration_val = entry.get('duration')
        duration_int = int(duration_val) if duration_val is not None else None

        # Safely get thumbnail: thumbnails is a list, so we take the last one (usually highest quality)
        thumbnail_url = None
        if entry.get('thumbnails'):
            thumbnail_url = entry['thumbnails'][-1]['url']

        # Append the parsed result to the list
        parsed_list.append(
            SongSearchResult(
                name=entry.get('title', 'N/A'),
                artist_name=entry.get('uploader', 'N/A'),
                url=f"https://www.youtube.com/watch?v={entry.get('id')}",
                thumbnail=thumbnail_url,
                duration=duration_int
            )
        )
    return parsed_list
from typing import List, Dict, Any
import yt_dlp
from yt_dlp.utils import DownloadError
from schema.ouput_schema import SongSearchResult
import json


def fetch_youtube_data(queries: List[str]) -> List[Dict[str, Any]]:
    """
    Handles searching YouTube for a list of queries using yt-dlp.
    It aggregates the results from all queries into a single list.
    
    Args:
        queries (List[str]): A list of song titles or search terms.

    Returns:
        List[Dict[str, Any]]: A combined list of raw 'entries' from all searches.
    """
    ydl_opts = {
        'noplaylist': True,
        'quiet': True,
        'extract_flat': True,
        'force_generic_extractor': True
    }
    
    all_entries = []
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            for query in queries:
                search_query = f"ytsearch1:{query}"
                result = ydl.extract_info(search_query, download=False)
                
                if result and 'entries' in result:
                    all_entries.extend(result.get('entries', []))
                    
    except (DownloadError, Exception) as e:
        print(f"An error occurred while fetching from YouTube: {e}")
        raise
        
    print("Finished fetching all data.")
    return all_entries

def parse_search_results(entries: List[Dict[str, Any]]) -> List[SongSearchResult]:
    """
    Transforms the raw YouTube data from multiple searches into a clean,
    structured list of SongSearchResult objects.
    (This function remains unchanged as it's already designed to process a list).
    """
    parsed_list = []
    for entry in entries:
        if not entry:
            continue

        duration_val = entry.get('duration')
        duration_int = int(duration_val) if duration_val is not None else None

        thumbnail_url = None
        if entry.get('thumbnails'):
            thumbnail_url = entry['thumbnails'][-1]['url']

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

def search_multiple_songs(queries: List[str]) -> List[SongSearchResult]:
    """
    A wrapper function that orchestrates the process:
    1. Fetches raw data for a list of queries.
    2. Parses the combined raw data into a structured list.
    """
    raw_entries = fetch_youtube_data(queries)
    parsed_results = parse_search_results(raw_entries)
    return parsed_results

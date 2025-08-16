import pandas as pd
from fastapi import FastAPI, HTTPException
from typing import List
from schema.ouput_schema import *
from src.search_result import fetch_youtube_data, parse_search_results
from src.stream_data import fetch_stream_data, parse_stream_url

from yt_dlp.utils import DownloadError

app = FastAPI(
    title="Music Streaming API",
    description="An API for searching, streaming, and getting song recommendations.",
    version="1.3.0",
)


@app.get("/search", response_model=List[SongSearchResult])
async def search_song(query: str):
    """
    The main endpoint, now simplified to orchestrate calls to the service layer.
    """
    if not query:
        raise HTTPException(status_code=400, detail="A search query is required.")

    try:
        raw_youtube_entries = fetch_youtube_data(query)

        search_results = parse_search_results(raw_youtube_entries)
        
        return search_results

    except DownloadError:
        raise HTTPException(
            status_code=503, 
            detail="Service is unable to fetch data from YouTube. This may be due to network issues or API changes. Please try again later."
        )
    except Exception:
        raise HTTPException(status_code=500, detail="An internal server error occurred.")


@app.get("/stream", response_model=StreamInfo)
async def get_stream_url(url: str):
    """
    The main stream endpoint, orchestrating calls to the service layer.
    """
    if not url:
        raise HTTPException(status_code=400, detail="A YouTube video URL is required.")

    try:
        video_info = fetch_stream_data(url)

        audio_url = parse_stream_url(video_info)
        
        if audio_url:
            return StreamInfo(stream_url=audio_url)
        else:
            raise HTTPException(status_code=404, detail="Could not find a valid audio-only stream.")

    except DownloadError:
        raise HTTPException(status_code=503, detail="Failed to get stream URL from YouTube.")
    except Exception:
        raise HTTPException(status_code=500, detail="An internal server error occurred while fetching the stream.")
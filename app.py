import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

# For interacting with YouTube
import yt_dlp
from yt_dlp.utils import DownloadError

# For the recommendation engine
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# --- Pydantic Models ---
class SongSearchResult(BaseModel):
    name: str
    artist_name: str
    url: str
    thumbnail: str
    duration: int

class StreamInfo(BaseModel):
    stream_url: str

class SongFeatures(BaseModel):
    track_name: str
    artist_name: str
    genre: str

class RecommendedSong(BaseModel):
    track_name: str
    artist_name: str
    genre: str

# --- App Initialization ---
app = FastAPI(
    title="Music Streaming API",
    description="An API for searching, streaming, and getting song recommendations.",
    version="1.3.0",
)

# --- Recommendation Engine Globals ---
dataframe = None
cosine_sim_matrix = None

# --- Startup Event ---
@app.on_event("startup")
async def load_and_process_data():
    global dataframe, cosine_sim_matrix
    try:
        dataframe = pd.read_csv("songs_dataset.csv")
        dataframe = dataframe.drop_duplicates(subset='track_name')
        dataframe['genre'] = dataframe['genre'].fillna('')
        dataframe['artist_name'] = dataframe['artist_name'].fillna('')
        dataframe['features'] = dataframe['artist_name'] + ' ' + dataframe['genre']
        tfidf_vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf_vectorizer.fit_transform(dataframe['features'])
        cosine_sim_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)
        print("--- Recommendation engine data loaded successfully. ---")
    except FileNotFoundError:
        print("--- WARNING: 'songs_dataset.csv' not found. Recommendation endpoint will not work. ---")
    except Exception as e:
        print(f"--- ERROR loading data: {e} ---")


# --- API Endpoints ---

@app.get("/search", response_model=List[SongSearchResult])
async def search_song(query: str):
    if not query:
        raise HTTPException(status_code=400, detail="A search query is required.")

    # Changed from 'ytsearch5' to 'ytsearch1' to get only the top result.
    ydl_opts = {
        'noplaylist': True,
        'quiet': True,
        'default_search': 'ytsearch1',
        'extract_flat': 'in_playlist'
    }
    
    search_results = []
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(query, download=False)
            if 'entries' in result:
                for entry in result.get('entries', []):
                    search_results.append(
                        SongSearchResult(
                            name=entry.get('title', 'N/A'),
                            artist_name=entry.get('uploader', 'N/A'),
                            url=f"https://www.youtube.com/watch?v={entry.get('id')}",
                            thumbnail=entry.get('thumbnail', ''),
                            duration=int(entry.get('duration', 0))
                        )
                    )
    except DownloadError as e:
        print(f"YT-DLP DownloadError: {e}")
        raise HTTPException(
            status_code=503, 
            detail="Service is unable to fetch data from YouTube. This may be due to network issues or API changes. Please try again later."
        )
    except Exception as e:
        print(f"Generic Error: {e}")
        raise HTTPException(status_code=500, detail="An internal server error occurred.")

    return search_results

@app.get("/stream", response_model=StreamInfo)
async def get_stream_url(url: str):
    if not url:
        raise HTTPException(status_code=400, detail="A YouTube video URL is required.")

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            audio_url = None
            if 'url' in info:
                audio_url = info['url']
            else:
                for f in info.get('formats', []):
                    if f.get('acodec') != 'none' and f.get('vcodec') == 'none':
                        audio_url = f.get('url')
                        break
            
            if audio_url:
                return StreamInfo(stream_url=audio_url)
            else:
                raise HTTPException(status_code=404, detail="Could not find a valid audio-only stream.")

    except DownloadError as e:
        print(f"YT-DLP DownloadError on stream: {e}")
        raise HTTPException(status_code=503, detail="Failed to get stream URL from YouTube.")
    except Exception as e:
        print(f"Generic Error on stream: {e}")
        raise HTTPException(status_code=500, detail="An internal server error occurred while fetching the stream.")



# --- Pydantic Models ---
# This model defines the structure of each recommended song
class Song(BaseModel):
    name: str
    artist_name: str
    url: str
    thumbnail: str
    duration: int

# This model defines the expected input for the recommendation request
class RecommendationRequest(BaseModel):
    url: str


# --- Recommendation Endpoint ---
@app.post("/recommend", response_model=List[Song])
async def recommend_songs(request: RecommendationRequest):
    """
    Gets YouTube's "Up Next" list for a given video URL.
    This acts as our recommendation engine.
    """
    ydl_opts = {
        'quiet': True,
        'extract_flat': True, # We only need metadata, not full format info
        'playlistend': 16     # Get the video itself + 15 recommendations
    }

    recommendations = []
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # When you pass a single video URL, yt-dlp can extract the "Up Next" playlist
            result = ydl.extract_info(request.url, download=False)
            
            # The first entry is the original video, so we skip it using [1:]
            for entry in result.get('entries', [])[1:]:
                recommendations.append(
                    Song(
                        name=entry.get('title', 'N/A'),
                        artist_name=entry.get('uploader', 'N/A'),
                        url=f"https://www.youtube.com/watch?v={entry.get('id')}",
                        thumbnail=entry.get('thumbnail', ''),
                        duration=int(entry.get('duration', 0))
                    )
                )
    except DownloadError:
        raise HTTPException(status_code=503, detail="Could not fetch recommendations from YouTube.")
    except Exception:
        raise HTTPException(status_code=500, detail="An internal error occurred.")
        
    return recommendations
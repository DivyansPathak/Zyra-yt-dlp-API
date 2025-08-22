from pydantic import BaseModel
from typing import Optional

class SongSearchResult(BaseModel):
    name: str
    artist_name: str
    url: str
    thumbnail: Optional[str] = None
    duration: Optional[int]  = None

class StreamInfo(BaseModel):
    stream_url: str
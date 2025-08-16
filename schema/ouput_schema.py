from pydantic import BaseModel

class SongSearchResult(BaseModel):
    name: str
    artist_name: str
    url: str
    thumbnail: str
    duration: int

class StreamInfo(BaseModel):
    stream_url: str
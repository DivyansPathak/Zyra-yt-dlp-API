from pydantic import BaseModel
from typing import List

class SearchRequest(BaseModel):
    queries: List[str]
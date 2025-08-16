Here's an attractive and dynamic `README.md` file generated based on the provided project context:

---

# 🎵 MelodyStream API: Seamless Music Search & Streaming

[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111.0-009688.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/shiwangupadhyay/MelodyStream-API?style=social)](https://github.com/shiwangupadhyay/MelodyStream-API) <!-- Placeholder, assuming a GitHub repo -->

A powerful FastAPI application providing endpoints for searching YouTube music, extracting streamable audio URLs, and laying the groundwork for future song recommendations.

---

## 🚀 Key Features

*   **YouTube Music Search:** Effortlessly search for songs and retrieve comprehensive metadata including name, artist, YouTube URL, thumbnail, and duration.
*   **Direct Audio Stream Extraction:** Obtain direct, audio-only stream URLs for YouTube videos, perfect for integration into music players or services.
*   **Robust Error Handling:** Implements comprehensive error handling for network issues, invalid queries, and scenarios where streams are unavailable.
*   **Clean & Modular Architecture:** Designed with a clear separation of concerns, distinguishing between API endpoints, data fetching, and data parsing logic for maintainability and scalability.
*   **Pydantic Models:** Leverages Pydantic for strict data validation and clear, auto-generated API response schemas, ensuring reliable data exchange.
*   **FastAPI Powered:** Built on FastAPI, offering high performance, asynchronous capabilities, and automatic interactive API documentation (Swagger UI/ReDoc).

---

## 📂 Project Structure

```
.
├── app.py                      # Main FastAPI application entry point and API routes
├── LICENSE                     # Project licensing information (MIT License)
├── README.md                   # Project README file (You are here!)
├── requirements.txt            # Python dependencies
├── schema/                     # Pydantic data models for API input/output
│   ├── ouput_schema.py         # Defines SongSearchResult and StreamInfo models
│   └── __init__.py             # Initializes the schema package
└── src/                        # Core logic for data fetching and parsing
    ├── search_result.py        # Handles YouTube search data fetching and parsing
    ├── stream_data.py          # Handles YouTube stream URL extraction
    └── __init__.py             # Initializes the src package
```

---

## 🛠️ Technologies Used

This project is built using:

*   **Python 3.9+**
*   **FastAPI** - A modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints.
*   **Uvicorn** - An ASGI server for running asynchronous Python web applications.
*   **`yt-dlp`** - A powerful command-line program to download videos from YouTube.com and other video sites, used here for metadata extraction and stream URL discovery.
*   **Pydantic** - Data validation and settings management using Python type hints, ensuring robust API responses.
*   **Pandas** - (Included in `requirements.txt`) A powerful data manipulation and analysis library, though not extensively used in the core API logic provided, it's part of the environment.
*   **scikit-learn** - (Included in `requirements.txt`) A machine learning library, indicating potential future expansions for recommendation features as mentioned in the API description.

---

## ⚙️ Installation

To get this project up and running locally, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/shiwangupadhyay/MelodyStream-API.git # Replace with actual repo URL
    cd MelodyStream-API
    ```

2.  **Create and activate a virtual environment** (recommended):
    ```bash
    python -m venv venv
    # On macOS/Linux:
    source venv/bin/activate
    # On Windows:
    .\venv\Scripts\activate
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

---

## 🚀 Usage

Once the dependencies are installed, you can run the FastAPI application using Uvicorn:

```bash
uvicorn app:app --reload
```

This command will start the development server. You can then access the API at:

*   **API Documentation (Swagger UI):** `http://127.0.0.1:8000/docs`
*   **Alternative API Documentation (ReDoc):** `http://127.0.0.1:8000/redoc`

---

## 🌐 API Endpoints

The API exposes the following endpoints:

### 1. `GET /search`

Searches YouTube for songs based on a query and returns structured results.

*   **Description:** The main endpoint for searching music. It orchestrates calls to the service layer to fetch and parse YouTube data.
*   **Query Parameters:**
    *   `query` (string, **required**): The search term for the song or artist (e.g., `"Never Gonna Give You Up"`).
*   **Response Model:** `List[SongSearchResult]`

    ```python
    class SongSearchResult(BaseModel):
        name: str
        artist_name: str
        url: str
        thumbnail: str
        duration: int # Duration in seconds
    ```

*   **Example Request:**
    ```
    GET http://127.0.0.1:8000/search?query=bohemian%20rhapsody
    ```
*   **Example Success Response (200 OK):**
    ```json
    [
      {
        "name": "Queen – Bohemian Rhapsody (Official Video Remastered)",
        "artist_name": "Queen Official",
        "url": "https://www.youtube.com/watch?v=fJ9rUzIMcZQ",
        "thumbnail": "https://i.ytimg.com/vi/fJ9rUzIMcZQ/hq720.jpg",
        "duration": 355
      }
      // ... more results
    ]
    ```
*   **Example Error Response (400 Bad Request):**
    ```json
    {
      "detail": "A search query is required."
    }
    ```

### 2. `GET /stream`

Extracts a direct audio-only stream URL for a given YouTube video URL.

*   **Description:** Retrieves the streamable audio URL for a specified YouTube video.
*   **Query Parameters:**
    *   `url` (string, **required**): The full YouTube video URL (e.g., `https://www.youtube.com/watch?v=dQw4w9WgXcQ`).
*   **Response Model:** `StreamInfo`

    ```python
    class StreamInfo(BaseModel):
        stream_url: str
    ```

*   **Example Request:**
    ```
    GET http://127.0.0.1:8000/stream?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ
    ```
*   **Example Success Response (200 OK):**
    ```json
    {
      "stream_url": "https://rr2---sn-a5meknsz.googlevideo.com/videoplayback?expire=..."
    }
    ```
*   **Example Error Response (404 Not Found):**
    ```json
    {
      "detail": "Could not find a valid audio-only stream."
    }
    ```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
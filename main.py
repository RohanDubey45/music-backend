from fastapi import FastAPI
from yt_dlp import YoutubeDL
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow all origins (for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/search")
def search_music(query: str):
    try:
        search_term = f"ytsearch1:{query}"

        ydl_opts = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'quiet': True,
            'skip_download': True,
            'cachedir': False,
            'forcejson': True,
        }

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(search_term, download=False)

            if not info or 'entries' not in info or not info['entries']:
                return {"error": "No results found"}

            result = info['entries'][0]

        return {
            'title': result.get('title'),
            'url': result.get('url'),
            'thumbnail': result.get('thumbnail'),
            'webpage_url': result.get('webpage_url')
        }

    except Exception as e:
        return {"error": str(e)}

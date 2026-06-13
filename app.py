import os
import re
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from google import genai
from youtube_transcript_api import YouTubeTranscriptApi
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class VideoRequest(BaseModel):
    url: str

@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    try:
        with open("index.html", "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return "<h3>Error: index.html file not found in the project folder.</h3>"

def get_youtube_transcript(video_url):
    regex_pattern = r"(?:v=|\/shorts\/|\/embed\/|\/v\/|youtu\.be\/|\/watch\?v=|\&v=)([^#\&\?]*)"
    match = re.search(regex_pattern, video_url)
    if match and len(match.group(1)) == 11:
        video_id = match.group(1)
    else:
        raise ValueError("Invalid YouTube URL ID pattern.")

    print(f"Fetching transcript for video ID: {video_id}...")
    
    try:
        # The official, robust way to pass cookies in the library
        if os.path.exists("cookies.txt"):
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id, cookies="cookies.txt")
        else:
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            
        # Dynamically grab the first available transcript (handles any language automatically)
        data = None
        for transcript in transcript_list:
            data = transcript.fetch()
            break
            
        if not data:
            raise ValueError("No transcripts found for this video.")
            
        # Safely handle both dictionary and object formats depending on your exact library version
        try:
            return " ".join([segment['text'] for segment in data])
        except TypeError:
            return " ".join([segment.text for segment in data])
            
    except Exception as e:
        raise ValueError(f"Transcript extraction failed. Error: {str(e)}")

@app.post("/api/generate-notes")
async def generate_notes_endpoint(request: VideoRequest):
    if not os.getenv("GEMINI_API_KEY"):
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY missing on server. Check your .env file.")
    
    try:
        transcript_text = get_youtube_transcript(request.url)
        
        client = genai.Client()
        system_instruction = """
        You are an elite technical summary assistant. I will provide a transcript from a YouTube video. 
        Your goal is to extract the absolute core value of the video with zero fluff, zero introductory filler, and no repetitive sentences.
        Structure your notes clearly using Markdown headers (##), bold text, and clean bullet points.
        """
        
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"{system_instruction}\n\nTranscript:\n{transcript_text}"
        )
        return {"notes": response.text}
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

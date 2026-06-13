import os
import re
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from google import genai
from youtube_transcript_api import YouTubeTranscriptApi

app = FastAPI()

# Allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class VideoRequest(BaseModel):
    url: str

# Render needs this route to serve your web page!
@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    try:
        with open("index.html", "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return "<h3>Error: index.html file not found.</h3>"

def get_youtube_transcript(video_url):
    regex_pattern = r"(?:v=|\/shorts\/|\/embed\/|\/v\/|youtu\.be\/|\/watch\?v=|\&v=)([^#\&\?]*)"
    match = re.search(regex_pattern, video_url)
    if match and len(match.group(1)) == 11:
        video_id = match.group(1)
    else:
        raise ValueError("Invalid YouTube URL ID pattern.")

    ytt_api = YouTubeTranscriptApi()
    transcript_list = ytt_api.fetch(video_id)
    return " ".join([segment.text for segment in transcript_list])

# The main API endpoint
@app.post("/api/generate-notes")
async def generate_notes_endpoint(request: VideoRequest):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="API Key missing in Render Environment Variables.")
    
    try:
        transcript_text = get_youtube_transcript(request.url)
        
        client = genai.Client(api_key=api_key)
        system_instruction = """
        You are an elite technical summary assistant. I will provide a transcript from a YouTube video. 
        Your goal is to extract the absolute core value of the video with zero fluff.
        Structure your notes clearly using Markdown headers (##), bold text, and clean bullet points.
        """
        
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"{system_instruction}\n\nTranscript:\n{transcript_text}"
        )
        return {"notes": response.text}
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
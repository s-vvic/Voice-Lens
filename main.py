# main.py

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os

# create FastAPI app instance
app = FastAPI(title="Voice-Lens API")

# cors settings(it will be restricted later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins for now(can be restricted later)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# temporary upload directory
UPLOAD_DIR = "temp_images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
async def read_root():
    return {"message": "Voice-Lens API is running!"}

@app.post("/analyze")
async def analyze_image(file: UploadFile = File(...)):
    """
    [for team member C]
    You can send an image file to this endpoint,
    and it will return the analyzed text and audio(later).
    """
    try:
        # 1. save the uploaded file temporarily
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # ---------------------------------------------------------
        # [team member B will fill this part]
        # it will connect to ai_service.py functions later.
        # result_text = ai_service.get_description(file_path)
        # ---------------------------------------------------------
        
        # send back a dummy response for now
        result_text = f"이미지({file.filename})가 성공적으로 서버에 도착했습니다."

        return {
            "filename": file.filename,
            "description": result_text,
            "audio_url": None # add later
        }

    except Exception as e:
        # if any error occurs, return 500 error
        raise HTTPException(status_code=500, detail=str(e))
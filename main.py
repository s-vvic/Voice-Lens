# main.py

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
import uuid
import ai_service

# create FastAPI app instance
app = FastAPI(title="Voice-Lens API")

# cors settings(it will be restricted later)
# allow all origins for now(can be restricted later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# temporary upload directory
UPLOAD_DIR = "temp_images"
# if the upload directory does not exist, create it
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

@app.get("/")
async def read_root():
    return {"message": "Voice-Lens API is running!"}

@app.post("/analyze")
async def analyze_image(file: UploadFile = File(...)):
    # check if a file is provided
    #file.content_type has the same values as 'image/jpeg', 'image/png'
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="이미지 파일만 업로드 가능합니다.")

    try:
        # prevent directory duplication attacks (use uuid for filename)
        # ex: original.jpg -> sd89-f789-asdf-8978.jpg
        file_extension = file.filename.split(".")[-1]  # extract file extension
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        
        # make the full file path
        file_path = os.path.join(UPLOAD_DIR, unique_filename)

        # save the uploaded file to the temporary directory
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)


        # call the AI service to get image description
        try:
            description = ai_service.get_image_description(file_path)
        except Exception as e:
            print(f"AI 분석 실패: {e}")
            description = "죄송합니다. AI 분석 중 오류가 발생했습니다."
        return {
            "status": "success",
            "original_filename": file.filename,
            "saved_filename": unique_filename,
            "file_path": file_path,
            "description": description,
            "message": "파일이 안전하게 저장되었습니다."
        }

    except Exception as e:
        # if any error occurs during file saving
        print(f"Error: {e}")  # server-side logging
        raise HTTPException(status_code=500, detail="파일 저장 중 오류가 발생했습니다.")
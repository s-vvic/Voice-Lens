from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
import uuid
import ai_service
from tts_service import text_to_speech

# create FastAPI app instance
app = FastAPI(title="Voice-Lens API")

# cors settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# temporary directories
UPLOAD_DIR = "temp_images"
AUDIO_DIR = "temp_audio"
for dir_path in [UPLOAD_DIR, AUDIO_DIR]:
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

# Mount static file directories
app.mount("/audio", StaticFiles(directory=AUDIO_DIR), name="audio")


@app.get("/")
async def read_root():
    return {"message": "Voice-Lens API is running!"}


@app.post("/analyze")
async def analyze_image(request: Request, file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="이미지 파일만 업로드 가능합니다.")

    try:
        file_extension = file.filename.split(".")[-1]
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        description = "오류: AI 분석에 실패했습니다."
        audio_url = None

        try:
            description = ai_service.get_image_description(file_path)
            audio_path = text_to_speech(description)  # Returns "temp_audio/filename.mp3"
            audio_filename = os.path.basename(audio_path)
            # Construct full URL: http://.../audio/filename.mp3
            audio_url = f"{str(request.base_url).rstrip('/')}/audio/{audio_filename}"

        except Exception as e:
            print(f"AI 또는 TTS 실패: {e}")
            description = "죄송합니다. AI 분석 또는 음성 변환 중 오류가 발생했습니다."
            # audio_url remains None

        return {
            "status": "success",
            "description": description,
            "audio_url": audio_url,
            "message": "파일이 안전하게 저장 및 처리되었습니다."
        }

    except Exception as e:
        print(f"파일 저장 오류: {e}")
        raise HTTPException(status_code=500, detail="파일 처리 중 오류가 발생했습니다.")
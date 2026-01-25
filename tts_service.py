# tts_service.py
from gtts import gTTS
import os
import uuid

OUTPUT_DIR = "temp_audio"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def text_to_speech(text: str, lang: str = "ko") -> str:
    """
    텍스트를 mp3 파일로 변환하는 TTS 모듈.
    각 호출마다 고유한 파일명을 생성하여 덮어쓰기 문제를 방지합니다.
    """
    filename = f"{uuid.uuid4()}.mp3"
    path = os.path.join(OUTPUT_DIR, filename)

    tts = gTTS(text=text, lang=lang)
    tts.save(path)

    return path


if __name__ == "__main__":
    # 단독 실행 테스트
    test_text = "이 문장은 TTS 모듈 단독 테스트용 더미 텍스트입니다."
    audio_path = text_to_speech(test_text)
    print(f"TTS 생성 완료: {audio_path}")

# ai_service.py
import os
import google.generativeai as genai
from dotenv import load_dotenv

# .env 파일에서 API 키 로드
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

# Gemini 설정
genai.configure(api_key=API_KEY)

def get_image_description(image_path: str):
    """
    이미지 경로를 받아서 Gemini에게 설명을 요청하는 함수
    """
    try:
        # 1. 모델 준비 (Gemini Pro Vision)
        model = genai.GenerativeModel('gemini-1.5-flash') # 또는 gemini-pro-vision

        # 2. 이미지 파일 열기
        # (Gemini가 읽을 수 있는 형태로 변환)
        # ※ 실제 구현 시 PIL 라이브러리 필요할 수 있음 (pip install Pillow) -> 추가하게되면 requirements.txt에 반영 필요
        import PIL.Image
        img = PIL.Image.open(image_path)

        # 3. 프롬프트 설정 (상황별로 다르게 하려면 이 부분을 수정)
        prompt = "이 이미지는 시각장애인을 위해 묘사되어야 해. 눈앞에 무엇이 있는지, 위험 요소는 없는지 한국어로 구체적으로 설명해줘."

        # 4. API 호출
        response = model.generate_content([prompt, img])
        
        # 5. 결과 텍스트 반환
        return response.text

    except Exception as e:
        return f"AI 분석 중 오류가 발생했습니다: {str(e)}"
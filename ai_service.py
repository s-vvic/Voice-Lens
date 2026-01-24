# ai_service.py

import os
from google import genai
from dotenv import load_dotenv
import PIL.Image

# .env 파일에서 API 키 로드
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

# API 키가 없으면 에러가 나지 않도록 처리 (실수를 방지하기 위해)
if not API_KEY:
    print("Warning: GOOGLE_API_KEY가 설정되지 않았습니다.")
    client = None
else:
    # 1. 클라이언트 초기화
    client = genai.Client(api_key=API_KEY)

def get_image_description(image_path: str):
    """
    이미지 경로를 받아서 최신 google-genai SDK를 통해 설명을 요청하는 함수
    """
    # 키가 없을 경우 방어 코드
    if not client:
        return "오류: 서버에 GOOGLE_API_KEY가 설정되지 않았습니다."

    try:
        # 2. 이미지 파일 열기
        img = PIL.Image.open(image_path)

        # 3. 프롬프트 설정 (팀원 B가 나중에 더 수정할 부분)
        prompt = (
            "이 이미지는 시각장애인을 위해 묘사되어야 해. "
            "눈앞에 무엇이 있는지, 위험 요소는 없는지 한국어로 구체적으로 설명해줘."
        )

        # 4. API 호출 (모델명은 gemini-1.5-flash 또는 gemini-2.0-flash-exp 등 사용 가능)
        response = client.models.generate_content(
            model='gemini-1.5-flash',
            contents=[prompt, img]
        )
        
        # 5. 결과 텍스트 반환
        return response.text

    except Exception as e:
        print(f"AI Error: {e}") # 서버 로그에 에러 출력
        return "AI 분석 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요."
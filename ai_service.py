import os
from google import genai
from dotenv import load_dotenv
import PIL.Image

# .env 파일에서 API 키 로드
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

client = genai.Client(api_key=API_KEY)

def get_image_description(image_path: str):
    """
    이미지 경로를 받아서 최신 google-genai SDK를 통해 설명을 요청하는 함수
    """
    try:
        
        img = PIL.Image.open(image_path)

        prompt = (
            "이 이미지는 시각장애인을 위해 묘사되어야 해. "
            "눈앞에 무엇이 있는지, 위험 요소는 없는지 한국어로 구체적으로 설명해줘."
        )

        # 4. API 호출 (client.models.generate_content 사용)
        response = client.models.generate_content(
            model='gemini-1.5-flash',
            contents=[prompt, img]
        )
        
        # 5. 결과 텍스트 반환
        return response.text

    except Exception as e:
        return f"AI 분석 중 오류가 발생했습니다: {str(e)}"

# test code
# if __name__ == "__main__":
#     print(get_image_description("test_image.jpg"))
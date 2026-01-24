# test_ai.py
from ai_service import get_image_description

# 1. 테스트할 이미지 경로 설정 (이미지 파일이 있는 경로로 수정하세요)
test_image = "제목 없음.png" 

print("--- [Voice Lens] 프롬프트 테스트 시작 ---")

# 2. 함수 호출 및 결과 출력
result = get_image_description(test_image)

print("\n[AI의 답변]:")
print(result)
print("\n--- 테스트 완료 ---")
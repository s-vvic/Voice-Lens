# app.py
import streamlit as st
import requests

# 백엔드 서버 주소 (팀장 A가 띄워놓은 주소)
BACKEND_URL = "http://127.0.0.1:8000/analyze"

st.title("Voice-Lens")
st.write("시각장애인을 위한 AI 이미지 해설 서비스")

# 1. 이미지 업로드 위젯
uploaded_file = st.file_uploader("이미지를 업로드하세요", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # 화면에 이미지 보여주기
    st.image(uploaded_file, caption="업로드된 이미지", use_column_width=True)

    if st.button("분석 시작"):
        with st.spinner("AI가 이미지를 분석 중입니다..."):
            try:
                # 2. 백엔드 서버로 파일 전송 (FastAPI와 통신)
                files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
                response = requests.post(BACKEND_URL, files=files)

                # 3. 결과 받아서 출력
                if response.status_code == 200:
                    result = response.json()
                    description = result["description"]
                    
                    st.success("분석 완료!")
                    st.markdown(f"### AI 해설\n{description}")
                    
                    # 오디오 기능: 백엔드에서 받은 audio_url로 음성 재생
                    audio_url = result.get("audio_url")
                    if audio_url:
                        st.audio(audio_url, format="audio/mp3", start_time=0)
                    else:
                        st.warning("음성 파일을 재생할 수 없습니다.")
                else:
                    st.error(f"서버 오류: {response.status_code}")
            
            except Exception as e:
                st.error(f"연결 실패: {e}")
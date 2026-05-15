import streamlit as st
import pandas as pd
import time
import requests
import json


# 1. 페이지 설정
st.set_page_config(page_title="솔라매니저 AI", layout="centered")

# 상단 대표 이미지 (SolarManager)
col1, col2, col3 = st.columns([0.1, 0.8, 0.1])
with col2:
    # 파일명이 'solar.png'인지 다시 한번 확인해주세요!
    st.image(
        "solar.png", 
        use_container_width=True,
        caption="태양광 패널 사진을 업로드하면 Solar Manager AI가 오염도와 예상 손실액을 계산합니다.."
    )
    
# 2. 헤더 섹션
st.title("☀️ 솔라매니저 AI")
st.subheader("사진 한 장으로 내 발전소 수익을 지키세요")
st.info("태양광 패널 사진을 업로드하면 AI가 오염도와 예상 손실액을 계산합니다.")

# 3. 1단계: 사진 업로드
uploaded_file = st.file_uploader("패널 사진을 선택하거나 촬영하세요", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # 사진 표시
    st.image(uploaded_file, caption="업로드된 패널 이미지", use_column_width=True)
    
    with st.spinner("AI가 패널 상태를 정밀 분석 중입니다..."):
        # 분석 시뮬레이션 (여기에 형님의 Vision 모델 추론 로직 삽입)
        time.sleep(2) 
        
        # 가상의 결과 데이터
        status = "주의"
        loss_rate = 12.5
        loss_amount = 15400
        
    st.divider()

    # 4. 2단계: 분석 결과 대시보드
    st.header("🔍 AI 진단 결과")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("종합 상태", status, delta="-오염 감지", delta_color="inverse")
    col2.metric("예상 손실률", f"{loss_rate}%")
    col3.metric("월 손실 금액", f"₩{loss_amount:,}")

    # 상세 판독 테이블
    df = pd.DataFrame({
        "탐지 항목": ["표면 오염", "미세 균열", "핫스팟"],
        "상태": ["심각", "정상", "의심"],
        "권고 사항": ["전체 세척 권장", "이상 없음", "배선 점검 필요"]
    })
    st.table(df)

    # 5. 3단계: 액션 버튼
    st.success(f"💡 지금 세척하면 이번 달 약 {loss_amount:,}원을 더 벌 수 있습니다!")
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🧼 인근 세정 업체 견적 받기"):
            st.write("가까운 전문 업체 3곳에 견적을 요청했습니다. (준비 중)")
    with c2:
        if st.button("📄 상세 PDF 리포트 다운로드"):
            st.write("리포트를 생성 중입니다. (준비 중)")

else:
    st.warning("분석을 시작하려면 사진을 업로드해 주세요.")



def create_github_issue(email, plan):
    """결제 시도 데이터를 깃허브 이슈로 전송합니다."""
    token = st.secrets["GITHUB_TOKEN"]
    repo = st.secrets["REPO_NAME"]
    url = f"https://api.github.com/repos/{repo}/issues"
    
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    data = {
        "title": f"🚀 결제 시도: {email}",
        "body": f"**플랜:** {plan}\n**이메일:** {email}\n**일시:** {st.session_state.get('current_time', 'N/A')}",
        "labels": ["fake-door-test", "lead"]
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.status_code

# 결제 버튼 클릭 후 폼 부분
if st.button("월 9,900원에 Pro 시작하기"):
    st.session_state['show_form'] = True

if st.session_state.get('show_form'):
    st.info("현재 Pro 버전은 사전 예약 중입니다. 특별 혜택을 놓치지 마세요!")
    with st.form("payment_lead"):
        email = st.text_input("혜택을 받으실 이메일")
        submitted = st.form_submit_button("사전 예약하고 50% 할인받기")
        if submitted:
            if email:
                # 함수를 호출하고 결과값을 받습니다.
                token = st.secrets["GITHUB_TOKEN"]
                repo = st.secrets["REPO_NAME"]
                url = f"https://api.github.com/repos/{repo}/issues"
                headers = {"Authorization": f"token {token}"}
                data = {"title": f"결제시도: {email}", "body": f"Plan: Pro"}
                
                response = requests.post(url, headers=headers, json=data)
                
                if response.status_code == 201:
                    st.success("예약 완료!")
                else:
                    # 여기에서 진짜 범인을 잡습니다!
                    st.error(f"실패 원인: {response.status_code}")
                    st.write(response.json()) # 구체적인 에러 메시지 출력


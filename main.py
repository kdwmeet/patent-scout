import streamlit as st
from app.scout import analyze_patent_risk
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Patent Scout", layout="wide")

st.title("특허 침해 가능성 진단기")
st.caption("당신의 아이디어가 이미 특허로 등록되어 있을까요? AI 변리사가 선행 기술을 조사해 드립니다.")
st.divider()

# --- 입력 섹션 ---
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("내 아이디어 설명")
    user_idea = st.text_area(
        "발명 내용을 상세히 적어주세요.",
        height=300,
        placeholder="예시: 스마트폰과 연동되는 접이식 드론으로, 셀카 모드 시 자동으로 얼굴을 추적하고 장애물을 회피하는 기능을 가진 촬영 장치"
    )

    analyze_btn = st.button("침해 가능성 진당 시작", type="primary", width="stretch")

# --- 결과 섹션 ---
with col2:
    st.subheader("진단 리포트")

    if analyze_btn:
        if not user_idea:
            st.warning("아이디어를 입력해주세요")
        else:
            with st.spinner("1. 핵심 키워드 추출중...\n2. 전세계 특허 DB 검색 중...\n3. 구성요소 비교 분석 중..."):
                result = analyze_patent_risk(user_idea)

                if "error" in result:
                    st.error("분석 중 오류가 발생했습니다.")
                    st.write(result)
                else:
                    # 종합 등급
                    score = result.get("risk_score", 0)
                    level = result.get("risk_level", "알 수 없음")

                    if score >= 80:
                        st.error(f"🚨 위험도: {level} ({score}점)")
                    elif score >= 50:
                        st.warning(f"⚠️ 위험도: {level} ({score}점)")
                    else:
                        st.success(f"✅ 위험도: {level} ({score}점)")

                    st.divider()

                    # 유사 특허 목록
                    st.markdown("#### 발견된 유사 선행 기술")
                    for patent in result.get("similar_patents", []):
                        st.info(f"**{patent.get('title')}** (유사도: {patent.get('similarity')})\n\n- 분석: {patent.get('reason')}")
                    
                    st.divider()

                    # 회피 설계 조언
                    st.markdown("#### 변리사의 조언 (회피 설계)")
                    st.write(result.get("advice"))
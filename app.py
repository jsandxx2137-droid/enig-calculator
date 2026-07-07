import streamlit as st

# 웹페이지 기본 설정 (타이틀 및 와이드 레이아웃)
st.set_page_config(page_title="ENIG Loading Factor Simulator", layout="centered")

# 고급스러운 커스텀 디자인을 위한 스타일 CSS 주입
st.markdown("""
    <style>
    /* 전체 폰트 및 배경 스타일 정돈 */
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    /* 메인 타이틀 스타일 */
    .main-title {
        font-size: 28px !important;
        font-weight: 800 !important;
        color: #1E3A8A;
        margin-bottom: 5px !important;
    }
    /* 결과 카드 스타일 */
    .result-card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 20px;
        margin-top: 15px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
    /* 가장 중요한 최종 결과 텍스트 왕대박 크게 */
    .total-score {
        font-size: 40px !important;
        font-weight: 900 !important;
        color: #0284C7;
        text-align: center;
        padding: 15px 0;
        background: #F0F9FF;
        border-radius: 8px;
        border: 2px dashed #0EA5E9;
        margin: 10px 0;
    }
    /* 서브 타이틀 세션 스타일 */
    .section-header {
        font-size: 18px !important;
        font-weight: 700 !important;
        color: #334155;
        border-left: 5px solid #0EA5E9;
        padding-left: 10px;
        margin-top: 25px;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# 메인 헤더 타이틀 부 구역
st.markdown('<p class="main-title">🧪 ENIG Loading Factor 시뮬레이터</p>', unsafe_allow_html=True)
st.caption("공정 조건 및 제품/더미 수량을 입력하여 실시간 부하율을 모니터링하세요.")
st.markdown("---")

# ==========================================
# [우리 회사 모델별 1 PNL당 도금 면적 Raw Data]
# ==========================================
MODEL_DATABASE = {
    "선택하세요 (직접 입력)": 0,
    "AMU849PJ03-550": 94878,
    "M272A_P1_QSMC": 40170,
    "M271_P1_04819-01": 32708,
    "AMUA30PU01_P2_POR_HYBRIDE": 127204
}

# 1. 왼쪽 사이드바 공정 설정 구역 디자인
st.sidebar.markdown("### ⚙ 공정 기본 스펙")
tank_volume = st.sidebar.number_input("도금조 용량 (Volume, L)", min_value=1.0, value=820.0, step=10.0)
fixed_dummy_loading = st.sidebar.number_input("더미 1 PNL당 고유 부하율 (dm²/L)", min_value=0.0, value=0.04878049, format="%.8f")

# 2. 메인 화면 입력부 레이아웃 정돈
st.markdown('<p class="section-header">투입 공정 데이터 입력</p>', unsafe_allow_html=True)

# 모델 선택부
selected_model = st.selectbox("품명 / 모델명 선택", list(MODEL_DATABASE.keys()))
default_area = MODEL_DATABASE[selected_model]

# 입력 편의를 위해 2열 배치 (면적 입력과 제품 수량)
col_in1, col_in2 = st.columns(2)
with col_in1:
    prod_area_mm2 = st.number_input("선택 모델 PNL 면적 (mm²)", min_value=0, value=default_area, step=1000)
with col_in2:
    input_pnl = st.number_input("제품 투입 수량 (PNL)", min_value=0, value=30, step=1)

# 더미 수량 입력은 아래에 깔끔하게 배치
dummy_pnl = st.number_input("추가 더미 투입 수량 (PNL)", min_value=0, value=4, step=1)

st.markdown("<br>", unsafe_allow_html=True)

# 3. 계산 및 시각화 구역
if st.button("📊 부하율 실시간 시뮬레이션 개시", type="primary", use_container_width=True):
    # 계산식 실행
    prod_area_dm2 = (prod_area_mm2 / 10000) * input_pnl
    prod_loading = prod_area_dm2 / tank_volume
    dummy_loading = fixed_dummy_loading * dummy_pnl
    total_loading = prod_loading + dummy_loading
    
    # 시뮬레이션 결과 섹션 디자인
    st.markdown('<p class="section-header">Loading Factor 시뮬레이션 결과</p>', unsafe_allow_html=True)
    
    # 2열 카드로 개별 기여도 노출
    col_res1, col_res2 = st.columns(2)
    with col_res1:
        st.markdown(f"""
        <div style="background-color: #FFFFFF; border: 1px solid #E2E8F0; padding: 15px; border-radius: 8px; text-align: center;">
            <span style="font-size: 14px; color: #64748B; font-weight: 600;">① 제품 자체 부하율</span><br>
            <span style="font-size: 22px; font-weight: 700; color: #334155;">{prod_loading:.5f} <span style="font-size:14px;">dm²/L</span></span>
        </div>
        """, unsafe_allow_html=True)
        
    with col_res2:
        st.markdown(f"""
        <div style="background-color: #FFFFFF; border: 1px solid #E2E8F0; padding: 15px; border-radius: 8px; text-align: center;">
            <span style="font-size: 14px; color: #64748B; font-weight: 600;">② 추가 더미 부하율</span><br>
            <span style="font-size: 22px; font-weight: 700; color: #334155;">{dummy_loading:.5f} <span style="font-size:14px;">dm²/L</span></span>
        </div>
        """, unsafe_allow_html=True)
        
    # 종합 최종 결과 대형 카드 출력
    st.markdown(f"""
    <div class="result-card">
        <div style="text-align: center; font-size: 16px; font-weight: 700; color: #475569;">▣ 최종 합산 Loading Factor (① + ②)</div>
        <div class="total-score">{total_loading:.5f} dm²/L</div>
    </div>
    """, unsafe_allow_html=True)
    
    # 엔지니어 분석용 세부 내역 데이터
    with st.expander("🔍 공정 데이터 세부 내역 분석 (접기/펼치기)"):
        st.markdown(f"""
        * **제품 총 도금 면적**: `{prod_area_dm2:.2f} dm²`
        * **더미 1장당 고유 기여도**: `{fixed_dummy_loading:.8f} dm²/L`
        * **투입 더미 총 부하율 기여도**: `{dummy_loading:.5f} dm²/L`
        * **전체 합산 가용 면적 환산값**: `{(prod_area_dm2 + (dummy_loading * tank_volume)):.2f} dm²`
        """)


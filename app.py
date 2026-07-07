import streamlit as st

# 웹페이지 기본 설정
st.set_page_config(page_title="ENIG Loading Factor Simulator", layout="centered")

st.title("🧪 ENIG 제품/더미별 Loading Factor 계산기")
st.markdown("현장 모니터링 및 시뮬레이션용 웹 프로그램입니다.")
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

# 1. 설비 및 공정 조건 입력 세션
st.sidebar.header("⚙ 기본 공정 조건 설정")
tank_volume = st.sidebar.number_input("1. 도금조 볼륨 (L)", min_value=1.0, value=820.0, step=10.0)
fixed_dummy_loading = st.sidebar.number_input("4. 더미 1 PNL당 고유 부하율 (dm²/L)", min_value=0.0, value=0.04878049, format="%.8f")

st.header("📋 투입 데이터 입력")

# 2. 제품 모델 선택 드롭다운
selected_model = st.selectbox("2. 제품 모델명 선택 (Raw Data)", list(MODEL_DATABASE.keys()))

# 모델 선택에 따른 면적 자동 설정
default_area = MODEL_DATABASE[selected_model]
prod_area_mm2 = st.number_input("   └ 선택 모델 PNL 면적 (mm²)", min_value=0, value=default_area, step=1000)

# 수량 입력
input_pnl = st.number_input("3. 투입할 제품 수량 (PNL)", min_value=0, value=20, step=1)
dummy_pnl = st.number_input("5. 투입할 더미 수량 (PNL)", min_value=0, value=5, step=1)

st.markdown("---")

# 3. 실시간 계산 로직
if st.button("📊 각 부하율(Loading Factor) 자동 계산하기", type="primary"):
    try:
        # 제품 부하율 계산
        prod_area_dm2 = (prod_area_mm2 / 10000) * input_pnl
        prod_loading = prod_area_dm2 / tank_volume
        
        # 더미 부하율 계산
        dummy_loading = fixed_dummy_loading * dummy_pnl
        
        # 합산 최종 부하율
        total_loading = prod_loading + dummy_loading
        
        # 결과 화면 출력
        st.header("🎯 Loading Factor 시뮬레이션 결과")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="① 제품 자체 Loading Factor", value=f"{prod_loading:.5f} dm²/L")
        with col2:
            st.metric(label="② 추가 더미 Loading Factor", value=f"{dummy_loading:.5f} dm²/L")
            
        st.success(f"▣ 최종 합산 Loading Factor (① + ②) : **{total_loading:.5f} dm²/L**")
        
        # 상세 데이터 내역 출력
        st.markdown("### 🔍 상세 내역")
        st.text(f"• 제품 총 면적: {prod_area_dm2:.2f} dm²\n"
                f"• 더미 1 PNL당 고유 부하율: {fixed_dummy_loading:.8f} dm²/L\n"
                f"• 투입 더미 총 부하율 기여도: {dummy_loading:.5f} dm²/L\n"
                f"• 전체 합산 기여 면적 환산값: {(prod_area_dm2 + (dummy_loading * tank_volume)):.2f} dm²")
                
    except Exception as e:
        st.error(f"계산 중 오류가 발생했습니다. 입력값을 확인해 주세요. ({e})")

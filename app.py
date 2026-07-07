import streamlit as st

# 웹페이지 기본 설정
st.set_page_config(page_title="ENIG Loading Factor Simulator", layout="centered")

# 고급스러운 커스텀 디자인 CSS 주입
st.markdown("""
    <style>
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    .main-title {
        font-size: 28px !important;
        font-weight: 800 !important;
        color: #1E3A8A;
        margin-bottom: 5px !important;
    }
    .result-card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 20px;
        margin-top: 15px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
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

# ==========================================
# [다국어 사전 데이터베이스 - 한국어 / 베트남어]
# ==========================================
LANG_DB = {
    "KO": {
        "title": "🧪 ENIG Loading Factor 시뮬레이터",
        "subtitle": "공정 조건 및 제품/더미 수량을 입력하여 실시간 부하율을 모니터링하세요.",
        "sidebar_title": "⚙️ 공정 기본 스펙",
        "tank_vol": "도금조 용량 (Volume, L)",
        "dummy_loading_unit": "더미 1 PNL당 고유 부하율 (dm²/L)",
        "input_header": "투입 공정 데이터 입력",
        "model_select": "품명 / 모델명 선택",
        "model_custom": "선택하세요 (직접 입력)",
        "area_label": "선택 모델 PNL 면적 (mm²)",
        "prod_pnl": "제품 투입 수량 (PNL)",
        "dummy_pnl": "추가 더미 투입 수량 (PNL)",
        "btn_calc": "📊 부하율 실시간 시뮬레이션 개시",
        "res_header": "Loading Factor 시뮬레이션 결과",
        "res_prod": "① 제품 자체 부하율",
        "res_dummy": "② 추가 더미 부하율",
        "res_total_title": "▣ 최종 합산 Loading Factor (① + ②)",
        "detail_header": "🔍 공정 데이터 세부 내역 분석 (접기/펼치기)",
        "detail_prod_area": "제품 총 도금 면적",
        "detail_dummy_unit": "더미 1장당 고유 기여도",
        "detail_dummy_total": "투입 더미 총 부하율 기여도",
        "detail_area_sum": "전체 합산 가용 면적 환산값"
    },
    "VI": {
        "title": "🧪 Trình mô phỏng hệ số tải (Loading Factor) ENIG",
        "subtitle": "Nhập điều kiện công đoạn và số lượng hàng/dummy để theo dõi hệ số tải theo thời gian thực.",
        "sidebar_title": "⚙️ Thông số bể xi cơ bản",
        "tank_vol": "Dung tích bể xi (Volume, L)",
        "dummy_loading_unit": "Hệ số tải cố định của 1 PNL Dummy (dm²/L)",
        "input_header": "Nhập dữ liệu công đoạn",
        "model_select": "Chọn mã hàng / Tên Model",
        "model_custom": "Chọn (Nhập trực tiếp)",
        "area_label": "Diện tích PNL Model đã chọn (mm²)",
        "prod_pnl": "Số lượng hàng bỏ vào (PNL)",
        "dummy_pnl": "Số lượng Dummy bỏ thêm (PNL)",
        "btn_calc": "📊 Bắt đầu mô phỏng hệ số tải",
        "res_header": "Kết quả mô phỏng Hệ số tải (Loading Factor)",
        "res_prod": "① Hệ số tải của riêng sản phẩm",
        "res_dummy": "② Hệ số tải của Dummy bỏ thêm",
        "res_total_title": "▣ Tổng hệ số tải cuối cùng (① + ②)",
        "detail_header": "🔍 Phân tích chi tiết dữ liệu công đoạn (Đóng/Mở)",
        "detail_prod_area": "Tổng diện tích mạ của sản phẩm",
        "detail_dummy_unit": "Mức độ ảnh hưởng cố định của 1 tấm Dummy",
        "detail_dummy_total": "Tổng hệ số tải đóng góp của Dummy",
        "detail_area_sum": "Giá trị quy đổi tổng diện tích khả dụng"
    }
}

# ==========================================
# [우리 회사 모델별 1 PNL당 도금 면적 Raw Data]
# ==========================================
MODEL_DATABASE = {
    "AMSA50KN01_MAIN_TEST_ANA38409E": 33152.4,
"I272_DROP0_NMC": 102668,
"AMUA849JK01_P1_8L": 44647,
"KCI_I261_PEEL_OFF_TEST_COUPON": 67888,
"AMUA11PF01_POC": 111028,
"AMUA11PF01_POC": 111028,
"AMUA30PH01_POC": 105317,
"AMUA30PH01_POC": 105317,
"AMUA30PUO1_DROP1_FNM_JC": 65068,
"AMUA30PUO1_DROP1_FNM_JC": 65068,
"AMUA10PV01_DROP1_FNM_JC": 69653,
"AMUA10PV01_DROP1_FNM_JC": 69653,
"AMUA30PU01_DROP1_FNM_JC": 65068,
"AMUA30PU01_DROP1_FNM_JC": 65068,
"ATNA40HQ07_MAIN_PCB": 52945,
"AMUA849JK01_P2": 44592,
"AMUA849JK01_P2": 44592,
"AMUA30PU01_DROP1_LT": 65090,
"AMUA30PU01_DROP1_NMC": 104954,
"AMUA849JK01_P2_10L": 44539,
"AMUA10PV01_DROP1_LT": 69688,
"AMUA849JK01_P2_LT": 90206,
"ATUA63N701_P2": 40073,
"M10_TYPE5": 99437.64,
"M10_TYPE3": 99437.54,
"M20_TYPE1": 99773.56,
"I271_NMC_DOE": 126730,
"ATUA407V03_0P39T_PCB": 22031,
"M30_TYPE1": 99422,
"AMUD84NA01_BRIDGE1": 5859,
"I272_NMC_DOE": 103825,
"AMUA30PH01_POC_LT": 100937,
"AMUD84NA01_BRIDGE4": 6942,
"AMUA30PU01_DEV": 102034,
"ATUA42Q501_P2": 40137,
"AMUA11PF01_POC_LT": 106586,
"ATNA40HQ13_MAIN_PCB": 53017,
"AMSA70NR01_MAIN_PCB": 50941,
"AMUA11PF01_DEV_MAIN": 111676,
"AMUA30PH01_DEV_MAIN": 105980,
"AMUA10PV01_DEV": 107587,
"AMUA11PF01_DEV_JC": 111741,
"AMUA30PU01_DEV_LT": 105358,
"AMUA30PH01_POC_LT": 100937,
"ATNA40HQ02_MAIN_PCB": 26498,
"AMUA30PU01_DEV_2CORE": 104624,
"AMUA10PV01_DEV_2CORE": 107166,
"AMUA849JK01_DOE_10L_04636": 99709,
"AMUA10PV01_DEV_LT": 106981,
"AMUA11M901_IP281": 49792,
"AMUA11PF01_POC_LT": 106586,
"AMUA30PU01_P1": 106350,
"AMUA849JK01_EVT_LT": 90305,
"AMUA849JK01_EVT_10L_04397": 99648,
"ATUA63N701_EVT": 43665,
"AMUA10PV01_P1": 109513,
"ATNA40LE04_MAIN_PCB": 45773,
"AMUA11PF01_P1": 127591,
"ATNA40HQ13_MAIN_PCB": 53017,
"ATNA40KW04_MAIN_PCB": 37621,
"AMUA30PU01_P1_363_2CORE": 105777,
"ATNA40LE04_MAIN_PCB": 45773,
"AMSA33KP01_MAIN_PCB": 50376,
"AMSA50KN01_MAIN_PCB": 33590,
"AMUA11PF01_P1_NEW_MINI": 127557.9,
"AMUA30PH01_P1_NEW_MINI": 131697,
"AMUA849JK01_P2_10L": 44539,
"AMUA849JK01_P2_10L": 44539,
"AMUA30PH01_DEV_MAIN": 105980,
"ATNA40LE05_MAIN_PCB": 49831,
"ATNA40HQ03_MAIN_PCB": 59716,
"AMSA33KP01_MAIN_PCB": 50376,
"M272A_P1_PCB": 44203,
"ATNA40HQ16_MAIN_PCB": 53503,
"AMUA30PH01_P1_NEW_MINI": 131697,
"AMUA849JK01_DVT_10L_04397": 95178,
"ATNA40HQ16_MAIN_PCB": 53503,
"AMUA30PH01_P1_LT": 120497,
"AMUA30PH01_P1_NEW_MINI": 131697,
"AMUA849JK01_DVT_10L_04636": 95703,
"AMU849PJ03-005": 94878,
"AMU849PJ03-006": 94962,
"AMSA70NR01_MAIN_PCB": 50941,
"AMSA10LJ01_MAIN_PCB": 58780,
"AMUA11PF01_WVB": 127401,
"M272A_P1_QSMC": 40170,
"AMUA30PH01_WVB": 81310,
"AMUA30PU01_P2_POR_HYBRIDE": 127204,
"M271_P1_04819-01": 32708,
}

# 1. 사이드바 - 언어 선택 기능 최상단 배치
st.sidebar.markdown("### 🌐 Language / 언어 선택")
lang_select = st.sidebar.radio("Choose Language", ["한국어", "Tiếng Việt"], label_visibility="collapsed")
lang = "KO" if lang_select == "한국어" else "VI"

# 번역 사전 연결
T = LANG_DB[lang]

# 2. 사이드바 - 공정 설정 구역
st.sidebar.markdown(f"### {T['sidebar_title']}")
tank_volume = st.sidebar.number_input(T['tank_vol'], min_value=1.0, value=820.0, step=10.0)
fixed_dummy_loading = st.sidebar.number_input(T['dummy_loading_unit'], min_value=0.0, value=0.04878049, format="%.8f")

# 3. 메인 화면 헤더 구역
st.markdown(f'<p class="main-title">{T["title"]}</p>', unsafe_allow_html=True)
st.caption(T["subtitle"])
st.markdown("---")

# 4. 메인 화면 입력부 레이아웃
st.markdown(f'<p class="section-header">{T["input_header"]}</p>', unsafe_allow_html=True)

# 모델 드롭다운 리스트 동적 구성
model_options = [T["model_custom"]] + list(MODEL_DATABASE.keys())
selected_model = st.selectbox(T["model_select"], model_options)

default_area = 0
if selected_model != T["model_custom"]:
    default_area = MODEL_DATABASE[selected_model]

# 입력창 2열 배치
col_in1, col_in2 = st.columns(2)
with col_in1:
    prod_area_mm2 = st.number_input(T["area_label"], min_value=0, value=default_area, step=1000)
with col_in2:
    input_pnl = st.number_input(T["prod_pnl"], min_value=0, value=30, step=1)

dummy_pnl = st.number_input(T["dummy_pnl"], min_value=0, value=4, step=1)

st.markdown("<br>", unsafe_allow_html=True)

# 5. 계산 및 시각화 구역
if st.button(T["btn_calc"], type="primary", use_container_width=True):
    # 계산 로직
    prod_area_dm2 = (prod_area_mm2 / 10000) * input_pnl
    prod_loading = prod_area_dm2 / tank_volume
    dummy_loading = fixed_dummy_loading * dummy_pnl
    total_loading = prod_loading + dummy_loading
    
    st.markdown(f'<p class="section-header">{T["res_header"]}</p>', unsafe_allow_html=True)
    
    # 2열 카드로 제품/더미 결과 노출
    col_res1, col_res2 = st.columns(2)
    with col_res1:
        st.markdown(f"""
        <div style="background-color: #FFFFFF; border: 1px solid #E2E8F0; padding: 15px; border-radius: 8px; text-align: center;">
            <span style="font-size: 14px; color: #64748B; font-weight: 600;">{T['res_prod']}</span><br>
            <span style="font-size: 22px; font-weight: 700; color: #334155;">{prod_loading:.5f} <span style="font-size:14px;">dm²/L</span></span>
        </div>
        """, unsafe_allow_html=True)
        
    with col_res2:
        st.markdown(f"""
        <div style="background-color: #FFFFFF; border: 1px solid #E2E8F0; padding: 15px; border-radius: 8px; text-align: center;">
            <span style="font-size: 14px; color: #64748B; font-weight: 600;">{T['res_dummy']}</span><br>
            <span style="font-size: 22px; font-weight: 700; color: #334155;">{dummy_loading:.5f} <span style="font-size:14px;">dm²/L</span></span>
        </div>
        """, unsafe_allow_html=True)
        
    # 종합 최종 결과 대형 카드 출력
    st.markdown(f"""
    <div class="result-card">
        <div style="text-align: center; font-size: 16px; font-weight: 700; color: #475569;">{T['res_total_title']}</div>
        <div class="total-score">{total_loading:.5f} dm²/L</div>
    </div>
    """, unsafe_allow_html=True)
    
    # 엔지니어 분석용 세부 내역 데이터
    with st.expander(T["detail_header"]):
        st.markdown(f"""
        * **{T['detail_prod_area']}**: `{prod_area_dm2:.2f} dm²`
        * **{T['detail_dummy_unit']}**: `{fixed_dummy_loading:.8f} dm²/L`
        * **{T['detail_dummy_total']}**: `{dummy_loading:.5f} dm²/L`
        * **{T['detail_area_sum']}**: `{(prod_area_dm2 + (dummy_loading * tank_volume)):.2f} dm²`
        """)

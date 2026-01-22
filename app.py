import streamlit as st
import google.generativeai as genai
import os

# --- Page Configuration ---
st.set_page_config(
    page_title="Chief Hank - Southern Production Supervisor",
    page_icon="👷‍♂️",
    layout="centered"
)

# --- Custom Styling ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    .main-header {
        font-size: 2.5rem;
        font-weight: 800;
        color: #1a1a1a;
        text-align: center;
        margin-bottom: 0.5rem;
        letter-spacing: -1px;
    }
    
    .sub-header {
        font-size: 1.1rem;
        color: #4a4a4a;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .output-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        border: 1px solid #eee;
        margin-top: 2rem;
        white-space: pre-wrap;
    }
    
    .stTextArea textarea {
        border-radius: 10px;
        border: 2px solid #e5e7eb;
    }

    .stTextArea label {
        color: #1a1a1a !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #d97706 !important;
        box-shadow: 0 0 0 2px rgba(217, 119, 6, 0.2) !important;
    }
    
    .stButton button {
        width: 100%;
        background-color: #d97706;
        color: white;
        border-radius: 10px;
        font-weight: 600;
        padding: 0.75rem;
        border: none;
        transition: all 0.2s;
    }
    
    .stButton button:hover {
        background-color: #b45309;
        transform: translateY(-1px);
    }

    /* Sidebar info style */
    .sidebar-info {
        background: #f1f5f9;
        padding: 1rem;
        border-radius: 8px;
        font-size: 0.9rem;
        color: #475569;
        border: 1px solid #e2e8f0;
    }
    </style>
""", unsafe_allow_html=True)

# --- Logic: Get API Key Securely ---
# Streamlit Cloud 실배포 시에는 Settings > Secrets에 저장된 키를 우선 사용합니다.
api_key = None

if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
else:
    # 로컬 개발 환경용 영구 저장 로직
    def save_key_to_local(key):
        try:
            os.makedirs(".streamlit", exist_ok=True)
            with open(".streamlit/secrets.toml", "w", encoding="utf-8") as f:
                f.write(f'GOOGLE_API_KEY = "{key}"')
            return True
        except Exception as e:
            st.error(f"키 저장 실패: {e}")
            return False

    with st.sidebar:
        st.title("⚙️ Settings")
        input_key = st.text_input("Gemini API Key", type="password", help="Streamlit Cloud 배포 설정에서 키를 등록하면 이 창이 나타나지 않습니다.")
        if input_key:
            if st.button("내 컴퓨터에 영구 저장"):
                if save_key_to_local(input_key):
                    st.success("API Key가 저장되었습니다! 새로고침 해주세요.")
                    st.rerun()
            api_key = input_key
        else:
            st.info("💡 배포 팁: Cloud 설정의 Secrets에 'GOOGLE_API_KEY'를 등록하면 모든 사용자가 키 없이 이용할 수 있습니다.")

# --- App Layout ---
st.markdown('<h1 class="main-header">Chief Hank\'s Foreman Desk</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">30-year Veteran Production Superintendent from Georgia</p>', unsafe_allow_html=True)

# --- Logic: Translation ---
def translate_to_hank(korean_text):
    if not api_key:
        st.error("API Key가 없습니다. 배포 환경의 Secrets에 등록하거나 사이드바에서 입력해주세요.")
        return None
    
    try:
        genai.configure(api_key=api_key)
        # 최신 1.5 Pro 모델 사용
        model = genai.GenerativeModel('gemini-1.5-pro')
        
        system_prompt = """
        Your name is "Chief Hank". You are a veteran 'Production Superintendent' with over 30 years of experience 
        in manufacturing plants in the Southern US (Georgia, Alabama). 
        
        Your Mission:
        Translate Korean production plans into 'Southern US English Work Instructions' for local US workers.
        
        Tone & Style:
        1. Professional yet warm: Use colloquialisms and politeness typical of the South (e.g., "mighty fine", "reckon").
        2. Southern Nuance: Use "Y'all" or "Folks" instead of "Everyone/Guys". 
           Use indirect commands like "I need y'all to go ahead and handle this..." instead of blunt "Do this".
           Maintain mutual respect with "Please" or "Thank you".
        3. Clarity: Ensure numbers regarding Safety and Quality are crystal clear.
        4. Terminology: Use correct manufacturing terms (Assembly, Line stop, Defect, Shift, quota, etc.).
        
        Input: [Korean production plan content]
        Output Format MUST be:
        ---
        **🗣️ Foreman's Instruction (작업 지시서):**
        [Southern US English translation]

        **💡 Key Point:**
        [Summary of the most critical point in short English]
        ---
        """
        
        response = model.generate_content(f"{system_prompt}\n\nInput: {korean_text}")
        return response.text
    except Exception as e:
        # Fallback to flash if pro is unavailable
        if "404" in str(e) or "quota" in str(e).lower():
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(f"{system_prompt}\n\nInput: {korean_text}")
                return response.text
            except Exception as e2:
                st.error(f"Error: {e2}")
        else:
            st.error(f"Error: {e}")
        return None

# --- UI: Input & Output ---
korean_input = st.text_area("한국어 생산 계획 입력", placeholder="예: 오늘 2라인 A교대 근무자들은 안전 장구 착용 확인하고, 오후 3시까지 할당량 500개 마무리하세요.", height=150)

if st.button("Chief Hank에게 전달하기"):
    if korean_input:
        with st.spinner("Hank가 담배 한 대 태우고 지시서 작성하는 중..."):
            result = translate_to_hank(korean_input)
            if result:
                st.markdown(f'<div class="output-card">{result}</div>', unsafe_allow_html=True)
    else:
        st.warning("내용을 입력해주세요.")

# Footer
st.markdown("---")
st.caption("© 2024 Southern Industrial Solutions | Focused on Quality & Safety")

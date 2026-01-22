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
    }
    
    .foreman-title {
        color: #d97706;
        font-weight: 700;
        font-size: 1.2rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .instruction-text {
        font-size: 1.25rem;
        line-height: 1.6;
        color: #1f2937;
        font-style: italic;
        padding: 1rem;
        border-left: 4px solid #d97706;
        background: #fffcf0;
    }
    
    .key-point-card {
        background: #fdf2f2;
        border: 1px solid #fecaca;
        padding: 1rem;
        border-radius: 8px;
        margin-top: 1.5rem;
    }
    
    .key-point-title {
        color: #dc2626;
        font-weight: 700;
        font-size: 0.9rem;
        text-transform: uppercase;
        margin-bottom: 0.5rem;
    }

    /* Input area styling */
    .stTextArea textarea {
        border-radius: 10px;
        border: 2px solid #e5e7eb;
    }
    
    .stTextArea textarea:focus {
        border-color: #d97706;
        box-shadow: 0 0 0 2px rgba(217, 119, 6, 0.2);
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
    </style>
""", unsafe_allow_html=True)

# --- Sidebar: API Key ---
with st.sidebar:
    st.title("⚙️ Settings")
    api_key = st.text_input("Gemini API Key", type="password", help="Enter your Google Gemini API Key here.")
    st.info("이 앱은 'Chief Hank'라는 남부 베테랑 감독관 페르소나를 사용하여 한국어 생산 지시를 현지 영어로 번역합니다.")

# --- App Layout ---
st.markdown('<h1 class="main-header">Chief Hank\'s Foreman Desk</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">30-year Veteran Production Superintendent from Georgia</p>', unsafe_allow_html=True)

# --- Logic: Translation ---
def translate_to_hank(korean_text):
    if not api_key:
        st.error("Please enter your Gemini API Key in the sidebar.")
        return None
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        system_prompt = """
        Your name is "Chief Hank". You are a veteran 'Production Superintendent' with over 30 years of experience 
        in manufacturing plants in the Southern US (Georgia, Alabama). 
        
        Your Mission:
        Translate Korean production plans into 'Southern US English Work Instructions' for local US workers.
        
        Tone & Style:
        1. Professional yet warm: Use colloquialisms and politeness typical of the South.
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
        st.error(f"Error: {e}")
        return None

# --- UI: Input & Output ---
korean_input = st.text_area("한국어 생산 계획 입력", placeholder="예: 오늘 2라인 A교대 근무자들은 안전 장구 착용 확인하고, 오후 3시까지 할당량 500개 마무리하세요. 불량률 1% 넘지 않게 주의하세요.", height=150)

if st.button("Chief Hank에게 전달하기"):
    if korean_input:
        with st.spinner("Hank가 담배 한 대 태우고 지시서 작성하는 중..."):
            result = translate_to_hank(korean_input)
            if result:
                # Basic parsing if needed, but Gemini usually follows the format
                st.markdown(f'<div class="output-card">{result}</div>', unsafe_allow_html=True)
    else:
        st.warning("내용을 입력해주세요.")

# Footer
st.markdown("---")
st.caption("© 2024 Southern Industrial Solutions | Focused on Quality & Safety")

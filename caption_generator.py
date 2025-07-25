import streamlit as st
import google.generativeai as genai
from streamlit_option_menu import option_menu

# --- Page & Style ---
st.set_page_config(
    page_title="Social Media Caption Generator",
    page_icon="📱",
    layout="centered"
)
st.markdown("""
    <style>
    .main-header {
        font-size:2.7rem;
        font-weight:bold;
        text-align:center;
        color:#184773;
    }
    .sub-header {
        font-size:1.2rem;
        text-align:center;
        color:#1DA1F2;
    }
    .stButton>button {
        background:linear-gradient(90deg,#1DA1F2,#184773);
        color:white;
        height:3em;
        width:100%;
        font-size:1.2em;
        border-radius:10px;
    }
    </style>
""", unsafe_allow_html=True)

# --- App Titles ---
st.markdown("<div class='main-header'>📱 Social Media Caption Generator</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>Unleash catchy, AI-crafted captions with a single click!</div>", unsafe_allow_html=True)

# --- Sidebar Instructions ---
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/ai.png", width=80)
    st.header("How to Use")
    st.write("""
      1. Select a social platform.
      2. Enter your content theme or keyword.
      3. Click 'Generate Caption' and copy your result!
    """)
    st.info("Powered by Google Gemini AI")

# --- Gemini API Key and Model Setup ---
try:
    GEMINI_API_KEY = "your-actual-api-key"
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])


    model = genai.GenerativeModel("models/gemini-1.5-flash")
except Exception as e:
    st.error("Gemini API key not found or invalid. Please add your key in Streamlit secrets as GEMINI_API_KEY and ensure the Gemini API is enabled for your Google Cloud project.")
    st.stop()

# --- Platform Selection ---
selected_platform = option_menu(
    menu_title=None,
    options=["Instagram", "LinkedIn", "Twitter"],
    icons=["instagram", "linkedin", "twitter"],
    orientation="horizontal"
)

# --- Keyword Input ---
keyword = st.text_input("🎯 Enter a theme/keyword (e.g., fitness, coding, travel)")
st.markdown("---")

# --- Caption Generation ---
if st.button("✨ Generate Caption"):
    if not keyword.strip():
        st.warning("⚠️ Please enter a keyword!")
    else:
        with st.spinner("Generating your caption..."):
            try:
                prompt = f"Short, catchy {selected_platform} caption about '{keyword}' with emojis."
                response = model.generate_content(
                    prompt,
                    generation_config=genai.types.GenerationConfig(
                        max_output_tokens=60
                    )
                )
                caption = getattr(response, 'text', '').strip()
                if caption:
                    st.success("Here's your caption:")
                    st.code(caption, language='markdown')
                else:
                    st.error("No caption generated. Please check your API status or try again.")
            except Exception as e:
                if "API key not valid" in str(e):
                    st.error("Gemini API key not valid. Please check your API key, re-add it in Streamlit secrets, and verify the Gemini API is enabled in your Cloud Console.")
                elif "timeout" in str(e).lower() or "deadline" in str(e).lower():
                    st.error("⏰ Request timed out. Please try again, simplify the prompt, or check your quota.")
                else:
                    st.error(f"An error occurred: {e}")

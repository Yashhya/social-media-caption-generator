import streamlit as st
import google.generativeai as genai
from streamlit_option_menu import option_menu

# --- Page Configuration ---
st.set_page_config(
    page_title="Social Media Caption Generator",
    page_icon="📱",
    layout="centered"
)

# --- Custom Styles ---
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

# --- Titles ---
st.markdown("<div class='main-header'>📱 Social Media Caption Generator</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>Unleash catchy, AI-crafted captions with a single click!</div>", unsafe_allow_html=True)

# --- Sidebar Instructions and Branding ---
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/ai.png", width=80)
    st.header("How to Use")
    st.write("""
      1. Select a social platform.
      2. Enter your content theme or keyword.
      3. Click 'Generate Caption' and copy your result!
    """)
    st.info("Powered by Google Gemini AI")

# --- Gemini API Key (from Streamlit secrets) ---
try:
   GEMINI_API_KEY = "your-actual-gemini-api-key"
    model = genai.GenerativeModel("models/gemini-1.5-flash")
except Exception as e:
    st.error("API key not set or invalid. Please add a valid Gemini API key in Streamlit secrets as GEMINI_API_KEY.")
    st.stop()

# --- Platform Selection with Logos ---
selected_platform = option_menu(
    menu_title=None,
    options=["Instagram", "LinkedIn", "Twitter"],
    icons=["instagram", "linkedin", "twitter"],
    orientation="horizontal"
)

# --- Keyword Input ---
keyword = st.text_input("🎯 Enter a theme/keyword (e.g., fitness, coding, travel)")
st.markdown("---")

# --- Caption Generation Logic ---
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
                    ),
                    safety_settings={
                        "HARASSMENT": "BLOCK_NONE",
                        "HATE_SPEECH": "BLOCK_NONE",
                        "SEXUAL": "BLOCK_NONE",
                        "DANGEROUS": "BLOCK_NONE"
                    },
                )
                caption = getattr(response, 'text', '').strip()
                if caption:
                    st.success("Here's your caption:")
                    st.code(caption, language='markdown')
                else:
                    st.error("No caption generated. Please retry or check API status.")
            except Exception as e:
                if "timeout" in str(e).lower() or "deadline" in str(e).lower():
                    st.error("⏰ Request timed out. Try again, use a simpler keyword, and check your API quota.")
                else:
                    st.error(f"An error occurred: {e}")

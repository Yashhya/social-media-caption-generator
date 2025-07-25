import streamlit as st
import google.generativeai as genai
from streamlit_option_menu import option_menu


# Page config
st.set_page_config(
    page_title="Social Media Caption Generator",
    page_icon="📱",
    layout="centered"
)

# Custom CSS (optional for style boost)
st.markdown("""
    <style>
    .main-header {font-size:2.7rem;font-weight:bold;text-align:center;color:#184773;}
    .sub-header {font-size:1.2rem;text-align:center;color:#1DA1F2;}
    .stButton>button {background:linear-gradient(90deg,#1DA1F2,#184773);color:white;height:3em;width:100%;font-size:1.2em;border-radius:10px;}
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-header'>📱 Social Media Caption Generator</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>Unleash catchy, AI-crafted captions with a single click!</div>", unsafe_allow_html=True)

with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/ai.png", width=80)
    st.header("How to Use")
    st.write("""
      1. Select a social platform below.
      2. Enter your content theme or keyword.
      3. Click 'Generate Caption' and copy your result!
    """)
    st.info("Powered by Google Gemini AI")

# Configure Gemini API key securely
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("models/gemini-1.5-flash")

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

# --- Generate Caption ---
if st.button("✨ Generate Caption"):
    if not keyword:
        st.warning("⚠️ Please enter a keyword!")
    else:
        try:
            prompt = (
                f"Generate a creative, short, and catchy caption for {selected_platform} "
                f"related to '{keyword}'. Add emojis if suitable."
            )
            response = model.generate_content(prompt)
            caption = response.text.strip()
            st.success("Here's your caption:")
            st.code(caption, language='markdown')
        except Exception as e:
            st.error(f"Error: {e}")

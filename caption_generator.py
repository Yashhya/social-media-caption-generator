import streamlit as st
import google.generativeai as genai

# Set page config for a modern look
st.set_page_config(
    page_title="Social Media Caption Generator",
    page_icon="📱",
    layout="centered"
)

# Custom CSS for style enhancements
st.markdown("""
    <style>
    .main-header {font-size:2.7rem;font-weight:bold;text-align:center;color:#184773;}
    .sub-header {font-size:1.2rem;text-align:center;color:#1DA1F2;}
    .stButton>button {background:linear-gradient(90deg,#1DA1F2,#184773);color:white;height:3em;width:100%;font-size:1.2em;border-radius:10px;}
    </style>
""", unsafe_allow_html=True)

# Main header and tagline
st.markdown("<div class='main-header'>📱 Social Media Caption Generator</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>Unleash catchy, AI-crafted captions with a single click!</div>", unsafe_allow_html=True)

# Sidebar instructions and About info
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/ai.png", width=80)
    st.header("How to Use")
    st.write("""
      1. Select a social platform below.
      2. Enter your content theme or keyword.
      3. Click 'Generate Caption' and copy your result!
    """)
    st.info("Powered by Google Gemini AI")

# Set up Gemini API key using Streamlit secrets
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("models/gemini-1.5-flash")

# Platform logo URLs
logo_urls = {
    "Instagram": "https://img.icons8.com/color/48/instagram-new.png",
    "Twitter": "https://img.icons8.com/color/48/twitter-circled.png",
    "LinkedIn": "https://img.icons8.com/color/48/linkedin-circled--v1.png"
}

# Show platform logos above the radio selector
cols = st.columns(3)
platform_names = list(logo_urls.keys())
for i, name in enumerate(platform_names):
    with cols[i]:
        st.image(logo_urls[name], width=40)
        st.markdown(f"**{name}**", unsafe_allow_html=True)

# Platform selection radio (simple, uses names as above logos)
platform = st.radio(
    "Choose platform",
    platform_names,
    horizontal=True
)

# Keyword input
keyword = st.text_input("🎯 Enter a theme/keyword (e.g., fitness, coding, travel)")
st.markdown("---")

# Caption generation
if st.button("✨ Generate Caption"):
    if not keyword:
        st.warning("⚠️ Please enter a keyword!")
    else:
        try:
            prompt = (
                f"Generate a creative, short, and catchy caption for {platform} "
                f"related to '{keyword}'. Add emojis if suitable."
            )
            response = model.generate_content(prompt)
            caption = response.text.strip()
            st.success("Here's your caption:")
            st.code(caption, language='markdown')
        except Exception as e:
            st.error(f"Error: {e}")

import streamlit as st
import openai
from streamlit_option_menu import option_menu

# -- Streamlit Page Config --
st.set_page_config(
    page_title="Social Media Caption Generator",
    page_icon="📱",
    layout="centered"
)

# -- Custom Styles --
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

# -- Main Title & Tagline --
st.markdown("<div class='main-header'>📱 Social Media Caption Generator</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>Unleash catchy, AI-crafted captions with a single click!</div>", unsafe_allow_html=True)

# -- Sidebar Instructions & Branding --
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/ai.png", width=80)
    st.header("How to Use")
    st.write("""
      1. Select a social platform below.
      2. Enter your content theme or keyword.
      3. Click 'Generate Caption' and copy your result!
    """)
    st.info("Powered by OpenAI GPT-3.5 Turbo")

# -- OpenAI API Key (secure) --
openai.api_key = st.secrets["OPENAI_API_KEY"]

# -- Platform Selection With Logo/Name --
selected_platform = option_menu(
    menu_title=None,
    options=["Instagram", "LinkedIn", "Twitter"],
    icons=["instagram", "linkedin", "twitter"],
    orientation="horizontal"
)

# -- Keyword Input --
keyword = st.text_input("🎯 Enter a theme/keyword (e.g., fitness, coding, travel)")
st.markdown("---")

# -- Caption Generation Section --
if st.button("✨ Generate Caption"):
    if not keyword:
        st.warning("⚠️ Please enter a keyword!")
    else:
        with st.spinner("Generating your caption..."):
            try:
                prompt = (
                    f"Create a short, catchy {selected_platform} caption about '{keyword}' with emojis."
                )
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=60,
                    temperature=0.8,
                )
                caption = response['choices'][0]['message']['content'].strip()
                if caption:
                    st.success("Here's your caption:")
                    st.code(caption, language='markdown')
                else:
                    st.error("No caption generated. Check your API status or try again.")
            except Exception as e:
                st.error(f"Error: {e}")

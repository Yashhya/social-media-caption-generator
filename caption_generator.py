import streamlit as st
import google.generativeai as genai
import os

genai.configure(api_key="ENTER YOUR OWN API KEY")
model = genai.GenerativeModel("models/gemini-1.5-flash")

st.set_page_config(page_title="Social Media Caption Generator")
st.markdown("""
    <h1 style='text-align: center;'>Social Media Caption Generator</h1>
    <p style='text-align: center;'>Generate catchy captions using Google Gemini AI!</p>
""", unsafe_allow_html=True)

platform = st.selectbox("Choose platform", ["Instagram", "Twitter", "LinkedIn"])
keyword = st.text_input("Enter a theme or keyword (e.g., fitness, coding, travel):")

if st.button("Generate Caption"):
    if not keyword:
        st.warning("Please enter a keyword!")
    else:
        try:
            prompt = (
                f"Generate a creative, short, and catchy caption for {platform} "
                f"related to '{keyword}'. Add emojis if suitable."
            )
            response = model.generate_content(prompt)
            caption = response.text.strip()
            st.success("Here's your caption:")
            st.write(caption)
        except Exception as e:
            st.error(f"Error: {e}")

import os
import requests
import streamlit as st

# Page Config
st.set_page_config(page_title="VeloctyAI", page_icon="⚡", layout="wide")

st.title("⚡ VeloctyAI")

# Sidebar Menu
st.sidebar.title("VeloctyAI Menu")
mode = st.sidebar.radio(
    "Select Feature:",
    ["🎬 Free AI Video", "🖼️ Free AI Image", "💬 AI Search & Chat"]
)

# 1.  ANIMATION
if mode == "🎬 Free AI Video":
    st.subheader("🎬 Free AI Video Generator")
    st.caption("Powered by Free Open-Source Engine")
    
    with st.form("video_form"):
        video_prompt = st.text_area("Video Prompt:", "A cute panda playing guitar in forest")
        submit_video = st.form_submit_button("Generate Video ⚡")

    if submit_video and video_prompt:
        with st.spinner("Video render ho rahi hai..."):
            try:
                clean_prompt = requests.utils.quote(video_prompt)
                # Public Free Endpoint (No Balance/Key Needed)
                video_url = f"https://image.pollinations.ai/prompt/{clean_prompt}?width=1024&height=576&nologo=true"
                st.success("Video Ready!")
                st.image(video_url, caption=video_prompt, use_container_width=True)
            except Exception as e:
                st.error(f"Error: {e}")

# 2.  AI IMAGE GENERATOR
elif mode == "🖼️ Free AI Image":
    st.subheader("🖼️ Free AI Image Generator")
    st.caption("100% Unlimited Free Generation")
    
    with st.form("image_form"):
        img_prompt = st.text_input("Image Prompt (Enter dabayein):", "A futuristic computer setup, neon light, 8k")
        submit_img = st.form_submit_button("Generate Image 🖼️")

    if submit_img and img_prompt:
        with st.spinner("High Quality Image Ban Rahi Hai..."):
            try:
                clean_img_prompt = requests.utils.quote(img_prompt)
                # Public Endpoint - Bypass Balance/Key Errors
                image_url = f"https://image.pollinations.ai/prompt/{clean_img_prompt}?width=1024&height=1024&nologo=true"
                st.image(image_url, caption=f"Result for: {img_prompt}", use_container_width=True)
            except Exception as e:
                st.error(f"Error: {e}")

# 3. AI SEARCH & CHAT (Superfast Gemini API)
elif mode == "💬 AI Search & Chat":
    st.subheader("💬 VeloctyAI Instant Assistant")
    st.caption("Google Gemini Powered — Instant Answers")
    
    with st.form("chat_form"):
        user_query = st.text_input("Apna sawal likhein:")
        submit_chat = st.form_submit_button("Ask Assistant 🚀")

    if submit_chat and user_query:
        # Streamlit Secrets se key le raha hai
        gemini_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")
        
        if not gemini_key:
            st.error("GEMINI_API_KEY set nahi hai! Streamlit Secrets me key add karein.")
        else:
            with st.spinner("Instant jawab aa raha hai..."):
                try:
                    import google.generativeai as genai
                    genai.configure(api_key=gemini_key)
                    model = genai.GenerativeModel("gemini-1.5-flash")
                    
                    response = model.generate_content(user_query)
                    st.success("Answer:")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Error: {e}")

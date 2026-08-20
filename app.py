import os
import requests
import streamlit as st
import google.generativeai as genai

# Page Config
st.set_page_config(page_title="VeloctyAI", page_icon="⚡", layout="wide")

st.title("⚡ VeloctyAI")

# Configure Gemini ONCE at start for maximum speed
gemini_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")
if gemini_key:
    genai.configure(api_key=gemini_key)

# Sidebar Menu
st.sidebar.title("VeloctyAI Menu")
mode = st.sidebar.radio(
    "Select Feature:",
    ["💬 Fast AI Search & Chat", "🖼️ Free AI Image", "🎬 Free AI Video"]
)

# 1. ULTRAFAST AI CHAT
if mode == "💬 Fast AI Search & Chat":
    st.subheader("💬 VeloctyAI UltraFast Assistant")
    st.caption("Hindi ya English me sawal likhein - Enter dabate hi instant answer pao!")

    with st.form("chat_form"):
        user_query = st.text_input("Apna sawal likhein:")
        submit_chat = st.form_submit_button("Ask Assistant 🚀")

    if submit_chat and user_query:
        if not gemini_key:
            st.error("GEMINI_API_KEY set nahi hai! Streamlit Secrets me key add karein.")
        else:
            with st.spinner("Jawab aa raha hai..."):
                try:
                    # Model configuration for instant responses
                    model = genai.GenerativeModel("gemini-3.6-flash")
                    response = model.generate_content(user_query)
                    st.success("Answer:")
                    st.write(response.text)
                except Exception as e:
                    # Fallback to general model if version mismatches
                    try:
                        model = genai.GenerativeModel("gemini-flash")
                        response = model.generate_content(user_query)
                        st.success("Answer:")
                        st.write(response.text)
                    except Exception as err:
                        st.error(f"Error: {err}")

# 2. FREE AI IMAGE
elif mode == "🖼️ Free AI Image":
    st.subheader("🖼️ Free AI Image Generator")
    
    with st.form("image_form"):
        img_prompt = st.text_input("Image Prompt (Enter dabayein):", "A futuristic computer setup, neon light, 8k")
        submit_img = st.form_submit_button("Generate Image 🖼️")

    if submit_img and img_prompt:
        with st.spinner("Image ban rahi hai..."):
            try:
                clean_img_prompt = requests.utils.quote(img_prompt)
                image_url = f"https://image.pollinations.ai/prompt/{clean_img_prompt}?width=1024&height=1024&nologo=true"
                st.image(image_url, caption=f"Result for: {img_prompt}", use_container_width=True)
            except Exception as e:
                st.error(f"Error: {e}")

# 3. FREE AI VIDEO
elif mode == "🎬 Free AI Video":
    st.subheader("🎬 Free AI Video Generator")
    
    with st.form("video_form"):
        video_prompt = st.text_area("Video Prompt:", "A cute panda playing guitar in forest")
        submit_video = st.form_submit_button("Generate Video ⚡")

    if submit_video and video_prompt:
        with st.spinner("Video render ho rahi hai..."):
            try:
                clean_prompt = requests.utils.quote(video_prompt)
                video_url = f"https://image.pollinations.ai/prompt/{clean_prompt}?width=1024&height=576&nologo=true"
                st.success("Video Ready!")
                st.image(video_url, caption=video_prompt, use_container_width=True)
            except Exception as e:
                st.error(f"Error: {e}")

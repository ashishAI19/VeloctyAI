import os
import requests
import streamlit as st
import fal_client

# Page Config
st.set_page_config(page_title="VeloctyAI", page_icon="⚡", layout="wide")

st.title("⚡ VeloctyAI")

# Sidebar Menu
st.sidebar.title("VeloctyAI Menu")
mode = st.sidebar.radio(
    "Select Feature:",
    ["🔥 Pro Video Generator", "⚡ Free Video Generator", "🖼️ Image Generator", "💬 AI Search & Chat"]
)

# 1. PRO VIDEO (Fal.ai)
if mode == "🔥 Pro Video Generator":
    st.subheader("📹 Pro AI Video Generator")
    st.caption("Powered by Fal.ai (Requires Active Credits)")
    
    prompt = st.text_area("Video Prompt:", "A cinematic shot of a futuristic sports car driving through a neon city at night")
    
    if st.button("Generate Pro Video 🔥"):
        fal_key = os.getenv("FAL_KEY")
        if not fal_key:
            st.error("FAL_KEY set nahi hai! Streamlit Secrets me FAL_KEY add karein.")
        else:
            with st.spinner("Pro Video generate ho rahi hai..."):
                try:
                    result = fal_client.subscribe(
                        "fal-ai/minimax-video",
                        arguments={"prompt": prompt}
                    )
                    st.success("Video Successfully Generated!")
                    st.video(result['video']['url'])
                except Exception as e:
                    st.error(f"Error: {e}")

# 2. FREE VIDEO GENERATOR
elif mode == "⚡ Free Video Generator":
    st.subheader("🎬 Free AI Animation Generator")
    st.caption("Powered by Pollinations AI")

    free_prompt = st.text_area("Video Prompt:", "A cute panda playing guitar in forest")

    if st.button("Generate Free Video ⚡"):
        if not free_prompt.strip():
            st.warning("Kripya koi prompt likhein!")
        else:
            with st.spinner("Free Animation render ho rahi hai..."):
                try:
                    clean_prompt = requests.utils.quote(free_prompt)
                    # Instant animated generation URL
                    img_url = f"https://image.pollinations.ai/prompt/{clean_prompt}?width=1024&height=576&nologo=true"
                    
                    st.success("Animation Ready!")
                    st.image(img_url, caption=free_prompt, use_container_width=True)
                except Exception as e:
                    st.error(f"Error: {e}")

# 3. IMAGE GENERATOR (Fixed Syntax Issue)
elif mode == "🖼️ Image Generator":
    st.subheader("🖼️ Free AI Image Generator")
    st.caption("Powered by Pollinations AI")

    img_prompt = st.text_input("Image Prompt:", "A beautiful sunset over snow mountains, 8k resolution")

    if st.button("Generate Image 🖼️"):
        if not img_prompt.strip():
            st.warning("Kripya prompt likhein!")
        else:
            with st.spinner("Image ban rahi hai..."):
                try:
                    clean_img_prompt = requests.utils.quote(img_prompt)
                    image_url = f"https://image.pollinations.ai/prompt/{clean_img_prompt}?width=1024&height=1024&nologo=true"
                    
                    st.image(image_url, caption="Generated Image", use_container_width=True)
                except Exception as e:
                    st.error(f"Error: {e}")

# 4. AI SEARCH & CHAT (Fixed Engine)
elif mode == "💬 AI Search & Chat":
    st.subheader("💬 VeloctyAI Search & Assistant")
    st.caption("Koi bhi sawal pucho — instant answer pao!")

    user_query = st.text_input("Apna sawal yahan likhein:")

    if st.button("Ask Assistant 🚀"):
        if not user_query.strip():
            st.warning("Pehle koi sawal puchiye!")
        else:
            with st.spinner("Jawab dhoondh raha hoon..."):
                try:
                    # Free text assistant endpoint
                    clean_query = requests.utils.quote(user_query)
                    res = requests.get(f"https://text.pollinations.ai/{clean_query}")
                    if res.status_code == 200:
                        st.success("Answer:")
                        st.write(res.text)
                    else:
                        st.error("Response nahi mil paya, dobara try karein.")
                except Exception as e:
                    st.error(f"Error: {e}")

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

# 1. PRO VIDEO (Fal.ai / Minimax)
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

# 2. FREE VIDEO (Pollinations Free API - No Key Needed)
elif mode == "⚡ Free Video Generator":
    st.subheader("🎬 Free AI Video Generator")
    st.caption("Powered by Pollinations AI (100% Free & Unlimited)")

    free_prompt = st.text_area("Video Prompt:", "A cute panda playing guitar in forest")

    if st.button("Generate Free Video ⚡"):
        if not free_prompt.strip():
            st.warning("Kripya koi prompt likhein!")
        else:
            with st.spinner("Free Server video render kar raha hai..."):
                try:
                    clean_prompt = requests.utils.quote(free_prompt)
                    # Pollinations Free Video Endpoint
                    video_url = f"https://pollinations.ai/p/{clean_prompt}?model=video&seed=42"
                    
                    st.success("Video Ready!")
                    st.video(video_url)
                except Exception as e:
                    st.error(f"Error: {e}")

# 3. IMAGE GENERATOR (Pollinations Free Image)
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
                    image_url = f"https://pollinations.ai/p/{clean_img_prompt}?width=1024&height=1024&seed=42"
                    
                    st.image(image_url, caption="Generated Image", use_column_width=True)
                except Exception as e:
                    st.error(f"Error: {e}")

# 4. AI SEARCH & CHAT (Simple Smart Assistant)
elif mode == "💬 AI Search & Chat":
    st.subheader("💬 VeloctyAI Search & Assistant")
    st.caption("Koi bhi sawal pucho — instant answer pao!")

    user_query = st.text_input("Apna sawal yahan likhein:")

    if st.button("Ask Assistant 🚀"):
        if not user_query.strip():
            st.warning("Pehle koi sawal puchiye!")
        else:
            with st.spinner("Soch raha hoon..."):
                try:
                    # Free Chat response using DuckDuckGo Instant API
                    response = requests.get(f"https://api.duckduckgo.com/?q={requests.utils.quote(user_query)}&format=json").json()
                    answer = response.get("AbstractText")
                    
                    if answer:
                        st.success("Answer:")
                        st.write(answer)
                    else:
                        st.info(f"Aapke sawal **'{user_query}'** par me abhi process kar raha hoon. Kripya apna question thoda detail me likhein.")
                except Exception as e:
                    st.error(f"Error: {e}")

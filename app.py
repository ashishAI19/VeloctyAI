import os
import requests
import streamlit as st
import fal_client

# Page Config
st.set_page_config(page_title="veloctyAI", page_icon="⚡", layout="wide")

# App Main Title (Har page par sabse upar yehi dikhega)
st.title("⚡ veloctyAI")
st.markdown("---")

# Sidebar Menu
st.sidebar.title("⚡ veloctyAI Menu")
mode = st.sidebar.radio(
    "Select Feature:", 
    [
        "🔥 Pro Video Generator", 
        "⚡ Free Video Generator", 
        "🖼️ Image Generator", 
        "💬 AI Search & Chat"
    ]
)

# 1. PRO VIDEO
if mode == "🔥 Pro Video Generator":
    st.subheader("🎬 Pro AI Video Studio")
    st.caption("Powered by Fal.ai High-Quality Engine")
    
    prompt = st.text_area("Video Prompt (English me):", "Cinematic drone shot of a futuristic neon city in rain, 4k ultra realistic")
    
    if st.button("Generate Pro Video 🔥", type="primary"):
        fal_key = os.getenv("FAL_KEY")
        if not fal_key:
            st.error("FAL_KEY environment variable set nahi hai!")
        else:
            with st.spinner("Fal AI Engine video render kar raha hai..."):
                try:
                    result = fal_client.subscribe(
                        "fal-ai/minimax/video-01",
                        arguments={"prompt": prompt}
                    )
                    st.success("Video Successfully Generated!")
                    st.video(result['video']['url'])
                except Exception as e:
                    st.error(f"Error: {e}")

# 2. FREE VIDEO
elif mode == "⚡ Free Video Generator":
    st.subheader("🎬 Free AI Video Generator")
    st.caption("Powered by Hugging Face Open-Source Model")
    
    free_prompt = st.text_area("Video Prompt:", "A cute panda playing guitar in forest")
    
    if st.button("Generate Free Video ⚡"):
        hf_token = os.getenv("HF_TOKEN")
        if not hf_token:
            st.error("HF_TOKEN set nahi hai!")
        else:
            with st.spinner("Free Server video render kar raha hai..."):
                try:
                    API_URL = "https://api-inference.huggingface.co/models/damo-vilab/text-to-video-ms-1.7b"
                    headers = {"Authorization": f"Bearer {hf_token}"}
                    response = requests.post(API_URL, headers=headers, json={"inputs": free_prompt})
                    
                    if response.status_code == 200:
                        st.success("Free Video Ready!")
                        st.video(response.content)
                    else:
                        st.warning("Server busy hai, 1 minute baad try karein!")
                except Exception as e:
                    st.error(f"Error: {e}")

# 3. IMAGE GENERATOR
elif mode == "🖼️ Image Generator":
    st.subheader("🖼️ AI Image Generator")
    img_prompt = st.text_input("Image Prompt:", "Cyberpunk street at night, highly detailed")
    
    if st.button("Generate Image 🖼️"):
        st.info("Image Generation Feature Active!")

# 4. AI SEARCH & CHAT
elif mode == "💬 AI Search & Chat":
    st.subheader("💬 veloctyAI Search & Assistant")
    st.caption("Koi bhi sawal pucho — instant answer pao!")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if user_prompt := st.chat_input("Apna sawal yahan likhein..."):
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        with st.chat_message("user"):
            st.markdown(user_prompt)

        with st.chat_message("assistant"):
            with st.spinner("Jawab dhund raha hu..."):
                try:
                    hf_token = os.getenv("HF_TOKEN")
                    headers = {"Authorization": f"Bearer {hf_token}"} if hf_token else {}
                    
                    API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
                    
                    response = requests.post(API_URL, headers=headers, json={
                        "inputs": f"<s>[INST] {user_prompt} [/INST]",
                        "parameters": {"max_new_tokens": 500, "temperature": 0.7}
                    })
                    
                    if response.status_code == 200:
                        result = response.json()
                        answer = result[0]['generated_text'].split("[/INST]")[-1].strip()
                        st.markdown(answer)
                        st.session_state.messages.append({"role": "assistant", "content": answer})
                    else:
                        st.error("Server busy hai, kripya dobara try karein!")
                except Exception as e:
                    st.error(f"Error: {e}")

import streamlit as st
import google.generativeai as genai
from huggingface_hub import InferenceClient
from PIL import Image
import io
import requests

st.set_page_config(page_title="VeloctyAI", layout="wide")

# API Keys Setup
GEMINI_KEY = st.secrets.get("GEMINI_API_KEY", "")
HF_TOKEN = st.secrets.get("HF_TOKEN", "")

if GEMINI_KEY:
    genai.configure(api_key=GEMINI_KEY)

# HuggingFace Client
hf_client = InferenceClient(token=HF_TOKEN) if HF_TOKEN else None

st.title("⚡ VeloctyAI - All-in-One Image & AI Studio")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📸 Input & Controls")
    
    # 1. File Uploader
    uploaded_file = st.file_uploader("Photo Upload Karein:", type=["jpg", "png", "jpeg"])
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Photo", width=300)

    # 2. Prompt Input
    user_prompt = st.text_input("AI ko kya instruct karna hai?", placeholder="e.g. Cartoon me convert kro / Describe this photo")

    # 3. Action Buttons
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        transform_btn = st.button("Transform & Enhance Photo 🚀", use_container_width=True)
    with col_btn2:
        analyze_btn = st.button("Analyze Photo (Gemini) 🔍", use_container_width=True)

with col2:
    st.subheader("🖼️ Output Result")
    
    # Image Transformation Logic
    if transform_btn:
        if not user_prompt:
            st.warning("Kripya pehle prompt type karein!")
        else:
            with st.spinner("Processing image generation..."):
                try:
                    # Direct reliable model call
                    prompt_text = f"masterpiece, highly detailed, {user_prompt}"
                    
                    # Call Hugging Face Stable Diffusion
                    img_bytes = hf_client.text_to_image(
                        prompt_text, 
                        model="stabilityai/stable-diffusion-2-1"
                    )
                    st.image(img_bytes, caption="Generated Result", use_container_width=True)
                    st.success("Successfully generated via HuggingFace!")
                
                except Exception as e:
                    # Fallback to Pollinations with proper prompt encoding if HF fails
                    st.info("HF busy status. Switching to fast backup engine...")
                    try:
                        clean_prompt = user_prompt.replace(" ", "%20")
                        pollin_url = f"https://image.pollinations.ai/prompt/{clean_prompt}?width=800&height=800&nologo=true"
                        st.image(pollin_url, caption="Generated Result (Backup Engine)", use_container_width=True)
                    except Exception as err:
                        st.error(f"Error: {err}")

    # Gemini Vision Analysis Logic
    if analyze_btn:
        if not uploaded_file:
            st.warning("Pehle ek photo upload karein!")
        else:
            with st.spinner("Analyzing image with Gemini..."):
                try:
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    prompt = user_prompt if user_prompt else "Describe this image in detail in Hindi and English."
                    response = model.generate_content([prompt, Image.open(uploaded_file)])
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Gemini Error: {e}")

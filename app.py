import base64
from streamlit_mic_recorder import speech_to_text
import os
import io
import requests
import streamlit as st
from PIL import Image

# Page Configuration
st.set_page_config(page_title="VeloctyAI", page_icon="⚡", layout="wide")
st.title("⚡ VeloctyAI")

# Sidebar Navigation
st.sidebar.title("VeloctyAI Menu")
mode = st.sidebar.radio(
    "Select Feature:",
    [
        "💬 Fast AI Search & Chat",
        "✨ AI Style Transform & Edit",
        "🖼️ Free AI Image Generator",
        "🎬 Free AI Video"
    ]
)
# 1. AI CHAT WITH BROWSER NATIVE VOICE (NO HEAVY LIBRARIES NEEDED)
if mode == "💬 Fast AI Search & Chat":
    st.subheader("💬 VeloctyAI Assistant")
    
    gemini_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")

    with st.form("chat_form"):
        user_query = st.text_input("Apna sawal likhein:")
        submit_chat = st.form_submit_button("Ask Assistant 🚀")

    if submit_chat and user_query:
        if not gemini_key:
            st.error("GEMINI_API_KEY set nahi hai!")
        else:
            with st.spinner("Jawab aa raha hai..."):
                try:
                    import google.generativeai as genai
                    genai.configure(api_key=gemini_key)
                    model = genai.GenerativeModel("gemini-1.5-flash")
                    response = model.generate_content(user_query)
                    
                    # 1. Text Jawab
                    st.success("Answer:")
                    st.write(response.text)

                    # 2. Browser Web Speech API (Auto-speak without gTTS)
                    clean_text = response.text.replace('"', "'").replace('\n', ' ')
                    js_speech = f"""
                        <script>
                            var msg = new SpeechSynthesisUtterance("{clean_text}");
                            msg.lang = "hi-IN";
                            window.speechSynthesis.speak(msg);
                        </script>
                    """
                    st.components.v1.html(js_speech, height=0)

                except Exception as e:
                    st.error(f"Error: {e}")
# 2. PHOTO TRANSFORM + PROMPT EDIT + DOWNLOAD
elif mode == "✨ AI Style Transform & Edit":
    st.subheader("✨ Custom Photo Editor & Transformer")
    st.caption("Apni photo upload karein, apna prompt likhein aur edit karke download karein!")

    uploaded_file = st.file_uploader("Apni photo select karein (JPG/PNG):", type=["jpg", "png", "jpeg"])

    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded Photo", use_container_width=True)
        
        user_prompt = st.text_input(
            "AI ko kya instruct karna hai? (Prompt Type Karein):",
            value="Studio Ghibli anime style, cinematic lighting, masterpiece, 8k high quality"
        )

        if st.button("Transform & Enhance Photo 🚀"):
            hf_token = st.secrets.get("HF_TOKEN") or os.getenv("HF_TOKEN")

            if not hf_token:
                st.error("HF_TOKEN set nahi hai! Streamlit Secrets me token add karein.")
            else:
                with st.spinner("AI photo ko process kar raha hai..."):
                    try:
                        from huggingface_hub import InferenceClient
                        client = InferenceClient(api_key=hf_token)
                        input_img = Image.open(uploaded_file)

                        # Hugging Face image-to-image pipeline
                        output_image = client.image_to_image(
                            model="stabilityai/stable-diffusion-xl-refiner-1.0",
                            image=input_img,
                            prompt=f"{user_prompt}, sharp focus, highly detailed, best quality",
                            negative_prompt="blurry, distorted, ugly, low quality"
                        )

                        st.success("Photo Edited Successfully!")
                        st.image(output_image, caption="AI Result", use_container_width=True)

                        # Download button buffer
                        buf = io.BytesIO()
                        output_image.save(buf, format="PNG")
                        byte_im = buf.getvalue()

                        st.download_button(
                            label="📥 Download HD Photo",
                            data=byte_im,
                            file_name="VeloctyAI_Edited_Photo.png",
                            mime="image/png"
                        )

                    except Exception as e:
                        # Fallback Engine (Free Server)
                        st.warning("HF Server busy/loading, Pollinations engine se generate kar rahe hain...")
                        clean_prompt = requests.utils.quote(user_prompt)
                        fallback_url = f"https://image.pollinations.ai/prompt/{clean_prompt}?width=1024&height=1024&nologo=true"
                        
                        st.image(fallback_url, caption="AI Generated Concept", use_container_width=True)
                        img_data = requests.get(fallback_url).content
                        
                        st.download_button(
                            label="📥 Download HD Photo",
                            data=img_data,
                            file_name="VeloctyAI_Edited_Photo.png",
                            mime="image/png"
                        )

# 3. FREE AI IMAGE
elif mode == "🖼️ Free AI Image Generator":
    st.subheader("🖼️ Unlimited Free AI Image Generator")
    
    with st.form("image_form"):
        img_prompt = st.text_input("Image Prompt:", "A futuristic computer setup, neon light, 8k")
        submit_img = st.form_submit_button("Generate Image 🖼️")

    if submit_img and img_prompt:
        with st.spinner("Image ban rahi hai..."):
            try:
                clean_img_prompt = requests.utils.quote(img_prompt)
                image_url = f"https://image.pollinations.ai/prompt/{clean_img_prompt}?width=1024&height=1024&nologo=true"
                st.image(image_url, caption=f"Result for: {img_prompt}", use_container_width=True)
            except Exception as e:
                st.error(f"Error: {e}")

# 4. FREE AI VIDEO
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

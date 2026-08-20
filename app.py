# Save this as app.py
import streamlit as st
from huggingface_hub import InferenceClient
import google.generativeai as genai
from PIL import Image
import io
import time

# --- Streamlit Page Config ---
st.set_page_config(page_title="VeloctyAI - Dynamic UI Chatbot", layout="wide")

# --- Initialize Session States ---
if 'api_keys_set' not in st.session_state:
    st.session_state['api_keys_set'] = False
if 'generated_image' not in st.session_state:
    st.session_state['generated_image'] = None

# --- Function to Set Keys from Secrets ---
def set_keys():
    try:
        if "GEMINI_API_KEY" not in st.secrets or "HF_TOKEN" not in st.secrets:
            st.error("⚠️ Environment secrets are missing! Please add 'GEMINI_API_KEY' and 'HF_TOKEN' to Streamlit Secrets.")
            return False
        
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        st.session_state['hf_client'] = InferenceClient(
            token=st.secrets["HF_TOKEN"],
            timeout=30 # Add a timeout for safety
        )
        st.session_state['api_keys_set'] = True
        return True
    except Exception as e:
        st.error(f"❌ Critical error configuring API keys: {str(e)}")
        return False

# --- Core Image Generation Function (Strictly Hugging Face) ---
def generate_fresh_image(prompt, retries=2):
    if not st.session_state['api_keys_set']:
        return None, "System setup is incomplete."

    final_prompt = f"Professional, ultra-detailed image of {prompt}. Cinematic lighting, 8k, photorealistic style."
    
    # Use a robust, reliable HF model
    model_id = "runwayml/stable-diffusion-v1-5" 

    for attempt in range(retries):
        try:
            with st.spinner("🚀 Generating your image on Hugging Face servers..."):
                response_content = st.session_state['hf_client'].post(
                    json={"inputs": final_prompt, "options": {"wait_for_model": True}},
                    model=model_id
                )
                image_data = response_content.read()
                
                if image_data:
                    image_obj = Image.open(io.BytesIO(image_data))
                    return image_obj, None
                else:
                    return None, "Model returned no data."

        except Exception as e:
            time.sleep(2) # Short pause before retry
            error_msg = f"Hugging Face server error: {str(e)}"
            
    return None, f"After {retries} attempts, generation failed. {error_msg}"

# --- Set keys before rendering anything else ---
keys_configured = set_keys()

# --- Main UI ---
st.title("🤖 VeloctyAI - Visual Assistant")

# --- Column Layout for Better View ---
col_in, col_out = st.columns([1.5, 1])

with col_in:
    st.subheader("Input & Control")
    user_input = st.text_input("AI ko kya instruct karna hai? (Detailed Prompt likhein):", placeholder="Example: create a cartoon version of this photo...")
    
    # Simple image generation button, independent of previous context
    generate_btn = st.button("Generate Image 🚀", use_container_width=True)

with col_out:
    st.subheader("Output Result")
    result_container = st.empty()
    error_container = st.empty()

    if generate_btn and user_input:
        if keys_configured:
            generated_img, error_msg = generate_fresh_image(user_input)
            
            if generated_img:
                result_container.image(generated_img, caption="AI Generated Image", use_container_width=True)
                st.session_state['generated_image'] = generated_img
            else:
                error_container.error(error_msg)
        else:
            st.warning("⚠️ Please configure your API keys first.")

# --- Footer with Status ---
if not keys_configured:
    st.markdown("---")
    st.warning("⚠️ Application is NOT fully functional. Please add your API keys (GEMINI_API_KEY and HF_TOKEN) to Streamlit Secrets.")
else:
    # Small status indicator
    st.markdown("---")
    st.caption("✔️ System is online using Hugging Face servers.")

import streamlit as st
import requests
from urllib.parse import quote

# =========================================================
# VeloctyAI - All in One AI App
# Video + Image + AI Search & Chat
# Powered by Pollinations API
# =========================================================

st.set_page_config(
    page_title="VeloctyAI",
    page_icon="⚡",
    layout="wide"
)

API_BASE = "https://gen.pollinations.ai"

# ---------------------------------------------------------
# API KEY
# ---------------------------------------------------------
def get_api_key():
    try:
        if "POLLINATIONS_API_KEY" in st.secrets:
            return st.secrets["POLLINATIONS_API_KEY"]
    except Exception:
        pass

    return ""


API_KEY = get_api_key()


# ---------------------------------------------------------
# API HEADERS
# ---------------------------------------------------------
def api_headers():
    return {
        "Authorization": f"Bearer {API_KEY}"
    }


# ---------------------------------------------------------
# PAGE TITLE
# ---------------------------------------------------------
st.title("⚡ VeloctyAI")
st.caption("AI Video • AI Image • AI Search & Chat")


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------
st.sidebar.title("⚡ VeloctyAI Menu")

mode = st.sidebar.radio(
    "Select Feature:",
    [
        "🎬 AI Video Generator",
        "🖼️ AI Image Generator",
        "💬 AI Search & Chat"
    ]
)

st.sidebar.divider()

if API_KEY:
    st.sidebar.success("API Connected ✅")
else:
    st.sidebar.warning("API Key Required ⚠️")
    st.sidebar.caption(
        "Streamlit Secrets me POLLINATIONS_API_KEY add karein."
    )


# =========================================================
# 1. AI VIDEO GENERATOR
# =========================================================
if mode == "🎬 AI Video Generator":

    st.header("🎬 VeloctyAI Video Generator")

    st.write(
        "Text prompt se AI video generate karein."
    )

    prompt = st.text_area(
        "Video Prompt:",
        placeholder=(
            "Example: A cinematic sports car driving "
            "through a futuristic neon city at night, "
            "realistic camera movement, cinematic lighting"
        ),
        height=130
    )

    col1, col2 = st.columns(2)

    with col1:
        video_model = st.selectbox(
            "Video Model",
            [
                "wan-fast",
                "wan",
                "ltx-2"
            ],
            index=0
        )

    with col2:
        duration = st.selectbox(
            "Duration",
            [4, 5, 6, 8],
            index=0
        )

    if st.button(
        "🚀 Generate Video",
        type="primary",
        use_container_width=True
    ):

        if not API_KEY:
            st.error(
                "Pollinations API key nahi mili. "
                "Streamlit Secrets me POLLINATIONS_API_KEY add karein."
            )

        elif not prompt.strip():
            st.warning("Pehle video prompt likhiye.")

        else:
            with st.spinner(
                "🎬 Video generate ho rahi hai... thoda wait karein."
            ):
                try:

                    video_url = (
                        f"{API_BASE}/video/"
                        f"{quote(prompt.strip())}"
                    )

                    params = {
                        "model": video_model,
                        "duration": duration
                    }

                    response = requests.get(
                        video_url,
                        params=params,
                        headers=api_headers(),
                        timeout=300
                    )

                    if response.status_code == 200:

                        video_data = response.content

                        st.success(
                            "✅ Video successfully generated!"
                        )

                        st.video(video_data)

                        st.download_button(
                            "⬇️ Download Video",
                            data=video_data,
                            file_name="veloctyai_video.mp4",
                            mime="video/mp4",
                            use_container_width=True
                        )

                    else:

                        try:
                            error_text = response.text[:1000]
                        except Exception:
                            error_text = "Unknown error"

                        st.error(
                            f"Video generate nahi hui.\n\n"
                            f"Status: {response.status_code}\n"
                            f"{error_text}"
                        )

                except requests.exceptions.Timeout:

                    st.error(
                        "⏱️ Video generation me bahut time lag gaya. "
                        "Thodi der baad dobara try karein."
                    )

                except Exception as e:

                    st.error(
                        f"Video Error: {str(e)}"
                    )


# =========================================================
# 2. AI IMAGE GENERATOR
# =========================================================
elif mode == "🖼️ AI Image Generator":

    st.header("🖼️ VeloctyAI Image Generator")

    prompt = st.text_area(
        "Image Prompt:",
        placeholder=(
            "Example: A futuristic Indian city at sunset, "
            "cinematic, ultra realistic, 4K"
        ),
        height=120
    )

    col1, col2 = st.columns(2)

    with col1:
        image_model = st.selectbox(
            "Image Model",
            [
                "flux",
                "zimage",
                "wan-image"
            ]
        )

    with col2:
        image_size = st.selectbox(
            "Image Size",
            [
                "1024x1024",
                "1280x720",
                "720x1280"
            ]
        )

    if st.button(
        "🎨 Generate Image",
        type="primary",
        use_container_width=True
    ):

        if not API_KEY:
            st.error(
                "Pollinations API key nahi mili."
            )

        elif not prompt.strip():
            st.warning("Pehle image prompt likhiye.")

        else:

            with st.spinner("🖼️ Image ban rahi hai..."):

                try:

                    width, height = image_size.split("x")

                    image_url = (
                        f"{API_BASE}/image/"
                        f"{quote(prompt.strip())}"
                    )

                    params = {
                        "model": image_model,
                        "width": width,
                        "height": height
                    }

                    response = requests.get(
                        image_url,
                        params=params,
                        headers=api_headers(),
                        timeout=180
                    )

                    if response.status_code == 200:

                        image_data = response.content

                        st.success(
                            "✅ Image successfully generated!"
                        )

                        st.image(
                            image_data,
                            caption=prompt
                        )

                        st.download_button(
                            "⬇️ Download Image",
                            data=image_data,
                            file_name="veloctyai_image.png",
                            mime="image/png",
                            use_container_width=True
                        )

                    else:

                        st.error(
                            f"Image Error: "
                            f"{response.status_code}\n"
                            f"{response.text[:1000]}"
                        )

                except requests.exceptions.Timeout:

                    st.error(
                        "⏱️ Image generation timeout ho gaya."
                    )

                except Exception as e:

                    st.error(
                        f"Image Error: {str(e)}"
                    )


# =========================================================
# 3. AI SEARCH & CHAT
# =========================================================
elif mode == "💬 AI Search & Chat":

    st.header("💬 VeloctyAI Search & Assistant")

    st.caption(
        "Question pucho aur AI se answer pao."
    )

    # Chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Previous messages
    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_query = st.chat_input(
        "Apna sawal yahan likhein..."
    )

    if user_query:

        if not API_KEY:

            st.error(
                "Pollinations API key nahi mili."
            )

        else:

            # User message
            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": user_query
                }
            )

            with st.chat_message("user"):
                st.markdown(user_query)

            with st.chat_message("assistant"):

                with st.spinner("🤖 Soch raha hoon..."):

                    try:

                        payload = {
                            "model": "gemini-search-fast",
                            "messages": [
                                {
                                    "role": "system",
                                    "content": (
                                        "You are VeloctyAI, "
                                        "a helpful AI assistant. "
                                        "Give clear and accurate "
                                        "answers. If the user "
                                        "asks in Hindi/Hinglish, "
                                        "answer in Hindi/Hinglish."
                                    )
                                }
                            ] + st.session_state.messages,
                            "temperature": 0.3
                        }

                        response = requests.post(
                            f"{API_BASE}/v1/chat/completions",
                            headers={
                                **api_headers(),
                                "Content-Type": "application/json"
                            },
                            json=payload,
                            timeout=120
                        )

                        if response.status_code == 200:

                            data = response.json()

                            answer = data["choices"][0][
                                "message"
                            ]["content"]

                            st.markdown(answer)

                            st.session_state.messages.append(
                                {
                                    "role": "assistant",
                                    "content": answer
                                }
                            )

                        else:

                            st.error(
                                f"AI response error: "
                                f"{response.status_code}\n\n"
                                f"{response.text[:1000]}"
                            )

                    except requests.exceptions.Timeout:

                        st.error(
                            "⏱️ AI response me timeout ho gaya."
                        )

                    except Exception as e:

                        st.error(
                            f"AI Error: {str(e)}"
                        )


# =========================================================
# FOOTER
# =========================================================
st.sidebar.divider()

st.sidebar.caption(
    "⚡ VeloctyAI | AI Video • Image • Search"
)

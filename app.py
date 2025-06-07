# app.py

import streamlit as st
from voicebot_utils import (
    record_audio_to_text,
    translate_text,
    get_chatgpt_response,
    generate_tts_audio
)
from pydub import AudioSegment
from io import BytesIO

st.set_page_config(page_title="🎤 AI Voice Chat", layout="centered")
st.title("🌍 AI Chatbot Translator")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "You are a helpful multilingual assistant."}]
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if st.button("🎙️ Speak"):
    text = record_audio_to_text()
    if text.startswith("[Error]"):
        st.error(text)
    else:
        st.success(f"You said: `{text}`")
        translated, src_lang = translate_text(text)
        st.info(f"Translated: `{translated}`")

        response, st.session_state.messages = get_chatgpt_response(translated, st.session_state.messages)
        back_translated, _ = translate_text(response, dest=src_lang)
        st.success(f"🤖 ChatGPT: `{back_translated}`")

        st.session_state.chat_history.append((text, back_translated))

        tts_path = generate_tts_audio(back_translated, src_lang)
        audio = AudioSegment.from_file(tts_path)
        audio_bytes = BytesIO()
        audio.export(audio_bytes, format="wav")
        st.audio(audio_bytes, format="audio/wav")
        os.remove(tts_path)

# Show history
if st.session_state.chat_history:
    st.subheader("Conversation History")
    for user, bot in reversed(st.session_state.chat_history):
        st.markdown(f"**You**: {user}")
        st.markdown(f"**Bot**: {bot}")

import streamlit as st
import openai
import tempfile
import os

from voice_utils import (
    transcribe_audio_file,
    translate_text,
    get_chatgpt_response,
    translate_back,
    synthesize_speech,
)

openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="AI Chat Translator", layout="centered")
st.title("🌍 AI Chatbot Translator with Voice")
st.markdown("Upload your voice in any language, and talk to an AI that replies in your language.")

uploaded_file = st.file_uploader("🎤 Upload a voice file (.wav)", type=["wav"])

if uploaded_file:
    st.audio(uploaded_file, format="audio/wav")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_audio:
        tmp_audio.write(uploaded_file.read())
        tmp_audio_path = tmp_audio.name

    st.info("Transcribing...")
    transcribed_text = transcribe_audio_file(tmp_audio_path)
    st.success(f"📝 Transcribed: {transcribed_text}")

    if transcribed_text and not transcribed_text.startswith("Error"):
        translated_input, source_lang = translate_text(transcribed_text, dest_lang="en")
        st.markdown(f"🌐 **Translated to English:** {translated_input} _(from {source_lang})_")

        with st.spinner("🤖 ChatGPT thinking..."):
            response_en = get_chatgpt_response(translated_input)

        st.markdown(f"💬 **ChatGPT Response (English):** {response_en}")

        response_translated = translate_back(response_en, target_lang=source_lang)
        st.markdown(f"🔁 **Response in {source_lang}:** {response_translated}")

        audio_bytes = synthesize_speech(response_translated, lang=source_lang)
        st.audio(audio_bytes, format="audio/mp3")
    else:
        st.warning("No valid transcription to proceed.")

    st.subheader("Conversation History")
    for user, bot in reversed(st.session_state.chat_history):
        st.markdown(f"**You**: {user}")
        st.markdown(f"**Bot**: {bot}")

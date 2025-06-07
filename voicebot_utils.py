# voicebot_utils.py

import openai
from googletrans import Translator
from gtts import gTTS
import os
import speech_recognition as sr
import tempfile

openai.api_key = os.getenv("OPENAI_API_KEY")

translator = Translator()

def record_audio_to_text():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source, timeout=5)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
        f.write(audio.get_wav_data())
        audio_path = f.name

    with sr.AudioFile(audio_path) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
            os.remove(audio_path)
            return text
        except Exception as e:
            os.remove(audio_path)
            return f"[Error] Could not transcribe: {e}"

def translate_text(text, dest="en"):
    trans = translator.translate(text, dest=dest)
    return trans.text, trans.src

def get_chatgpt_response(text, messages=None):
    if messages is None:
        messages = [{"role": "system", "content": "You are a helpful multilingual assistant."}]
    messages.append({"role": "user", "content": text})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    reply = response.choices[0].message.content.strip()
    messages.append({"role": "assistant", "content": reply})
    return reply, messages

def generate_tts_audio(text, lang):
    tts = gTTS(text=text, lang=lang)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tts_file:
        tts.save(tts_file.name)
        return tts_file.name

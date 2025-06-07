import os
import tempfile
from io import BytesIO
from gtts import gTTS
from googletrans import Translator
import speech_recognition as sr
import openai

# =============== Transcribe Speech ================
def transcribe_audio_file(file_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio = recognizer.record(source)
    try:
        return sr.Recognizer().recognize_google(audio)
    except sr.UnknownValueError:
        return "Could not understand audio."
    except sr.RequestError as e:
        return f"Error: {e}"

# =============== Translate Text ================
def translate_text(text, dest_lang="en"):
    translator = Translator()
    translation = translator.translate(text, dest=dest_lang)
    return translation.text, translation.src

def translate_back(text, target_lang):
    if target_lang == "en":
        return text
    translator = Translator()
    translation = translator.translate(text, dest=target_lang)
    return translation.text

# =============== ChatGPT ================
def get_chatgpt_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful multilingual assistant."},
            {"role": "user", "content": prompt},
        ]
    )
    return response.choices[0].message.content.strip()

# =============== Text-to-Speech ================
def synthesize_speech(text, lang="en"):
    tts = gTTS(text=text, lang=lang)
    mp3_fp = BytesIO()
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)
    return mp3_fp

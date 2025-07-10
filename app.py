import streamlit as st
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
from io import BytesIO
import tempfile

# Mapping language names to codes
LANGUAGE_CODES = {
    "Hindi": "hi", "Tamil": "ta", "Telugu": "te", "Malayalam": "ml",
    "Kannada": "kn", "Bengali": "bn", "Gujarati": "gu", "Marathi": "mr",
    "Punjabi": "pa", "Odia": "or", "Urdu": "ur", "Assamese": "as"
}

# Convert speech to text
def speech_to_text(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio, language="en-IN")
    except sr.UnknownValueError:
        return "Could not understand the audio."
    except sr.RequestError:
        return "Google Speech API request failed."

# Translate text
def translate_text(text, target_lang):
    translator = Translator()
    translated = translator.translate(text, dest=target_lang)
    return translated.text

# Convert text to speech
def text_to_speech(text, lang_code):
    tts = gTTS(text=text, lang=lang_code)
    fp = BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    return fp

# Main app
def main():
    st.title("🎙️ Voice Translator for Indian Languages")

    st.subheader("Step 1: Upload a WAV audio file")
    audio_file = st.file_uploader("Upload a WAV file", type=["wav"])

    if audio_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
            tmp_file.write(audio_file.read())
            tmp_path = tmp_file.name

        st.success("✅ Audio uploaded successfully!")

        # Convert audio to text
        with st.spinner("📝 Transcribing audio..."):
            text = speech_to_text(tmp_path)
            st.text_area("📜 Detected English Text", text, height=100)

        st.subheader("Step 2: Choose a language for translation")
        selected_lang = st.selectbox("Select Language", list(LANGUAGE_CODES.keys()))
        lang_code = LANGUAGE_CODES[selected_lang]

        if st.button("Translate and Speak"):
            with st.spinner("🌐 Translating..."):
                translated = translate_text(text, lang_code)
                st.text_area("🌍 Translated Text", translated, height=100)

            st.subheader("🎧 Translated Voice Output")
            audio_fp = text_to_speech(translated, lang_code)
            st.audio(audio_fp, format='audio/mp3')

        st.caption("🔊 Supports 12 Indian languages using Google APIs.")

if __name__ == "__main__":
    main()

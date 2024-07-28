import streamlit as st:
import speech_recognition as sr:
from gtts import gTTS:
from pydub import AudioSegment:
from pydub.playback import play:
import tempfile:
import os:

# Initialize recognizer class (for recognizing the speech)
recognizer = sr.Recognizer()

# Function to process voice input
def process_voice(audio_file):
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)
        try:
            # Convert voice input to text
            text = recognizer.recognize_google(audio_data, language="ur-PK")
            return text
        except sr.UnknownValueError:
            return "Could not understand the audio"
        except sr.RequestError as e:
            return f"Error: {e}"

# Function to convert text to speech
def text_to_speech(text, lang="ur"):
    tts = gTTS(text=text, lang=lang, slow=False)
    return tts

# Streamlit interface
st.title("Urdu Voice Input and Output Application")
st.write("Please record your voice in Urdu and get a response in Urdu voice.")

# Record voice input
st.write("### Record your voice in Urdu")
uploaded_file = st.file_uploader("Upload an audio file", type=["wav", "mp3"])

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(uploaded_file.read())
        temp_file_path = temp_file.name

    # Process the voice input
    st.write("Processing voice input...")
    urdu_text = process_voice(temp_file_path)
    st.write(f"Recognized Text: {urdu_text}")

    # Generate a response based on the input text
    # For demonstration, let's just echo the input text as the response
    response_text = f"آپ نے کہا: {urdu_text}"

    # Convert the response text to speech
    st.write("Generating speech output...")
    tts = text_to_speech(response_text)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio_file:
        tts.save(temp_audio_file.name)
        temp_audio_path = temp_audio_file.name

    # Play the generated speech
    st.audio(temp_audio_path, format='audio/mp3')

    # Clean up temporary files
    os.remove(temp_file_path)
    os.remove(temp_audio_path)

from flask import Flask, request, render_template, Response
from google.cloud import texttospeech
from google.cloud import translate_v2 as translate
from loguru import logger
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Dictionary to map language names to their respective codes
language_codes = {
    "en": "en-US",  # English
    "es": "es-ES",  # Spanish
    "fr": "fr-FR",  # French
    "de": "de-DE",  # German
    "hi":"hi-IN"    #Hindi
    # Add more language codes as needed
}

def translate_text(text, target_language):
    translate_client = translate.Client()
    result = translate_client.translate(text, target_language=target_language)
    return result['translatedText']

def convert_text_to_speech_google_cloud(text, language_code):
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    return response.audio_content

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form['text']
        target_language = request.form['language']

        # Translate text to the target language
        translated_text = translate_text(text, target_language)

        # Get the appropriate language code for Google Cloud TTS
        language_code = language_codes[target_language]

        # Convert the translated text to speech using Google Cloud
        audio_content = convert_text_to_speech_google_cloud(translated_text, language_code)

        return Response(audio_content, mimetype="audio/mpeg")

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

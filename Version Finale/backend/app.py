from flask import Flask, request, jsonify, send_file
from flask_cors import CORS  
import os
import torch
import whisper
from TTS.api import TTS
import tempfile
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# 📌 Répertoire pour stocker les fichiers audio générés
AUDIO_DIR = "audio"
os.makedirs(AUDIO_DIR, exist_ok=True)

# 📌 Modèles TTS et Whisper (Lazy Loading)
tts_model = None
whisper_model = None
yourtts_model = None

@app.route('/')
def home():
    return "Flask API is running! Available endpoints: /tts, /stt, /s2s"

def load_tts_model():
    global tts_model
    if tts_model is None:
        print("🔄 Chargement du modèle TTS...")
        tts_model = TTS("tts_models/en/ljspeech/glow-tts", progress_bar=False).to("cpu")

def load_whisper_model():
    global whisper_model
    if whisper_model is None:
        print("🔄 Chargement du modèle Whisper...")
        whisper_model = whisper.load_model("base")

def load_yourtts_model():
    global yourtts_model
    if yourtts_model is None:
        print("🔄 Chargement du modèle YourTTS...")
        yourtts_model = TTS("tts_models/multilingual/multi-dataset/your_tts", progress_bar=False).to("cpu")

# 📌 Endpoint STT : Transcription de l'audio en texte
@app.route('/stt', methods=['POST'])
def speech_to_text():
    load_whisper_model()
    
    if 'audio' not in request.files:
        return jsonify({"error": "Aucun fichier audio reçu. Assurez-vous d'avoir activé votre micro."}), 400
    
    audio_file = request.files['audio']
    
    try:
        file_path = os.path.join(tempfile.gettempdir(), secure_filename(audio_file.filename))
        audio_file.save(file_path)

        result = whisper_model.transcribe(file_path)
        transcription = result["text"]

        return jsonify({"transcription": transcription})
    except Exception as e:
        return jsonify({"error": f"Erreur lors de la transcription : {str(e)}"}), 500

# 📌 Endpoint S2S : Clonage vocal
@app.route('/s2s', methods=['POST'])
def speech_to_speech():
    load_yourtts_model()

    if 'audio' not in request.files:
        return jsonify({"error": "Aucun fichier audio reçu"}), 400

    audio_file = request.files['audio']
    file_path = os.path.join(tempfile.gettempdir(), secure_filename(audio_file.filename))
    audio_file.save(file_path)

    output_path = os.path.join(AUDIO_DIR, "s2s_output.wav")
    yourtts_model.tts_to_file("Bonjour, ceci est un test de clonage vocal.", speaker_wav=file_path, file_path=output_path)

    return jsonify({"audio_url": f"http://127.0.0.1:5000/audio/s2s_output.wav"})



if __name__ == '__main__':
    app.run(debug=True)

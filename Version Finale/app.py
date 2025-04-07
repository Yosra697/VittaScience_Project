from flask import Flask, request, jsonify, send_file, render_template, abort
from flask_cors import CORS
import os
import torch
import whisper
from TTS.api import TTS
import tempfile
from werkzeug.utils import secure_filename
import time
import traceback
import sounddevice as sd
import numpy as np
import torchaudio
from TTS.tts.configs.xtts_config import XttsConfig, XttsAudioConfig
from TTS.config.shared_configs import BaseDatasetConfig
from TTS.tts.models.xtts import XttsArgs
import torch.serialization

torch.serialization.add_safe_globals({XttsConfig, XttsAudioConfig, BaseDatasetConfig, XttsArgs})



app = Flask(__name__)
CORS(app)

AUDIO_DIR = "audio"
os.makedirs(AUDIO_DIR, exist_ok=True)
TEMP_DIR = tempfile.gettempdir()

tts_model = None
whisper_model = None

def load_whisper_model():
    global whisper_model
    if whisper_model is None:
        print("🔄 Chargement du modèle Whisper...")
        whisper_model = whisper.load_model("base")

MODEL_CONFIG = {
    'xtts': {
        'model_name': 'tts_models/multilingual/multi-dataset/xtts_v2',
        'requires_speaker': True,
        'is_multilingual': True
    },
    'vits': {
        'model_name': 'tts_models/fr/css10/vits',
        'requires_speaker': False,
        'is_multilingual': False
    }
}

def synthesize_voice(text, model_choice, input_audio_path=None, output_path=None):
    config = MODEL_CONFIG.get(model_choice)
    print("🔧 Configuration du modèle :", config)
    if not config:
        raise ValueError("Modèle non supporté.")

    tts_model_local = TTS(model_name=config["model_name"], progress_bar=False)

    params = {
        "text": text.strip(),
        "file_path": output_path
    }

    if config["requires_speaker"]:
        if not input_audio_path:
            raise ValueError("Ce modèle nécessite un échantillon vocal.")
        params["speaker_wav"] = input_audio_path

    if config["is_multilingual"]:
        params["language"] = "fr"

    tts_model_local.tts_to_file(**params)

def record_audio(duration=5, fs=16000):
    print("🎙️ Enregistrement audio...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float32')
    sd.wait()
    audio = recording.flatten()
    if np.max(np.abs(audio)) < 0.01:
        raise ValueError("Aucun son détecté.")
    return audio

@app.route('/')
def home():
    return "Flask API is running! Available endpoints: /tts, /stt, /s2s, /record"

@app.route('/stt', methods=['POST'])
def speech_to_text():
    load_whisper_model()
    if 'audio' not in request.files:
        return jsonify({"error": "Aucun fichier audio reçu."}), 400

    audio_file = request.files['audio']
    try:
        file_path = os.path.join(tempfile.gettempdir(), secure_filename(audio_file.filename))
        audio_file.save(file_path)
        result = whisper_model.transcribe(file_path)
        return jsonify({"transcription": result["text"]})
    except Exception as e:
        return jsonify({"error": f"Erreur STT : {str(e)}"}), 500

@app.route('/record', methods=['POST'])
def record():
    print("✅ /record a bien reçu une requête POST !")
    input_audio_path = None
    try:
        model_choice = request.form.get("model_choice", "xtts")
        print("🎯 Modèle choisi :", model_choice)

        audio = record_audio()
        print("🎧 Audio enregistré !")

        input_audio_path = os.path.join(TEMP_DIR, f"input_{int(time.time())}.wav")
        torchaudio.save(input_audio_path, torch.tensor(audio).unsqueeze(0), 16000)
        print("💾 Audio sauvegardé temporairement :", input_audio_path)

        load_whisper_model()
        print("🧠 Whisper chargé")
        result = whisper_model.transcribe(input_audio_path, language="fr", fp16=False)
        transcribed_text = result["text"]
        print("✍️ Texte transcrit :", transcribed_text)

        output_filename = f"output_{int(time.time())}.wav"
        output_path = os.path.join(TEMP_DIR, output_filename)

        synthesize_voice(transcribed_text, model_choice, input_audio_path, output_path)
        print("🗣️ Synthèse vocale générée :", output_filename)

        return jsonify({
            "transcribed_text": transcribed_text,
            "output_audio": output_filename
        })

    except Exception as e:
        print("🚨 Erreur dans /record :", e)
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

    finally:
        if input_audio_path and os.path.exists(input_audio_path):
            os.remove(input_audio_path)
            print("🧹 Fichier temporaire supprimé")

@app.route('/get_audio/<path:filename>')
def get_audio(filename):
    try:
        safe_filename = os.path.basename(filename)
        file_path = os.path.join(TEMP_DIR, safe_filename)
        if not os.path.isfile(file_path):
            abort(404, description="Fichier introuvable.")
        return send_file(file_path, as_attachment=True, download_name="audio.wav")
    except Exception as e:
        app.logger.error(f"Erreur de lecture audio : {e}")
        abort(500, description="Erreur serveur.")

@app.route('/sts')
def serve_sts_page():
    return render_template("STS.html")

if __name__ == '__main__':
    app.run(debug=True)

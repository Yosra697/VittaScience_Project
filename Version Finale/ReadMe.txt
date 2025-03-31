# 🗣️ Application Text-to-Speech (TTS) et Speech-to-Text (STT)

## 📌 Description
Cette application permet de :
- **Convertir du texte en audio (TTS - Text-to-Speech)** 🎧
- **Transcrire la voix en texte (STT - Speech-to-Text)** 🎤
- **Sauvegarder les fichiers audio générés** 🗂️

Elle utilise **JavaScript** pour la synthèse vocale et l'enregistrement, et **Flask (Python)** pour gérer le traitement du son.

---

## 🚀 Fonctionnalités
✅ **Synthèse vocale (TTS)** avec choix de :
- **Langue** (`Français, Anglais, Espagnol, Arabe, Chinois`)
- **Voix** (`Homme / Femme`)
- **Hauteur (Pitch)**, **Vitesse (Rate)**, **Volume** et **Timbre**

✅ **Transcription vocale (STT)**
- Enregistrement de la voix et conversion en texte avec **Whisper (OpenAI)**

✅ **Sauvegarde des fichiers audio**
- Les audios générés sont sauvegardés et téléchargeables

✅ **Interface moderne et intuitive**
- Utilisation de **HTML + CSS + JavaScript** avec une mise en page claire et responsive

---

## ⚙️ Installation et Exécution

### 📥 **1. Cloner le projet**
```bash
git clone https://github.com/ton-repo/text-to-speech-app.git
cd text-to-speech-app


🐍 2. Installer les dépendances (Backend - Flask)
python -m venv venv
venv\Scripts\activate OU source venv/bin/activate (macOS)
pip install flask flask-cors torch whisper TTS werkzeug

▶️ 3. Lancer le serveur Flask

venv\Scripts\activate
python app.py

🌐 4. Ouvrir le projet dans le navigateur
Ouvre index.html dans ton navigateur

📌 Texte de test :
🇫🇷 Français :
"Bonjour et bienvenue sur cette application de synthèse vocale. Ce test permet de vérifier que la voix fonctionne correctement et que le texte est bien lu à haute voix."

🇬🇧 English :
"Hello and welcome to this text-to-speech application. This test ensures that the voice works correctly and that the text is properly read aloud."

🇸🇦 العربية :
"مرحبًا بكم في هذا التطبيق لتحويل النص إلى كلام. يهدف هذا الاختبار إلى التحقق من أن الصوت يعمل بشكل صحيح وأن النص يُقرأ بصوت عالٍ."
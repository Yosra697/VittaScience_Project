# 🗣️ **Application Text-to-Speech (TTS), Speech-to-Text (STT), Speech-to-Speech (STS) et Générateur Musical IA**

## 📌 **Description**
Cette application permet de :
- **Convertir du texte en audio (TTS - Text-to-Speech)** 🎧
- **Transcrire la voix en texte (STT - Speech-to-Text)** 🎤
- **Générer de la voix à partir de la parole (STS - Speech-to-Speech)** 🔄
- **Générer de la musique à partir de prompts** 🎶

Elle utilise **JavaScript** pour la synthèse vocale et l'enregistrement, **Flask (Python)** pour gérer le traitement des voix et des fichiers audio, et **Stability AI** pour générer de la musique.

---

## 🚀 **Fonctionnalités**
### ✅ **Synthèse vocale (TTS)** avec choix de :
- **Langue** (`Français, Anglais, Espagnol, Arabe, Chinois`)
- **Voix** (`Homme / Femme`)
- **Hauteur (Pitch)**, **Vitesse (Rate)**, **Volume** et **Timbre**

### ✅ **Transcription vocale (STT)**
- Enregistrement de la voix et conversion en texte avec **Whisper (OpenAI)**

### ✅ **Speech-to-Speech (STS)**
- Utilisation de modèles TTS pour transformer la parole en version clonée de voix

### ✅ **Génération musicale IA**
- Utilisation de l'API **Stability AI** pour générer de la musique à partir de descriptions textuelles, avec un choix de genres et d'ambiances.

### ✅ **Sauvegarde des fichiers audio**
- Les audios générés sont sauvegardés et téléchargeables en **MP3** ou **WAV**

### ✅ **Interface moderne et intuitive**
- Utilisation de **HTML + CSS + JavaScript** avec une mise en page claire et responsive

---

## ⚙️ **Installation et Exécution**

### 📥 **1. Cloner le projet**
```bash
git clone https://github.com/ton-repo/text-to-speech-app.git
cd text-to-speech-app

###  **2. Installer les dépendances (Backend - Flask)**
```bash
python -m venv venv
venv\Scripts\activate  # Sur Windows
source venv/bin/activate  # Sur macOS / Linux
pip install requirements.text

###  **3. Installer les dépendances (NodeJs)**
```bash
npm install 


### ▶️  **4. Lancer le serveur Flask**

1. **Ouvrir Developer Command Prompt** ou **Command Prompt** (sur Windows).
2. **Naviguer vers le répertoire de votre projet** avec la commande :
   ```bash
   cd "C:\Users\Lenovo\Desktop\Sup Galilée - Cours\Gestion du projet\VittaScience_Project\Version Finale"

3. **Lancer le serveur Flask :** avec la commande :
   ```bash
   python app.py

### ▶️  **5. Lancer le serveur Node.js**

1. **Ouvrir Developer Command Prompt** ou **Command Prompt** (sur Windows).
2. **Naviguer vers le répertoire de votre projet** avec la commande :
   ```bash
   cd "C:\Users\Lenovo\Desktop\Sup Galilée - Cours\Gestion du projet\VittaScience_Project\Version Finale\templates"
   
3. **Lancer le serveur Node.js :** avec la commande :
   ```bash
   node server.js



Cela permettra de bien expliquer comment lancer les serveurs Flask et Node.js dans deux terminaux différents.

📌 **Exemples de Texte pour la Synthèse Vocale (TTS)**

🇫🇷 **Français** :
> "Bonjour et bienvenue sur cette application de synthèse vocale. Ce test permet de vérifier que la voix fonctionne correctement et que le texte est bien lu à haute voix."

🇬🇧 **English** :
> "Hello and welcome to this text-to-speech application. This test ensures that the voice works correctly and that the text is properly read aloud."

🇸🇦 **العربية** :
> "مرحبًا بكم في هذا التطبيق لتحويل النص إلى كلام. يهدف هذا الاختبار إلى التحقق من أن الصوت يعمل بشكل صحيح وأن النص يُقرأ بصوت عالٍ."

STS:
Est-ce que tu peux m'aider à préparer mes examens ?

🎶 **Génération musicale** :
Lien pour générer les clés : 

https://platform.stability.ai/account/keys

Exemples de prompts à essayer :

- Musique chill café avec piano jazz et ambiance pluie
- Thème épique pour trailer de jeu vidéo - orchestre, chœur et percussions puissantes
- Musique de fond pour étudier
- Mélodie triste avec un violon
- Musique douce pour se détendre


sk-RmNOyZpbmb42Bt9ew5gbancxBmnRmyQ6UXUycCl8gd29hfgq ( 2 ou 3 essaie reste)



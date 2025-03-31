const speakButton = document.getElementById('speakButton');
const textArea = document.getElementById('text');
const languageSelect = document.getElementById('language');
const pitchSlider = document.getElementById('pitch');
const rateSlider = document.getElementById('rate');
const volumeSlider = document.getElementById('volume');
const voicesSelect = document.getElementById('voices');
const errorMessage = document.getElementById("error-message");
const ttsStatus = document.getElementById("tts-status");

// 🎯 Mappage des langues avec voix (Homme/Femme)
const voiceMap = {
    "en-US": { "Femme": "Microsoft Ava Online (Natural) - English (United States)", "Homme": "Microsoft Andrew Online (Natural) - English (United States)" },
    "fr-FR": { "Femme": "Microsoft Julie - French (France)", "Homme": "Microsoft Paul - French (France)" },
    "es-ES": { "Femme": "Microsoft Elvira Online (Natural) - Spanish (Spain)", "Homme": "Microsoft Alvaro Online (Natural) - Spanish (Spain)" },
    "ar-SA": { "Femme": "Microsoft Zariyah Online (Natural) - Arabic (Saudi Arabia)", "Homme": "Microsoft Hamed Online (Natural) - Arabic (Saudi Arabia)" },
    "zh-CN": { "Femme": "Microsoft Xiaoxiao Online (Natural) - Chinese (Mainland)", "Homme": "Microsoft Yunxi Online (Natural) - Chinese (Mainland)" }
};

// ✅ Forcer le chargement des voix à l'avance
let voicesLoaded = false;

const loadVoices = () => {
    return new Promise(resolve => {
        const voices = speechSynthesis.getVoices();
        if (voices.length > 0) {
            voicesLoaded = true;
            resolve();
        } else {
            speechSynthesis.onvoiceschanged = () => {
                voicesLoaded = true;
                resolve();
            };
        }
    });
};

window.addEventListener('load', async () => {
    await loadVoices(); // Charger les voix dès le chargement

    const defaultOption = document.createElement('option');
    defaultOption.value = "";
    defaultOption.textContent = "-- Sélectionnez une langue --";
    defaultOption.disabled = true;
    defaultOption.selected = true;
    
    languageSelect.appendChild(defaultOption);

    Object.keys(voiceMap).forEach(lang => {
        const option = document.createElement('option');
        option.value = lang;
        option.textContent = new Intl.DisplayNames(['fr'], { type: 'language' }).of(lang);
        languageSelect.appendChild(option);
    }); 

    voicesSelect.innerHTML = '<option value="" disabled selected>-- Sélectionnez une voix --</option>';
});

// 📌 Mettre à jour les voix disponibles en fonction de la langue sélectionnée
const updateVoices = () => {
    const selectedLanguage = languageSelect.value;
    voicesSelect.innerHTML = ''; // Vide la liste

    const defaultOption = document.createElement('option');
    defaultOption.value = "";
    defaultOption.textContent = "Sélectionnez une voix";
    defaultOption.disabled = true;
    defaultOption.selected = true;
    voicesSelect.appendChild(defaultOption);

    if (voiceMap[selectedLanguage]) {
        Object.keys(voiceMap[selectedLanguage]).forEach(gender => {
            const option = document.createElement('option');
            option.value = gender;
            option.textContent = `Voix ${gender}`;
            voicesSelect.appendChild(option);
        });
    }
};


// 📌 Fonction pour générer, jouer et sauvegarder l'audio avec JavaScript
const generateAndDownloadAudio = async () => {
    const text = textArea.value.trim();
    if (!text) {
        alert("Veuillez entrer un texte à lire !");
        return;
    }

    const selectedLanguage = languageSelect.value;
    const selectedGender = voicesSelect.value;
    const voiceName = voiceMap[selectedLanguage]?.[selectedGender];

    if (!voiceName) {
        alert("Veuillez sélectionner une voix valide !");
        return;
    }

    ttsStatus.style.display = "block";
    ttsStatus.textContent = "🔊 Génération en cours...";

    try {
        // 📌 Enregistrer l'audio avec `MediaRecorder`
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        const mediaRecorder = new MediaRecorder(stream);
        const audioChunks = [];

        mediaRecorder.ondataavailable = event => audioChunks.push(event.data);
        mediaRecorder.start();

        const utterance = new SpeechSynthesisUtterance(text);

        // ✅ S'assurer que les voix sont chargées
        if (!voicesLoaded) await loadVoices();

        const voices = speechSynthesis.getVoices();
        const selectedVoice = voices.find(voice => voice.name === voiceName);
        if (selectedVoice) utterance.voice = selectedVoice;

        utterance.pitch = parseFloat(pitchSlider.value);
        utterance.rate = parseFloat(rateSlider.value);
        utterance.volume = parseFloat(volumeSlider.value);

        mediaRecorder.onstop = () => {
            const audioBlob = new Blob(audioChunks, { type: "audio/wav" });
            const timestamp = Date.now();
            const filename = `tts_audio_${timestamp}.wav`;

            const downloadLink = document.createElement("a");
            downloadLink.href = window.URL.createObjectURL(audioBlob);
            downloadLink.download = filename;
            document.body.appendChild(downloadLink);
            downloadLink.click();
            document.body.removeChild(downloadLink);

            ttsStatus.textContent = "✅ Audio enregistré et téléchargé !";
            setTimeout(() => ttsStatus.style.display = "none", 3000);
        };

        speechSynthesis.speak(utterance);

        utterance.onend = () => {
            mediaRecorder.stop();
            stream.getTracks().forEach(track => track.stop());
        };

    } catch (error) {
        console.error("Erreur TTS:", error);
        ttsStatus.textContent = "❌ Erreur lors de la génération.";
    }
};

// 📌 Lier l'événement au bouton
speakButton.addEventListener('click', generateAndDownloadAudio);
languageSelect.addEventListener('change', updateVoices);


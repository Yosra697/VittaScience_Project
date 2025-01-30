if ('speechSynthesis' in window) {
    const speakButton = document.getElementById('speakButton');
    const textArea = document.getElementById('text');
    const languageSelect = document.getElementById('language');
    const pitchSlider = document.getElementById('pitch');
    const rateSlider = document.getElementById('rate');
    const volumeSlider = document.getElementById('volume');
    const voicesSelect = document.getElementById('voices');

    // Liste des voix avec leurs étiquettes d'affichage
    const allowedVoices = [
        { name: "Microsoft Hortense - French (France)", label: "Femme - Français", lang: "fr-FR" },
        { name: "Microsoft Paul - French (France)", label: "Homme - Français", lang: "fr-FR" },
        { name: "Microsoft Hazel - English (United Kingdom)", label: "Femme - Anglais", lang: "en-US" },
        { name: "Microsoft George - English (United Kingdom)", label: "Homme - Anglais", lang: "en-US" }
    ];

    // Charger et filtrer les voix disponibles
    const loadVoices = () => {
        const voices = speechSynthesis.getVoices();
        const selectedLanguage = languageSelect.value; // Langue sélectionnée dans la liste
        voicesSelect.innerHTML = '';

        // Filtrer les voix autorisées en fonction de la langue sélectionnée
        const filteredVoices = voices.filter(voice => {
            console.log(voice.name);
            return allowedVoices.some(allowed => allowed.name === voice.name && allowed.lang === selectedLanguage);
        });

        // Ajouter les options avec les labels personnalisés
        filteredVoices.forEach((voice, index) => {
            const allowedVoice = allowedVoices.find(allowed => allowed.name === voice.name);
            const option = document.createElement('option');
            option.value = index;
            option.textContent = allowedVoice ? allowedVoice.label : `${voice.name} (${voice.lang})`;
            voicesSelect.appendChild(option);
        });

        if (filteredVoices.length === 0) {
            console.warn("Aucune voix autorisée n'a été trouvée pour la langue sélectionnée.");
        }
    };

    // Assurez-vous que les voix sont chargées avant de les utiliser
    if (speechSynthesis.onvoiceschanged !== undefined) {
        speechSynthesis.onvoiceschanged = loadVoices;
    }

    // Mettre à jour les voix disponibles lorsque la langue change
    languageSelect.addEventListener('change', loadVoices);

    loadVoices();

    // Fonction pour lire le texte
    speakButton.addEventListener('click', () => {
        const text = textArea.value.trim();
        if (!text) {
            alert("Veuillez entrer un texte à lire !");
            return;
        }

        const pitchValue = parseFloat(pitchSlider.value) || 1;
        const rateValue = parseFloat(rateSlider.value) || 1;
        const volumeValue = parseFloat(volumeSlider.value) || 1;
        const selectedVoiceIndex = parseInt(voicesSelect.value, 10);

        const utterance = new SpeechSynthesisUtterance(text);
        utterance.pitch = pitchValue;
        utterance.rate = rateValue;
        utterance.volume = volumeValue;

        const voices = speechSynthesis.getVoices();
        const selectedLanguage = languageSelect.value;
        const filteredVoices = voices.filter(voice =>
            allowedVoices.some(allowed => allowed.name === voice.name && allowed.lang === selectedLanguage)
        );

        if (filteredVoices[selectedVoiceIndex]) {
            utterance.voice = filteredVoices[selectedVoiceIndex];
        } else {
            alert("Veuillez sélectionner une voix valide !");
            return;
        }

        // Annuler toutes les voix en cours avant de commencer la nouvelle
        window.speechSynthesis.cancel();
        window.speechSynthesis.speak(utterance);
    });
} else {
    alert("Désolé, votre navigateur ne prend pas en charge l'API Web Speech.");
}

document.getElementById("startSTSRecording").addEventListener("click", async () => {
    const recordBtn = document.getElementById("startSTSRecording");
    const recordingStatus = document.getElementById("stsRecordingStatus");
    const processingStatus = document.getElementById("stsProcessingStatus");
    const successStatus = document.getElementById("stsSuccessStatus");
    const errorStatus = document.getElementById("stsError");
    const transcription = document.getElementById("stsTranscription");
    const audio = document.getElementById("generatedAudio");
    const audioPlayback = document.getElementById("audioPlayback");

    // Reset UI
    recordBtn.disabled = true;
    recordingStatus.style.display = "block";
    recordingStatus.innerText = "🔴 Initialisation de l'enregistrement (5s)...";
    processingStatus.style.display = "none";
    successStatus.style.display = "none";
    errorStatus.style.display = "none";
    transcription.innerText = "📝 Transcription : ...";
    audioPlayback.style.display = "none";

    try {
        const formData = new FormData();
        formData.append("model_choice", "xtts");


        recordingStatus.innerText = "🎙️ Enregistrement en cours...";

        const response = await fetch("http://127.0.0.1:5000/record", {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            throw new Error(`Erreur HTTP : ${response.status}`);
        }

        processingStatus.style.display = "block";
        processingStatus.innerText = "🔄 Traitement du clonage vocal...";

        const data = await response.json();

        if (data.transcribed_text && data.output_audio) {
            transcription.innerText = `📝 Transcription : ${data.transcribed_text}`;
            audio.src = `http://127.0.0.1:5000/get_audio/${data.output_audio}`;
            audioPlayback.style.display = "block";
            successStatus.style.display = "block";
        } else {
            transcription.innerText = "❌ Échec de la transcription.";
        }

    } catch (error) {
        errorStatus.innerText = "❌ Erreur : " + error.message;
        errorStatus.style.display = "block";
        transcription.innerText = "❌ Erreur lors de l’enregistrement.";
    } finally {
        recordingStatus.style.display = "none";
        processingStatus.style.display = "none";
        recordBtn.disabled = false;
    }
});

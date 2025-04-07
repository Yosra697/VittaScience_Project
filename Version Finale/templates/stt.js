const recordingStatus = document.getElementById("recordingStatus");
const transcriptionStatus = document.getElementById("transcriptionStatus");
const recordingTimer = document.getElementById("recording-timer");
const startRecordingButton = document.getElementById("startRecording");
const transcriptionText = document.getElementById("transcription");

let mediaRecorderSTT;
let isRecording = false;
let recordingStartTime;

startRecordingButton.addEventListener("click", async () => {
    console.log("here") ; 
    if (!isRecording) {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorderSTT = new MediaRecorder(stream);
        const audioChunks = [];

        mediaRecorderSTT.ondataavailable = (event) => {
            audioChunks.push(event.data);
        };

        mediaRecorderSTT.onstop = async () => {
            recordingStatus.style.display = "none";
            transcriptionStatus.style.display = "block";
            startRecordingButton.disabled = true;

            const audioBlob = new Blob(audioChunks, { type: "audio/wav" });
            const formData = new FormData();
            formData.append("audio", audioBlob);

            try {
                const response = await fetch("http://127.0.0.1:5000/stt", { method: "POST", body: formData });
                const data = await response.json();
                transcriptionStatus.style.display = "none";
                transcriptionText.innerHTML = `📝 Transcription : ${data.transcription}`;
            } catch (error) {
                transcriptionStatus.textContent = "❌ Erreur lors de la transcription.";
            } finally {
                startRecordingButton.disabled = false;
            }
        };

        startRecordingButton.textContent = "⏹️ Arrêter l'enregistrement";
        recordingStatus.style.display = "block";
        recordingStartTime = Date.now();

        mediaRecorderSTT.start();
        isRecording = true;
    } else {
        mediaRecorderSTT.stop();
        startRecordingButton.textContent = "🎤 Enregistrer et Transcrire";
        isRecording = false;
    }
});

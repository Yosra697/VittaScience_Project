import whisper

# Load the model (can be 'tiny', 'base', 'small', 'medium', 'large')
model = whisper.load_model("base")

# Transcribe an audio file
result = model.transcribe("test.wav")

# Print the transcription
print("Transcription:")
print(result["text"])

# Save the transcription to a file
with open("transcription.txt", "w") as f:
    f.write(result["text"])

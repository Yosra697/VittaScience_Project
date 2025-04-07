import whisper
import json

model = whisper.load_model("medium") 

result = model.transcribe("test.wav", word_timestamps=True)

timeline = []

for segment in result["segments"]:
    for word in segment.get("words", []):  
        word_text = word.get("word", "") 
        start_time = word["start"]
        end_time = word["end"]
        duration = end_time - start_time

        if len(word_text) > 0:
            letter_duration = duration / len(word_text)  
            for i, letter in enumerate(word_text):
                letter_start = start_time + (i * letter_duration)
                letter_end = letter_start + letter_duration
                timeline.append({
                    "letter": letter,
                    "start": round(letter_start, 3),
                    "end": round(letter_end, 3)
                })

with open("timeline.json", "w", encoding="utf-8") as f:
    json.dump(timeline, f, indent=4)

print("Letter-by-letter timeline saved to timeline.json")

import cv2
import subprocess
import json
import tempfile
import os
import sys
from gtts import gTTS

def text_to_wav(text, output_file):
    """Convert text to WAV audio file using gTTS"""
    print("Converting text to speech...")
    tts = gTTS(text=text, lang='fr')
    mp3_path = output_file.replace('.wav', '.mp3')
    tts.save(mp3_path)
    
    print("Converting MP3 to WAV...")
    subprocess.run([
        'ffmpeg',
        '-i', mp3_path,
        '-acodec', 'pcm_s16le',
        '-ar', '44100',
        output_file,
        '-y'
    ], check=True)
    
    os.remove(mp3_path)

def merge_video_audio(video_path, audio_path, output_path):
    """Merge video with audio using FFmpeg"""
    print("Merging video with audio...")
    subprocess.run([
        'ffmpeg',
        '-i', video_path,
        '-i', audio_path,
        '-c:v', 'copy',
        '-c:a', 'aac',
        output_path,
        '-y'
    ], check=True)

def create_animation(text, output_path):
    """Create animation from phonemes"""
    # Map phonemes to corresponding images
    phoneme_to_image = {
        'A': 'open_mouth.jpg',
        'E': 'smile_mouth.jpg',
        'I': 'smile_mouth.jpg',
        'O': 'round_mouth.jpg',
        'U': 'round_mouth.jpg',
        'B': 'wide_mouth.jpg',
        'M': 'wide_mouth.jpg',
        'P': 'wide_mouth.jpg',
    }
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        wav_file = os.path.join(tmp_dir, 'speech.wav')
        phoneme_file = os.path.join(tmp_dir, 'phonemes.json')
        temp_video = os.path.join(tmp_dir, 'temp_video.mp4')
        
        # Create audio and get phonemes
        text_to_wav(text, wav_file)
        
        try:
            print("Running Rhubarb for phoneme detection...")
            subprocess.run([
                'rhubarb',
                '-f', 'json',
                '-o', phoneme_file,
                wav_file
            ], check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            print("Rhubarb error:", e.stderr)
            raise
        
        
        with open(phoneme_file) as f:
            phoneme_data = json.load(f)
        
        # Get first image to determine dimensions
        first_image = cv2.imread(list(phoneme_to_image.values())[0])
        if first_image is None:
            raise ValueError("Could not load mouth images")
        
        height, width = first_image.shape[:2]
        
        # Create video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(temp_video, fourcc, 30.0, (width, height))
        
        if not out.isOpened():
            raise ValueError("Could not open video writer")
        
        print("Generating animation frames...")
        for mouthcue in phoneme_data.get('mouthCues', []):
            phoneme = mouthcue['value']
            image_path = phoneme_to_image.get(phoneme, 'wide_mouth.jpg')
            
            try:
                # Load the image for this phoneme
                frame = cv2.imread(image_path)
                if frame is None:
                    raise ValueError(f"Could not load image: {image_path}")
                
                # Calculate how many frames to show this image
                duration = int((mouthcue['end'] - mouthcue['start']) * 30)  # 30 fps
                
                # Write the frame multiple times based on duration
                for _ in range(max(1, duration)):
                    out.write(frame)
                    
            except Exception as e:
                print(f"Error processing phoneme {phoneme}: {e}")
                continue
        
        out.release()
        
        # Merge video with audio
        merge_video_audio(temp_video, wav_file, output_path)
        print(f"Animation saved to: {output_path}")

def main():
    text = "Vous écoutez la voie mondiale. Bienvenue pour fêter notre 6e anniversaire. Vous écoutez de Global Voice. Bienvenue pour fêter notre 6e anniversaire."
    output_path = "mouth_animation.mp4"
    
    try:
        create_animation(text, output_path)
        print("Animation completed successfully!")
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
import json
import cv2
import dlib
import numpy as np
from moviepy.editor import ImageSequenceClip, AudioFileClip

# Configuration
FACE_MODEL = "shape_predictor_68_face_landmarks.dat"
MOUTH_IMAGES_DIR = "mouth/"
MOUTH_SCALE_FACTOR = 1.5  # Adjust this to change mouth size
FPS = 24

def load_mouth_mapping():
    return {
        'A': 'A.png', 'B': 'B.png', 'C': 'C.png',
        'D': 'D.png', 'E': 'E.png', 'F': 'F.png',
        'G': 'G.png', 'H': 'H.png', 'I': 'I.png',
        'J': 'J.png', 'K': 'K.png', 'L': 'L.png',
        'M': 'M.png', 'N': 'N.png', 'O': 'O.png',
        'P': 'P.png', 'Q': 'Q.png', 'R': 'R.png',
        'S': 'S.png', 'T': 'T.png', 'U': 'U.png',
        'V': 'V.png', 'W': 'W.png', 'X': 'X.png',
        'Y': 'Y.png', 'Z': 'Z.png',
        'FERME': 'FERME.png', 'AU': 'AU.png', 
        'OU': 'OU.png', 'AN': 'AN.png',
        'ON': 'ON.png', 'EU': 'EU.png', 
        'EN': 'EN.png'
    }

def detect_mouth_position(image_path):
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(FACE_MODEL)
    
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)
    
    for face in faces:
        landmarks = predictor(gray, face)
        mouth_points = [(landmarks.part(n).x, landmarks.part(n).y) 
                       for n in range(48, 68)]
        x, y, w, h = cv2.boundingRect(np.array(mouth_points))
        return (x, y, w, h), mouth_points
    
    raise ValueError("No face detected in image")

def generate_frames(base_image_path, timeline_path):
    base_img = cv2.imread(base_image_path)
    mouth_rect, mouth_points = detect_mouth_position(base_image_path)
    mouth_mapping = load_mouth_mapping()
    
    with open(timeline_path) as f:
        timeline = json.load(f)
    
    duration = max(entry["end"] for entry in timeline)
    
    frames = []
    for frame_time in np.linspace(0, duration, int(FPS * duration)):
        current_letter = "FERME"
        for entry in timeline:
            if entry["start"] <= frame_time < entry["end"]:
                current_letter = entry["letter"].upper()
                break

        current_letter = current_letter.translate(str.maketrans({
            'É': 'E', 'Ê': 'E', 'È': 'E', 'À': 'A', 'Â': 'A',
            'Ù': 'U', 'Û': 'U', 'Î': 'I', 'Ï': 'I', 'Ô': 'O', 'Ë': 'E'
        }))
        
        # Calcul de la zone à flouter
        x, y, w, h = mouth_rect
        new_w = int(w * MOUTH_SCALE_FACTOR)
        new_h = int(h * MOUTH_SCALE_FACTOR)
        new_x = max(0, x - (new_w - w) // 2)+6
        new_y = max(0, y - (new_h - h) // 2)
        
        frame = base_img.copy()
        
        # Application du flou ovale
        y1, y2 = max(new_y, 0), min(new_y + new_h, frame.shape[0])
        x1, x2 = max(new_x, 0), min(new_x + new_w, frame.shape[1])
        
        if y2 > y1 and x2 > x1:
            mouth_roi = frame[y1:y2, x1:x2].copy()
            
            # Création d'un masque ovale
            mask = np.zeros((mouth_roi.shape[0], mouth_roi.shape[1]), dtype=np.uint8)
            center = (mask.shape[1] // 2, mask.shape[0] // 2)
            axes = (mask.shape[1] // 2, mask.shape[0] // 2)
            cv2.ellipse(mask, center, axes, 0, 0, 360, 255, -1)
            
            # Application du flou uniquement dans le masque
            blurred = cv2.GaussianBlur(mouth_roi, (99, 99), 30)
            mouth_roi = np.where(mask[..., None] == 255, blurred, mouth_roi)
            
            frame[y1:y2, x1:x2] = mouth_roi
        
        # Superposition de l'image de bouche
        mouth_file = mouth_mapping.get(current_letter, 'FERME.png')
        mouth_img = cv2.imread(f"{MOUTH_IMAGES_DIR}{mouth_file}", cv2.IMREAD_UNCHANGED)
        
        if mouth_img is not None:
            mouth_img = cv2.resize(mouth_img, (new_w, new_h))
            
            y1, y2 = max(new_y, 0), min(new_y + new_h, frame.shape[0])
            x1, x2 = max(new_x, 0), min(new_x + new_w, frame.shape[1])
            
            if y2 > y1 and x2 > x1:
                mouth_roi = mouth_img[0:y2-y1, 0:x2-x1]
                
                if mouth_roi.shape[2] == 4:
                    alpha = mouth_roi[:, :, 3] / 255.0
                    for c in range(3):
                        frame[y1:y2, x1:x2, c] = (
                            alpha * mouth_roi[:, :, c] + 
                            (1 - alpha) * frame[y1:y2, x1:x2, c]
                        )
                else:
                    frame[y1:y2, x1:x2] = mouth_roi
            
        frames.append(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    
    return frames

def create_lipsync_video(input_image, audio_file, timeline_json, output_file):
    frames = generate_frames(input_image, timeline_json)
    video_clip = ImageSequenceClip(frames, fps=FPS)
    audio_clip = AudioFileClip(audio_file)
    video_clip = video_clip.set_audio(audio_clip)
    video_clip.write_videofile(output_file, codec='libx264', audio_codec='aac')

# Run directly
if __name__ == "__main__":
    create_lipsync_video(
        input_image="input.jpg",
        audio_file="audio.wav",
        timeline_json="timeline.json",
        output_file="output.mp4"
    )
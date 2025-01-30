import cv2
import mediapipe as mp
import numpy as np
from pathlib import Path

class FaceExpressionGenerator:
    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=True,
            max_num_faces=1,
            min_detection_confidence=0.5,
            refine_landmarks=True
        )
        
    def get_mouth_landmarks(self, image):
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(image_rgb)
        
        if not results.multi_face_landmarks:
            raise ValueError("No face detected in the image")
        
        # Updated mouth landmarks for better mouth shape detection
        OUTER_LIPS = [61, 146, 91, 181, 84, 17, 314, 405, 321, 375, 291, 409, 270, 269, 267]
        INNER_LIPS = [78, 95, 88, 178, 87, 14, 317, 402, 318, 324, 308, 415, 310, 311, 312]
        MOUTH_INDICES = OUTER_LIPS + INNER_LIPS
        
        landmarks = results.multi_face_landmarks[0]
        mouth_points = []
        
        for idx in MOUTH_INDICES:
            point = landmarks.landmark[idx]
            x = int(point.x * image.shape[1])
            y = int(point.y * image.shape[0])
            mouth_points.append([x, y])
            
        return np.array(mouth_points)
    
    def create_smooth_mask(self, image, mouth_points):
        mask = np.zeros(image.shape[:2], dtype=np.uint8)
        cv2.fillPoly(mask, [mouth_points[:15]], 255)  # Only outer lips for mask
        mask = cv2.GaussianBlur(mask, (7, 7), 3)
        return mask
    
    def modify_expression(self, image, expression_type):
        result = image.copy()
        mouth_points = self.get_mouth_landmarks(image)
        
        # Separate inner and outer lip points
        outer_points = mouth_points[:15]
        
        # Get mouth bounding box
        min_x, min_y = np.min(outer_points, axis=0)
        max_x, max_y = np.max(outer_points, axis=0)
        mouth_center = np.mean(outer_points, axis=0).astype(int)
        
        # Calculate mouth dimensions
        width = max_x - min_x
        height = max_y - min_y
        
        src_points = np.float32([
            [min_x, min_y],  # Top-left
            [max_x, min_y],  # Top-right
            [min_x, max_y],  # Bottom-left
            [max_x, max_y]   # Bottom-right
        ])
        
        # Define expression-specific transformations
        if expression_type == "smile_mouth":
            curve = height * 0.3
            dst_points = np.float32([
                [min_x - width * 0.1, min_y + curve],  # Top-left
                [max_x + width * 0.1, min_y + curve],  # Top-right
                [min_x, max_y],  # Bottom-left
                [max_x, max_y]   # Bottom-right
            ])
            
        elif expression_type == "round_mouth":
            radius = min(width, height) * 0.6
            dst_points = np.float32([
                [mouth_center[0] - radius, mouth_center[1] - radius],  # Top-left
                [mouth_center[0] + radius, mouth_center[1] - radius],  # Top-right
                [mouth_center[0] - radius, mouth_center[1] + radius],  # Bottom-left
                [mouth_center[0] + radius, mouth_center[1] + radius]   # Bottom-right
            ])
            
        elif expression_type == "open_mouth":
            scale = 1.4
            dst_points = np.float32([
                [min_x, min_y - height * 0.2],  # Top-left
                [max_x, min_y - height * 0.2],  # Top-right
                [min_x, max_y + height * 0.2],  # Bottom-left
                [max_x, max_y + height * 0.2]   # Bottom-right
            ])
            
        elif expression_type == "pursed_mouth":
            compress = width * 0.3
            dst_points = np.float32([
                [min_x + compress, min_y],  # Top-left
                [max_x - compress, min_y],  # Top-right
                [min_x + compress, max_y],  # Bottom-left
                [max_x - compress, max_y]   # Bottom-right
            ])
            
        elif expression_type == "wide_mouth":
            stretch = width * 0.2
            dst_points = np.float32([
                [min_x - stretch, min_y],  # Top-left
                [max_x + stretch, min_y],  # Top-right
                [min_x - stretch, max_y],  # Bottom-left
                [max_x + stretch, max_y]   # Bottom-right
            ])
            
        elif expression_type == "frown_mouth":
            curve = height * 0.3
            dst_points = np.float32([
                [min_x - width * 0.1, min_y],  # Top-left
                [max_x + width * 0.1, min_y],  # Top-right
                [min_x, max_y - curve],  # Bottom-left
                [max_x, max_y - curve]   # Bottom-right
            ])
        
        # Calculate transformation matrix
        M = cv2.getPerspectiveTransform(src_points, dst_points)
        
        # Apply the transformation
        warped = cv2.warpPerspective(result, M, (result.shape[1], result.shape[0]))
        
        # Create smooth mask and blend
        mask = self.create_smooth_mask(image, mouth_points)
        result = cv2.seamlessClone(
            warped, result, mask,
            (mouth_center[0], mouth_center[1]),
            cv2.MIXED_CLONE
        )
        
        return result

    def generate_expressions(self, image_path):
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Could not read image: {image_path}")
            
        expressions = {}
        expression_types = ["smile_mouth", "round_mouth", "open_mouth",
                          "pursed_mouth", "wide_mouth", "frown_mouth"]
        
        for exp_type in expression_types:
            try:
                expressions[exp_type] = self.modify_expression(image, exp_type)
            except Exception as e:
                print(f"Error generating {exp_type}: {str(e)}")
                
        return expressions

def main():
    output_dir = Path("output_expressions")
    output_dir.mkdir(exist_ok=True)
    
    generator = FaceExpressionGenerator()
    
    input_path = "face.jpg"
    try:
        expressions = generator.generate_expressions(input_path)
        
        for exp_type, exp_image in expressions.items():
            output_path = output_dir / f"{exp_type}.jpg"
            cv2.imwrite(str(output_path), exp_image)
            print(f"Saved {exp_type} to {output_path}")
            
    except Exception as e:
        print(f"Error processing image: {str(e)}")

if __name__ == "__main__":
    main()
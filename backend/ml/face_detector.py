import cv2
import numpy as np
from typing import List, Tuple, Optional
from backend.ml.model_manager import model_manager

class FaceDetector:
    """Face detection using SCRFD"""
    
    def __init__(self, confidence_threshold: float = 0.5):
        self.confidence_threshold = confidence_threshold
        self.detector = model_manager.detector
    
    def detect_faces(self, image: np.ndarray) -> List[dict]:
        """
        Detect faces in image
        
        Returns:
            List of detected faces with:
            - bbox: [x1, y1, x2, y2]
            - confidence: confidence score
            - landmarks: facial landmarks
        """
        if self.detector is None:
            raise RuntimeError("Detector not loaded")
        
        # Prepare input
        h, w = image.shape[:2]
        blob = cv2.dnn.blobFromImage(
            image, 1.0, (640, 640),
            (0, 0, 0), swapRB=False, crop=False
        )
        
        try:
            # Run inference
            outputs = self.detector.run(None, {'images': blob})
            
            # Parse outputs
            faces = []
            scores = outputs[0][0]  # Confidence scores
            bboxes = outputs[1][0]  # Bounding boxes
            landmarks = outputs[2][0]  # Landmarks
            
            for i in range(len(scores)):
                if scores[i] > self.confidence_threshold:
                    # Scale bbox to original image size
                    bbox = bboxes[i] * np.array([w/640, h/640, w/640, h/640])
                    
                    # Scale landmarks
                    pts = landmarks[i].reshape(-1, 2) * np.array([w/640, h/640])
                    
                    faces.append({
                        'bbox': bbox.astype(int),
                        'confidence': float(scores[i]),
                        'landmarks': pts
                    })
            
            return faces
        
        except Exception as e:
            print(f"Error detecting faces: {e}")
            return []
    
    def get_best_face(self, image: np.ndarray) -> Optional[dict]:
        """Get the best (largest/most confident) face"""
        faces = self.detect_faces(image)
        
        if not faces:
            return None
        
        # Sort by area (largest first)
        faces_sorted = sorted(
            faces,
            key=lambda f: (f['bbox'][2] - f['bbox'][0]) * (f['bbox'][3] - f['bbox'][1]),
            reverse=True
        )
        
        return faces_sorted[0]
    
    def crop_face(self, image: np.ndarray, face: dict, expand: float = 0.1) -> np.ndarray:
        """
        Crop face region from image with optional expansion
        
        Args:
            image: Input image
            face: Face detection result
            expand: Expand ratio (0.1 = 10% expansion)
        
        Returns:
            Cropped face image
        """
        x1, y1, x2, y2 = face['bbox']
        h, w = image.shape[:2]
        
        # Expand bbox
        width = x2 - x1
        height = y2 - y1
        expand_x = int(width * expand)
        expand_y = int(height * expand)
        
        x1 = max(0, x1 - expand_x)
        y1 = max(0, y1 - expand_y)
        x2 = min(w, x2 + expand_x)
        y2 = min(h, y2 + expand_y)
        
        return image[y1:y2, x1:x2]
    
    def visualize_detection(self, image: np.ndarray, faces: List[dict]) -> np.ndarray:
        """Visualize face detections on image"""
        output = image.copy()
        
        for face in faces:
            x1, y1, x2, y2 = face['bbox']
            conf = face['confidence']
            
            # Draw bbox
            cv2.rectangle(output, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            # Draw confidence
            cv2.putText(
                output, f"{conf:.2f}", (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2
            )
            
            # Draw landmarks
            for pt in face['landmarks']:
                cv2.circle(output, tuple(pt.astype(int)), 2, (0, 0, 255), -1)
        
        return output

face_detector = FaceDetector()
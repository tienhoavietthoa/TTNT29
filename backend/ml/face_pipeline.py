import cv2
import numpy as np
from typing import Optional, Tuple, List
from backend.ml.face_detector import face_detector
from backend.ml.face_aligner import face_aligner
from backend.ml.face_recognizer import face_recognizer
from backend.ml.anti_spoof import anti_spoof

class FacePipeline:
    """Complete face recognition pipeline"""
    
    def __init__(self, confidence_threshold: float = 0.6):
        self.confidence_threshold = confidence_threshold
    
    def process_image(self, image: np.ndarray) -> dict:
        """
        Complete pipeline: detect → align → recognize → liveness check
        
        Returns:
            {
                'success': bool,
                'faces': [
                    {
                        'bbox': [x1, y1, x2, y2],
                        'embedding': [512D vector],
                        'is_live': bool,
                        'liveness_score': float,
                        'landmarks': array,
                        'aligned_face': image
                    }
                ],
                'error': str (if any)
            }
        """
        try:
            result = {
                'success': False,
                'faces': [],
                'error': None
            }
            
            # Step 1: Detect faces
            faces = face_detector.detect_faces(image)
            if not faces:
                result['error'] = 'No faces detected'
                return result
            
            # Step 2-4: Process each face
            for face in faces:
                face_data = {
                    'bbox': face['bbox'],
                    'confidence': face['confidence'],
                    'landmarks': face['landmarks']
                }
                
                # Crop face
                face_crop = face_detector.crop_face(image, face)
                
                # Step 2: Align face
                aligned_face = face_aligner.align_face(face_crop, face['landmarks'])
                face_data['aligned_face'] = aligned_face
                
                # Step 3: Get embedding
                embedding = face_recognizer.get_embedding(aligned_face)
                face_data['embedding'] = embedding
                
                # Step 4: Check liveness
                is_live, liveness_score = anti_spoof.check_liveness(aligned_face)
                face_data['is_live'] = is_live
                face_data['liveness_score'] = liveness_score
                
                result['faces'].append(face_data)
            
            result['success'] = True
            return result
        
        except Exception as e:
            return {
                'success': False,
                'faces': [],
                'error': str(e)
            }
    
    def process_video_frame(self, frame: np.ndarray) -> Optional[dict]:
        """Process single video frame"""
        return self.process_image(frame)
    
    def match_face(self, image: np.ndarray, database_embeddings: np.ndarray) -> dict:
        """
        Detect and match face against database
        
        Returns:
            {
                'matched': bool,
                'match_index': int,
                'similarity': float,
                'is_live': bool,
                'face_data': dict
            }
        """
        result = self.process_image(image)
        
        if not result['success'] or not result['faces']:
            return {
                'matched': False,
                'match_index': -1,
                'similarity': 0,
                'is_live': False,
                'face_data': None
            }
        
        best_face = result['faces'][0]
        
        # Check liveness first
        if not best_face['is_live']:
            return {
                'matched': False,
                'match_index': -1,
                'similarity': 0,
                'is_live': False,
                'face_data': best_face
            }
        
        # Find best match in database
        match_result = face_recognizer.find_best_match(
            best_face['embedding'],
            database_embeddings,
            self.confidence_threshold
        )
        
        return {
            'matched': match_result['matched'],
            'match_index': match_result['index'],
            'similarity': match_result['similarity'],
            'is_live': best_face['is_live'],
            'face_data': best_face
        }

face_pipeline = FacePipeline()
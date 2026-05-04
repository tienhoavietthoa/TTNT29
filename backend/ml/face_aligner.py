import cv2
import numpy as np
from typing import Tuple
from backend.ml.model_manager import model_manager

class FaceAligner:
    """Face alignment using landmarks"""
    
    def __init__(self):
        self.landmark_2d = model_manager.landmark_2d
        self.landmark_3d = model_manager.landmark_3d
    
    def get_2d_landmarks(self, face_image: np.ndarray) -> np.ndarray:
        """Get 106 2D landmarks"""
        if self.landmark_2d is None:
            raise RuntimeError("2D landmark detector not loaded")
        
        try:
            # Prepare input (usually 192x192)
            blob = cv2.dnn.blobFromImage(
                face_image, 1.0, (192, 192),
                (0, 0, 0), swapRB=False
            )
            
            outputs = self.landmark_2d.run(None, {'data': blob})
            landmarks = outputs[0].reshape(-1, 2)
            
            return landmarks
        except Exception as e:
            print(f"Error getting 2D landmarks: {e}")
            return np.array([])
    
    def get_3d_landmarks(self, face_image: np.ndarray) -> np.ndarray:
        """Get 68 3D landmarks"""
        if self.landmark_3d is None:
            raise RuntimeError("3D landmark detector not loaded")
        
        try:
            blob = cv2.dnn.blobFromImage(
                face_image, 1.0, (192, 192),
                (0, 0, 0), swapRB=False
            )
            
            outputs = self.landmark_3d.run(None, {'data': blob})
            landmarks = outputs[0].reshape(-1, 3)
            
            return landmarks
        except Exception as e:
            print(f"Error getting 3D landmarks: {e}")
            return np.array([])
    
    def align_face(self, image: np.ndarray, landmarks: np.ndarray, 
                   output_size: Tuple[int, int] = (112, 112)) -> np.ndarray:
        """
        Align face using landmarks (normalize pose/rotation)
        
        Args:
            image: Face crop
            landmarks: Face landmarks
            output_size: Output size (112x112 for ArcFace)
        
        Returns:
            Aligned face image
        """
        if len(landmarks) < 5:
            return cv2.resize(image, output_size)
        
        # Use 5 key points for alignment (similar to InsightFace)
        # Point indices: left_eye, right_eye, nose, left_mouth, right_mouth
        src_pts = landmarks[:5].astype(np.float32)
        
        # Target points (predefined for 112x112)
        dst_pts = np.array([
            [38.2946, 51.6963],
            [73.5318, 51.5014],
            [56.0252, 71.7366],
            [41.5493, 92.3655],
            [70.7299, 92.2041]
        ], dtype=np.float32)
        
        # Compute affine transformation
        M = cv2.getAffineTransform(src_pts[:3], dst_pts[:3])
        
        # Warp image
        aligned = cv2.warpAffine(image, M, output_size)
        
        return aligned
    
    def estimate_pose(self, landmarks_3d: np.ndarray) -> Tuple[float, float, float]:
        """
        Estimate head pose (yaw, pitch, roll) from 3D landmarks
        
        Returns:
            (yaw, pitch, roll) in degrees
        """
        if len(landmarks_3d) < 68:
            return 0, 0, 0
        
        # Define 3D model points (68 points subset)
        model_points = landmarks_3d
        
        # Camera matrix (approximate)
        focal_length = 1
        center = (0, 0)
        camera_matrix = np.array([
            [focal_length, 0, center[0]],
            [0, focal_length, center[1]],
            [0, 0, 1]
        ], dtype=float)
        
        # Distortion coefficients
        dist_coeffs = np.zeros((4, 1))
        
        # Solve PnP
        success, rotation_vec, translation_vec = cv2.solvePnP(
            model_points, landmarks_3d[:, :2],
            camera_matrix, dist_coeffs
        )
        
        if success:
            # Convert rotation vector to Euler angles
            rotation_mat, _ = cv2.Rodrigues(rotation_vec)
            yaw = np.arctan2(rotation_mat[1, 0], rotation_mat[0, 0])
            pitch = np.arcsin(-rotation_mat[2, 0])
            roll = np.arctan2(rotation_mat[2, 1], rotation_mat[2, 2])
            
            return np.degrees(yaw), np.degrees(pitch), np.degrees(roll)
        
        return 0, 0, 0

face_aligner = FaceAligner()
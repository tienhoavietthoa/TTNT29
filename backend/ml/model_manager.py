import os
import numpy as np
from typing import Tuple, Optional, List
import onnxruntime as ort
import cv2
from pathlib import Path

class ModelManager:
    """Manage all ML models (InsightFace)"""
    
    def __init__(self, model_dir: str = "models"):
        self.model_dir = model_dir
        self.ensure_model_dir()
        
        # Initialize models
        self.detector = None
        self.recognizer = None
        self.landmark_2d = None
        self.landmark_3d = None
        self.gender_age = None
        
        self.load_models()
    
    def ensure_model_dir(self):
        """Create model directory if not exists"""
        Path(self.model_dir).mkdir(parents=True, exist_ok=True)
    
    def load_models(self):
        """Load all models"""
        print("Loading ML models...")
        
        try:
            # Load detector (SCRFD)
            detector_path = os.path.join(self.model_dir, "det_10g.onnx")
            if os.path.exists(detector_path):
                self.detector = ort.InferenceSession(
                    detector_path,
                    providers=['CUDAExecutionProvider', 'CPUExecutionProvider']
                )
                print("✓ Detector (SCRFD) loaded")
            else:
                print("⚠ Detector not found. Download det_10g.onnx")
            
            # Load recognizer (ArcFace ResNet50)
            recognizer_path = os.path.join(self.model_dir, "w600k_r50.onnx")
            if os.path.exists(recognizer_path):
                self.recognizer = ort.InferenceSession(
                    recognizer_path,
                    providers=['CUDAExecutionProvider', 'CPUExecutionProvider']
                )
                print("✓ Recognizer (ArcFace) loaded")
            else:
                print("⚠ Recognizer not found. Download w600k_r50.onnx")
            
            # Load 2D landmarks
            landmark_2d_path = os.path.join(self.model_dir, "2d106det.onnx")
            if os.path.exists(landmark_2d_path):
                self.landmark_2d = ort.InferenceSession(
                    landmark_2d_path,
                    providers=['CUDAExecutionProvider', 'CPUExecutionProvider']
                )
                print("✓ 2D Landmarks detector loaded")
            
            # Load 3D landmarks
            landmark_3d_path = os.path.join(self.model_dir, "1k3d68.onnx")
            if os.path.exists(landmark_3d_path):
                self.landmark_3d = ort.InferenceSession(
                    landmark_3d_path,
                    providers=['CUDAExecutionProvider', 'CPUExecutionProvider']
                )
                print("✓ 3D Landmarks detector loaded")
            
            # Load gender/age classifier
            gender_age_path = os.path.join(self.model_dir, "genderage.onnx")
            if os.path.exists(gender_age_path):
                self.gender_age = ort.InferenceSession(
                    gender_age_path,
                    providers=['CUDAExecutionProvider', 'CPUExecutionProvider']
                )
                print("✓ Gender/Age classifier loaded")
        
        except Exception as e:
            print(f"Error loading models: {e}")
    
    def is_ready(self) -> bool:
        """Check if models are ready"""
        return self.detector is not None and self.recognizer is not None
    
    def get_download_instructions(self) -> str:
        """Get model download instructions"""
        return """
        Models are required. Download from InsightFace:
        
        1. Download buffalo_l model:
           - Visit: https://github.com/deepinsight/insightface/releases/download/v0.7/buffalo_l.zip
           - Extract to: backend/models/
        
        Files needed:
        - det_10g.onnx (SCRFD detector)
        - w600k_r50.onnx (ArcFace recognizer)
        - 2d106det.onnx (2D landmarks)
        - 1k3d68.onnx (3D landmarks)
        - genderage.onnx (Gender/Age classifier)
        
        Or use automatic download:
        - python -m insightface.app install-models
        """

model_manager = ModelManager()
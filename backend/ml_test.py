"""
Test ML models and face recognition pipeline
Run: python ml_test.py
"""

import cv2
import numpy as np
from backend.ml.model_manager import model_manager
from backend.ml.face_pipeline import face_pipeline
from backend.ml.face_detector import face_detector
from backend.ml.face_recognizer import face_recognizer

def test_models_loading():
    """Test if models are loaded"""
    print("Testing model loading...")
    print("-" * 50)
    
    if model_manager.is_ready():
        print("✓ All models loaded successfully!")
        return True
    else:
        print("✗ Models not loaded. Please download models first.")
        print(model_manager.get_download_instructions())
        return False

def test_face_detection():
    """Test face detection with sample image"""
    print("\nTesting face detection...")
    print("-" * 50)
    
    try:
        # Create sample face image (or load from file)
        sample_image = cv2.imread("sample_face.jpg")
        
        if sample_image is None:
            print("⚠ sample_face.jpg not found. Creating synthetic image...")
            sample_image = np.random.randint(0, 256, (480, 640, 3), dtype=np.uint8)
        
        faces = face_detector.detect_faces(sample_image)
        print(f"✓ Detected {len(faces)} face(s)")
        
        for i, face in enumerate(faces):
            print(f"  Face {i+1}:")
            print(f"    - Bbox: {face['bbox']}")
            print(f"    - Confidence: {face['confidence']:.2f}")
            print(f"    - Landmarks: {len(face['landmarks'])} points")
        
        return len(faces) > 0
    
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_face_recognition():
    """Test face recognition pipeline"""
    print("\nTesting face recognition...")
    print("-" * 50)
    
    try:
        sample_image = cv2.imread("sample_face.jpg")
        
        if sample_image is None:
            print("⚠ sample_face.jpg not found")
            return False
        
        result = face_pipeline.process_image(sample_image)
        
        if result['success']:
            print(f"✓ Pipeline successful!")
            print(f"  - Faces detected: {len(result['faces'])}")
            
            for i, face in enumerate(result['faces']):
                print(f"  Face {i+1}:")
                print(f"    - Embedding dim: {len(face['embedding'])}")
                print(f"    - Is live: {face['is_live']}")
                print(f"    - Liveness score: {face['liveness_score']:.2f}")
            
            return True
        else:
            print(f"✗ Pipeline failed: {result['error']}")
            return False
    
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_embedding_comparison():
    """Test embedding comparison"""
    print("\nTesting embedding comparison...")
    print("-" * 50)
    
    try:
        # Create sample embeddings
        emb1 = np.random.randn(512).astype(np.float32)
        emb1 = emb1 / np.linalg.norm(emb1)
        
        emb2 = emb1.copy()  # Same embedding
        emb3 = np.random.randn(512).astype(np.float32)  # Different embedding
        emb3 = emb3 / np.linalg.norm(emb3)
        
        # Compare same
        sim12, match12 = face_recognizer.compare_embeddings(emb1, emb2, 0.6)
        print(f"Same embedding similarity: {sim12:.4f} (matched: {match12})")
        
        # Compare different
        sim13, match13 = face_recognizer.compare_embeddings(emb1, emb3, 0.6)
        print(f"Different embedding similarity: {sim13:.4f} (matched: {match13})")
        
        assert match12 == True, "Same embeddings should match"
        assert match13 == False, "Different embeddings should not match"
        
        print("✓ Embedding comparison works!")
        return True
    
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 50)
    print("ML Model Testing")
    print("=" * 50)
    
    tests = [
        test_models_loading,
        test_face_detection,
        test_face_recognition,
        test_embedding_comparison
    ]
    
    results = []
    for test in tests:
        try:
            results.append(test())
        except Exception as e:
            print(f"✗ Test failed: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    print(f"Tests passed: {sum(results)}/{len(results)}")
    print("=" * 50)

if __name__ == "__main__":
    main()
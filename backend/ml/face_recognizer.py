import cv2
import numpy as np
from typing import Tuple
from backend.ml.model_manager import model_manager

class FaceRecognizer:
    """Face recognition using ArcFace ResNet50"""
    
    def __init__(self):
        self.recognizer = model_manager.recognizer
        self.embedding_dim = 512
    
    def get_embedding(self, face_image: np.ndarray) -> np.ndarray:
        """
        Extract face embedding (512D vector)
        
        Args:
            face_image: Aligned face image (112x112)
        
        Returns:
            Embedding vector (512D)
        """
        if self.recognizer is None:
            raise RuntimeError("Recognizer not loaded")
        
        if face_image.shape != (112, 112, 3):
            face_image = cv2.resize(face_image, (112, 112))
        
        try:
            # Normalize image
            blob = cv2.dnn.blobFromImage(
                face_image, 1.0/127.5, (112, 112),
                (127.5, 127.5, 127.5), swapRB=False
            )
            
            # Get embedding
            outputs = self.recognizer.run(None, {'data': blob})
            embedding = outputs[0][0]
            
            # Normalize embedding
            embedding = embedding / np.linalg.norm(embedding)
            
            return embedding.astype(np.float32)
        
        except Exception as e:
            print(f"Error getting embedding: {e}")
            return np.zeros(self.embedding_dim, dtype=np.float32)
    
    def compare_embeddings(self, emb1: np.ndarray, emb2: np.ndarray, 
                          threshold: float = 0.6) -> Tuple[float, bool]:
        """
        Compare two embeddings using cosine similarity
        
        Args:
            emb1: First embedding
            emb2: Second embedding
            threshold: Similarity threshold for matching
        
        Returns:
            (similarity_score, is_match)
        """
        # Normalize if needed
        emb1 = emb1 / np.linalg.norm(emb1)
        emb2 = emb2 / np.linalg.norm(emb2)
        
        # Cosine similarity
        similarity = np.dot(emb1, emb2)
        is_match = similarity >= threshold
        
        return float(similarity), bool(is_match)
    
    def batch_compare(self, query_emb: np.ndarray, database_embs: np.ndarray,
                     threshold: float = 0.6) -> list:
        """
        Compare query embedding with multiple embeddings
        
        Args:
            query_emb: Query embedding
            database_embs: Array of embeddings from database (N x 512)
            threshold: Similarity threshold
        
        Returns:
            List of (index, similarity, is_match)
        """
        results = []
        
        for idx, db_emb in enumerate(database_embs):
            similarity, is_match = self.compare_embeddings(query_emb, db_emb, threshold)
            results.append({
                'index': idx,
                'similarity': similarity,
                'is_match': is_match
            })
        
        return sorted(results, key=lambda x: x['similarity'], reverse=True)
    
    def find_best_match(self, query_emb: np.ndarray, database_embs: np.ndarray,
                       threshold: float = 0.6) -> dict:
        """
        Find best matching embedding from database
        
        Returns:
            {'index': int, 'similarity': float, 'matched': bool}
        """
        results = self.batch_compare(query_emb, database_embs, threshold)
        
        if results and results[0]['is_match']:
            return results[0]
        
        return {'index': -1, 'similarity': 0, 'matched': False}

face_recognizer = FaceRecognizer()
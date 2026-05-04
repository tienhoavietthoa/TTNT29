from sqlalchemy.orm import Session
import numpy as np
import cv2
import io
from datetime import datetime
from crud import face_crud, attendance_crud, class_crud
from core.exceptions import NotFoundException, BadRequestException
from ml.face_pipeline import face_pipeline
from ml.face_recognizer import face_recognizer

class FaceRecognitionService:
    """Enhanced service with ML models"""
    
    EMBEDDING_THRESHOLD = 0.6
    
    @staticmethod
    def process_enrollment_image(image_bytes: bytes, id_student: int, id_class_attendance: int):
        """
        Process image for face enrollment
        
        1. Detect face
        2. Align face
        3. Extract embedding
        4. Check liveness
        5. Save to database
        """
        try:
            # Convert bytes to image
            nparr = np.frombuffer(image_bytes, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if image is None:
                raise BadRequestException("Invalid image")
            
            # Process through pipeline
            result = face_pipeline.process_image(image)
            
            if not result['success'] or not result['faces']:
                raise BadRequestException(f"Face detection failed: {result['error']}")
            
            face_data = result['faces'][0]
            
            # Check liveness
            if not face_data['is_live']:
                raise BadRequestException(
                    f"Not a real face. Liveness score: {face_data['liveness_score']:.2f}"
                )
            
            # Get embedding
            embedding = face_data['embedding']
            embedding_bytes = embedding.tobytes()
            
            # Save image
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"student_{id_student}_class_{id_class_attendance}_{timestamp}.jpg"
            
            # Save aligned face
            cv2.imwrite(f"statics/face_embeddings/{filename}", face_data['aligned_face'])
            
            # Save embedding to database
            face_embedding = face_crud.create_face_embedding(
                db=None,  # Will be provided by service caller
                id_student=id_student,
                id_class_attendance=id_class_attendance,
                img_filename_embedding=filename,
                embedding_data=embedding_bytes
            )
            
            return {
                'success': True,
                'embedding_id': face_embedding.id_embedding,
                'liveness_score': face_data['liveness_score'],
                'filename': filename
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    @staticmethod
    def process_attendance_image(image_bytes: bytes, id_class_attendance: int, 
                                 id_session_attendance: int, db: Session):
        """
        Process image for attendance marking
        
        1. Detect face
        2. Recognize (match with database)
        3. Check liveness
        4. Mark attendance
        """
        try:
            # Convert bytes to image
            nparr = np.frombuffer(image_bytes, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if image is None:
                raise BadRequestException("Invalid image")
            
            # Get all embeddings for this class
            embeddings_data = face_crud.get_embeddings_by_class(db, id_class_attendance)
            
            if not embeddings_data:
                raise BadRequestException("No face data for this class")
            
            # Extract embedding vectors
            database_embeddings = np.array([
                np.frombuffer(emb.embedding_data, dtype=np.float32)
                for emb in embeddings_data
            ])
            
            # Match face
            match_result = face_pipeline.match_face(image, database_embeddings)
            
            if not match_result['is_live']:
                raise BadRequestException("Liveness check failed")
            
            if not match_result['matched']:
                raise BadRequestException(
                    f"Face not recognized. Similarity: {match_result['similarity']:.2f}"
                )
            
            # Get matched student
            matched_embedding = embeddings_data[match_result['match_index']]
            student_id = matched_embedding.id_student
            
            # Save attendance image
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            img_filename = f"attendance_{student_id}_session_{id_session_attendance}_{timestamp}.jpg"
            cv2.imwrite(f"statics/attendance_images/{img_filename}", 
                       match_result['face_data']['aligned_face'])
            
            # Record attendance
            attendance = attendance_crud.create_attendance(
                db=db,
                id_session_attendance=id_session_attendance,
                id_student=student_id,
                id_class_attendance=id_class_attendance,
                status_attendance="present",
                checkin_time_attendance=datetime.utcnow(),
                img_filename_attendance=img_filename,
                id_embedding=matched_embedding.id_embedding
            )
            
            return {
                'success': True,
                'student_id': student_id,
                'similarity': match_result['similarity'],
                'attendance_id': attendance.id_attendance
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    @staticmethod
    def check_similar_embeddings(db: Session, id_class_attendance: int, 
                                new_embedding_bytes: bytes, threshold: float = 0.7) -> list:
        """Check for duplicate/similar faces in class"""
        try:
            embeddings_data = face_crud.get_embeddings_by_class(db, id_class_attendance)
            new_embedding = np.frombuffer(new_embedding_bytes, dtype=np.float32)
            
            similar = []
            for emb_data in embeddings_data:
                db_emb = np.frombuffer(emb_data.embedding_data, dtype=np.float32)
                similarity, match = face_recognizer.compare_embeddings(
                    new_embedding, db_emb, threshold
                )
                
                if match:
                    similar.append({
                        'student_id': emb_data.id_student,
                        'student_name': emb_data.student.name_student,
                        'similarity': similarity
                    })
            
            return similar
        
        except Exception as e:
            print(f"Error checking similar embeddings: {e}")
            return []
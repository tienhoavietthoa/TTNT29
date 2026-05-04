from sqlalchemy.orm import Session
from sqlalchemy import and_
from models.face_models import FaceEmbedding
from datetime import datetime

def create_face_embedding(
    db: Session,
    id_student: int,
    id_class_attendance: int,
    img_filename_embedding: str = None,
    embedding_data: bytes = None,
    notes_embedding: str = None
) -> FaceEmbedding:
    """Create face embedding"""
    db_embedding = FaceEmbedding(
        id_student=id_student,
        id_class_attendance=id_class_attendance,
        img_filename_embedding=img_filename_embedding,
        embedding_data=embedding_data,
        notes_embedding=notes_embedding
    )
    db.add(db_embedding)
    db.commit()
    db.refresh(db_embedding)
    return db_embedding

def get_face_embedding_by_id(db: Session, id_embedding: int) -> FaceEmbedding:
    """Get face embedding by id"""
    return db.query(FaceEmbedding).filter(
        FaceEmbedding.id_embedding == id_embedding
    ).first()

def get_face_embedding_by_student_and_class(
    db: Session,
    id_student: int,
    id_class_attendance: int
) -> FaceEmbedding:
    """Get face embedding by student and class"""
    return db.query(FaceEmbedding).filter(
        and_(
            FaceEmbedding.id_student == id_student,
            FaceEmbedding.id_class_attendance == id_class_attendance
        )
    ).first()

def get_embeddings_by_class(db: Session, id_class_attendance: int):
    """Get all embeddings in a class"""
    return db.query(FaceEmbedding).filter(
        FaceEmbedding.id_class_attendance == id_class_attendance
    ).all()

def update_face_embedding(
    db: Session,
    id_embedding: int,
    embedding_data: bytes = None,
    img_filename_embedding: str = None,
    notes_embedding: str = None
) -> FaceEmbedding:
    """Update face embedding"""
    db_embedding = get_face_embedding_by_id(db, id_embedding)
    if not db_embedding:
        return None
    
    if embedding_data is not None:
        db_embedding.embedding_data = embedding_data
    if img_filename_embedding:
        db_embedding.img_filename_embedding = img_filename_embedding
    if notes_embedding:
        db_embedding.notes_embedding = notes_embedding
    
    db.commit()
    db.refresh(db_embedding)
    return db_embedding

def delete_face_embedding(db: Session, id_embedding: int) -> bool:
    """Delete face embedding"""
    db_embedding = get_face_embedding_by_id(db, id_embedding)
    if not db_embedding:
        return False
    db.delete(db_embedding)
    db.commit()
    return True

def delete_face_embedding_by_student_and_class(
    db: Session,
    id_student: int,
    id_class_attendance: int
) -> bool:
    """Delete face embedding by student and class"""
    db_embedding = get_face_embedding_by_student_and_class(
        db, id_student, id_class_attendance
    )
    if not db_embedding:
        return False
    db.delete(db_embedding)
    db.commit()
    return True

def check_if_student_has_embedding(
    db: Session,
    id_student: int,
    id_class_attendance: int
) -> bool:
    """Check if student has embedding in class"""
    return get_face_embedding_by_student_and_class(
        db, id_student, id_class_attendance
    ) is not None
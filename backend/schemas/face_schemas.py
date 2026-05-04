from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class FaceEmbeddingResponse(BaseModel):
    id_embedding: int
    id_student: int
    img_filename_embedding: Optional[str]
    created_at_embedding: datetime
    
    class Config:
        from_attributes = True

class FaceEnrollRequest(BaseModel):
    id_student: int
    id_class_attendance: int
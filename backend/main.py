import sys
import os
from pathlib import Path

# ✅ Thêm dòng này
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ✅ SỬA: Loại bỏ "backend." prefix
from database import Base, engine
from routers import (
    auth_router, user_router, class_router,
    attendance_router, message_router, contact_router
)
from config import get_settings

# Create tables
Base.metadata.create_all(bind=engine)

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="Attendance Management System API"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(class_router)
app.include_router(attendance_router)
app.include_router(message_router)
app.include_router(contact_router)

@app.get("/")
async def root():
    return {
        "message": "Welcome to Attendance Management System API",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
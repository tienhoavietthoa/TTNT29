import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Configuration
    API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000/api")
    
    # App Configuration
    APP_NAME = "Hệ Thống Điểm Danh Sinh Viên"
    APP_VERSION = "1.0.0"
    DEBUG = os.getenv("DEBUG", "False") == "True"
    
    # UI Configuration
    WINDOW_WIDTH = 1200
    WINDOW_HEIGHT = 800
    THEME = "light"
    
    # Token storage
    TOKEN_FILE = ".token"
    
    # Image paths
    UPLOAD_DIR = "uploads"
    TEMP_IMAGE_DIR = "temp_images"
    
    # Face recognition settings
    FACE_RECOGNITION_THRESHOLD = 0.6
    MAX_FACES_TO_TRAIN = 20

config = Config()
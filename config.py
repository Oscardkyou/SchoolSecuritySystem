import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Database connection URL
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    # Folder for file uploads
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
    # Maximum allowed file size
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
# Institution Website Configuration

# Database Configuration
DATABASE_URL = 'sqlite:///institution.db'

# Flask Configuration
SECRET_KEY = 'your-secret-key-change-this-in-production'
DEBUG = True
HOST = '0.0.0.0'
PORT = 5000

# Email Configuration (for notifications)
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USERNAME = 'your-email@gmail.com'
SMTP_PASSWORD = 'your-app-password'

# File Upload Configuration
UPLOAD_FOLDER = 'uploads'
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB

# Security Configuration
CORS_ORIGINS = ['http://localhost:3000', 'http://127.0.0.1:3000']

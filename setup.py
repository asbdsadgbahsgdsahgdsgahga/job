
"""
Institution Website Setup Script
This script automates the setup process for the institution website.
"""

import os
import sys
import subprocess
import sqlite3
from pathlib import Path

def print_banner():
    """Print setup banner"""
    print("=" * 60)
    print("    INSTITUTION WEBSITE SETUP")
    print("=" * 60)
    print()

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("❌ Error: Python 3.7 or higher is required")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    print(f"✅ Python version: {sys.version.split()[0]}")

def install_dependencies():
    """Install Python dependencies"""
    print("📦 Installing Python dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        sys.exit(1)

def create_directories():
    """Create necessary directories"""
    directories = [
        "backend",
        "css",
        "js",
        "database",
        "uploads",
        "logs"
    ]
    
    print("📁 Creating directories...")
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created directory: {directory}")

def initialize_database():
    """Initialize the SQLite database"""
    print("🗄️  Initializing database...")
    
    # Copy schema file to backend directory
    schema_file = Path("database/schema.sql")
    backend_schema = Path("backend/schema.sql")
    
    if schema_file.exists():
        import shutil
        shutil.copy(schema_file, backend_schema)
        print("✅ Schema file copied to backend directory")
    
    # Initialize database using Flask app
    try:
        # Change to backend directory
        os.chdir("backend")
        
        # Import and run Flask app initialization
        sys.path.append('.')
        from app import init_db
        init_db()
        
        print("✅ Database initialized successfully")
        os.chdir("..")
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        os.chdir("..")
        sys.exit(1)

def create_config_file():
    """Create configuration file"""
    config_content = """# Institution Website Configuration

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
"""
    
    config_file = Path("backend/config.py")
    if not config_file.exists():
        with open(config_file, 'w') as f:
            f.write(config_content)
        print("✅ Configuration file created")
    else:
        print("ℹ️  Configuration file already exists")

def create_startup_scripts():
    """Create startup scripts for different platforms"""
    
    # Windows batch file
    windows_script = """@echo off
echo Starting Institution Website...
cd backend
python app.py
pause
"""
    
    # Unix/Linux shell script
    unix_script = """#!/bin/bash
echo "Starting Institution Website..."
cd backend
python3 app.py
"""
    
    # Create Windows script
    with open("start_website.bat", "w") as f:
        f.write(windows_script)
    print("✅ Windows startup script created: start_website.bat")
    
    # Create Unix script
    with open("start_website.sh", "w") as f:
        f.write(unix_script)
    
    # Make Unix script executable
    os.chmod("start_website.sh", 0o755)
    print("✅ Unix startup script created: start_website.sh")

def create_htaccess():
    """Create .htaccess file for Apache"""
    htaccess_content = """RewriteEngine On

# Handle API requests
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule ^api/(.*)$ backend/app.py [QSA,L]

# Handle admin panel
RewriteRule ^admin/?$ backend/admin.php [L]

# Security headers
Header always set X-Content-Type-Options nosniff
Header always set X-Frame-Options DENY
Header always set X-XSS-Protection "1; mode=block"

# Cache static files
<FilesMatch "\\.(css|js|png|jpg|jpeg|gif|ico|svg)$">
    ExpiresActive On
    ExpiresDefault "access plus 1 month"
</FilesMatch>
"""
    
    with open(".htaccess", "w") as f:
        f.write(htaccess_content)
    print("✅ Apache .htaccess file created")

def create_docker_files():
    """Create Docker configuration files"""
    
    # Dockerfile
    dockerfile_content = """FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p uploads logs

# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "backend/app.py"]
"""
    
    # docker-compose.yml
    docker_compose_content = """version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./uploads:/app/uploads
      - ./logs:/app/logs
      - ./backend:/app/backend
    environment:
      - FLASK_ENV=production
      - DATABASE_URL=sqlite:///institution.db
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./:/var/www/html
    depends_on:
      - web
    restart: unless-stopped
"""
    
    # nginx.conf
    nginx_conf_content = """events {
    worker_connections 1024;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;
    
    upstream flask_app {
        server web:5000;
    }
    
    server {
        listen 80;
        server_name localhost;
        
        root /var/www/html;
        index index.html;
        
        # Handle static files
        location ~* \\.(css|js|png|jpg|jpeg|gif|ico|svg)$ {
            expires 1M;
            add_header Cache-Control "public, immutable";
        }
        
        # Handle API requests
        location /api/ {
            proxy_pass http://flask_app;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
        
        # Handle admin panel
        location /admin {
            try_files $uri $uri/ /backend/admin.php;
        }
        
        # Default location
        location / {
            try_files $uri $uri/ /index.html;
        }
    }
}
"""
    
    # Create Docker files
    with open("Dockerfile", "w") as f:
        f.write(dockerfile_content)
    print("✅ Dockerfile created")
    
    with open("docker-compose.yml", "w") as f:
        f.write(docker_compose_content)
    print("✅ docker-compose.yml created")
    
    with open("nginx.conf", "w") as f:
        f.write(nginx_conf_content)
    print("✅ nginx.conf created")

def run_tests():
    """Run basic tests to ensure everything is working"""
    print("🧪 Running basic tests...")
    
    # Test database connection
    try:
        conn = sqlite3.connect("backend/institution.db")
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM programs")
        program_count = cursor.fetchone()[0]
        print(f"✅ Database test passed - {program_count} programs found")
        conn.close()
    except Exception as e:
        print(f"❌ Database test failed: {e}")
    
    # Test Flask app import
    try:
        sys.path.append('backend')
        from app import app
        print("✅ Flask app import test passed")
    except Exception as e:
        print(f"❌ Flask app import test failed: {e}")

def print_next_steps():
    """Print next steps for the user"""
    print("\n" + "=" * 60)
    print("🎉 SETUP COMPLETE!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Start the website:")
    print("   - Windows: Double-click 'start_website.bat'")
    print("   - Unix/Linux: ./start_website.sh")
    print("   - Or manually: cd backend && python app.py")
    print()
    print("2. Access the website:")
    print("   - Main website: http://localhost:5000")
    print("   - Admin panel: http://localhost:5000/admin")
    print()
    print("3. Default admin credentials:")
    print("   - Username: admin")
    print("   - Password: admin123")
    print()
    print("4. Customize the website:")
    print("   - Edit index.html for content")
    print("   - Modify css/style.css for styling")
    print("   - Update js/script.js for functionality")
    print()
    print("5. For production deployment:")
    print("   - Use Docker: docker-compose up -d")
    print("   - Configure web server (Apache/Nginx)")
    print("   - Set up SSL certificate")
    print("   - Update database credentials")
    print()
    print("📚 Documentation: README.md")
    print("🐛 Issues: Check the logs in the 'logs' directory")
    print()

def main():
    """Main setup function"""
    print_banner()
    
    # Check Python version
    check_python_version()
    
    # Install dependencies
    install_dependencies()
    
    # Create directories
    create_directories()
    
    # Initialize database
    initialize_database()
    
    # Create configuration file
    create_config_file()
    
    # Create startup scripts
    create_startup_scripts()
    
    # Create .htaccess for Apache
    create_htaccess()
    
    # Create Docker files
    create_docker_files()
    
    # Run tests
    run_tests()
    
    # Print next steps
    print_next_steps()

if __name__ == "__main__":
    main() 
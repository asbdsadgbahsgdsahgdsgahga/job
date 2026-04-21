from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sqlite3
import os
from datetime import datetime
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Database configuration
DATABASE = 'institution.db'

def init_db():
    """Initialize the database with required tables"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Create admissions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            program TEXT NOT NULL,
            message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create contact_messages table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contact_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            subject TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create users table for admin panel
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT NOT NULL,
            role TEXT DEFAULT 'admin',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create programs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS programs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            duration TEXT NOT NULL,
            category TEXT NOT NULL,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create faculty table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS faculty (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            title TEXT NOT NULL,
            department TEXT NOT NULL,
            bio TEXT,
            email TEXT,
            image_url TEXT,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    """Serve the main HTML page"""
    return render_template('index.html')

@app.route('/api/admissions', methods=['POST'])
def submit_admission():
    """Handle admission form submissions"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'email', 'phone', 'program']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        # Validate email format
        if '@' not in data['email'] or '.' not in data['email']:
            return jsonify({'error': 'Invalid email format'}), 400
        
        # Insert into database
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO admissions (name, email, phone, program, message)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            data['name'],
            data['email'],
            data['phone'],
            data['program'],
            data.get('message', '')
        ))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'message': 'Admission application submitted successfully!',
            'status': 'success'
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/contact', methods=['POST'])
def submit_contact():
    """Handle contact form submissions"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['contactName', 'contactEmail', 'subject', 'contactMessage']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        # Validate email format
        if '@' not in data['contactEmail'] or '.' not in data['contactEmail']:
            return jsonify({'error': 'Invalid email format'}), 400
        
        # Insert into database
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO contact_messages (name, email, subject, message)
            VALUES (?, ?, ?, ?)
        ''', (
            data['contactName'],
            data['contactEmail'],
            data['subject'],
            data['contactMessage']
        ))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'message': 'Message sent successfully!',
            'status': 'success'
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/programs', methods=['GET'])
def get_programs():
    """Get all active programs"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM programs WHERE is_active = 1
            ORDER BY created_at DESC
        ''')
        
        programs = cursor.fetchall()
        conn.close()
        
        return jsonify([dict(program) for program in programs]), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/faculty', methods=['GET'])
def get_faculty():
    """Get all active faculty members"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM faculty WHERE is_active = 1
            ORDER BY created_at DESC
        ''')
        
        faculty = cursor.fetchall()
        conn.close()
        
        return jsonify([dict(member) for member in faculty]), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get website statistics"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Count admissions
        cursor.execute('SELECT COUNT(*) as count FROM admissions')
        admissions_count = cursor.fetchone()['count']
        
        # Count contact messages
        cursor.execute('SELECT COUNT(*) as count FROM contact_messages')
        messages_count = cursor.fetchone()['count']
        
        # Count programs
        cursor.execute('SELECT COUNT(*) as count FROM programs WHERE is_active = 1')
        programs_count = cursor.fetchone()['count']
        
        # Count faculty
        cursor.execute('SELECT COUNT(*) as count FROM faculty WHERE is_active = 1')
        faculty_count = cursor.fetchone()['count']
        
        conn.close()
        
        return jsonify({
            'admissions': admissions_count,
            'messages': messages_count,
            'programs': programs_count,
            'faculty': faculty_count
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/admissions', methods=['GET'])
def get_admissions_admin():
    """Get all admissions for admin panel"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM admissions 
            ORDER BY created_at DESC
        ''')
        
        admissions = cursor.fetchall()
        conn.close()
        
        return jsonify([dict(admission) for admission in admissions]), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/messages', methods=['GET'])
def get_messages_admin():
    """Get all contact messages for admin panel"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM contact_messages 
            ORDER BY created_at DESC
        ''')
        
        messages = cursor.fetchall()
        conn.close()
        
        return jsonify([dict(message) for message in messages]), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/programs', methods=['POST'])
def add_program():
    """Add a new program"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'description', 'duration', 'category']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO programs (name, description, duration, category)
            VALUES (?, ?, ?, ?)
        ''', (
            data['name'],
            data['description'],
            data['duration'],
            data['category']
        ))
        
        conn.commit()
        conn.close()
        
        return jsonify({'message': 'Program added successfully'}), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/faculty', methods=['POST'])
def add_faculty():
    """Add a new faculty member"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'title', 'department']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO faculty (name, title, department, bio, email, image_url)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            data['name'],
            data['title'],
            data['department'],
            data.get('bio', ''),
            data.get('email', ''),
            data.get('image_url', '')
        ))
        
        conn.commit()
        conn.close()
        
        return jsonify({'message': 'Faculty member added successfully'}), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Initialize database
    init_db()
    
    # Run the application
    app.run(debug=True, host='0.0.0.0', port=5000) 
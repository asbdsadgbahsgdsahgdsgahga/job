-- Institution Website Database Schema
-- This file contains all the necessary tables and sample data

-- Enable foreign key constraints
PRAGMA foreign_keys = ON;

-- Users table for admin authentication
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    email TEXT NOT NULL,
    role TEXT DEFAULT 'admin',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Admissions table for storing application submissions
CREATE TABLE IF NOT EXISTS admissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT NOT NULL,
    program TEXT NOT NULL,
    message TEXT,
    status TEXT DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Contact messages table
CREATE TABLE IF NOT EXISTS contact_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    subject TEXT NOT NULL,
    message TEXT NOT NULL,
    status TEXT DEFAULT 'unread',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Programs table
CREATE TABLE IF NOT EXISTS programs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    duration TEXT NOT NULL,
    category TEXT NOT NULL,
    is_active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Faculty table
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
);

-- News and announcements table
CREATE TABLE IF NOT EXISTS announcements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    author TEXT NOT NULL,
    is_published BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Events table
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    event_date DATE NOT NULL,
    event_time TIME,
    location TEXT,
    is_active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_admissions_email ON admissions(email);
CREATE INDEX IF NOT EXISTS idx_admissions_created_at ON admissions(created_at);
CREATE INDEX IF NOT EXISTS idx_contact_email ON contact_messages(email);
CREATE INDEX IF NOT EXISTS idx_contact_created_at ON contact_messages(created_at);
CREATE INDEX IF NOT EXISTS idx_programs_category ON programs(category);
CREATE INDEX IF NOT EXISTS idx_programs_active ON programs(is_active);
CREATE INDEX IF NOT EXISTS idx_faculty_department ON faculty(department);
CREATE INDEX IF NOT EXISTS idx_faculty_active ON faculty(is_active);
CREATE INDEX IF NOT EXISTS idx_events_date ON events(event_date);
CREATE INDEX IF NOT EXISTS idx_events_active ON events(is_active);

-- Insert sample data

-- Sample admin user (password: admin123)
INSERT OR IGNORE INTO users (username, password, email, role) VALUES 
('admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/5Q5qKqG', 'admin@institution.edu', 'admin');

-- Sample programs
INSERT OR IGNORE INTO programs (name, description, duration, category) VALUES 
('Bachelor of Computer Science', 'Comprehensive program covering software development, algorithms, and computer systems.', '4 years', 'undergraduate'),
('Master of Business Administration', 'Advanced business program focusing on leadership, strategy, and management.', '2 years', 'graduate'),
('Data Science Certificate', 'Intensive program covering data analysis, machine learning, and statistical methods.', '6 months', 'professional'),
('Online Marketing Course', 'Flexible online program teaching digital marketing strategies and tools.', '3 months', 'online');

-- Sample faculty members
INSERT OR IGNORE INTO faculty (name, title, department, bio, email, image_url) VALUES 
('Dr. John Smith', 'Dean of Engineering', 'Computer Science', 'Expert in mechanical engineering with 15+ years of experience in academia and industry.', 'john.smith@institution.edu', 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=400&q=80'),
('Dr. Sarah Johnson', 'Head of Computer Science', 'Computer Science', 'Leading researcher in artificial intelligence and machine learning with numerous publications.', 'sarah.johnson@institution.edu', 'https://images.unsplash.com/photo-1494790108755-2616b612b786?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=400&q=80'),
('Dr. Michael Brown', 'Professor of Business', 'Business Administration', 'Former executive with expertise in strategic management and organizational behavior.', 'michael.brown@institution.edu', 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=400&q=80'),
('Dr. Emily Davis', 'Associate Professor', 'Mathematics', 'Specialist in applied mathematics and statistics with focus on data analysis.', 'emily.davis@institution.edu', 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=400&q=80'),
('Prof. Robert Wilson', 'Professor of Economics', 'Economics', 'Expert in macroeconomics and financial markets with extensive industry experience.', 'robert.wilson@institution.edu', 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=400&q=80');

-- Sample announcements
INSERT OR IGNORE INTO announcements (title, content, author) VALUES 
('Welcome to the New Academic Year', 'We are excited to welcome all students to the new academic year. Classes begin on September 1st.', 'Admin'),
('Research Grant Awarded', 'Our institution has been awarded a $2M research grant for artificial intelligence studies.', 'Research Office'),
('Campus Safety Update', 'New safety protocols have been implemented across campus. Please review the updated guidelines.', 'Security Office'),
('Student Achievement Recognition', 'Congratulations to our students who won the national programming competition.', 'Student Affairs');

-- Sample events
INSERT OR IGNORE INTO events (title, description, event_date, event_time, location) VALUES 
('Open House 2024', 'Join us for our annual open house to learn about our programs and meet faculty.', '2024-03-15', '10:00:00', 'Main Campus'),
('Career Fair', 'Connect with leading employers and explore career opportunities.', '2024-04-20', '14:00:00', 'Student Center'),
('Alumni Reunion', 'Annual alumni gathering and networking event.', '2024-05-10', '18:00:00', 'Conference Hall'),
('Research Symposium', 'Presentations of cutting-edge research by our faculty and students.', '2024-06-05', '09:00:00', 'Science Building');

-- Sample admissions (for testing)
INSERT OR IGNORE INTO admissions (name, email, phone, program, message) VALUES 
('Alice Johnson', 'alice.johnson@email.com', '+1234567890', 'undergraduate', 'Interested in computer science program'),
('Bob Smith', 'bob.smith@email.com', '+1234567891', 'graduate', 'Looking for MBA program information'),
('Carol Davis', 'carol.davis@email.com', '+1234567892', 'online', 'Interested in online learning options');

-- Sample contact messages (for testing)
INSERT OR IGNORE INTO contact_messages (name, email, subject, message) VALUES 
('David Wilson', 'david.wilson@email.com', 'General Inquiry', 'I would like to learn more about your programs.'),
('Eva Brown', 'eva.brown@email.com', 'Admission Requirements', 'What are the admission requirements for the MBA program?'),
('Frank Miller', 'frank.miller@email.com', 'Campus Visit', 'I would like to schedule a campus visit.');

-- Create views for common queries
CREATE VIEW IF NOT EXISTS v_active_programs AS
SELECT * FROM programs WHERE is_active = 1 ORDER BY created_at DESC;

CREATE VIEW IF NOT EXISTS v_active_faculty AS
SELECT * FROM faculty WHERE is_active = 1 ORDER BY created_at DESC;

CREATE VIEW IF NOT EXISTS v_recent_admissions AS
SELECT * FROM admissions ORDER BY created_at DESC LIMIT 10;

CREATE VIEW IF NOT EXISTS v_recent_messages AS
SELECT * FROM contact_messages ORDER BY created_at DESC LIMIT 10;

CREATE VIEW IF NOT EXISTS v_upcoming_events AS
SELECT * FROM events 
WHERE event_date >= DATE('now') AND is_active = 1 
ORDER BY event_date ASC;

-- Create triggers for data integrity
CREATE TRIGGER IF NOT EXISTS tr_admissions_created_at
AFTER INSERT ON admissions
BEGIN
    UPDATE admissions SET created_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

CREATE TRIGGER IF NOT EXISTS tr_contact_messages_created_at
AFTER INSERT ON contact_messages
BEGIN
    UPDATE contact_messages SET created_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

-- Create stored procedures (SQLite doesn't support stored procedures, but we can create functions)
-- Note: SQLite doesn't support stored procedures, but we can create helper functions in the application layer

-- Database maintenance queries
-- These can be run periodically to maintain database performance

-- Analyze database for query optimization
ANALYZE;

-- Update statistics
-- Note: SQLite automatically maintains statistics, but you can run ANALYZE periodically

-- Clean up old data (example: delete admissions older than 2 years)
-- DELETE FROM admissions WHERE created_at < DATE('now', '-2 years');

-- Clean up old contact messages (example: delete messages older than 1 year)
-- DELETE FROM contact_messages WHERE created_at < DATE('now', '-1 year');

-- Export database schema and data
-- This can be used for backup or migration purposes
-- .schema
-- .dump 
-- Creating database schema for Student Course Management System

-- Drop tables if they exist to ensure clean schema creation
DROP TABLE IF EXISTS enrollments;
DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS departments;
DROP TABLE IF EXISTS roles;

-- Create roles table
CREATE TABLE roles (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    role_name VARCHAR(50) NOT NULL UNIQUE
);

-- Create departments table
CREATE TABLE departments (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    department_name VARCHAR(100) NOT NULL UNIQUE
);

-- Create users table
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(512) NOT NULL, -- Hashed password
    role INTEGER NOT NULL,
    phone VARCHAR(20),
    email VARCHAR(255) NOT NULL UNIQUE,
    department_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (role) REFERENCES roles(id) ON DELETE RESTRICT,
    FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE RESTRICT
);

-- Create courses table
CREATE TABLE courses (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    course_name VARCHAR(100) NOT NULL,
    instructor_id INTEGER NOT NULL,
    location VARCHAR(100),
    schedule VARCHAR(100),
    semester VARCHAR(20),
    FOREIGN KEY (instructor_id) REFERENCES users(id) ON DELETE RESTRICT
);

-- Create enrollments table
CREATE TABLE enrollments (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    student_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    UNIQUE (student_id, course_id), -- Prevent duplicate enrollments
    FOREIGN KEY (student_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
);

-- Create indexes for performance
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_courses_instructor ON courses(instructor_id);
CREATE INDEX idx_enrollments_student_course ON enrollments(student_id, course_id);

-- Insert initial roles
INSERT INTO roles (role_name) VALUES ('admin'), ('instructor'), ('student');

-- Insert sample departments
INSERT INTO departments (department_name) VALUES ('CECS'), ('CAS'), ('CBM'), ('CHS');
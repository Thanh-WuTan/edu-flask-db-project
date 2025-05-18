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
    department_name VARCHAR(255) NOT NULL UNIQUE
);

-- Create users table
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL, -- Hashed password
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
    course_name VARCHAR(255) NOT NULL,
    department_id INTEGER NOT NULL,
    instructor_id INTEGER,
    location VARCHAR(255),
    schedule VARCHAR(255),
    semester VARCHAR(20),
    availability INTEGER NOT NULL, -- new
    FOREIGN KEY (instructor_id) REFERENCES users(id) ON DELETE SET NULL,
    FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE RESTRICT
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
INSERT INTO roles (role_name)  VALUES ('admin'), ('instructor'), ('student'), ('guest');

-- Insert sample departments
INSERT INTO departments (department_name) VALUES ('CECS'), ('CAS'), ('CBM'), ('CHS'), ('guest');


DELIMITER //
CREATE PROCEDURE get_user_role_counts()
BEGIN
    SELECT r.role_name, COUNT(u.id) AS user_count
    FROM users u
    LEFT JOIN roles r ON u.role = r.id
    GROUP BY r.role_name;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE get_course_department_counts()
BEGIN
    SELECT d.department_name, COUNT(c.id) AS course_count
    FROM courses c
    LEFT JOIN departments d ON c.department_id = d.id
    GROUP BY d.department_name;
END //
DELIMITER ;


-- Trigger to manage course availability on enrollment
DELIMITER //
CREATE TRIGGER before_enrollment_insert
BEFORE INSERT ON enrollments
FOR EACH ROW
BEGIN
    DECLARE current_availability INT;
    SELECT availability INTO current_availability FROM courses WHERE id = NEW.course_id FOR UPDATE;
    IF current_availability <= 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Cannot enroll: Course has no available seats.';
    END IF;
    UPDATE courses SET availability = availability - 1 WHERE id = NEW.course_id;
END //
DELIMITER ;


-- Trigger to increase course availability on unenrollment
DELIMITER //
CREATE TRIGGER after_enrollment_delete
AFTER DELETE ON enrollments
FOR EACH ROW
BEGIN
    UPDATE courses SET availability = availability + 1 WHERE id = OLD.course_id;
END //
DELIMITER ;

-- Create view for course information with instructor details (without enrolled students)
CREATE VIEW view_course_details AS
SELECT 
    c.id AS course_id,
    c.course_name,
    c.department_id,
    c.instructor_id,
    u.username AS instructor_name,
    c.location,
    c.schedule,
    c.semester,
    c.availability
FROM 
    courses c
    LEFT JOIN users u ON c.instructor_id = u.id;

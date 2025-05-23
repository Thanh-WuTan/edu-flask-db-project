# Course Enrollment Management System

This is a web-based application designed for managing course enrollment in educational institutions. It supports multiple roles (Administrators, Instructors, Students) with role-specific functionalities, including course management, enrollment tracking, and analytics dashboards.


## Project Overview
- Purpose: Facilitate course enrollment and management with a focus on usability, security, and scalability.
- Technologies: Flask, Bootstrap, MySQL.

## Functional Requirements

### Course Management:
- The system must display a list of courses with filters by course name, department, and schedule, supporting pagination (10 courses per page).
- Users can view detailed course information (e.g., ID, name, department, instructor, location, schedule, semester, availability) on a course detail page.
- Admins can add, edit, and delete courses, while instructors and students can only view course details.
- The system must track and display enrolled students for each course.

### Enrollment Management:
- Students must be able to enroll in a course if availability is greater than zero and they are not already enrolled, with a confirmation dialog before submission.
- Students must be able to unenroll from a course if they are enrolled, with a confirmation dialog before submission.
- The system must update course availability automatically when students enroll or unenroll.
- The system must prevent enrollment if the course is full (availability ≤ 0) or if the student is already enrolled.

### User Interface and Navigation:
- The system must provide a responsive web interface using Bootstrap for consistent styling across devices.
- Each role (student, instructor, admin) must have a dedicated dashboard with role-specific options.
- Flash messages must be displayed to provide feedback on actions (e.g., success or error messages for login, enrollment).

### Analytics:
- Administrators should have access to dashboards that provide detailed reports on institutional courses.


## Non-Functional Requirements

### Performance:
- The system must have high uptime, with all errors handled to prevent crashes.
- Queries should execute within 0.5 seconds for a dataset of 1000 enrollments.

### Security:
- Passwords must be encrypted using the bcrypt hashing function when stored in the database.
- Role-based access control must be implemented to prevent unauthorized information access or disclosure.
- The system must include preventions or mitigations for common web security vulnerabilities, including SQL Injection and Cross-site Scripting (XSS).

### Scalability:
- The application must be scalable to handle an increasing number of users, supporting around 300 users during peak times.

### Usability:
- The system must provide an easy-to-navigate interface, with a responsive UI built using the Bootstrap library.

### Reliability:
- Data integrity must be ensured with a normalized database design (3NF) and appropriate constraints.

## Installation and Setup
1. Clone the Repository:

```bash
git clone https://github.com/Thanh-WuTan/edu-flask-db-project.git
cd edu-flask-db-project
```

2. Set Up Environment Variables:
Create a `.env` file in the project root with the following content:

```bash
SECRET_KEY=yoursecretkey
MYSQL_HOST=db
MYSQL_USER=root
MYSQL_PASSWORD=mysqlpasswd
MYSQL_DB=edudb
MYSQL_PORT=3306
DEFAULT_ADMIN_USERNAME=admin
DEFAULT_ADMIN_EMAIL=admin@admin.admin
DEFAULT_ADMIN_PASSWORD=admin
```

+ `MYSQL_*` keys are for the config of the MySQL container. 
+ `DEFAULT_ADMIN_*` are information for the default admin account. Please remove this account after create the app.


3. Build and Run the Containers:
```bash
docker-compose up -d
```

4. Access the Application:
- Once the containers are running, the web application is accessible at http://localhost:5000.
- The MySQL database is available at localhost:3306 (use the credentials from .env).

## Supporting Documentation
- Design Document: Full details in DesignDocument.pdf (included in repo).
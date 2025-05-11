# Student Course Management System

## 📄 Brief Description
The Student Course Management System is a web-based application designed to streamline the management of courses, instructors, and students in an academic institution. 

## 🎯 Functional & Non-functional Requirements
### Functional Requirements

**Admin Role:**
- Create, update, and delete courses, instructors, and students.
- Edit course and user information.


**Instructor Role:**
- Add students to their teaching courses.
- View the list of students enrolled in their courses.
- Edit their courses' information


**Student Role:**
- Register and enroll in courses.
- View the list of courses they are enrolled in and students in those courses.


**Analytics:**
- tbd


**User Authentication:**
- Secure login for all roles with role-based access control.

### Non-functional Requirements

- **Performance:** Queries should execute within 0.05 seconds for a dataset of 1000 enrollments.
- **Security:** Encrypt passwords, use role-based privileges, and prevent SQL injection.
- **Scalability**: Support at least 100 concurrent users via Docker containerization.
- **Usability:** Provide a simple, responsive UI using Bootstrap.
- **Reliability:** Ensure data integrity with normalized database design (3NF) and constraints.

## 🧱 Planned Core Entities

- Users: Stores common attributes (user_id, email, password, role, name) for all roles.
- Instructors: Links to Users, includes instructor_id and department_id.
- Students: Links to Users, includes student_id and department_id.
- Courses: Stores course_id, name, department_id, and instructor_id.
- Enrollments: Junction table for student-course relationships (student_id, course_id, enrollment_date).
Departments: Stores department_id and name (CECS, CAS, CBM, CHS).

## 🔧 Tech Stack

- Database: MySQL 8.0 (normalized to 3NF, with views, stored procedures, triggers, and indexes).
Backend: Flask (Python) for REST API, handling CRUD operations and authentication.
- Frontend: HTML/CSS with Bootstrap 5.1.3 for a responsive, simple user interface.
- Containerization: Docker and Docker Compose for MySQL and Flask app deployment.
- Testing: Postman for API testing, manual testing for UI.

## 👥 Team Members and Roles

- Nguyen Tuan Anh: Testing, Backend Development
- Truong Gia Bao: Frontend Development, Testing 
- Vu Ai Thanh: Database Design, Backend Development

## 📅 Timeline

- May 1 - May 6, 2025: Project planning, requirements gathering, initial ERD design.
- May 7 - May 10, 2025: Database setup (DDL scripts, normalization), Docker configuration.
- May 11 - May 17, 2025: Backend development (Flask API, authentication, CRUD endpoints).
- May 18 - May 22, 2025: Frontend development (HTML/CSS with Bootstrap), integration with backend.
- May 23 - May 25, 2025: End-to-end testing, analytics implementation, documentation.
- May 26 - May 27, 2025: Final report and slides preparation, presentation rehearsal, submission.



## Setup Instructions
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
- The MySQL database is available at localhost:3308 (use the credentials from .env).

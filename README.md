# Course-Management-system
Streamlined academic administration by automating course management processes and improving data accessibility for students and faculty

# Course Management System

A comprehensive database system for managing academic courses, student registrations, and grading processes. Streamlines academic administration by automating course management processes and improving data accessibility for students and faculty.

## Features

- **Student Course Registration System** - Automated enrollment with capacity management
- **Automated Grading and Grade Tracking** - Assignment management and GPA calculations
- **Course Catalog and Scheduling Management** - Course creation and section scheduling
- **Student and Faculty Profile Management** - User authentication and profile systems
- **Academic Record Maintenance** - Transcript generation and academic tracking

## Tech Stack

- **Backend:** Python
- **Database:** MySQL
- **Libraries:** mysql-connector-python

## Installation

1. **Install dependencies:**
   ```bash
   pip install mysql-connector-python
   ```

2. **Setup MySQL database:**
   ```sql
   CREATE DATABASE course_management_system;
   ```

3. **Configure database connection in `course_management_system.py`:**
   ```python
   user='your_username', password='your_password'
   ```

4. **Run the application:**
   ```bash
   python course_management_system.py
   ```

## Database Schema

| Table | Description |
|-------|-------------|
| `users` | User authentication and management |
| `students` | Student profiles and academic data |
| `faculty` | Faculty profiles and department info |
| `courses` | Course catalog and descriptions |
| `course_sections` | Section scheduling and management |
| `enrollments` | Student-course relationships |
| `assignments` | Assignment tracking |
| `grades` | Grade recording and calculations |
| `transcripts` | Academic record maintenance |

## Usage

```python
# Initialize system
cms = CourseManagementSystem()
cms.connect_database()
cms.create_database_structure()

# Register student
user_id = cms.register_user("john_doe", "john@email.com", "password", "student")
student_id = cms.add_student(user_id, "John", "Doe", "john@email.com")

# Create course and enroll student
course_id = cms.create_course("CS101", "Intro to Programming", "Basic concepts", 3, "CS")
section_id = cms.create_course_section(course_id, faculty_id, "001", "Fall", 2024)
cms.enroll_student(student_id, section_id)
```

## Skills Demonstrated

- **Relational Databases** - Normalized schema design with proper relationships
- **SQL** - Complex queries, joins, and database optimization
- **Query Optimization** - Strategic indexing and performance tuning
- **User Authentication** - Secure password hashing and session management

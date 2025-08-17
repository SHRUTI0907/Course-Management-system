import mysql.connector
from mysql.connector import Error
from datetime import datetime
import hashlib

class CourseManagementSystem:
    def __init__(self):
        self.connection = None
        self.cursor = None
        
    def connect_database(self):
        """Establish connection to MySQL database"""
        try:
            self.connection = mysql.connector.connect(
                host='localhost',
                database='course_management',
                user='root',  # Change as needed
                password='password'  # Change as needed
            )
            self.cursor = self.connection.cursor()
            print("Connected to MySQL database successfully!")
            return True
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            return False
    
    def create_database_tables(self):
        """Create necessary tables for the course management system"""
        try:
            # Create Students table
            create_students_table = """
            CREATE TABLE IF NOT EXISTS students (
                student_id INT AUTO_INCREMENT PRIMARY KEY,
                first_name VARCHAR(50) NOT NULL,
                last_name VARCHAR(50) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                phone VARCHAR(15),
                date_of_birth DATE,
                enrollment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
            
            # Create Instructors table
            create_instructors_table = """
            CREATE TABLE IF NOT EXISTS instructors (
                instructor_id INT AUTO_INCREMENT PRIMARY KEY,
                first_name VARCHAR(50) NOT NULL,
                last_name VARCHAR(50) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                department VARCHAR(100),
                hire_date DATE
            )
            """
            
            # Create Courses table
            create_courses_table = """
            CREATE TABLE IF NOT EXISTS courses (
                course_id INT AUTO_INCREMENT PRIMARY KEY,
                course_code VARCHAR(10) UNIQUE NOT NULL,
                course_name VARCHAR(100) NOT NULL,
                description TEXT,
                credits INT DEFAULT 3,
                instructor_id INT,
                semester VARCHAR(20),
                year INT,
                max_students INT DEFAULT 30,
                FOREIGN KEY (instructor_id) REFERENCES instructors(instructor_id)
            )
            """
            
            # Create Enrollments table
            create_enrollments_table = """
            CREATE TABLE IF NOT EXISTS enrollments (
                enrollment_id INT AUTO_INCREMENT PRIMARY KEY,
                student_id INT,
                course_id INT,
                enrollment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                grade VARCHAR(2),
                status ENUM('enrolled', 'completed', 'withdrawn') DEFAULT 'enrolled',
                FOREIGN KEY (student_id) REFERENCES students(student_id),
                FOREIGN KEY (course_id) REFERENCES courses(course_id),
                UNIQUE KEY unique_enrollment (student_id, course_id)
            )
            """
            
            # Execute table creation
            self.cursor.execute(create_students_table)
            self.cursor.execute(create_instructors_table)
            self.cursor.execute(create_courses_table)
            self.cursor.execute(create_enrollments_table)
            
            self.connection.commit()
            print("Database tables created successfully!")
            
        except Error as e:
            print(f"Error creating tables: {e}")
    
    def add_student(self, first_name, last_name, email, phone=None, date_of_birth=None):
        """Add a new student to the database"""
        try:
            query = """
            INSERT INTO students (first_name, last_name, email, phone, date_of_birth)
            VALUES (%s, %s, %s, %s, %s)
            """
            values = (first_name, last_name, email, phone, date_of_birth)
            
            self.cursor.execute(query, values)
            self.connection.commit()
            
            student_id = self.cursor.lastrowid
            print(f"Student added successfully! Student ID: {student_id}")
            return student_id
            
        except Error as e:
            print(f"Error adding student: {e}")
            return None
    
    def add_instructor(self, first_name, last_name, email, department=None, hire_date=None):
        """Add a new instructor to the database"""
        try:
            query = """
            INSERT INTO instructors (first_name, last_name, email, department, hire_date)
            VALUES (%s, %s, %s, %s, %s)
            """
            values = (first_name, last_name, email, department, hire_date)
            
            self.cursor.execute(query, values)
            self.connection.commit()
            
            instructor_id = self.cursor.lastrowid
            print(f"Instructor added successfully! Instructor ID: {instructor_id}")
            return instructor_id
            
        except Error as e:
            print(f"Error adding instructor: {e}")
            return None
    
    def add_course(self, course_code, course_name, description=None, credits=3, 
                   instructor_id=None, semester=None, year=None, max_students=30):
        """Add a new course to the database"""
        try:
            query = """
            INSERT INTO courses (course_code, course_name, description, credits, 
                               instructor_id, semester, year, max_students)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (course_code, course_name, description, credits, 
                     instructor_id, semester, year, max_students)
            
            self.cursor.execute(query, values)
            self.connection.commit()
            
            course_id = self.cursor.lastrowid
            print(f"Course added successfully! Course ID: {course_id}")
            return course_id
            
        except Error as e:
            print(f"Error adding course: {e}")
            return None
    
    def enroll_student(self, student_id, course_id):
        """Enroll a student in a course"""
        try:
            # Check if enrollment already exists
            check_query = """
            SELECT * FROM enrollments 
            WHERE student_id = %s AND course_id = %s
            """
            self.cursor.execute(check_query, (student_id, course_id))
            
            if self.cursor.fetchone():
                print("Student is already enrolled in this course!")
                return False
            
            # Check course capacity
            capacity_query = """
            SELECT c.max_students, COUNT(e.enrollment_id) as current_enrollment
            FROM courses c
            LEFT JOIN enrollments e ON c.course_id = e.course_id AND e.status = 'enrolled'
            WHERE c.course_id = %s
            GROUP BY c.course_id, c.max_students
            """
            self.cursor.execute(capacity_query, (course_id,))
            result = self.cursor.fetchone()
            
            if result and result[1] >= result[0]:
                print("Course is full! Cannot enroll student.")
                return False
            
            # Enroll student
            query = """
            INSERT INTO enrollments (student_id, course_id)
            VALUES (%s, %s)
            """
            self.cursor.execute(query, (student_id, course_id))
            self.connection.commit()
            
            print("Student enrolled successfully!")
            return True
            
        except Error as e:
            print(f"Error enrolling student: {e}")
            return False
    
    def assign_grade(self, student_id, course_id, grade):
        """Assign a grade to a student for a specific course"""
        try:
            query = """
            UPDATE enrollments 
            SET grade = %s, status = 'completed'
            WHERE student_id = %s AND course_id = %s
            """
            self.cursor.execute(query, (grade, student_id, course_id))
            
            if self.cursor.rowcount > 0:
                self.connection.commit()
                print("Grade assigned successfully!")
                return True
            else:
                print("Enrollment not found!")
                return False
                
        except Error as e:
            print(f"Error assigning grade: {e}")
            return False
    
    def get_student_courses(self, student_id):
        """Get all courses for a specific student"""
        try:
            query = """
            SELECT c.course_code, c.course_name, c.credits, 
                   CONCAT(i.first_name, ' ', i.last_name) as instructor_name,
                   e.grade, e.status, e.enrollment_date
            FROM enrollments e
            JOIN courses c ON e.course_id = c.course_id
            LEFT JOIN instructors i ON c.instructor_id = i.instructor_id
            WHERE e.student_id = %s
            ORDER BY e.enrollment_date DESC
            """
            self.cursor.execute(query, (student_id,))
            results = self.cursor.fetchall()
            
            if results:
                print(f"\nCourses for Student ID {student_id}:")
                print("-" * 80)
                for row in results:
                    print(f"Code: {row[0]} | Name: {row[1]} | Credits: {row[2]}")
                    print(f"Instructor: {row[3]} | Grade: {row[4] or 'N/A'} | Status: {row[5]}")
                    print(f"Enrolled: {row[6]}")
                    print("-" * 80)
            else:
                print("No courses found for this student.")
                
        except Error as e:
            print(f"Error retrieving student courses: {e}")
    
    def get_course_enrollments(self, course_id):
        """Get all students enrolled in a specific course"""
        try:
            query = """
            SELECT s.student_id, CONCAT(s.first_name, ' ', s.last_name) as student_name,
                   s.email, e.grade, e.status, e.enrollment_date
            FROM enrollments e
            JOIN students s ON e.student_id = s.student_id
            WHERE e.course_id = %s
            ORDER BY s.last_name, s.first_name
            """
            self.cursor.execute(query, (course_id,))
            results = self.cursor.fetchall()
            
            if results:
                print(f"\nStudents enrolled in Course ID {course_id}:")
                print("-" * 80)
                for row in results:
                    print(f"ID: {row[0]} | Name: {row[1]} | Email: {row[2]}")
                    print(f"Grade: {row[3] or 'N/A'} | Status: {row[4]} | Enrolled: {row[5]}")
                    print("-" * 80)
            else:
                print("No students found for this course.")
                
        except Error as e:
            print(f"Error retrieving course enrollments: {e}")
    
    def search_courses(self, search_term=""):
        """Search for courses by name or code"""
        try:
            query = """
            SELECT c.course_id, c.course_code, c.course_name, c.credits,
                   CONCAT(i.first_name, ' ', i.last_name) as instructor_name,
                   c.semester, c.year, c.max_students,
                   COUNT(e.enrollment_id) as current_enrollment
            FROM courses c
            LEFT JOIN instructors i ON c.instructor_id = i.instructor_id
            LEFT JOIN enrollments e ON c.course_id = e.course_id AND e.status = 'enrolled'
            WHERE c.course_name LIKE %s OR c.course_code LIKE %s
            GROUP BY c.course_id
            ORDER BY c.course_code
            """
            search_pattern = f"%{search_term}%"
            self.cursor.execute(query, (search_pattern, search_pattern))
            results = self.cursor.fetchall()
            
            if results:
                print(f"\nSearch Results for '{search_term}':")
                print("-" * 100)
                for row in results:
                    print(f"ID: {row[0]} | Code: {row[1]} | Name: {row[2]}")
                    print(f"Credits: {row[3]} | Instructor: {row[4] or 'TBA'}")
                    print(f"Semester: {row[5] or 'TBA'} {row[6] or ''}")
                    print(f"Enrollment: {row[8]}/{row[7]} students")
                    print("-" * 100)
            else:
                print(f"No courses found matching '{search_term}'")
                
        except Error as e:
            print(f"Error searching courses: {e}")
    
    def close_connection(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("Database connection closed.")

def main():
    """Main function to demonstrate the Course Management System"""
    cms = CourseManagementSystem()
    
    # Connect to database
    if not cms.connect_database():
        print("Failed to connect to database. Exiting...")
        return
    
    # Create tables
    cms.create_database_tables()
    
    # Sample data insertion
    print("\n=== Adding Sample Data ===")
    
    # Add instructors
    instructor1 = cms.add_instructor("John", "Smith", "john.smith@university.edu", "Computer Science", "2020-01-15")
    instructor2 = cms.add_instructor("Sarah", "Johnson", "sarah.johnson@university.edu", "Mathematics", "2019-08-20")
    
    # Add students
    student1 = cms.add_student("Alice", "Brown", "alice.brown@student.edu", "555-0101", "2000-05-15")
    student2 = cms.add_student("Bob", "Wilson", "bob.wilson@student.edu", "555-0102", "1999-12-20")
    student3 = cms.add_student("Carol", "Davis", "carol.davis@student.edu", "555-0103", "2001-03-10")
    
    # Add courses
    course1 = cms.add_course("CS101", "Introduction to Programming", "Basic programming concepts", 3, instructor1, "Fall", 2024, 25)
    course2 = cms.add_course("CS201", "Data Structures", "Advanced data structures and algorithms", 4, instructor1, "Spring", 2024, 20)
    course3 = cms.add_course("MATH101", "Calculus I", "Differential calculus", 4, instructor2, "Fall", 2024, 30)
    
    # Enroll students
    print("\n=== Enrolling Students ===")
    cms.enroll_student(student1, course1)
    cms.enroll_student(student1, course3)
    cms.enroll_student(student2, course1)
    cms.enroll_student(student2, course2)
    cms.enroll_student(student3, course3)
    
    # Assign grades
    print("\n=== Assigning Grades ===")
    cms.assign_grade(student1, course1, "A")
    cms.assign_grade(student2, course1, "B+")
    
    # Display information
    print("\n=== Course Information ===")
    cms.search_courses()
    
    print("\n=== Student Course History ===")
    cms.get_student_courses(student1)
    
    print("\n=== Course Enrollment List ===")
    cms.get_course_enrollments(course1)
    
    # Close connection
    cms.close_connection()

if __name__ == "__main__":
    main()

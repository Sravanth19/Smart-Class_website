#!/usr/bin/env python
"""
Simple Data Expansion Script for Smart Classroom System
This script will add realistic amounts of data safely without conflicts.
"""

import os
import sys
import django
from datetime import datetime, timedelta, date
import random
from faker import Faker

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_classroom.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.utils import timezone
from users.models import AdminProfile, TeacherProfile, StudentProfile, ParentProfile
from classroom.models import Classroom
from subject.models import Subject
from grades.models import Grade
from assignments.models import Assignment, AssignmentSubmission
from attendance.models import AttendanceSession, AttendanceRecord
from feedback.models import FeedbackCategory, FeedbackSession, FeedbackResponse

User = get_user_model()
fake = Faker()

# Data configurations
GRADES_LIST = ['6th', '7th', '8th', '9th', '10th', '11th', '12th']
SUBJECTS_DATA = [
    {'name': 'Mathematics', 'description': 'Advanced Mathematics and Problem Solving'},
    {'name': 'Physics', 'description': 'Physics fundamentals and laboratory experiments'},
    {'name': 'Chemistry', 'description': 'Chemistry basics and practical applications'},
    {'name': 'Biology', 'description': 'Biology and Life Sciences'},
    {'name': 'English Literature', 'description': 'English Literature and Language Arts'},
    {'name': 'History', 'description': 'World History and Social Studies'},
    {'name': 'Geography', 'description': 'Physical and Human Geography'},
    {'name': 'Computer Science', 'description': 'Programming and Computer Applications'},
    {'name': 'Art', 'description': 'Visual Arts and Creative Expression'},
    {'name': 'Music', 'description': 'Music Theory and Performance'},
]

def create_basic_users():
    """Create basic users safely"""
    print("👥 Creating basic users...")
    
    users_created = 0
    
    # Create 10 teachers
    for i in range(10):
        username = f"teacher_demo_{i+1}"
        if not User.objects.filter(username=username).exists():
            teacher = User.objects.create_user(
                username=username,
                email=f"{username}@school.edu",
                password='teacher123',
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                role='teacher'
            )
            users_created += 1
    
    # Create 30 students
    for i in range(30):
        username = f"student_demo_{i+1}"
        if not User.objects.filter(username=username).exists():
            student = User.objects.create_user(
                username=username,
                email=f"{username}@school.edu",
                password='student123',
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                role='student'
            )
            users_created += 1
    
    # Create 20 parents
    for i in range(20):
        username = f"parent_demo_{i+1}"
        if not User.objects.filter(username=username).exists():
            parent = User.objects.create_user(
                username=username,
                email=f"{username}@school.edu",
                password='parent123',
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                role='parent'
            )
            users_created += 1
    
    print(f"✅ Created {users_created} new users")
    return users_created

def create_subjects():
    """Create subjects"""
    print("📚 Creating subjects...")
    
    subjects_created = 0
    for subject_data in SUBJECTS_DATA:
        subject, created = Subject.objects.get_or_create(
            name=subject_data['name'],
            defaults={'description': subject_data['description']}
        )
        if created:
            subjects_created += 1
    
    print(f"✅ Created {subjects_created} new subjects")
    return Subject.objects.all()

def create_classrooms():
    """Create classrooms"""
    print("🏫 Creating classrooms...")
    
    teachers = User.objects.filter(role='teacher')
    if not teachers.exists():
        print("❌ No teachers found. Please create teachers first.")
        return []
    
    classrooms_created = 0
    for i, grade in enumerate(GRADES_LIST[:5]):  # Create 5 classrooms
        name = f"Class {grade} - Section A"
        classroom, created = Classroom.objects.get_or_create(
            name=name,
            defaults={
                'grade': grade,
                'teacher': random.choice(teachers)
            }
        )
        if created:
            classrooms_created += 1
    
    print(f"✅ Created {classrooms_created} new classrooms")
    return Classroom.objects.all()

def assign_students_to_classrooms():
    """Assign students to classrooms"""
    print("📝 Assigning students to classrooms...")
    
    students = User.objects.filter(role='student')
    classrooms = Classroom.objects.all()
    
    if not students.exists() or not classrooms.exists():
        print("❌ No students or classrooms found.")
        return
    
    assignments = 0
    for student in students:
        if hasattr(student, 'student_profile') and not student.student_profile.classroom:
            classroom = random.choice(classrooms)
            student.student_profile.classroom = classroom
            student.student_profile.grade = classroom.grade
            student.student_profile.save()
            assignments += 1
    
    print(f"✅ Assigned {assignments} students to classrooms")

def create_assignments():
    """Create assignments"""
    print("📋 Creating assignments...")
    
    teachers = User.objects.filter(role='teacher')
    subjects = Subject.objects.all()
    classrooms = Classroom.objects.all()
    
    if not all([teachers.exists(), subjects.exists(), classrooms.exists()]):
        print("❌ Missing required data (teachers, subjects, or classrooms)")
        return []
    
    assignments_created = 0
    for i in range(20):  # Create 20 assignments
        teacher = random.choice(teachers)
        subject = random.choice(subjects)
        classroom = random.choice(classrooms)
        
        title = f"{subject.name} Assignment {i+1}"
        due_date = timezone.now() + timedelta(days=random.randint(1, 30))
        
        assignment, created = Assignment.objects.get_or_create(
            title=title,
            subject=subject,
            classroom=classroom,
            teacher=teacher,
            due_date=due_date,
            defaults={
                'description': f"Complete the {title} as instructed.",
                'max_points': random.choice([50, 75, 100]),
                'status': 'published',
                'priority': random.choice(['low', 'medium', 'high'])
            }
        )
        if created:
            assignments_created += 1
    
    print(f"✅ Created {assignments_created} new assignments")
    return Assignment.objects.all()

def create_grades():
    """Create grades"""
    print("📊 Creating grades...")
    
    students = User.objects.filter(role='student')
    subjects = Subject.objects.all()
    teachers = User.objects.filter(role='teacher')
    
    if not all([students.exists(), subjects.exists(), teachers.exists()]):
        print("❌ Missing required data")
        return
    
    grades_created = 0
    for i in range(50):  # Create 50 grades
        student = random.choice(students)
        subject = random.choice(subjects)
        teacher = random.choice(teachers)
        
        title = f"{subject.name} Test {i+1}"
        percentage = random.randint(60, 100)
        points_possible = 100
        points_earned = (percentage / 100) * points_possible
        
        grade, created = Grade.objects.get_or_create(
            student=student,
            subject=subject,
            teacher=teacher,
            title=title,
            defaults={
                'grade_type': random.choice(['assignment', 'quiz', 'exam']),
                'points_earned': points_earned,
                'points_possible': points_possible,
                'percentage': percentage,
                'date_assigned': fake.date_between(start_date='-30d', end_date='today'),
                'comments': random.choice(['Good work!', 'Excellent!', 'Keep it up!', 'Well done!'])
            }
        )
        if created:
            grades_created += 1
    
    print(f"✅ Created {grades_created} new grades")

def create_attendance_data():
    """Create attendance sessions and records"""
    print("📅 Creating attendance data...")
    
    teachers = User.objects.filter(role='teacher')
    classrooms = Classroom.objects.all()
    students = User.objects.filter(role='student')
    
    if not all([teachers.exists(), classrooms.exists(), students.exists()]):
        print("❌ Missing required data")
        return
    
    sessions_created = 0
    records_created = 0
    
    # Create 20 attendance sessions
    for i in range(20):
        teacher = random.choice(teachers)
        classroom = random.choice(classrooms)
        
        session_date = fake.date_time_between(start_date='-30d', end_date='now', tzinfo=timezone.get_current_timezone())
        
        session, created = AttendanceSession.objects.get_or_create(
            title=f"Daily Attendance - {session_date.strftime('%B %d')}",
            classroom=classroom,
            teacher=teacher,
            start_time=session_date,
            defaults={
                'description': 'Daily attendance session',
                'end_time': session_date + timedelta(hours=1),
                'status': 'completed',
                'attendance_type': 'daily'
            }
        )
        
        if created:
            sessions_created += 1
            
            # Create attendance records for students in this classroom
            classroom_students = students.filter(student_profile__classroom=classroom)
            for student in classroom_students:
                status = random.choices(['present', 'late', 'absent'], weights=[0.8, 0.15, 0.05])[0]
                
                record, record_created = AttendanceRecord.objects.get_or_create(
                    session=session,
                    student=student,
                    defaults={
                        'status': status,
                        'marked_at': session.start_time + timedelta(minutes=random.randint(0, 30)),
                        'marked_by': teacher
                    }
                )
                if record_created:
                    records_created += 1
    
    print(f"✅ Created {sessions_created} attendance sessions and {records_created} records")

def create_feedback_data():
    """Create feedback categories and sessions"""
    print("💬 Creating feedback data...")
    
    # Create feedback categories
    categories_data = [
        {'name': 'Course Feedback', 'description': 'General course feedback'},
        {'name': 'Teacher Evaluation', 'description': 'Teacher performance feedback'},
        {'name': 'Student Experience', 'description': 'Student experience feedback'},
    ]
    
    categories_created = 0
    for cat_data in categories_data:
        category, created = FeedbackCategory.objects.get_or_create(
            name=cat_data['name'],
            defaults=cat_data
        )
        if created:
            categories_created += 1
    
    # Create feedback sessions
    teachers = User.objects.filter(role='teacher')
    classrooms = Classroom.objects.all()
    subjects = Subject.objects.all()
    categories = FeedbackCategory.objects.all()
    
    sessions_created = 0
    if all([teachers.exists(), classrooms.exists(), subjects.exists(), categories.exists()]):
        for i in range(10):  # Create 10 feedback sessions
            teacher = random.choice(teachers)
            classroom = random.choice(classrooms)
            subject = random.choice(subjects)
            category = random.choice(categories)
            
            title = f"{subject.name} Feedback Session {i+1}"
            
            session, created = FeedbackSession.objects.get_or_create(
                title=title,
                created_by=teacher,
                defaults={
                    'description': f"Please provide feedback for {title}",
                    'category': category,
                    'classroom': classroom,
                    'subject': subject,
                    'status': 'active',
                    'visibility': 'public',
                    'allow_anonymous': True,
                    'start_date': timezone.now(),
                    'end_date': timezone.now() + timedelta(days=7)
                }
            )
            if created:
                sessions_created += 1
    
    print(f"✅ Created {categories_created} feedback categories and {sessions_created} sessions")

def main():
    """Main function to run data expansion"""
    print("🚀 SIMPLE DATA EXPANSION FOR SMART CLASSROOM")
    print("=" * 50)
    print("Adding realistic data to your website...")
    print("=" * 50)
    
    try:
        # Step 1: Create users
        print("\n📊 STEP 1: Creating Users")
        print("-" * 25)
        users_created = create_basic_users()
        
        # Step 2: Create subjects
        print("\n📊 STEP 2: Creating Subjects")
        print("-" * 27)
        subjects = create_subjects()
        
        # Step 3: Create classrooms
        print("\n📊 STEP 3: Creating Classrooms")
        print("-" * 29)
        classrooms = create_classrooms()
        
        # Step 4: Assign students
        print("\n📊 STEP 4: Assigning Students")
        print("-" * 29)
        assign_students_to_classrooms()
        
        # Step 5: Create assignments
        print("\n📊 STEP 5: Creating Assignments")
        print("-" * 30)
        assignments = create_assignments()
        
        # Step 6: Create grades
        print("\n📊 STEP 6: Creating Grades")
        print("-" * 25)
        create_grades()
        
        # Step 7: Create attendance
        print("\n📊 STEP 7: Creating Attendance")
        print("-" * 28)
        create_attendance_data()
        
        # Step 8: Create feedback
        print("\n📊 STEP 8: Creating Feedback")
        print("-" * 27)
        create_feedback_data()
        
        # Summary
        print("\n" + "=" * 50)
        print("🎉 DATA EXPANSION COMPLETED!")
        print("=" * 50)
        
        # Count totals
        total_users = User.objects.count()
        total_subjects = Subject.objects.count()
        total_classrooms = Classroom.objects.count()
        total_assignments = Assignment.objects.count()
        total_grades = Grade.objects.count()
        total_attendance = AttendanceSession.objects.count()
        total_feedback = FeedbackSession.objects.count()
        
        print(f"\n📈 CURRENT TOTALS:")
        print(f"👥 Total Users: {total_users}")
        print(f"📚 Total Subjects: {total_subjects}")
        print(f"🏫 Total Classrooms: {total_classrooms}")
        print(f"📝 Total Assignments: {total_assignments}")
        print(f"📊 Total Grades: {total_grades}")
        print(f"📅 Total Attendance Sessions: {total_attendance}")
        print(f"💬 Total Feedback Sessions: {total_feedback}")
        
        print(f"\n🔐 LOGIN CREDENTIALS:")
        print("- Teachers: teacher_demo_1 to teacher_demo_10 / teacher123")
        print("- Students: student_demo_1 to student_demo_30 / student123")
        print("- Parents: parent_demo_1 to parent_demo_20 / parent123")
        
        print(f"\n🌟 YOUR WEBSITE NOW HAS:")
        print("✅ Multiple teachers, students, and parents")
        print("✅ Various subjects and classrooms")
        print("✅ Realistic assignments and grades")
        print("✅ Attendance tracking data")
        print("✅ Feedback system data")
        print("✅ Student-classroom assignments")
        
        print(f"\n🚀 READY FOR TESTING!")
        print("Your Smart Classroom system now has comprehensive data")
        print("for testing and demonstration purposes.")
        
    except Exception as e:
        print(f"❌ Error during data expansion: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
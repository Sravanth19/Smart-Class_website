#!/usr/bin/env python
"""
Add More Data Script - Safely adds additional data to existing Smart Classroom system
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

def add_more_users():
    """Add more users with unique naming to avoid conflicts"""
    print("👥 Adding more users...")
    
    users_created = 0
    
    # Add more teachers (teacher2, teacher3, etc.)
    for i in range(2, 12):  # teacher2 to teacher11
        username = f"teacher{i}"
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
    
    # Add more students (student6, student7, etc.)
    for i in range(6, 36):  # student6 to student35
        username = f"student{i}"
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
    
    # Add more parents (parent2, parent3, etc.)
    for i in range(2, 22):  # parent2 to parent21
        username = f"parent{i}"
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
    
    print(f"✅ Added {users_created} new users")
    return users_created

def add_more_subjects():
    """Add more subjects"""
    print("📚 Adding more subjects...")
    
    additional_subjects = [
        {'name': 'Physics', 'description': 'Physics fundamentals and experiments'},
        {'name': 'Chemistry', 'description': 'Chemistry basics and lab work'},
        {'name': 'Biology', 'description': 'Biology and Life Sciences'},
        {'name': 'English Literature', 'description': 'English Literature and Language'},
        {'name': 'History', 'description': 'World History and Social Studies'},
        {'name': 'Geography', 'description': 'Physical and Human Geography'},
        {'name': 'Computer Science', 'description': 'Programming and Applications'},
        {'name': 'Art', 'description': 'Visual Arts and Creative Expression'},
        {'name': 'Music', 'description': 'Music Theory and Performance'},
        {'name': 'Physical Education', 'description': 'Physical Fitness and Sports'},
    ]
    
    subjects_created = 0
    for subject_data in additional_subjects:
        subject, created = Subject.objects.get_or_create(
            name=subject_data['name'],
            defaults={'description': subject_data['description']}
        )
        if created:
            subjects_created += 1
    
    print(f"✅ Added {subjects_created} new subjects")
    return Subject.objects.all()

def add_more_classrooms():
    """Add more classrooms"""
    print("🏫 Adding more classrooms...")
    
    teachers = User.objects.filter(role='teacher')
    grades = ['6th', '7th', '8th', '9th', '10th', '11th', '12th']
    
    classrooms_created = 0
    for i, grade in enumerate(grades):
        for section in ['A', 'B']:
            name = f"Class {grade} - Section {section}"
            if not Classroom.objects.filter(name=name).exists():
                classroom = Classroom.objects.create(
                    name=name,
                    grade=grade,
                    teacher=random.choice(teachers)
                )
                classrooms_created += 1
    
    print(f"✅ Added {classrooms_created} new classrooms")
    return Classroom.objects.all()

def assign_students_to_new_classrooms():
    """Assign students to classrooms"""
    print("📝 Assigning students to classrooms...")
    
    students = User.objects.filter(role='student')
    classrooms = Classroom.objects.all()
    
    assignments = 0
    for student in students:
        if hasattr(student, 'student_profile'):
            if not student.student_profile.classroom:
                classroom = random.choice(classrooms)
                student.student_profile.classroom = classroom
                student.student_profile.grade = classroom.grade
                student.student_profile.save()
                assignments += 1
    
    print(f"✅ Assigned {assignments} students to classrooms")

def link_parents_to_students():
    """Link parents to students"""
    print("👨‍👩‍👧‍👦 Linking parents to students...")
    
    parents = User.objects.filter(role='parent')
    students = User.objects.filter(role='student')
    
    links_created = 0
    for parent in parents:
        if hasattr(parent, 'parent_profile'):
            # Link each parent to 1-3 random students
            num_children = random.randint(1, min(3, len(students)))
            selected_students = random.sample(list(students), num_children)
            
            for student in selected_students:
                if hasattr(student, 'student_profile'):
                    parent.parent_profile.students.add(student.student_profile)
                    links_created += 1
    
    print(f"✅ Created {links_created} parent-student links")

def add_more_assignments():
    """Add more assignments"""
    print("📋 Adding more assignments...")
    
    teachers = User.objects.filter(role='teacher')
    subjects = Subject.objects.all()
    classrooms = Classroom.objects.all()
    
    assignments_created = 0
    assignment_types = [
        'Homework Assignment',
        'Project Work',
        'Quiz',
        'Lab Report',
        'Essay Writing',
        'Research Paper',
        'Presentation',
        'Group Work'
    ]
    
    for i in range(30):  # Create 30 more assignments
        teacher = random.choice(teachers)
        subject = random.choice(subjects)
        classroom = random.choice(classrooms)
        assignment_type = random.choice(assignment_types)
        
        title = f"{subject.name} - {assignment_type} {i+1}"
        due_date = timezone.now() + timedelta(days=random.randint(1, 30))
        
        if not Assignment.objects.filter(title=title).exists():
            assignment = Assignment.objects.create(
                title=title,
                description=f"Complete the {assignment_type.lower()} for {subject.name}.",
                subject=subject,
                classroom=classroom,
                teacher=teacher,
                due_date=due_date,
                max_points=random.choice([50, 75, 100]),
                status='published',
                priority=random.choice(['low', 'medium', 'high'])
            )
            assignments_created += 1
    
    print(f"✅ Added {assignments_created} new assignments")

def add_assignment_submissions():
    """Add assignment submissions"""
    print("📝 Adding assignment submissions...")
    
    assignments = Assignment.objects.filter(status='published')
    students = User.objects.filter(role='student')
    
    submissions_created = 0
    for assignment in assignments:
        # Get students from the same classroom
        classroom_students = students.filter(student_profile__classroom=assignment.classroom)
        
        # 60-80% of students submit
        num_submissions = int(len(classroom_students) * random.uniform(0.6, 0.8))
        submitting_students = random.sample(list(classroom_students), min(num_submissions, len(classroom_students)))
        
        for student in submitting_students:
            if not AssignmentSubmission.objects.filter(assignment=assignment, student=student).exists():
                submission = AssignmentSubmission.objects.create(
                    assignment=assignment,
                    student=student,
                    submission_text=f"Submission for {assignment.title} by {student.get_full_name()}",
                    status='submitted',
                    grade=random.randint(70, 100),
                    feedback=random.choice(['Good work!', 'Excellent!', 'Well done!', 'Keep it up!'])
                )
                submissions_created += 1
    
    print(f"✅ Added {submissions_created} assignment submissions")

def add_more_grades():
    """Add more grades"""
    print("📊 Adding more grades...")
    
    students = User.objects.filter(role='student')
    subjects = Subject.objects.all()
    teachers = User.objects.filter(role='teacher')
    
    grades_created = 0
    grade_types = ['Test', 'Quiz', 'Assignment', 'Project', 'Exam', 'Participation']
    
    for i in range(100):  # Create 100 more grades
        student = random.choice(students)
        subject = random.choice(subjects)
        teacher = random.choice(teachers)
        grade_type = random.choice(grade_types)
        
        title = f"{subject.name} {grade_type} {i+1}"
        percentage = random.randint(65, 100)
        points_possible = 100
        points_earned = (percentage / 100) * points_possible
        
        if not Grade.objects.filter(student=student, title=title).exists():
            grade = Grade.objects.create(
                student=student,
                subject=subject,
                teacher=teacher,
                title=title,
                grade_type=grade_type.lower(),
                points_earned=points_earned,
                points_possible=points_possible,
                percentage=percentage,
                date_assigned=fake.date_between(start_date='-60d', end_date='today'),
                comments=random.choice([
                    'Excellent work!', 'Good job!', 'Keep improving!', 
                    'Well done!', 'Outstanding!', 'Good effort!'
                ])
            )
            grades_created += 1
    
    print(f"✅ Added {grades_created} new grades")

def add_more_attendance():
    """Add more attendance sessions and records"""
    print("📅 Adding more attendance data...")
    
    teachers = User.objects.filter(role='teacher')
    classrooms = Classroom.objects.all()
    subjects = Subject.objects.all()
    
    sessions_created = 0
    records_created = 0
    
    # Create attendance sessions for the past 30 days
    for i in range(50):  # Create 50 more sessions
        teacher = random.choice(teachers)
        classroom = random.choice(classrooms)
        subject = random.choice(subjects)
        
        session_date = fake.date_time_between(
            start_date='-30d', 
            end_date='now', 
            tzinfo=timezone.get_current_timezone()
        )
        
        title = f"{subject.name} - {classroom.name} - {session_date.strftime('%B %d')}"
        
        if not AttendanceSession.objects.filter(title=title).exists():
            session = AttendanceSession.objects.create(
                title=title,
                description=f"Attendance for {subject.name} class",
                classroom=classroom,
                subject=subject,
                teacher=teacher,
                start_time=session_date,
                end_time=session_date + timedelta(hours=1),
                status='completed',
                attendance_type='daily'
            )
            sessions_created += 1
            
            # Create attendance records for students in this classroom
            students = User.objects.filter(
                role='student',
                student_profile__classroom=classroom
            )
            
            for student in students:
                status = random.choices(
                    ['present', 'late', 'absent'], 
                    weights=[0.8, 0.15, 0.05]
                )[0]
                
                record = AttendanceRecord.objects.create(
                    session=session,
                    student=student,
                    status=status,
                    marked_at=session.start_time + timedelta(minutes=random.randint(0, 30)),
                    marked_by=teacher
                )
                records_created += 1
    
    print(f"✅ Added {sessions_created} attendance sessions and {records_created} records")

def add_more_feedback():
    """Add more feedback sessions"""
    print("💬 Adding more feedback data...")
    
    teachers = User.objects.filter(role='teacher')
    classrooms = Classroom.objects.all()
    subjects = Subject.objects.all()
    categories = FeedbackCategory.objects.all()
    
    sessions_created = 0
    responses_created = 0
    
    feedback_titles = [
        'Course Evaluation Survey',
        'Teaching Effectiveness Review',
        'Student Satisfaction Survey',
        'Mid-term Feedback',
        'End of Unit Assessment',
        'Learning Experience Review',
        'Class Environment Feedback',
        'Instructor Performance Review'
    ]
    
    for i in range(15):  # Create 15 more feedback sessions
        teacher = random.choice(teachers)
        classroom = random.choice(classrooms)
        subject = random.choice(subjects)
        category = random.choice(categories) if categories.exists() else None
        
        title = f"{random.choice(feedback_titles)} - {subject.name} {i+1}"
        
        if not FeedbackSession.objects.filter(title=title).exists():
            session = FeedbackSession.objects.create(
                title=title,
                description=f"Please provide your feedback for {subject.name}",
                category=category,
                classroom=classroom,
                subject=subject,
                created_by=teacher,
                status=random.choice(['active', 'active', 'completed']),  # More active
                visibility='public',
                allow_anonymous=True,
                start_date=timezone.now() - timedelta(days=random.randint(1, 10)),
                end_date=timezone.now() + timedelta(days=random.randint(1, 14))
            )
            sessions_created += 1
            
            # Add some responses for completed sessions
            if session.status == 'completed':
                students = User.objects.filter(
                    role='student',
                    student_profile__classroom=classroom
                )
                
                # 40-70% of students respond
                num_responses = int(len(students) * random.uniform(0.4, 0.7))
                responding_students = random.sample(list(students), min(num_responses, len(students)))
                
                for student in responding_students:
                    response_data = {
                        'rating': random.randint(3, 5),
                        'comment': random.choice([
                            'Great teaching methods!',
                            'Very helpful and clear explanations.',
                            'Could use more examples.',
                            'Enjoyed the interactive sessions.',
                            'Good pace of teaching.',
                            'Excellent course content.'
                        ])
                    }
                    
                    response = FeedbackResponse.objects.create(
                        session=session,
                        respondent=student,
                        response_data=response_data,
                        is_complete=True,
                        completion_time_seconds=random.randint(60, 300),
                        submitted_at=fake.date_time_between(
                            start_date=session.start_date,
                            end_date='now',
                            tzinfo=timezone.get_current_timezone()
                        )
                    )
                    responses_created += 1
    
    print(f"✅ Added {sessions_created} feedback sessions and {responses_created} responses")

def main():
    """Main function to add more data"""
    print("🚀 ADDING MORE DATA TO SMART CLASSROOM")
    print("=" * 45)
    print("Expanding your existing data with more realistic content...")
    print("=" * 45)
    
    try:
        # Step 1: Add more users
        print("\n📊 STEP 1: Adding More Users")
        print("-" * 28)
        users_added = add_more_users()
        
        # Step 2: Add more subjects
        print("\n📊 STEP 2: Adding More Subjects")
        print("-" * 30)
        subjects = add_more_subjects()
        
        # Step 3: Add more classrooms
        print("\n📊 STEP 3: Adding More Classrooms")
        print("-" * 32)
        classrooms = add_more_classrooms()
        
        # Step 4: Assign students to classrooms
        print("\n📊 STEP 4: Assigning Students")
        print("-" * 29)
        assign_students_to_new_classrooms()
        
        # Step 5: Link parents to students
        print("\n📊 STEP 5: Linking Parents & Students")
        print("-" * 35)
        link_parents_to_students()
        
        # Step 6: Add more assignments
        print("\n📊 STEP 6: Adding More Assignments")
        print("-" * 32)
        add_more_assignments()
        
        # Step 7: Add assignment submissions
        print("\n📊 STEP 7: Adding Assignment Submissions")
        print("-" * 38)
        add_assignment_submissions()
        
        # Step 8: Add more grades
        print("\n📊 STEP 8: Adding More Grades")
        print("-" * 28)
        add_more_grades()
        
        # Step 9: Add more attendance
        print("\n📊 STEP 9: Adding More Attendance")
        print("-" * 31)
        add_more_attendance()
        
        # Step 10: Add more feedback
        print("\n📊 STEP 10: Adding More Feedback")
        print("-" * 30)
        add_more_feedback()
        
        # Summary
        print("\n" + "=" * 45)
        print("🎉 DATA EXPANSION COMPLETED!")
        print("=" * 45)
        
        # Count totals
        total_users = User.objects.count()
        total_subjects = Subject.objects.count()
        total_classrooms = Classroom.objects.count()
        total_assignments = Assignment.objects.count()
        total_submissions = AssignmentSubmission.objects.count()
        total_grades = Grade.objects.count()
        total_attendance = AttendanceSession.objects.count()
        total_feedback = FeedbackSession.objects.count()
        
        print(f"\n📈 CURRENT TOTALS:")
        print(f"👥 Total Users: {total_users}")
        print(f"📚 Total Subjects: {total_subjects}")
        print(f"🏫 Total Classrooms: {total_classrooms}")
        print(f"📝 Total Assignments: {total_assignments}")
        print(f"📄 Total Submissions: {total_submissions}")
        print(f"📊 Total Grades: {total_grades}")
        print(f"📅 Total Attendance Sessions: {total_attendance}")
        print(f"💬 Total Feedback Sessions: {total_feedback}")
        
        print(f"\n🔐 LOGIN CREDENTIALS:")
        print("- Admin: admin / admin123")
        print("- Teachers: teacher1-teacher11 / teacher123")
        print("- Students: student1-student35 / student123")
        print("- Parents: parent1-parent21 / parent123")
        
        print(f"\n🌟 YOUR WEBSITE NOW HAS:")
        print("✅ Multiple teachers, students, and parents")
        print("✅ Comprehensive subject coverage")
        print("✅ Multi-grade classroom structure")
        print("✅ Rich assignment and submission data")
        print("✅ Extensive grade records")
        print("✅ Detailed attendance tracking")
        print("✅ Active feedback system")
        print("✅ Parent-student relationships")
        
        print(f"\n🚀 READY FOR DEMONSTRATION!")
        print("Your Smart Classroom system now has comprehensive")
        print("data suitable for showcasing all features!")
        
    except Exception as e:
        print(f"❌ Error during data expansion: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
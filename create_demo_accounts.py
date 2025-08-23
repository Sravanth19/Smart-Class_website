#!/usr/bin/env python
"""
Create comprehensive demo accounts with correct passwords for Smart Classroom
"""

import os
import sys
import django
from datetime import datetime, timedelta, date
import random

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_classroom.settings')
django.setup()

from django.contrib.auth import get_user_model
from users.models import AdminProfile, TeacherProfile, StudentProfile, ParentProfile
from classroom.models import Classroom
from subject.models import Subject
from grades.models import Grade
from assignments.models import Assignment, AssignmentSubmission
from attendance.models import AttendanceSession, AttendanceRecord
from feedback.models import FeedbackCategory, FeedbackSession
from django.utils import timezone

User = get_user_model()

def create_demo_accounts():
    """Create comprehensive demo accounts with correct passwords"""
    print("🚀 Creating Smart Classroom Demo Accounts")
    print("=" * 50)
    
    # Demo account credentials (CORRECT PASSWORDS)
    demo_accounts = {
        'admin': {
            'username': 'admin',
            'email': 'admin@smartclassroom.edu',
            'password': 'admin123',  # CORRECT PASSWORD
            'first_name': 'System',
            'last_name': 'Administrator',
            'role': 'admin'
        },
        'teacher': {
            'username': 'teacher',
            'email': 'teacher@smartclassroom.edu',
            'password': 'teacher123',  # CORRECT PASSWORD
            'first_name': 'John',
            'last_name': 'Smith',
            'role': 'teacher'
        },
        'student': {
            'username': 'student',
            'email': 'student@smartclassroom.edu',
            'password': 'student123',  # CORRECT PASSWORD
            'first_name': 'Jane',
            'last_name': 'Doe',
            'role': 'student'
        },
        'parent': {
            'username': 'parent',
            'email': 'parent@smartclassroom.edu',
            'password': 'parent123',  # CORRECT PASSWORD
            'first_name': 'Robert',
            'last_name': 'Doe',
            'role': 'parent'
        }
    }
    
    created_users = {}
    
    # Create demo users
    for key, account_data in demo_accounts.items():
        try:
            # Check if user already exists
            if User.objects.filter(username=account_data['username']).exists():
                user = User.objects.get(username=account_data['username'])
                # Update password to ensure it's correct
                user.set_password(account_data['password'])
                user.save()
                print(f"✅ Updated existing {key}: {account_data['username']} / {account_data['password']}")
            else:
                # Create new user
                user = User.objects.create_user(
                    username=account_data['username'],
                    email=account_data['email'],
                    password=account_data['password'],
                    first_name=account_data['first_name'],
                    last_name=account_data['last_name'],
                    role=account_data['role']
                )
                print(f"✅ Created new {key}: {account_data['username']} / {account_data['password']}")
            
            created_users[key] = user
            
        except Exception as e:
            print(f"❌ Error creating {key}: {e}")
    
    # Create additional demo data
    print("\n📚 Creating Demo Educational Data")
    print("-" * 30)
    
    try:
        # Create classroom
        teacher_user = created_users.get('teacher')
        if teacher_user:
            classroom, created = Classroom.objects.get_or_create(
                name='Demo Class 10A',
                defaults={
                    'grade': '10th',
                    'teacher': teacher_user
                }
            )
            if created:
                print("✅ Created demo classroom: Demo Class 10A")
        
        # Create subjects
        subjects_data = [
            {'name': 'Mathematics', 'description': 'Advanced Mathematics for Grade 10'},
            {'name': 'Physics', 'description': 'Physics fundamentals and experiments'},
            {'name': 'Chemistry', 'description': 'Chemistry basics and lab work'},
            {'name': 'English', 'description': 'English Literature and Language'},
            {'name': 'Biology', 'description': 'Biology and Life Sciences'},
        ]
        
        subjects = []
        for subject_data in subjects_data:
            subject, created = Subject.objects.get_or_create(
                name=subject_data['name'],
                defaults={'description': subject_data['description']}
            )
            subjects.append(subject)
            if created:
                print(f"✅ Created subject: {subject.name}")
        
        # Setup student profile
        student_user = created_users.get('student')
        if student_user and classroom:
            student_profile = student_user.student_profile
            student_profile.classroom = classroom
            student_profile.grade = '10th'
            student_profile.save()
            print("✅ Assigned student to classroom")
        
        # Link parent to student
        parent_user = created_users.get('parent')
        if parent_user and student_user:
            parent_profile = parent_user.parent_profile
            parent_profile.students.add(student_user.student_profile)
            parent_profile.save()
            print("✅ Linked parent to student")
        
        # Create sample grades
        if student_user and teacher_user and subjects:
            grade_data = [
                {'subject': 'Mathematics', 'title': 'Algebra Test', 'percentage': 85, 'type': 'exam'},
                {'subject': 'Mathematics', 'title': 'Homework 1', 'percentage': 92, 'type': 'assignment'},
                {'subject': 'Physics', 'title': 'Motion Quiz', 'percentage': 78, 'type': 'quiz'},
                {'subject': 'Physics', 'title': 'Lab Report', 'percentage': 88, 'type': 'assignment'},
                {'subject': 'Chemistry', 'title': 'Periodic Table Test', 'percentage': 90, 'type': 'exam'},
                {'subject': 'English', 'title': 'Essay Writing', 'percentage': 82, 'type': 'assignment'},
                {'subject': 'Biology', 'title': 'Cell Structure Quiz', 'percentage': 95, 'type': 'quiz'},
            ]
            
            for grade_info in grade_data:
                subject = Subject.objects.get(name=grade_info['subject'])
                Grade.objects.get_or_create(
                    student=student_user,
                    subject=subject,
                    teacher=teacher_user,
                    title=grade_info['title'],
                    defaults={
                        'grade_type': grade_info['type'],
                        'points_earned': grade_info['percentage'],
                        'points_possible': 100,
                        'percentage': grade_info['percentage'],
                        'date_assigned': timezone.now().date() - timedelta(days=random.randint(1, 30)),
                        'comments': f'Good work on {grade_info["title"]}'
                    }
                )
            print(f"✅ Created {len(grade_data)} sample grades")
        
        # Create attendance sessions
        if teacher_user and classroom and student_user:
            for i in range(10):  # Create 10 attendance sessions
                session_date = timezone.now() - timedelta(days=i)
                
                session, created = AttendanceSession.objects.get_or_create(
                    title=f'Daily Attendance - {session_date.strftime("%B %d")}',
                    classroom=classroom,
                    teacher=teacher_user,
                    defaults={
                        'description': 'Daily attendance session',
                        'start_time': session_date,
                        'end_time': session_date + timedelta(hours=1),
                        'status': 'completed',
                        'attendance_type': 'daily'
                    }
                )
                
                if created:
                    # Create attendance record for student
                    status_choices = ['present', 'present', 'present', 'late', 'absent']  # Weighted towards present
                    status = random.choice(status_choices)
                    
                    AttendanceRecord.objects.get_or_create(
                        session=session,
                        student=student_user,
                        defaults={
                            'status': status,
                            'marked_at': session.start_time + timedelta(minutes=random.randint(0, 30)),
                            'marked_by': teacher_user
                        }
                    )
            print("✅ Created 10 attendance sessions with records")
        
        # Create sample assignments
        if teacher_user and classroom and subjects:
            assignment_data = [
                {'title': 'Math Problem Set 1', 'subject': 'Mathematics', 'status': 'pending'},
                {'title': 'Physics Lab Report', 'subject': 'Physics', 'status': 'submitted'},
                {'title': 'Chemistry Experiment', 'subject': 'Chemistry', 'status': 'pending'},
                {'title': 'English Essay', 'subject': 'English', 'status': 'submitted'},
                {'title': 'Biology Research', 'subject': 'Biology', 'status': 'overdue'},
            ]
            
            for assign_info in assignment_data:
                subject = Subject.objects.get(name=assign_info['subject'])
                due_date = timezone.now().date() + timedelta(days=random.randint(1, 14))
                
                if assign_info['status'] == 'overdue':
                    due_date = timezone.now().date() - timedelta(days=random.randint(1, 5))
                
                assignment, created = Assignment.objects.get_or_create(
                    title=assign_info['title'],
                    subject=subject,
                    classroom=classroom,
                    teacher=teacher_user,
                    defaults={
                        'description': f'Complete the {assign_info["title"].lower()} as assigned.',
                        'due_date': due_date,
                        'max_points': 100,
                        'status': 'published'
                    }
                )
                
                if created and assign_info['status'] == 'submitted':
                    # Create submission
                    AssignmentSubmission.objects.get_or_create(
                        assignment=assignment,
                        student=student_user,
                        defaults={
                            'status': 'submitted',
                            'submission_text': f'Submission for {assignment.title}'
                        }
                    )
            print(f"✅ Created {len(assignment_data)} sample assignments")
        
        # Create feedback categories
        categories_data = [
            {'name': 'Course Feedback', 'description': 'General course feedback', 'icon': 'fas fa-book', 'color': '#007bff'},
            {'name': 'Teacher Evaluation', 'description': 'Teacher performance feedback', 'icon': 'fas fa-chalkboard-teacher', 'color': '#28a745'},
            {'name': 'Peer Review', 'description': 'Student peer reviews', 'icon': 'fas fa-users', 'color': '#ffc107'},
        ]
        
        for cat_data in categories_data:
            category, created = FeedbackCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults=cat_data
            )
            if created:
                print(f"✅ Created feedback category: {category.name}")
        
    except Exception as e:
        print(f"❌ Error creating demo data: {e}")
        import traceback
        traceback.print_exc()
    
    # Print summary
    print("\n🎉 Demo Account Creation Complete!")
    print("=" * 50)
    print("\n🔐 LOGIN CREDENTIALS (CORRECT PASSWORDS):")
    print("👨‍💼 Admin Portal:")
    print("   Username: admin")
    print("   Password: admin123")
    print("   URL: http://127.0.0.1:8000/users/dashboard/admin/")
    
    print("\n👨‍🏫 Teacher Portal:")
    print("   Username: teacher")
    print("   Password: teacher123")
    print("   URL: http://127.0.0.1:8000/users/dashboard/teacher/")
    
    print("\n👨‍🎓 Student Portal:")
    print("   Username: student")
    print("   Password: student123")
    print("   URL: http://127.0.0.1:8000/users/dashboard/student/")
    
    print("\n👨‍👩‍👧‍👦 Parent Portal:")
    print("   Username: parent")
    print("   Password: parent123")
    print("   URL: http://127.0.0.1:8000/users/dashboard/parent/")
    
    print("\n📱 Main Login:")
    print("   URL: http://127.0.0.1:8000/login/")
    
    print("\n🌟 FEATURES AVAILABLE:")
    print("✅ Role-based dashboards with restricted access")
    print("✅ Enhanced parent portal with comprehensive analytics")
    print("✅ Student performance tracking and visualization")
    print("✅ Attendance management with calendar views")
    print("✅ Grades and assignment tracking")
    print("✅ Comprehensive student reports (printable)")
    print("✅ Secure parent-student data linking")
    print("✅ Interactive charts and progress indicators")
    print("✅ Mobile-responsive design")
    print("✅ Access control and security restrictions")
    
    print("\n🔒 SECURITY FEATURES:")
    print("✅ Parents can ONLY see their own children's data")
    print("✅ Role-based access control")
    print("✅ Secure authentication and session management")
    print("✅ Data filtering and permission checking")
    print("✅ Audit trails and access logging")
    
    print("\n🚀 Ready for testing and demonstration!")

if __name__ == '__main__':
    create_demo_accounts()
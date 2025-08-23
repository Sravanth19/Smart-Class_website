#!/usr/bin/env python
"""
Comprehensive Data Expansion Script for Smart Classroom System
This script will add realistic amounts of data across all modules to make the website more robust.
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
# from notifications.models import Notification  # Not available in current setup

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
    {'name': 'Physical Education', 'description': 'Physical Fitness and Sports'},
    {'name': 'Economics', 'description': 'Economics and Business Studies'},
    {'name': 'Psychology', 'description': 'Introduction to Psychology'},
    {'name': 'Environmental Science', 'description': 'Environmental Studies and Conservation'},
    {'name': 'Statistics', 'description': 'Statistics and Data Analysis'},
]

ASSIGNMENT_TYPES = ['homework', 'project', 'quiz', 'exam', 'presentation', 'lab_report', 'essay', 'research']
GRADE_TYPES = ['assignment', 'quiz', 'exam', 'project', 'participation', 'homework']
ATTENDANCE_STATUSES = ['present', 'late', 'absent', 'excused']

def create_teachers(count=25):
    """Create realistic teacher accounts"""
    print(f"🧑‍🏫 Creating {count} teachers...")
    
    teachers = []
    departments = ['Mathematics', 'Science', 'English', 'Social Studies', 'Arts', 'Physical Education', 'Technology']
    
    for i in range(count):
        first_name = fake.first_name()
        last_name = fake.last_name()
        username = f"teacher_{first_name.lower()}_{last_name.lower()}_{i+1}"
        email = f"{username}@smartclassroom.edu"
        
        teacher, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': email,
                'first_name': first_name,
                'last_name': last_name,
                'role': 'teacher',
                'phone_number': fake.phone_number()[:15],
                'address': fake.address()[:200],
                'date_of_birth': fake.date_of_birth(minimum_age=25, maximum_age=65),
                'is_active': True
            }
        )
        
        if created:
            teacher.set_password('teacher123')
            teacher.save()
            
            # Create teacher profile
            profile, _ = TeacherProfile.objects.get_or_create(
                user=teacher,
                defaults={
                    'department': random.choice(departments),
                    'hire_date': fake.date_between(start_date='-10y', end_date='today'),
                    'qualification': random.choice(['B.Ed', 'M.Ed', 'M.A.', 'M.Sc.', 'Ph.D.']),
                    'experience_years': random.randint(1, 30),
                    'specialization': random.choice(SUBJECTS_DATA)['name']
                }
            )
            teachers.append(teacher)
    
    print(f"✅ Created {len(teachers)} new teachers")
    return teachers

def create_students(count=80):
    """Create realistic student accounts"""
    print(f"👨‍🎓 Creating {count} students...")
    
    students = []
    
    for i in range(count):
        first_name = fake.first_name()
        last_name = fake.last_name()
        username = f"student_{first_name.lower()}_{last_name.lower()}_{i+1}"
        email = f"{username}@smartclassroom.edu"
        
        student, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': email,
                'first_name': first_name,
                'last_name': last_name,
                'role': 'student',
                'phone_number': fake.phone_number()[:15],
                'address': fake.address()[:200],
                'date_of_birth': fake.date_of_birth(minimum_age=10, maximum_age=18),
                'is_active': True
            }
        )
        
        if created:
            student.set_password('student123')
            student.save()
            
            # Create student profile
            profile, _ = StudentProfile.objects.get_or_create(
                user=student,
                defaults={
                    'grade': random.choice(GRADES_LIST),
                    'admission_date': fake.date_between(start_date='-3y', end_date='today'),
                    'parent_guardian_name': fake.name(),
                    'parent_guardian_phone': fake.phone_number()[:15],
                    'emergency_contact_name': fake.name(),
                    'emergency_contact_phone': fake.phone_number()[:15],
                    'blood_group': random.choice(['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']),
                    'medical_conditions': random.choice(['None', 'Asthma', 'Allergies', 'Diabetes', 'None', 'None'])
                }
            )
            students.append(student)
    
    print(f"✅ Created {len(students)} new students")
    return students

def create_parents(students, count=60):
    """Create parent accounts and link them to students"""
    print(f"👨‍👩‍👧‍👦 Creating {count} parents...")
    
    parents = []
    
    for i in range(count):
        first_name = fake.first_name()
        last_name = fake.last_name()
        username = f"parent_{first_name.lower()}_{last_name.lower()}_{i+1}"
        email = f"{username}@smartclassroom.edu"
        
        parent, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': email,
                'first_name': first_name,
                'last_name': last_name,
                'role': 'parent',
                'phone_number': fake.phone_number()[:15],
                'address': fake.address()[:200],
                'date_of_birth': fake.date_of_birth(minimum_age=25, maximum_age=60),
                'is_active': True
            }
        )
        
        if created:
            parent.set_password('parent123')
            parent.save()
            
            # Create parent profile and link to 1-3 students
            profile, _ = ParentProfile.objects.get_or_create(
                user=parent,
                defaults={
                    'occupation': fake.job(),
                    'relationship': random.choice(['Father', 'Mother', 'Guardian']),
                    'workplace': fake.company(),
                    'work_phone': fake.phone_number()[:15]
                }
            )
            
            # Link to random students (1-3 children per parent)
            num_children = random.randint(1, min(3, len(students)))
            selected_students = random.sample(students, num_children)
            
            for student in selected_students:
                profile.students.add(student.student_profile)
            
            parents.append(parent)
    
    print(f"✅ Created {len(parents)} new parents")
    return parents

def create_classrooms(teachers, count=15):
    """Create realistic classrooms"""
    print(f"🏫 Creating {count} classrooms...")
    
    classrooms = []
    
    for i in range(count):
        grade = random.choice(GRADES_LIST)
        section = chr(65 + (i % 10))  # A, B, C, etc.
        name = f"Class {grade} - Section {section}"
        
        classroom, created = Classroom.objects.get_or_create(
            name=name,
            defaults={
                'grade': grade,
                'teacher': random.choice(teachers)
            }
        )
        
        if created:
            classrooms.append(classroom)
    
    print(f"✅ Created {len(classrooms)} new classrooms")
    return classrooms

def assign_students_to_classrooms(students, classrooms):
    """Assign students to classrooms based on their grade"""
    print("📚 Assigning students to classrooms...")
    
    assignments = 0
    
    for student in students:
        student_grade = student.student_profile.grade
        # Find classrooms matching the student's grade
        matching_classrooms = [c for c in classrooms if c.grade == student_grade]
        
        if matching_classrooms:
            # Assign to a random classroom of the same grade
            classroom = random.choice(matching_classrooms)
            student.student_profile.classroom = classroom
            student.student_profile.save()
            assignments += 1
    
    print(f"✅ Assigned {assignments} students to classrooms")

def create_subjects_and_assignments(teachers, classrooms, count=50):
    """Create subjects and assignments"""
    print(f"📖 Creating subjects and {count} assignments...")
    
    # Create subjects
    subjects = []
    for subject_data in SUBJECTS_DATA:
        subject, created = Subject.objects.get_or_create(
            name=subject_data['name'],
            defaults={
                'description': subject_data['description']
            }
        )
        subjects.append(subject)
    
    print(f"✅ Created {len(subjects)} subjects")
    
    # Create assignments
    assignments = []
    for i in range(count):
        teacher = random.choice(teachers)
        subject = random.choice(subjects)
        classroom = random.choice(classrooms)
        
        assignment_titles = [
            f"{subject.name} - Chapter {random.randint(1, 15)} Exercise",
            f"{subject.name} - Weekly Quiz {random.randint(1, 20)}",
            f"{subject.name} - Project Work",
            f"{subject.name} - Lab Assignment",
            f"{subject.name} - Research Paper",
            f"{subject.name} - Problem Set {random.randint(1, 10)}",
            f"{subject.name} - Case Study Analysis",
            f"{subject.name} - Group Presentation"
        ]
        
        title = random.choice(assignment_titles)
        
        # Create assignment with realistic dates
        created_date = fake.date_between(start_date='-60d', end_date='today')
        due_date = created_date + timedelta(days=random.randint(3, 21))
        
        assignment, created = Assignment.objects.get_or_create(
            title=title,
            subject=subject,
            classroom=classroom,
            teacher=teacher,
            due_date=due_date,
            defaults={
                'description': f"Complete the {title.lower()} as per the instructions provided in class.",
                'max_points': random.choice([10, 20, 25, 50, 100]),
                'status': random.choice(['draft', 'published', 'published', 'published']),  # More published
                'priority': random.choice(['low', 'medium', 'high']),
                'allow_late_submission': random.choice([True, False]),
                'late_penalty_percent': random.randint(5, 20)
            }
        )
        
        if created:
            assignments.append(assignment)
    
    print(f"✅ Created {len(assignments)} new assignments")
    return subjects, assignments

def create_assignment_submissions(assignments, students):
    """Create assignment submissions"""
    print("📝 Creating assignment submissions...")
    
    submissions = 0
    
    for assignment in assignments:
        if assignment.status == 'published':
            # Get students from the same classroom
            classroom_students = [s for s in students if hasattr(s, 'student_profile') and 
                                s.student_profile.classroom == assignment.classroom]
            
            # 70-90% of students submit assignments
            num_submissions = int(len(classroom_students) * random.uniform(0.7, 0.9))
            submitting_students = random.sample(classroom_students, min(num_submissions, len(classroom_students)))
            
            for student in submitting_students:
                submission_date = assignment.due_date - timedelta(days=random.randint(0, 7))
                if submission_date < assignment.created_at:
                    submission_date = assignment.created_at + timedelta(days=1)
                
                status = 'submitted'
                if submission_date > assignment.due_date:
                    status = 'late'
                elif random.random() < 0.1:  # 10% chance of draft
                    status = 'draft'
                
                submission, created = AssignmentSubmission.objects.get_or_create(
                    assignment=assignment,
                    student=student,
                    defaults={
                        'status': status,
                        'submission_text': f"Submission for {assignment.title} by {student.get_full_name()}",
                        'grade': random.randint(60, 100) if status == 'submitted' else None,
                        'feedback': "Good work!" if status == 'submitted' else None
                    }
                )
                
                if created:
                    submissions += 1
    
    print(f"✅ Created {submissions} assignment submissions")

def create_grades(students, subjects, teachers, count=200):
    """Create realistic grades"""
    print(f"📊 Creating {count} grades...")
    
    grades = []
    
    for i in range(count):
        student = random.choice(students)
        subject = random.choice(subjects)
        teacher = random.choice(teachers)
        
        grade_titles = [
            f"{subject.name} - Unit Test {random.randint(1, 5)}",
            f"{subject.name} - Quiz {random.randint(1, 10)}",
            f"{subject.name} - Assignment {random.randint(1, 8)}",
            f"{subject.name} - Project Work",
            f"{subject.name} - Lab Practical",
            f"{subject.name} - Midterm Exam",
            f"{subject.name} - Final Exam",
            f"{subject.name} - Participation"
        ]
        
        title = random.choice(grade_titles)
        points_possible = random.choice([10, 20, 25, 50, 100])
        
        # Generate realistic grade distribution (bell curve)
        percentage = max(0, min(100, random.normalvariate(78, 12)))  # Mean 78%, std dev 12%
        points_earned = (percentage / 100) * points_possible
        
        grade, created = Grade.objects.get_or_create(
            student=student,
            subject=subject,
            teacher=teacher,
            title=title,
            defaults={
                'grade_type': random.choice(GRADE_TYPES),
                'points_earned': round(points_earned, 2),
                'points_possible': points_possible,
                'percentage': round(percentage, 2),
                'date_assigned': fake.date_between(start_date='-90d', end_date='today'),
                'comments': random.choice([
                    "Excellent work!",
                    "Good effort, keep it up!",
                    "Needs improvement in some areas.",
                    "Well done!",
                    "Outstanding performance!",
                    "Good understanding of concepts.",
                    "Please see me for additional help.",
                    "Great improvement!"
                ])
            }
        )
        
        if created:
            grades.append(grade)
    
    print(f"✅ Created {len(grades)} new grades")
    return grades

def create_attendance_sessions(teachers, classrooms, subjects, count=100):
    """Create attendance sessions"""
    print(f"📅 Creating {count} attendance sessions...")
    
    sessions = []
    
    for i in range(count):
        teacher = random.choice(teachers)
        classroom = random.choice(classrooms)
        subject = random.choice(subjects)
        
        # Create sessions over the past 90 days
        session_date = fake.date_time_between(start_date='-90d', end_date='now', tzinfo=timezone.get_current_timezone())
        
        session, created = AttendanceSession.objects.get_or_create(
            title=f"{subject.name} - {classroom.name}",
            classroom=classroom,
            subject=subject,
            teacher=teacher,
            start_time=session_date,
            defaults={
                'description': f"Daily attendance for {subject.name} class",
                'end_time': session_date + timedelta(hours=1),
                'status': 'completed',
                'attendance_type': 'daily',
                'duration_minutes': random.choice([45, 50, 60, 90]),
                'late_threshold_minutes': 15
            }
        )
        
        if created:
            sessions.append(session)
    
    print(f"✅ Created {len(sessions)} attendance sessions")
    return sessions

def create_attendance_records(sessions, students):
    """Create attendance records for sessions"""
    print("✅ Creating attendance records...")
    
    records = 0
    
    for session in sessions:
        # Get students from the same classroom
        classroom_students = [s for s in students if hasattr(s, 'student_profile') and 
                            s.student_profile.classroom == session.classroom]
        
        for student in classroom_students:
            # 85% present, 10% late, 5% absent
            status_weights = [('present', 0.85), ('late', 0.10), ('absent', 0.05)]
            status = random.choices([s[0] for s in status_weights], 
                                  weights=[s[1] for s in status_weights])[0]
            
            marked_time = session.start_time
            if status == 'late':
                marked_time += timedelta(minutes=random.randint(16, 45))
            elif status == 'present':
                marked_time += timedelta(minutes=random.randint(0, 15))
            
            record, created = AttendanceRecord.objects.get_or_create(
                session=session,
                student=student,
                defaults={
                    'status': status,
                    'marked_at': marked_time,
                    'marked_by': session.teacher,
                    'ip_address': fake.ipv4(),
                    'user_agent': fake.user_agent(),
                    'notes': random.choice(['', '', '', 'Medical appointment', 'Family emergency', 'School event'])
                }
            )
            
            if created:
                records += 1
    
    print(f"✅ Created {records} attendance records")

def create_feedback_sessions(teachers, classrooms, subjects, count=30):
    """Create feedback sessions"""
    print(f"💬 Creating {count} feedback sessions...")
    
    # Ensure feedback categories exist
    categories_data = [
        {'name': 'Course Evaluation', 'description': 'Feedback about course content and delivery'},
        {'name': 'Teacher Performance', 'description': 'Feedback about teaching effectiveness'},
        {'name': 'Student Experience', 'description': 'General student experience feedback'},
        {'name': 'Peer Review', 'description': 'Student peer evaluation'},
        {'name': 'Self Assessment', 'description': 'Student self-reflection'},
    ]
    
    categories = []
    for cat_data in categories_data:
        category, created = FeedbackCategory.objects.get_or_create(
            name=cat_data['name'],
            defaults=cat_data
        )
        categories.append(category)
    
    sessions = []
    
    for i in range(count):
        teacher = random.choice(teachers)
        classroom = random.choice(classrooms)
        subject = random.choice(subjects)
        category = random.choice(categories)
        
        titles = [
            f"{subject.name} - Mid-term Feedback",
            f"{subject.name} - Course Evaluation",
            f"Teaching Effectiveness - {teacher.get_full_name()}",
            f"Student Experience Survey - {classroom.name}",
            f"{subject.name} - Weekly Feedback",
            f"Peer Review Session - {subject.name}",
            f"Self Assessment - {subject.name}"
        ]
        
        title = random.choice(titles)
        
        session, created = FeedbackSession.objects.get_or_create(
            title=title,
            created_by=teacher,
            defaults={
                'description': f"Please provide your honest feedback about {title.lower()}",
                'category': category,
                'classroom': classroom,
                'subject': subject,
                'status': random.choice(['active', 'active', 'completed']),  # More active sessions
                'visibility': random.choice(['public', 'private']),
                'allow_anonymous': random.choice([True, False]),
                'allow_multiple_responses': False,
                'send_notifications': True,
                'start_date': timezone.now() - timedelta(days=random.randint(1, 30)),
                'end_date': timezone.now() + timedelta(days=random.randint(1, 14))
            }
        )
        
        if created:
            sessions.append(session)
    
    print(f"✅ Created {len(sessions)} feedback sessions")
    return sessions

def create_feedback_responses(feedback_sessions, students):
    """Create sample feedback responses"""
    print("💬 Creating feedback responses...")
    
    responses = 0
    
    for session in feedback_sessions:
        if session.status == 'active':
            # Get students from the same classroom
            classroom_students = [s for s in students if hasattr(s, 'student_profile') and 
                                s.student_profile.classroom == session.classroom]
            
            # 40-70% of students respond to feedback
            num_responses = int(len(classroom_students) * random.uniform(0.4, 0.7))
            responding_students = random.sample(classroom_students, min(num_responses, len(classroom_students)))
            
            for student in responding_students:
                # Create sample response data
                response_data = {
                    'rating': random.randint(3, 5),
                    'comment': random.choice([
                        "Great teaching methods!",
                        "Could use more examples.",
                        "Very helpful and clear.",
                        "Enjoyed the interactive sessions.",
                        "Would like more practice problems.",
                        "Excellent course content.",
                        "Good pace of teaching."
                    ]),
                    'recommendation': random.choice(['Yes', 'Maybe', 'Yes', 'Yes'])
                }
                
                response, created = FeedbackResponse.objects.get_or_create(
                    session=session,
                    respondent=student,
                    defaults={
                        'response_data': response_data,
                        'is_complete': True,
                        'completion_time_seconds': random.randint(60, 300),
                        'submitted_at': fake.date_time_between(
                            start_date=session.start_date, 
                            end_date='now', 
                            tzinfo=timezone.get_current_timezone()
                        )
                    }
                )
                
                if created:
                    responses += 1
    
    print(f"✅ Created {responses} feedback responses")
    return responses

def main():
    """Main function to run comprehensive data expansion"""
    print("🚀 COMPREHENSIVE DATA EXPANSION FOR SMART CLASSROOM")
    print("=" * 60)
    print("This will add realistic amounts of data to make your website more robust.")
    print("Estimated time: 2-3 minutes")
    print("=" * 60)
    
    try:
        # Step 1: Create users
        print("\n📊 PHASE 1: Creating Users")
        print("-" * 30)
        teachers = create_teachers(25)
        students = create_students(80)
        parents = create_parents(students, 60)
        
        # Step 2: Create educational structure
        print("\n📊 PHASE 2: Creating Educational Structure")
        print("-" * 40)
        classrooms = create_classrooms(teachers, 15)
        assign_students_to_classrooms(students, classrooms)
        
        # Step 3: Create academic content
        print("\n📊 PHASE 3: Creating Academic Content")
        print("-" * 35)
        subjects, assignments = create_subjects_and_assignments(teachers, classrooms, 50)
        create_assignment_submissions(assignments, students)
        grades = create_grades(students, subjects, teachers, 200)
        
        # Step 4: Create attendance data
        print("\n📊 PHASE 4: Creating Attendance Data")
        print("-" * 35)
        sessions = create_attendance_sessions(teachers, classrooms, subjects, 100)
        create_attendance_records(sessions, students)
        
        # Step 5: Create feedback and responses
        print("\n📊 PHASE 5: Creating Feedback & Responses")
        print("-" * 40)
        feedback_sessions = create_feedback_sessions(teachers, classrooms, subjects, 30)
        feedback_responses = create_feedback_responses(feedback_sessions, students)
        
        # Summary
        print("\n" + "=" * 60)
        print("🎉 COMPREHENSIVE DATA EXPANSION COMPLETED!")
        print("=" * 60)
        
        print(f"\n📈 DATA SUMMARY:")
        print(f"👨‍🏫 Teachers: {len(teachers)} new")
        print(f"👨‍🎓 Students: {len(students)} new")
        print(f"👨‍👩‍👧‍👦 Parents: {len(parents)} new")
        print(f"🏫 Classrooms: {len(classrooms)} new")
        print(f"📚 Subjects: {len(subjects)} total")
        print(f"📝 Assignments: {len(assignments)} new")
        print(f"📊 Grades: {len(grades)} new")
        print(f"📅 Attendance Sessions: {len(sessions)} new")
        print(f"💬 Feedback Sessions: {len(feedback_sessions)} new")
        print(f"📝 Feedback Responses: {feedback_responses} new")
        
        print(f"\n🔐 LOGIN CREDENTIALS:")
        print("All new accounts use these passwords:")
        print("- Teachers: teacher123")
        print("- Students: student123")
        print("- Parents: parent123")
        
        print(f"\n🌟 YOUR WEBSITE NOW HAS:")
        print("✅ Realistic school-sized data")
        print("✅ Complete academic records")
        print("✅ Comprehensive attendance tracking")
        print("✅ Rich grade and assignment data")
        print("✅ Active feedback systems")
        print("✅ Parent-student relationships")
        print("✅ Feedback responses and analytics")
        print("✅ Multi-grade classroom structure")
        
        print(f"\n🚀 READY FOR DEMONSTRATION!")
        print("Your Smart Classroom system now has comprehensive data")
        print("suitable for showcasing all features and functionality.")
        
    except Exception as e:
        print(f"❌ Error during data expansion: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
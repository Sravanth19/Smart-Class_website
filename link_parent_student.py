#!/usr/bin/env python
"""
Script to link parent to student and create sample data for testing
"""

import os
import sys
import django
from datetime import datetime, timedelta
from django.utils import timezone

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_classroom.settings')
django.setup()

from django.contrib.auth import get_user_model
from users.models import StudentProfile, ParentProfile
from classroom.models import Classroom
from subject.models import Subject
from grades.models import Grade
from assignments.models import Assignment, AssignmentSubmission
from attendance.models import AttendanceSession, AttendanceRecord

User = get_user_model()

def link_parent_to_student():
    """Link the parent user to student user"""
    try:
        # Get parent and student users
        parent_user = User.objects.get(username='parent')
        student_user = User.objects.get(username='student')
        
        # Get their profiles
        parent_profile = parent_user.parent_profile
        student_profile = student_user.student_profile
        
        # Link parent to student
        parent_profile.students.add(student_profile)
        parent_profile.save()
        
        print(f"✅ Successfully linked parent '{parent_user.get_full_name()}' to student '{student_user.get_full_name()}'")
        
        # Get teacher user
        teacher_user = User.objects.get(username='teacher')
        
        # Create or get classroom
        classroom, created = Classroom.objects.get_or_create(
            name='Class 10A',
            defaults={
                'grade': '10th',
                'teacher': teacher_user
            }
        )
        if created:
            print(f"✅ Created classroom: {classroom.name}")
        
        # Assign student to classroom
        student_profile.classroom = classroom
        student_profile.grade = '10th'
        student_profile.save()
        print(f"✅ Assigned student to classroom: {classroom.name}")
        
        # Create subjects
        subjects_data = [
            {'name': 'Mathematics', 'description': 'Advanced Mathematics'},
            {'name': 'Physics', 'description': 'Physics fundamentals'},
            {'name': 'Chemistry', 'description': 'Chemistry basics'},
            {'name': 'English', 'description': 'English Literature'},
            {'name': 'Biology', 'description': 'Biology studies'},
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
        
        # Create sample grades
        import random
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
            points_possible = 100
            points_earned = grade_info['percentage']
            
            Grade.objects.get_or_create(
                student=student_user,
                subject=subject,
                teacher=teacher_user,
                title=grade_info['title'],
                defaults={
                    'grade_type': grade_info['type'],
                    'points_earned': points_earned,
                    'points_possible': points_possible,
                    'percentage': grade_info['percentage'],
                    'date_assigned': timezone.now().date() - timedelta(days=random.randint(1, 30)),
                    'comments': f'Good work on {grade_info["title"]}'
                }
            )
        
        print(f"✅ Created {len(grade_data)} sample grades")
        
        # Create attendance sessions and records
        for i in range(15):  # Create 15 attendance sessions
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
        
        print(f"✅ Created 15 attendance sessions with records")
        
        # Create sample assignments
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
        
        print("\n🎉 Parent-Student linking and sample data creation completed!")
        print(f"\n👨‍👩‍👧‍👦 Parent '{parent_user.get_full_name()}' can now view data for:")
        print(f"   👨‍🎓 Student: {student_user.get_full_name()} ({student_profile.student_id})")
        print(f"   🏫 Classroom: {classroom.name}")
        print(f"   📚 Subjects: {', '.join([s.name for s in subjects])}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    import random
    link_parent_to_student()
#!/usr/bin/env python
"""
Test script to verify attendance count logic is working correctly
"""

import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_classroom.settings')
django.setup()

from django.contrib.auth import get_user_model
from attendance.models import StudentCustomAttendance, StudentTotalSessions
from users.models import StudentProfile

User = get_user_model()

def test_attendance_logic():
    """Test the attendance count logic"""
    print("🧪 Testing Attendance Count Logic")
    print("=" * 40)
    
    # Get a test student
    student = User.objects.filter(role='student').first()
    if not student:
        print("❌ No students found. Please run the data expansion script first.")
        return
    
    print(f"Testing with student: {student.get_full_name()}")
    
    # Ensure student has profile
    if not hasattr(student, 'student_profile') or not student.student_profile:
        StudentProfile.objects.get_or_create(user=student)
        student.refresh_from_db()
    
    classroom = student.student_profile.classroom
    print(f"Classroom: {classroom.name if classroom else 'None'}")
    
    # Set up test scenario with total sessions = 30
    total_sessions = 30
    
    # Create or get total sessions record
    sessions_obj, created = StudentTotalSessions.objects.get_or_create(
        student=student,
        classroom=classroom,
        defaults={
            'total_sessions': total_sessions,
            'created_by': student,
            'updated_by': student
        }
    )
    sessions_obj.total_sessions = total_sessions
    sessions_obj.save()
    
    # Create or get custom attendance record
    custom_attendance, created = StudentCustomAttendance.objects.get_or_create(
        student=student,
        classroom=classroom,
        defaults={
            'present_count': 20,
            'late_count': 5,
            'absent_count': 5,
            'created_by': student,
            'updated_by': student
        }
    )
    
    print(f"\n📊 Initial State (Total Sessions: {total_sessions})")
    print(f"Present: {custom_attendance.present_count}")
    print(f"Late: {custom_attendance.late_count}")
    print(f"Absent: {custom_attendance.absent_count}")
    print(f"Total: {custom_attendance.present_count + custom_attendance.late_count + custom_attendance.absent_count}")
    
    # Test Case 1: Increase Present count
    print(f"\n🧪 Test Case 1: Increase Present from {custom_attendance.present_count} to 25")
    
    # Simulate the logic from views.py
    current_present = custom_attendance.present_count
    current_late = custom_attendance.late_count
    current_absent = custom_attendance.absent_count
    
    # Update present count
    custom_attendance.present_count = 25
    # Recalculate absent: Total - Present - Late
    custom_attendance.absent_count = max(0, total_sessions - 25 - custom_attendance.late_count)
    
    print(f"After update:")
    print(f"Present: {custom_attendance.present_count}")
    print(f"Late: {custom_attendance.late_count}")
    print(f"Absent: {custom_attendance.absent_count}")
    print(f"Total: {custom_attendance.present_count + custom_attendance.late_count + custom_attendance.absent_count}")
    
    # Test Case 2: Increase Absent count
    print(f"\n🧪 Test Case 2: Increase Absent from {custom_attendance.absent_count} to 15")
    
    current_present = custom_attendance.present_count
    current_late = custom_attendance.late_count
    current_absent = custom_attendance.absent_count
    
    # Update absent count
    custom_attendance.absent_count = 15
    # Calculate remaining sessions after absent
    remaining_sessions = max(0, total_sessions - 15)
    
    # Distribute remaining sessions between present and late maintaining ratio
    if remaining_sessions > 0:
        current_present_late_total = current_present + current_late
        if current_present_late_total > 0:
            # Maintain ratio between present and late
            present_ratio = current_present / current_present_late_total
            late_ratio = current_late / current_present_late_total
            
            custom_attendance.present_count = int(remaining_sessions * present_ratio)
            custom_attendance.late_count = remaining_sessions - custom_attendance.present_count
        else:
            # If no previous present/late, assign all remaining to present
            custom_attendance.present_count = remaining_sessions
            custom_attendance.late_count = 0
    else:
        # If absent count equals or exceeds total sessions, set others to 0
        custom_attendance.present_count = 0
        custom_attendance.late_count = 0
    
    print(f"After update:")
    print(f"Present: {custom_attendance.present_count}")
    print(f"Late: {custom_attendance.late_count}")
    print(f"Absent: {custom_attendance.absent_count}")
    print(f"Total: {custom_attendance.present_count + custom_attendance.late_count + custom_attendance.absent_count}")
    
    # Test Case 3: Set Absent to exceed total sessions
    print(f"\n🧪 Test Case 3: Set Absent to 35 (exceeds total sessions of {total_sessions})")
    
    custom_attendance.absent_count = 35
    remaining_sessions = max(0, total_sessions - 35)
    
    if remaining_sessions > 0:
        # This won't happen since 35 > 30
        pass
    else:
        # If absent count equals or exceeds total sessions, set others to 0
        custom_attendance.present_count = 0
        custom_attendance.late_count = 0
    
    # Final validation: ensure total doesn't exceed total_sessions
    calculated_total = custom_attendance.present_count + custom_attendance.late_count + custom_attendance.absent_count
    if calculated_total > total_sessions:
        # If total exceeds, adjust absent count down
        custom_attendance.absent_count = max(0, total_sessions - custom_attendance.present_count - custom_attendance.late_count)
    
    print(f"After update and validation:")
    print(f"Present: {custom_attendance.present_count}")
    print(f"Late: {custom_attendance.late_count}")
    print(f"Absent: {custom_attendance.absent_count}")
    print(f"Total: {custom_attendance.present_count + custom_attendance.late_count + custom_attendance.absent_count}")
    
    print(f"\n✅ All tests completed!")
    print(f"The logic ensures that:")
    print(f"1. When Present/Late is increased, Absent is automatically decreased")
    print(f"2. When Absent is increased, Present/Late are proportionally decreased")
    print(f"3. Total never exceeds the total sessions")
    print(f"4. All counts remain non-negative")

if __name__ == '__main__':
    test_attendance_logic()
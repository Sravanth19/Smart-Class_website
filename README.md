# 🎓 Smart-Class Management System

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![Django](https://img.shields.io/badge/Django-Framework-092E20?style=for-the-badge&logo=django)
![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)

**Smart-Class** is a comprehensive educational management platform designed to bridge the gap between administration, teachers, and parents. This system offers robust attendance tracking, real-time feedback loops, and a dedicated portal for parental monitoring.

---

## 🚀 Key Features

### 📅 Advanced Attendance System
* **Logic-Based Tracking**: accurate session counting with `ATTENDANCE_COUNT_LOGIC_FIX` ensuring data integrity.
* **Editable Records**: Flexible control for teachers to modify attendance logs (`ATTENDANCE_EDITABLE_COUNTS_GUIDE`).
* **Feedback Integration**: Built-in mechanisms to handle attendance discrepancies (`ATTENDANCE_FEEDBACK_FIXED`).
* **Session Analytics**: Detailed breakdown of total sessions and participation.

### 👨‍👩‍👧‍👦 Parent Portal
* **Student Linking**: Secure logic to map Parent accounts to specific Students (`link_parent_student.py`).
* **Real-Time Insight**: Parents can view their child's academic progress and attendance stats.
* **Documentation**: See `PARENT_PORTAL_SUMMARY.md` for a full feature breakdown.

### 🛠 Administrative Automation
* **One-Click Setup**: Scripts to instantly create demo accounts and populate the database (`create_demo_accounts.py`, `populate_data.py`).
* **Data Expansion**: Tools to scale the system with comprehensive sample data for stress testing (`comprehensive_data_expansion.py`).
* **System Health**: Includes extensive unit tests for views, logic, and system stability (`test_system.py`, `test_attendance.py`).

---

## 📂 Project Structure

The repository is organized for scalability:

* **`scripts/`**: Utility scripts for data generation and maintenance.
* **`templates/`**: Frontend HTML interfaces.
* **`tests/`**: Unit and integration tests.
* **Documentation**: Detailed guides including `PROJECT_STARTUP_PRESENTATION.md` and feature-specific summaries.

---

## ⚙️ Installation & Setup

Follow these steps to get the project running locally:

### 1. Clone the Repository
```bash
git clone [https://github.com/Sravanth19/Smart-Class_website.git](https://github.com/Sravanth19/Smart-Class_website.git)
cd Smart-Class_website


python -m venv Env
# Activate on Windows:
.\Env\Scripts\activate
# Activate on macOS/Linux:
source Env/bin/activate

python manage.py makemigrations
python manage.py migrate

python create_demo_accounts.py
python comprehensive_data_expansion.py

python manage.py runserver

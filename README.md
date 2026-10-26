## School Guide (Школьный Гид)

![HTML5](https://img.shields.io/badge/HTML5-orange)
![CSS3](https://img.shields.io/badge/CSS3-blueviolet)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6-yellow)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![Django](https://img.shields.io/badge/Django-4.2-green)
![SQLite](https://img.shields.io/badge/SQLite-3-lightgrey)

## 📌 Overview
**School Guide** is a web-based educational portal designed to consolidate learning materials and online platforms into a single, unified system for seamless interaction between students and teachers.  
The application streamlines information discovery across subjects and topics, making the learning process structured, efficient, and centralized.

## 🎯 Key Problems Solved
- **Centralized Hub:** Connects students and teachers within a single interactive space.
- **Structured Access:** Provides quick and organized access to study resources.
- **Platform Integration:** Combines external educational tools into one workflow.
- **Intuitive Navigation:** Enables fast searching across subjects, announcements, and schedules.

## ✨ Features
- Easy navigation through school subjects and learning modules.
- Instant access to educational resources and announcements.
- Integrated interactive map and school information cards.
- Multi-app modular Django architecture (Accounts, Blog, Grades, Map).

## 🛠 Tech Stack
* **Backend:** Python 3.11, Django 4.2
* **Frontend:** HTML5, CSS3, JavaScript (ES6)
* **Database:** SQLite3
* **Version Control:** Git & GitHub

---

## 📸 Interface Preview

![Home Page](https://i.imgur.com/A2lH8W9.png)

*Main dashboard interface featuring announcements, user profile access, and school map navigation.*

---

## 🏗 Project Architecture

```text
school-guide/
 ├─ accounts/        # Authentication & User Management
 ├─ blog/            # News & Announcements
 ├─ grades/          # Academic Performance & Grading
 ├─ map/             # Interactive School Map
 ├─ school_card/     # School Overview & Contact Info
 ├─ media/           # Uploaded User Media
 ├─ templates/       # Global HTML Templates
 ├─ static/          # CSS, JS, and Images
 ├─ models.py        # Core Models
 ├─ views.py         # App Views & Controllers
 ├─ urls.py          # Route Handling
 └─ settings.py      # Project Settings
```

## 📦 Getting Started
### Prerequisites
Make sure you have Python 3.10+ installed on your system.

### Installation
```bash
git clone [https://github.com/owiga/SchoolPortal.git](https://github.com/owiga/SchoolPortal.git)
cd SchoolPortal
# Linux/macOS
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

python manage.py migrate
python manage.py runserver
```
Access the app at http://127.0.0.1:8000/

## 📄 Project Resources & Attachments

- [Video Demo](https://disk.yandex.ru/d/en1P7ulS0zoENA)
- [Technical Specification](tech_info.pdf)
- [Project Presentation](presentation.pdf)

# Project Prerequisites & Requirements

This document describes the required environment, tools, and dependencies
needed to run the Mini Social Network Backend project.

---

## 🐍 Programming Language

- Python: 3.12 or higher  
  (Tested on Python 3.12.x)

---

## 🌐 Frameworks & Core Libraries

- Django: 5.x  
- Django REST Framework: 3.x

These frameworks are used to build the RESTful API, handle routing,
serialization, authentication, and permissions.

---

## 🔐 Authentication Libraries

- djangorestframework-simplejwt  
  Used for JWT-based authentication (access & refresh tokens)

- rest_framework.authtoken  
  Used for token-based authentication (login/logout with static tokens)

---

## 🗄️ Database

- SQLite (default, development environment)

The project is configured to use SQLite out of the box.
It can be easily switched to PostgreSQL or MySQL for production use.

---

## 🧰 Development Tools

- pip (Python package manager)
- virtualenv / venv (recommended)
- Git (for version control)
- GitHub (repository hosting)
- VS Code (recommended editor, optional)

---

## 📦 Python Dependencies

All required Python packages are listed in:

requirements.txt

Installation:

`bash
pip install -r requirements.txt


---

⚙️ Environment Setup

Before running the project, ensure that:

Python is added to system PATH

Virtual environment is activated

Database migrations are applied


python manage.py migrate
python manage.py runserver


---

🌍 Supported Platforms

Windows 10 / 11

Linux

macOS


(Tested primarily on Windows)


---

📌 Notes

No frontend or UI is required to run this project.

API can be tested using:

Browser (for GET requests)

PowerShell / cURL

Postman


This document corresponds to Phase 1 of the project.


---
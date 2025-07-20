# 💊 Smart PharmaNet – Graduation Project

An AI-powered medicine exchange platform for pharmacies, built with Django REST Framework. This system helps pharmacies share surplus or unused medicine and leverage AI features to streamline search and communication.

---

## 🎯 Project Overview

Smart PharmaNet is designed to help pharmacies across a region collaborate by:
- Uploading and sharing surplus medicine.
- Using AI chat for quick assistance.
- Searching for medicine by image using OCR (Optical Character Recognition).

---

## 🛠️ Tech Stack

### 🧩 Backend
- **Framework:** Django REST Framework
- **Architecture:** RESTful API (`GET`, `POST`, `PATCH`, `DELETE`)
- **Authentication:** JWT (access + refresh tokens) using `SimpleJWT`
- **ORM:** Django ORM
- **Database:** PostgreSQL (hosted on [Supabase](https://supabase.com/))

### 🤖 AI Integration
- **AI Chat Assistant:** Integrated with OpenRouter API
- **Medicine Search:** Image-to-text using OCR (Optical Character Recognition)

### ⚡ Performance Optimization
- **Pagination:** For scalable API response
- **Caching:** Reduced response time from ~30s ➝ ~2-3s

### 📘 API Documentation
- **Swagger UI (drf-yasg):** For clean and interactive API documentation

---

## 📸 Features

- 🔒 Secure login & token-based authentication
- 🏥 Pharmacy profile & medicine management
- 🤖 AI-powered assistant and image recognition
- 🔍 Fast and smart medicine search
- 📄 Auto-generated API docs for frontend integration

---

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/jooeNagy/Smart_PharmaNet.git
cd smartPharmanet

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Start the server
python manage.py runserver

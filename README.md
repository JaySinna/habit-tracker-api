# Habit Tracker API

A backend project built with **FastAPI** that allows users to create habits, track daily check-ins, and view streak statistics.  
This was developed as a portfolio project after completing my Software Development Diploma at Code Institute.

---

## 🚀 Live Demo
- API Docs: [https://habit-tracker-api-jay.herokuapp.com/docs](https://habit-tracker-api-jay.herokuapp.com/docs)

---

## 👤 Demo Login
Use this account to try the API right away (no setup needed):

- **Email**: `demo@demo.dev`  
- **Password**: `demo123`

---

## ✨ Features
- User registration and login with JWT authentication
- Create, list, and manage habits
- Add daily check-ins for habits
- View streak statistics (current and longest streaks)
- Deployed with PostgreSQL on Heroku

---

## 🛠️ Tech Stack
- **Backend**: Python 3.12, FastAPI
- **Database**: SQLModel (SQLAlchemy + Pydantic), PostgreSQL
- **Auth**: JWT (python-jose, passlib)
- **Testing**: Pytest
- **Deployment**: Heroku

---

## 🧪 Run Locally

Clone the repo and install dependencies:

```bash
git clone https://github.com/JaySinna/habit-tracker-api.git
cd habit-tracker-api

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

uvicorn app.main:app --reload
Then open: http://127.0.0.1:8000/docs

📖 Run Tests
PYTHONPATH=. pytest -q
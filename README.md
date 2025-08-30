# Trackflow: AI-Powered Personal Finance Predictor (Flask + PostgreSQL)

This is a starter project for **Trackflow**, a personal finance web app that predicts future spending patterns and suggests saving strategies.

## Features
- HTML/CSS frontend with Bootstrap + Chart.js
- Flask (Python) backend
- PostgreSQL database via SQLAlchemy
- User auth (register/login/logout) with password hashing
- Add income/expense, view history
- Dashboard charts (monthly totals)
- Simple ML prediction for next-month expense using Linear Regression (fallback to average if low data)
- Basic saving tips based on category spend and target goal

## Quick Start

### 1) Install system dependencies
- Python 3.10+
- PostgreSQL (create a database, e.g., `trackflow_db`)

### 2) Create DB and user (example)
```sql
CREATE DATABASE trackflow_db;
-- Optionally create a user:
-- CREATE USER trackuser WITH PASSWORD 'strongpassword';
-- GRANT ALL PRIVILEGES ON DATABASE trackflow_db TO trackuser;
```

### 3) Clone / extract this project
```
cd trackflow
```

### 4) Create virtual environment & install requirements
```
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt
```

### 5) Configure environment
Copy `.env.example` to `.env` and set values.
```
cp .env.example .env
```
Edit `.env` with your actual database URL and secret key.

### 6) Initialize database tables
The app will create tables automatically on first run if they don't exist.

### 7) Run the app
```
python run.py
```
Then open http://127.0.0.1:5000

---

## Project Structure
```
trackflow/
├── app.py
├── config.py
├── models.py
├── utils.py
├── run.py
├── requirements.txt
├── .env.example
├── templates/
│   ├── base.html
│   ├── _flash.html
│   ├── home.html
│   ├── register.html
│   ├── login.html
│   ├── dashboard.html
│   ├── add_transaction.html
│   ├── transactions.html
│   ├── predictions.html
│   ├── savings.html
│   ├── profile.html
│   └── about.html
└── static/
    ├── css/styles.css
    └── js/chart-setup.js
```

## Notes
- This is a learning-friendly scaffold. For production, add CSRF protection, input validation, migrations (Flask-Migrate), and stronger security practices.
- The ML prediction is illustrative, not a financial advisory.

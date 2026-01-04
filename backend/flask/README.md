# Flask Backend (Starter)

Prereqs: Python 3.9+, virtualenv

Install:

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Run:

```bash
set FLASK_APP=app.py
set FLASK_ENV=development
flask run
```

This starter uses SQLite `app.db` and exposes JWT-authenticated REST APIs for users, scholarships, and applications.

Seeding the database:

```powershell
# from project/backend/flask
.\venv\Scripts\python.exe seed.py
```

This creates example users (admin, institution, student), two scholarships, and one sample application.

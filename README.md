# Scholarship Portal Starter

Starter repository for a scholarship portal similar to scholarships.gov.in.

Repository structure
- `backend/flask`: Python Flask REST API with JWT auth and SQLite (development)
- `backend/springboot`: Java Spring Boot backend (development/profile)
- `frontend`: Static HTML/CSS/JS starter pages

## Quick Start (development)

These instructions get the frontend and backends running locally for development and testing.

1) Run the Flask backend (recommended for quick local testing)

PowerShell (Windows):

```powershell
cd C:\Users\lenovo\OneDrive\Desktop\project\backend\flask
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python seed.py   # optional: seeds example users/scholarships
python app.py
```

The Flask dev server will run on http://127.0.0.1:5000 by default.

2) Run the frontend static server

```powershell
cd C:\Users\lenovo\OneDrive\Desktop\project\frontend
python -m http.server 8000
```

Open http://localhost:8000 in your browser. The frontend is configured to call the Flask API at port 5000 by default.

3) Run the Spring Boot backend (optional)

If you have Maven installed:

```powershell
cd C:\Users\lenovo\OneDrive\Desktop\project\backend\springboot
mvn clean package
mvn spring-boot:run
```

If you don't have Maven installed, either install it or request that I add the Maven Wrapper (`mvnw`) to this project so you can build without a separate Maven install.

4) Configuration notes

- Flask: set environment variable `JWT_SECRET` to override the development default `dev-secret`.
- Spring Boot: JWT config is in `backend/springboot/src/main/resources/application.properties` (`jwt.secret`, `jwt.expiration`).
- Frontend: `frontend/js/app.js` stores `access_token` in `localStorage` and uses it for `Authorization: Bearer ...` requests.

5) Quick smoke test (PowerShell example for Flask)

```powershell
# login (seeded admin exists: admin@example.com / adminpass)
Invoke-RestMethod -Uri http://localhost:5000/auth/login -Method Post -Body (@{email='admin@example.com'; password='adminpass'} | ConvertTo-Json) -ContentType 'application/json'
```

Next steps I can take for you
- Add Maven Wrapper (`mvnw`) for the Spring Boot project so it builds without a local Maven install.
- Update the frontend to target the Spring Boot API (port 8080) and run an end-to-end test.
- Add simple `start-all` PowerShell scripts to launch the three services together for convenience.

If you want me to proceed, tell me which item to do next and I'll implement it.

## Docker & Fullstack (quick local deploy)

To run the full stack as a local website quickly (frontend + Flask + Spring Boot) using Docker:

Requirements: Docker and Docker Compose installed.

From the project root:

```powershell
docker-compose build --parallel
docker-compose up -d
```

After startup:
- Frontend UI: http://localhost:8000
- Flask API: http://localhost:5000
- Spring API: http://localhost:8080

To stop and remove containers:

```powershell
docker-compose down
```

Hosting publicly
- If you want a public URL, deploy these Docker containers to a VPS (DigitalOcean, AWS EC2) or a container platform (Render, Railway, Google Cloud Run). I can prepare a Render config or GitHub Actions to build & deploy automatically.

# Scholarship Portal Starter

Starter repository for a scholarship portal similar to scholarships.gov.in.

Structure:
- `backend/flask`: Python Flask REST API with JWT auth and SQLite (starter)
- `backend/springboot`: Java Spring Boot skeleton (starter)
- `frontend`: Static HTML/CSS/JS starter pages

See `backend/flask/README.md` for running the Flask backend.

## Quick public deploy (Render)

I added a `render.yaml` manifest to this repository. To publish the full stack (frontend + Flask + Spring Boot) with minimal setup:

1. Push this repository to GitHub (create a repo and push `main`).
2. Go to https://dashboard.render.com and sign in.
3. Click **New** → **Import from GitHub** and select this repository. Render will read `render.yaml` and propose services.
4. Confirm and create the services. Render builds and deploys each service and provides public URLs (e.g., `https://scholarship-frontend.onrender.com`).

Notes:
- Replace `repo: https://github.com/your/repo` in `render.yaml` if you want to hard-code the repo; otherwise Render will link automatically during import.
- If you prefer CI/CD automation, I can add a GitHub Actions workflow to trigger builds and updates.


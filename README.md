# Universal File Converter Web App

A comprehensive, fast, secure, reliable, and user-friendly online platform for converting files between a wide variety of formats.

## Tech Stack

*   **Backend:** FastAPI (Python), PostgreSQL, Redis, Celery, SQLAlchemy, Alembic, Pydantic
*   **Frontend:** React (TypeScript), Vite, Tailwind CSS, Zustand, React Router, Axios, React Hook Form, React Dropzone
*   **DevOps (Planned):** Docker, CI/CD (TBD)

## Current Status (End of Phase 4)

*   Project structure initialized (backend/frontend/docs).
*   Core backend setup with FastAPI, database connection (PostgreSQL/SQLAlchemy), and async support.
*   Core frontend setup with React/Vite, Tailwind CSS, routing, and state management (Zustand).
*   User authentication implemented (Registration, Login, JWT using `fastapi-users`).
*   Password reset backend endpoints available (frontend UI pending).
*   Basic file upload endpoint implemented on the backend.
*   File uploads queued to Celery for background processing (placeholder task).
*   Frontend integration for login, registration, and file upload.
*   Protected routes implemented for authenticated users.
*   Initial database migrations created (manually).

## Setup Instructions

1.  **Prerequisites:**
    *   Python 3.10+
    *   Node.js 18+ and npm
    *   PostgreSQL server running (e.g., locally on port 5432)
    *   Redis server running (e.g., locally on port 6379)

2.  **Clone Repository:** (Assuming you have pushed it to GitHub/etc.)
    ```bash
    git clone <your-repo-url>
    cd universal-file-converter # Or your project directory name
    ```

3.  **Configure Environment:**
    *   Copy `.env.example` to `.env`.
    *   Edit `.env` and replace placeholder values, **especially** for `DATABASE_URL` (update user, password, database name for your local PostgreSQL setup) and `SECRET_KEY` (generate a strong secret).

4.  **Backend Setup:**
    ```bash
    cd backend
    python -m venv venv
    # Activate virtual environment (Windows Powershell)
    .\venv\Scripts\Activate.ps1
    # (Other OS: source venv/bin/activate)
    pip install -r requirements.txt
    ```

5.  **Database Migrations:**
    *   Ensure your PostgreSQL server is running and the database specified in `.env` exists.
    *   Apply migrations:
        ```bash
        # Ensure you are in the 'backend' directory with venv active
        alembic upgrade head
        ```
        *(Note: Alembic autogenerate had issues, migrations were created manually. If you add/change models, you may need to manually create or fix migrations.)*

6.  **Frontend Setup:**
    ```bash
    cd ../frontend
    npm install
    ```

## Running the Application

1.  **Start Backend API Server:**
    *   Ensure you are in the `backend` directory with the virtual environment active.
    ```bash
    uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
    ```
    *   The API will be available at `http://127.0.0.1:8000`.
    *   API Docs (Swagger UI): `http://127.0.0.1:8000/docs`

2.  **Start Celery Worker:**
    *   Open a **new terminal**, navigate to the `backend` directory, and activate the virtual environment.
    ```bash
    celery -A app.core.celery_app worker --loglevel=info
    ```

3.  **Start Frontend Development Server:**
    *   Ensure you are in the `frontend` directory.
    ```bash
    npm run dev
    ```
    *   The frontend will be available at `http://localhost:5173` (or the port specified by Vite).

## Usage

1.  Open the frontend URL in your browser.
2.  Register a new account or log in with existing credentials.
3.  Use the drag-and-drop interface on the home page to upload a file.
4.  Select the desired output format.
5.  Click "Start Conversion".
6.  The file will be uploaded, and a background conversion task will be queued (currently simulated).

## Features Implemented

*   User Registration
*   User Login (JWT Authentication)
*   Basic File Upload (Drag & Drop / Browse)
*   Conversion Task Queuing (via Celery/Redis)
*   Protected Dashboard Route
*   Basic Project Structure (Backend/Frontend)
*   API Health Check

*(Features list will expand as development progresses)*

## Features

*(Features will be listed here as they are developed)*

## Status

*(Project status updates will be noted here)* 
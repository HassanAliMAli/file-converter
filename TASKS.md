# TASKS: Universal File Converter Web App

**Version:** 1.0
**Date:** 2025-04-12

**Instructions for AI Coding Agent:**

1.  **Process Tasks Sequentially:** Follow the tasks in the order presented unless dependencies are explicitly handled otherwise.
2.  **Mark Completion:** Upon successful completion and testing of each task, change the checkbox from `[ ]` to `[x]`.
3.  **Maintain `README.md`:** After completing *each* task, update the `README.md` file to reflect the current project status, setup instructions (if changed), features added/updated, and any relevant notes. *Also update the README.md after implementing any subsequent changes requested post-completion.*
4.  **Maintain `DOCUMENTATION.md`:** After completing *each* relevant feature task, add or update the corresponding section in `DOCUMENTATION.md`. This file should comprehensively document all user-facing features, options, limitations, supported formats, usage guides, and troubleshooting tips. *Also update the DOCUMENTATION.md after implementing any subsequent changes requested post-completion.*
5.  **Refer to `PRD.md`:** Constantly refer to the `PRD.md` file for detailed requirements, scope, and specifications for each feature.
6.  **Code Quality:** Write clean, modular, well-commented, and secure code following best practices for the chosen tech stack (Python/FastAPI, React/Vue). Implement logging and robust error handling.
7.  **Security Focus:** Implement security best practices at every step (input validation, secure defaults, dependency checks, etc.).
8.  **Testing:** Write unit and integration tests for backend logic where appropriate. Frontend testing as specified or feasible.

---

## Phase 0: Project Setup & Initialization

* [ ] **0.1:** Initialize Git repository. Create standard project structure (e.g., `/backend`, `/frontend`, `/docs`, `/scripts`).
* [ ] **0.2:** Create initial `README.md` with project title, brief description, and placeholder sections (Setup, Usage, Features, Status).
* [ ] **0.3:** Create initial `DOCUMENTATION.md` with project title and placeholder sections (Introduction, Features, Supported Formats, Usage Guide, Troubleshooting, Privacy).
* [ ] **0.4:** Set up virtual environments for backend (Python venv or Conda) and frontend (Node.js/npm/yarn).
* [ ] **0.5:** Create `.gitignore` file with appropriate entries for Python, Node.js, OS files, and sensitive data.
* [ ] **0.6:** Set up basic configuration management (e.g., using `.env` files or a config library) for settings like database URLs, API keys, secret keys. **Do not commit secrets.**
* [ ] **0.7:** Choose and set up code linters and formatters (e.g., Black, Flake8 for Python; ESLint, Prettier for Frontend).

## Phase 1: Core Backend Setup (FastAPI)

* [ ] **1.1:** Initialize FastAPI project structure.
* [ ] **1.2:** Set up database connection (PostgreSQL) using an ORM like SQLAlchemy with Alembic for migrations.
* [ ] **1.3:** Define initial database models (User, SubscriptionPlan, ConversionJob). Create initial migration.
* [ ] **1.4:** Implement basic API routing and a health check endpoint (`/health`).
* [ ] **1.5:** Set up CORS (Cross-Origin Resource Sharing) middleware for frontend communication.
* [ ] **1.6:** Implement basic logging setup.

## Phase 2: Core Frontend Setup (React/Vue)

* [ ] **2.1:** Initialize Frontend project using Create React App / Vue CLI or similar.
* [ ] **2.2:** Set up basic project structure (components, services, styles).
* [ ] **2.3:** Implement basic layout (Header, Footer, Main Content Area).
* [ ] **2.4:** Set up routing (e.g., React Router, Vue Router) for different pages (Home, Login, Register, Dashboard, Admin).
* [ ] **2.5:** Implement basic API service layer to communicate with the backend.
* [ ] **2.6:** Set up state management solution if needed (e.g., Redux, Zustand, Vuex, Pinia).

## Phase 3: User Authentication & Accounts

* [ ] **3.1 Backend:** Implement user registration endpoint (hash passwords using bcrypt).
* [ ] **3.2 Backend:** Implement user login endpoint (JWT or session-based authentication).
* [ ] **3.3 Backend:** Implement password recovery/reset mechanism (e.g., email-based token).
* [ ] **3.4 Backend:** Implement secure endpoint for fetching user profile data (requires authentication).
* [ ] **3.5 Backend:** Implement endpoint for updating user profile (e.g., password change).
* [ ] **3.6 Frontend:** Create Registration page/form and integrate with backend API.
* [ ] **3.7 Frontend:** Create Login page/form and integrate with backend API (handle token/session storage securely).
* [ ] **3.8 Frontend:** Implement password recovery flow.
* [ ] **3.9 Frontend:** Implement protected routes that require authentication.
* [ ] **3.10 Frontend:** Create basic User Profile/Dashboard page.
* [ ] **3.11 Docs:** Document Authentication flow and Account Management features in `DOCUMENTATION.md`.

## Phase 4: Admin Panel Basics

* [ ] **4.1 Backend:** Implement endpoints protected for Admin role only.
* [ ] **4.2 Backend:** Implement endpoint to list users (with pagination, search/filter).
* [ ] **4.3 Backend:** Implement endpoint to view specific user details.
* [ ] **4.4 Backend:** Implement endpoint to define/list Subscription Plans (initially from config or DB).
* [ ] **4.5 Backend:** Implement endpoint to manually assign/change user roles or subscription status (Admin function).
* [ ] **4.6 Frontend:** Create basic Admin section layout, protected by Admin role.
* [ ] **4.7 Frontend:** Implement User List view with data from backend.
* [ ] **4.8 Frontend:** Implement Subscription Plan viewing interface.
* [ ] **4.9 Frontend:** Implement basic User Detail view with ability to trigger role/subscription changes.
* [ ] **4.10 Docs:** Document Admin Panel features in `DOCUMENTATION.md`.

## Phase 5: Conversion Engine Infrastructure

* [ ] **5.1 Backend:** Integrate Celery with FastAPI.
* [ ] **5.2 Backend:** Configure Redis as the Celery broker and result backend.
* [ ] **5.3 Backend:** Set up Celery worker process(es).
* [ ] **5.4 Backend:** Define base Celery task structure for file conversions.
* [ ] **5.5 Backend:** Implement API endpoint to receive file upload(s) and conversion request, validate input, create `ConversionJob` record in DB (status: PENDING), and dispatch task to Celery queue. Use secure temporary storage for uploads (e.g., S3 presigned URL for direct upload or server temp storage).
* [ ] **5.6 Backend:** Implement API endpoint to check the status of a `ConversionJob`.
* [ ] **5.7 Backend:** Implement logic for Celery workers to update job status (RUNNING, SUCCESS, FAILED) and store result file location upon completion.
* [ ] **5.8 Backend:** Implement endpoint to provide a secure download link for the converted file (link should expire).
* [ ] **5.9 Backend:** Implement **strict file deletion logic** (delete input & output files immediately after successful download or short expiry). Add scheduled cleanup task as fallback.
* [ ] **5.10 Frontend:** Implement core file upload component (drag-and-drop, browse). Handle large file uploads (chunking if necessary).
* [ ] **5.11 Frontend:** Implement UI for selecting output format.
* [ ] **5.12 Frontend:** Integrate upload component with backend API to start conversion job.
* [ ] **5.13 Frontend:** Implement polling or WebSocket connection to check job status.
* [ ] **5.14 Frontend:** Display conversion progress/status to the user.
* [ ] **5.15 Frontend:** Provide download button/link upon successful conversion. Handle conversion errors gracefully.

## Phase 6: Conversion Logic Implementation

* **Instructions:** For each sub-task, implement the backend Celery task using the specified library, handle potential errors, write tests if applicable, update `DOCUMENTATION.md` with format details.
* **6.1 Documents:**
    * [ ] **6.1.1:** Implement PDF <-> DOCX (via LibreOffice headless or Pandoc).
    * [ ] **6.1.2:** Implement PDF -> TXT (e.g., using `PyPDF2` or similar).
    * [ ] **6.1.3:** Implement DOCX -> TXT (via Pandoc or python-docx).
    * [ ] **6.1.4:** Implement HTML -> PDF (e.g., using WeasyPrint or headless browser).
    * [ ] **6.1.5:** Implement EPUB <-> PDF (via Pandoc or Calibre CLI).
    * [ ] **6.1.6:** Implement ODT <-> DOCX (via LibreOffice headless or Pandoc).
    * [ ] **6.1.7:** Implement PDF -> JPG/PNG (page ranges, quality settings via `pdf2image`/Poppler).
    * [ ] **6.1.8:** Implement OCR (Image/Scanned PDF -> Searchable PDF/DOCX/TXT using Pytesseract).
* **6.2 Images:**
    * [ ] **6.2.1:** Implement JPG <-> PNG (via Pillow).
    * [ ] **6.2.2:** Implement JPG <-> WEBP (via Pillow).
    * [ ] **6.2.3:** Implement PNG <-> WEBP (via Pillow).
    * [ ] **6.2.4:** Implement GIF <-> MP4 (via FFmpeg).
    * [ ] **6.2.5:** Implement HEIC -> JPG/PNG (via `pyheif` or external library).
    * [ ] **6.2.6:** Implement BMP/TIFF -> JPG/PNG (via Pillow).
    * [ ] **6.2.7:** Implement SVG -> PNG (via `cairosvg` or similar).
    * [ ] **6.2.8:** Implement Basic Resize (via Pillow).
    * [ ] **6.2.9:** Implement Basic Compress (via Pillow).
* **6.3 Audio:**
    * [ ] **6.3.1:** Implement MP3 <-> WAV (via FFmpeg or `pydub`).
    * [ ] **6.3.2:** Implement MP3 <-> AAC (via FFmpeg).
    * [ ] **6.3.3:** Implement M4A <-> MP3 (via FFmpeg).
    * [ ] **6.3.4:** Implement FLAC <-> MP3 (via FFmpeg).
    * [ ] **6.3.5:** Implement WAV <-> FLAC (via FFmpeg or soundfile).
    * [ ] **6.3.6:** Implement OGG <-> MP3 (via FFmpeg).
    * [ ] **6.3.7:** Implement Extract Audio (Video -> Audio via FFmpeg).
* **6.4 Video:**
    * [ ] **6.4.1:** Implement MP4 <-> AVI (via FFmpeg).
    * [ ] **6.4.2:** Implement MP4 <-> MOV (via FFmpeg).
    * [ ] **6.4.3:** Implement MP4 <-> WEBM (via FFmpeg).
    * [ ] **6.4.4:** Implement MKV -> MP4 (via FFmpeg).
    * [ ] **6.4.5:** Implement FLV -> MP4 (via FFmpeg).
    * [ ] **6.4.6:** Implement Basic Compression (via FFmpeg - adjust bitrate/CRF).
    * [ ] **6.4.7:** Implement Resolution Change (via FFmpeg).
* **6.5 Archives:**
    * [ ] **6.5.1:** Implement ZIP Extraction (via `zipfile`).
    * [ ] **6.5.2:** Implement RAR/7Z/TAR.GZ Extraction (via `patool` or direct CLI calls).
    * [ ] **6.5.3:** Implement ZIP Creation (from multiple files via `zipfile`).

## Phase 7: Advanced Options Implementation

* [ ] **7.1 Frontend:** Design and implement UI components for selecting advanced options (sliders, dropdowns, input fields), displayed contextually.
* [ ] **7.2 Frontend:** Pass selected advanced options to the backend API when starting a conversion job.
* [ ] **7.3 Backend:** Modify API endpoint to accept advanced options.
* [ ] **7.4 Backend:** Modify Celery task dispatch logic to pass options to workers.
* [ ] **7.5 Backend:** Update individual conversion tasks (Phase 6) to utilize the passed advanced options when calling libraries (e.g., setting quality for Pillow, bitrate for FFmpeg).
* [ ] **7.6 Docs:** Document available advanced options for each relevant conversion type in `DOCUMENTATION.md`.

## Phase 8: Batch Processing Implementation

* [ ] **8.1 Frontend:** Enhance upload component to accept multiple files reliably.
* [ ] **8.2 Frontend:** Implement UI to display list of files in the batch.
* [ ] **8.3 Frontend:** Implement UI to set output format and advanced options for the entire batch.
* [ ] **8.4 Frontend:** (Optional/Premium) Implement UI to set options per-file within the batch.
* [ ] **8.5 Frontend:** Call backend API to initiate batch conversion job.
* [ ] **8.6 Backend:** Implement API endpoint to handle batch conversion requests.
* [ ] **8.7 Backend:** Implement logic to create multiple individual `ConversionJob` records or a single parent batch job, dispatching multiple tasks to Celery.
* [ ] **8.8 Backend:** Implement logic to track the progress of the entire batch.
* [ ] **8.9 Backend:** Implement task/endpoint to create a ZIP archive of all successfully converted files in the batch upon completion.
* [ ] **8.10 Backend:** Provide download link for the batch ZIP archive.
* [ ] **8.11 Frontend:** Display batch progress and provide download link for the ZIP file.
* [ ] **8.12 Docs:** Document Batch Processing feature in `DOCUMENTATION.md`.

## Phase 9: Cloud Storage Integration

* [ ] **9.1 Backend:** Integrate Google Drive API Python Client & Dropbox Python SDK.
* [ ] **9.2 Backend:** Implement OAuth 2.0 flow for connecting user accounts to Google Drive & Dropbox. Securely store tokens associated with the user account.
* [ ] **9.3 Backend:** Implement API endpoints for Browse user's cloud storage (list files/folders).
* [ ] **9.4 Backend:** Implement logic to download selected file(s) from cloud storage to temporary server storage for conversion.
* [ ] **9.5 Backend:** Implement logic to upload converted file(s) to the user's chosen cloud storage destination folder.
* [ ] **9.6 Backend:** Handle token refresh and errors related to cloud storage APIs.
* [ ] **9.7 Frontend:** Implement UI for connecting/disconnecting Google Drive & Dropbox accounts.
* [ ] **9.8 Frontend:** Implement file browser interface to select input files from connected cloud storage.
* [ ] **9.9 Frontend:** Implement UI option to save converted files back to cloud storage (allow choosing destination folder).
* [ ] **9.10 Docs:** Document Cloud Storage Integration feature in `DOCUMENTATION.md`.

## Phase 10: Monetization Infrastructure

* [ ] **10.1:** Select and integrate a Payment Gateway (e.g., Stripe, PayPal). Requires backend and frontend integration for handling payments and webhooks.
* [ ] **10.2 Backend:** Enhance Subscription Plan model in DB (link to Payment Gateway plans).
* [ ] **10.3 Backend:** Implement logic to handle subscription creation/cancellation via Payment Gateway webhooks. Update user subscription status in DB.
* [ ] **10.4 Backend:** Implement middleware or decorators to check user subscription status and enforce feature/usage limits (file size, batch size, daily conversions, feature access like OCR/Cloud Storage).
* [ ] **10.5 Frontend:** Implement Pricing Page displaying different tiers and features.
* [ ] **10.6 Frontend:** Integrate Payment Gateway's checkout flow.
* [ ] **10.7 Frontend:** Implement UI elements that are enabled/disabled based on user's subscription tier. Display usage limits.
* [ ] **10.8 Frontend:** Implement Subscription Management section in User Profile page.
* [ ] **10.9 Admin Panel:** Enhance Subscription Management view (link plans, view active subs).
* [ ] **10.10:** (Optional) Implement basic ad serving logic for the free tier (e.g., Google AdSense integration).
* [ ] **10.11 Docs:** Document subscription plans, features, and limits in `DOCUMENTATION.md`.

## Phase 11: UI/UX Refinement

* [ ] **11.1:** Apply consistent styling across the application based on design guidelines (modern, clean, eye-catching).
* [ ] **11.2:** Ensure responsiveness across all target devices (desktop, tablet, mobile). Thoroughly test layouts.
* [ ] **11.3:** Refine all user feedback mechanisms (progress bars, loading indicators, success messages, error messages) for clarity and consistency.
* [ ] **11.4:** Improve usability based on testing (internal or user testing if possible). Simplify complex workflows.
* [ ] **11.5:** Implement accessibility improvements (ARIA attributes, keyboard navigation, color contrast).

## Phase 12: Security Implementation & Hardening

* [ ] **12.1:** Configure HTTPS for the deployed application.
* [ ] **12.2:** Perform thorough review and implementation of input validation and output encoding across all endpoints and UI components.
* [ ] **12.3:** Implement rate limiting on sensitive API endpoints (login, registration, conversion initiation).
* [ ] **12.4:** Set up automated security scanning for dependencies (e.g., `pip-audit`, `npm audit`, Snyk, Dependabot).
* [ ] **12.5:** Configure appropriate HTTP security headers (CSP, HSTS, X-Frame-Options, etc.).
* [ ] **12.6:** Review and harden server configurations (disable unnecessary services, configure firewalls).
* [ ] **12.7:** Ensure all secrets (API keys, DB passwords, secret key) are managed securely (environment variables, secrets manager) and not hardcoded.
* [ ] **12.8:** Review file upload handling for security vulnerabilities (e.g., file type validation, scanning - if feasible).

## Phase 13: Testing

* [ ] **13.1 Backend:** Write unit tests for critical business logic (e.g., user auth, subscription checks, helper functions).
* [ ] **13.2 Backend:** Write integration tests for API endpoints and conversion task logic.
* [ ] **13.3 Frontend:** Implement unit/component tests for critical UI components.
* [ ] **13.4:** Perform end-to-end testing for major user flows (registration, login, conversion, batch, cloud, subscription).
* [ ] **13.5:** Perform security testing (manual or automated) to identify vulnerabilities.
* [ ] **13.6:** Perform usability testing.

## Phase 14: Deployment

* [ ] **14.1:** Dockerize the backend application (FastAPI, Celery workers).
* [ ] **14.2:** Dockerize the frontend application (ensure proper build process).
* [ ] **14.3:** Choose a cloud provider (AWS/GCP/Azure) and set up necessary services (Compute instances/App Runner/ECS/GKE, Managed PostgreSQL, Managed Redis, Object Storage).
* [ ] **14.4:** Configure deployment environments (Development, Staging, Production).
* [ ] **14.5:** Set up CI/CD pipeline (e.g., GitHub Actions, GitLab CI, Jenkins) to automate testing, building, and deployment.
* [ ] **14.6:** Configure DNS and HTTPS certificates (e.g., Let's Encrypt).
* [ ] **14.7:** Set up monitoring and alerting for the deployed application (server resources, application errors, uptime).

## Phase 15: Documentation Finalization

* [ ] **15.1:** Review and finalize `README.md` for launch (accurate setup, usage, status).
* [ ] **15.2:** Review and finalize `DOCUMENTATION.md` ensuring all features, formats, options, limits, and guides are complete and accurate for launch.
* [ ] **15.3:** Add Privacy Policy and Terms of Service pages (requires legal review).

---

**End of Task List (Version 1.0)**
Remember to update `README.md` and `DOCUMENTATION.md` after completing each task and upon any subsequent changes. Good luck!
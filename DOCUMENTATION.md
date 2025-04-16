# Universal File Converter Web App - Documentation

## Introduction

Welcome to the documentation for the Universal File Converter Web App. This document provides detailed information about the application's features, supported formats, usage instructions, and more.

## Features

### Authentication

*   **User Registration:** Users can create a new account using their email address and a password.
*   **User Login:** Registered users can log in using their email and password. Authentication is handled using JSON Web Tokens (JWT).
*   **Password Reset:** Users can request a password reset (backend endpoint exists, frontend UI pending).
*   **Protected Routes:** Certain pages (e.g., Dashboard) require users to be logged in.

### File Handling

*   **File Upload:** Authenticated users can upload files via a drag-and-drop interface or by browsing.
*   **Conversion Queuing:** Uploaded files are queued for conversion using a background task system (Celery with Redis).
*   **Output Format Selection:** Users can select the desired output format before starting the conversion.

*(More detailed feature descriptions will be added here as they are implemented)*

## Supported Formats

*(List of supported input and output formats will be maintained here once conversion logic is implemented)*

Currently supported for upload (validation example):
*   image/jpeg
*   image/png
*   application/pdf
*   text/plain

Currently supported for output selection (UI example):
*   PDF, DOCX, TXT, JPG, PNG, MP3

## Usage Guide

### Getting Started

1.  Ensure you have the application running (Backend API, Celery Worker, Frontend). Refer to the `README.md` for setup and running instructions.
2.  Open the frontend application in your web browser (usually `http://localhost:5173`).

### Registering an Account

1.  Navigate to the "Register" page (usually via a link on the Login page).
2.  Enter your email address.
3.  Enter a secure password (minimum 8 characters).
4.  Confirm your password.
5.  Click the "Register" button.
6.  Upon successful registration, you will be redirected to the Login page.

### Logging In

1.  Navigate to the "Login" page.
2.  Enter the email address and password associated with your account.
3.  Click the "Login" button.
4.  Upon successful login, you will typically be redirected to the Dashboard or Home page.

### Converting a File

1.  Make sure you are logged in.
2.  Navigate to the Home page.
3.  Drag and drop the file you want to convert onto the designated area, or click the area to browse and select a file.
4.  Once a file is selected, choose the desired output format from the dropdown menu.
5.  Click the "Start Conversion" button.
6.  You will receive a message indicating that the upload was successful and the conversion task has started, along with a Task ID.
7.  *(Functionality to check task status and download the converted file is pending implementation)*.

## Troubleshooting

*   **Login Failed:** Ensure you are using the correct email and password. Check for typos. If you have forgotten your password, use the (pending) password reset feature.
*   **Registration Failed:** Ensure your password meets the minimum length requirement. The email address might already be in use.
*   **File Upload Failed:** Ensure you are logged in. Check if the file type is supported (see Supported Formats). Check for specific error messages displayed on the page.
*   **Alembic Autogenerate Issues:** The automatic generation of database migrations (`alembic revision --autogenerate`) has shown instability in this environment. Migrations have been created manually. If you modify SQLAlchemy models (`backend/app/models/`), you may need to manually create or adjust the corresponding migration file in `backend/alembic/versions/`.

*(More common issues and solutions will be added here)*

## Privacy

*(Information regarding user data and file handling will be detailed here. Key principle: uploaded files are temporary and deleted after processing/download/expiry as per PRD)* 
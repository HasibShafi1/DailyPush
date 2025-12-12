# DailyPush

A habit-tracking web application built with Django, HTMX, Alpine.js, and Tailwind CSS.

## 🚀 Quick Start

### 1. Setup Environment

Ensure you have Python installed.

```bash
# Install dependencies
pip install django django-allauth netifaces requests requests-oauthlib PyJWT
```

### 2. Database Setup

The database is already configured with SQLite. If you need to reset it:

```bash
python manage.py migrate
```

### 3. Create Admin User

Create a superuser to access the Django Admin:

```bash
python manage.py createsuperuser
```

### 4. Google Login Configuration (Crucial)

To make "Continue with Google" work:

1.  Run the server: `python manage.py runserver`
2.  Go to `http://127.0.0.1:8000/admin/` and login.
3.  Navigate to **Social Accounts** > **Social Applications**.
4.  Click **Add Social Application**.
    *   **Provider**: Google
    *   **Name**: DailyPush Google (or anything)
    *   **Client ID**: *[Your Google Cloud Client ID]*
    *   **Secret Key**: *[Your Google Cloud Client Secret]*
    *   **Sites**: Select `example.com` (ID: 1) and move it to the right ->.
5.  Save.

> **Note**: For local development, ensure your Google Cloud Console "Authorized redirect URIs" includes:
> `http://127.0.0.1:8000/accounts/google/login/callback/`

### 5. Run the App

```bash
python manage.py runserver
```

Visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## 🛠️ Features

- **Dashboard**: 365-day contribution heat map.
- **Interactivity**: Toggle days instantly using HTMX (no reload).
- **Design**: "Pitch Black" aesthetic with Tailwind CSS.

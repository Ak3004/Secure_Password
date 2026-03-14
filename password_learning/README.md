# Secure Password Manager (Django Web UI)

This project is a simple password manager that stores user passwords in JSON files and provides a web-based user interface for basic password management operations.

## ✅ What's Included

- **JSON-backed storage**: Passwords are stored in `app_password.json`, with master credentials in `master_login.json`.
- **Web UI** (Django with session-based authentication)
- **Login/Dashboard** for managing password entries securely.

---

## 🚀 Setup (Windows)

1. **Activate the virtual environment**

```powershell
cd "c:\Users\ankit\Desktop\Ankita\GreatLearning\Week 2\Secure_Password\password_learning"
& "..\great_learning_env\Scripts\Activate.ps1"
```

2. **Install dependencies** (if not already installed)

```powershell
pip install -r ..\requirements.txt
```

> If `requirements.txt` is missing, install manually:
> ```powershell
> pip install django
> ```

3. **Run Django checks (optional)**

```powershell
python manage.py check
```

3a. **Apply migrations (required for session support)**

```powershell
python manage.py migrate
```

4. **Start the server**

```powershell
python manage.py runserver
```

> The web UI is available at: `http://127.0.0.1:8000/` (login with the credentials in `master_login.json`).

---

## 🧭 Web UI Usage

1. **Login**: Enter your UID and password from `master_login.json`.
2. **Dashboard**: View, add, update, or delete password entries for your account.
   - **Add**: Enter domain and password (optional; generates secure password if empty).
   - **Update**: Select an entry by index and provide new password.
   - **Delete**: Select an entry by index to remove it.
3. **Logout**: Clears the session and returns to login.

---

## 📝 Notes

- This is **not production secure**; it is intended for learning and demonstration.
- Passwords are stored in plain JSON format.
- If you want to reset the sample data, delete `app_password.json` and `master_login.json`; they will be recreated on next run.

---

Enjoy! 🗝️

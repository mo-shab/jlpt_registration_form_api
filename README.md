# JLPT Backend API

This is a Flask-based backend API for a JLPT (Japanese Language Proficiency Test) preparation application. It provides authentication, form submissions, and user management features with JWT-based security.

---

## 🚀 Features

- User Registration & Login
- JWT Authentication
- Password Reset (Token-based)
- Form Submission (linked to user)
- Retrieve User Submissions
- Clean database model structure with SQLAlchemy
- CORS enabled for frontend integration (e.g., React)

---

## 🛠 Tech Stack

- Python 3
- Flask
- Flask-JWT-Extended
- Flask-SQLAlchemy
- PostgreSQL (default via `.env`)
- Flask-Migrate
- Flask-CORS
- python-dotenv

---

## 📁 Project Structure

```
jlpt-backend/
│
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── models.py
│   └── routes/
│       ├── __init__.py
│       ├── auth.py
│       └── form_routes.py
│
├── migrations/
├── static/
├── templates/
├── .env
├── app.py
├── run.py
├── requirement.txt
└── README.md
```

---

## ⚙️ Setup Instructions

1. **Clone the Repository**
    ```sh
    git clone <repo-url>
    cd jlpt-backend
    ```

2. **Create and Activate a Virtual Environment**
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install Dependencies**
    ```sh
    pip install -r requirement.txt
    ```

4. **Configure Environment Variables**

    Create a `.env` file in the root directory (see example below).

    ```ini
    FLASK_APP=run.py
    FLASK_ENV=development
    DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/jlpt
    SECRET_KEY=your-secret-key
    JWT_SECRET_KEY=your_super_secret_key_here
    ```

5. **Run Database Migrations**
    ```sh
    flask db upgrade
    ```

6. **Start the Application**
    ```sh
    flask run
    # or
    python run.py
    ```

---

## 📬 API Endpoints

### Auth

| Method | Endpoint           | Description                |
|--------|--------------------|----------------------------|
| POST   | /auth/register     | Register a new user        |
| POST   | /auth/login        | Login and get JWT token    |
| GET    | /auth/me           | Get logged-in user info    |

### Password Reset

| Method | Endpoint               | Description                    |
|--------|------------------------|--------------------------------|
| POST   | /auth/request-reset    | Request a password reset token |
| POST   | /auth/reset-password   | Reset password using token     |

### Form Submission

| Method | Endpoint        | Description                        |
|--------|----------------|------------------------------------|
| POST   | /form          | Submit form (JWT required)         |
| GET    | /form/submissions | Get all submissions (JWT required) |

---

## 🧪 Sample Test with Postman

### Login

**Request**
```
POST http://localhost:5000/auth/login
Content-Type: application/json

{
  "email": "your@email.com",
  "password": "yourpassword"
}
```

**Response**
```json
{
  "access_token": "<token>",
  "user": {
    "id": "...",
    "email": "...",
    "full_name": "..."
  }
}
```

Use the token in the Authorization header for protected routes:

```
Authorization: Bearer <token>
```

---

### Submit Form

**Request**
```
POST http://localhost:5000/form
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "John Doe",
  "level": "N3",
  "score": 180
}
```

---

## 📄 Environment Variables (optional)

You can use a `.env` file and `python-dotenv` for configuration. Example:

```ini
FLASK_APP=run.py
FLASK_ENV=development
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/jlpt
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your_super_secret_key_here
```

---

## 📢 Notes

- Make sure PostgreSQL is running and the database specified in `DATABASE_URL` exists.
- For development, you can use SQLite by changing the `DATABASE_URL` in `.env` to `sqlite:///jlpt.db`.
- The password reset endpoint returns the reset token in the response for testing purposes. In production, you should send this token via email.

---

## 📝 License

MIT License

# Finance Dashboard — Backend API

A role-based finance management backend built with Flask and SQLite.

---

## Project Structure

```
finance_app/
├── app.py                  # Entry point — creates and runs the Flask app
├── config.py               # Loads settings from .env
├── extensions.py           # Shared db and cors instances (avoids circular imports)
├── requirements.txt        # Python dependencies
├── .env.example            # Copy this to .env before running
│
├── models/
│   ├── user.py             # User database model
│   └── record.py           # Financial record database model
│
├── routes/
│   ├── users.py            # POST /users, GET /users, PATCH /users/:id/status
│   ├── records.py          # CRUD for /records
│   └── dashboard.py        # GET /dashboard/summary, GET /dashboard/trends
│
├── services/
│   ├── auth_service.py     # get_current_user(), requires_role(), requires_auth()
│   └── record_service.py   # Aggregation logic: summary, trends
│
├── schemas/
│   ├── user_schema.py      # Input validation for user routes
│   └── record_schema.py    # Input validation for record routes
│
├── ui.html                 # API tester — open in browser to test all endpoints
└── dashboard.html          # Visual dashboard — charts, metrics, recent activity
```

---

## Setup

**1. Clone / copy the project folder**

**2. Create your `.env` file**
```bash
cp .env.example .env
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Run the server**
```bash
python app.py
```

Server starts at `http://127.0.0.1:5000`. A `finance.db` SQLite file is created automatically.

---

## Using the UI

Open `ui.html` in your browser to test all API endpoints interactively.
Open `dashboard.html` to see the visual dashboard with charts.

> Both files work by making fetch() calls to localhost:5000. No extra server needed.

---

## Roles

| Role     | Can Do |
|----------|--------|
| viewer   | Read records, view summary |
| analyst  | Read records, view summary, view trends |
| admin    | Everything — create/update/delete records and users |

---

## Authentication

This project uses a simple header-based identity system for demonstration.

Every request (except `POST /users`) must include:
```
X-User-Id: <your-user-id>
```

Get your user id by calling `POST /users` first.

---

## API Endpoints

### Users

| Method | Endpoint | Role Required | Description |
|--------|----------|---------------|-------------|
| POST | /users | none | Create a user |
| GET | /users | admin | List all users |
| PATCH | /users/:id/status | admin | Set user active/inactive |

### Records

| Method | Endpoint | Role Required | Description |
|--------|----------|---------------|-------------|
| POST | /records | admin | Create a record |
| GET | /records | any | List records (supports ?type, ?category, ?date filters) |
| PUT | /records/:id | admin | Update a record |
| DELETE | /records/:id | admin | Soft delete a record |

### Dashboard

| Method | Endpoint | Role Required | Description |
|--------|----------|---------------|-------------|
| GET | /dashboard/summary | any | Totals, net balance, category breakdown, recent 5 |
| GET | /dashboard/trends | analyst, admin | Monthly income vs expense |

---

## Assumptions Made

- Authentication is header-based (`X-User-Id`) — no passwords or JWT for simplicity.
- Soft delete is used for records (`deleted=True`) so data is never permanently lost.
- Dates are stored as strings in `YYYY-MM-DD` format.
- SQLite is used as the database — sufficient for local development and demos.
- CORS is enabled globally so the HTML files can call the API from the browser.

---

## What to Add Next (Optimization Path)

1. JWT authentication with `flask-jwt-extended`
2. Marshmallow schemas for cleaner validation
3. Pagination on `GET /records`
4. Password hashing with `bcrypt`
5. Unit tests with `pytest`
6. Deploy to Railway or Render with a PostgreSQL database

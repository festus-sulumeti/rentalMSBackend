# Rental Management System Backend

Flask REST API for managing rental properties, units, tenants, leases, payments, expenses, maintenance, invoices, and notifications.

## Features

- JWT authentication with role-aware access control
- Property, unit, lease, payment, expense, maintenance, invoice, notification, user, and dashboard endpoints
- Alembic migrations for the full rental-domain schema

## Requirements

- Python 3.8+
- pip

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/festus-sulumeti/rentalMSBackend.git
   ```
   ```bash
   cd rentalMSBackend
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   ```

   **Linux/macOS**

   ```bash
   source .venv/bin/activate
   ```

   **Windows**

   ```bash
   .venv\Scripts\activate
   ```

3. Install the project dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Environment Variables

Create a `.env` file in the project root directory and add the following variables:

```env
ADMIN_EMAIL=AdminMail
ADMIN_PASSWORD=Adminpasscode
DATABASE_URL=postgresql://user:password@localhost:5432/rentalms
JWT_SECRET_KEY=replace-with-a-long-random-secret
```

> **Note:** The `.env` file contains sensitive information and should never be committed to version control. Ensure it is included in your `.gitignore` file.


## Database Migrations (Alembic)

This project uses **Alembic** to manage database schema migrations.

### Initial Alembic Setup

If the `alembic/` directory or Alembic configuration files have been deleted or are not yet initialized, follow these steps:

1. Install Alembic:

   ```bash
   pip install alembic
   ```

2. Initialize Alembic:

   ```bash
   alembic init alembic
   ```

3. Generate a new migration after creating or updating your SQLAlchemy models:

   ```bash
   alembic revision --autogenerate -m "description_of_migration"
   ```

4. Apply the migration to the database:

   ```bash
   alembic upgrade head
   ```

### Creating New Migrations

If Alembic has already been initialized and the `alembic/` directory exists, you only need to generate and apply new migrations whenever your models change.

1. Generate a migration:

   ```bash
   alembic revision --autogenerate -m "description_of_migration"
   ```

2. Apply the migration:

   ```bash
   alembic upgrade head
   ```

### Viewing Migration History

Display the migration history:

```bash
alembic history
```

Display the current migration version applied to the database:

```bash
alembic current
```

Upgrade the database to the latest migration:

```bash
alembic upgrade head
```

Downgrade the database by one migration:

```bash
alembic downgrade -1
```

Downgrade the database to a specific revision:

```bash
alembic downgrade <revision_id>
```

## Running the Application

Start the Flask development server:

```bash
python app.py
```

The application will be available at:

```text
http://127.0.0.1:5000/
```

## Available Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Welcome endpoint |
| POST | `/auth/signup` | Register a user |
| POST | `/auth/login` | Log in and receive an access token |
| GET | `/auth/me` | Current user |
| CRUD | `/properties/` | Properties (authenticated owner/admin) |
| GET/POST/PUT | `/units/` | Rental units |
| GET/POST/PUT | `/leases/` | Leases |
| GET/POST | `/payments/`, `/expenses/`, `/invoices/` | Financial records |
| GET/POST/PATCH | `/maintenance/`, `/notifications/` | Operations and alerts |
| GET | `/dashboard/` | Property dashboard summary |

All routes except `/` and the signup/login endpoints require `Authorization: Bearer <access_token>`.

## Testing the API

### Welcome Endpoint

```bash
curl http://127.0.0.1:5000/
```

### Admin Login

```bash
curl -X POST http://127.0.0.1:5000/auth/login \
-H "Content-Type: application/json" \
-d '{
  "email": "admin@gmail.com",
  "password": "admin"
}'
```

The root endpoint returns a JSON welcome message for the API.

# Rental Management System Backend

This project is the initial backend for a Rental Management System API.

## Features

- Welcome route for the API
- Admin login using environment variables
- Flask-based backend structure
- Ready for future rental management endpoints

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
ADMIN_EMAIL=admin@gmail.com
ADMIN_PASSWORD=admin
```

> **Note:** The `.env` file contains sensitive information and should never be committed to version control. Ensure it is included in your `.gitignore` file.

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
| POST | `/login` | Admin login |
| GET | `/dashboard` | Admin dashboard |

## Testing the API

### Welcome Endpoint

```bash
curl http://127.0.0.1:5000/
```

### Admin Login

```bash
curl -X POST http://127.0.0.1:5000/login \
-H "Content-Type: application/json" \
-d '{
  "email": "admin@gmail.com",
  "password": "admin"
}'
```

The root endpoint returns a JSON welcome message for the API.
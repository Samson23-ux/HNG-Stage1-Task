# HNG Stage1 Task - Profile Management API

A robust FastAPI-based Profile Management REST API that integrates with external services to collect and manage user profile data including gender prediction and country information.

## Features ✨

- **Profile Management**: Create, read, and delete user profiles
- **Gender Prediction**: Automatically predicts gender from names with probability scores
- **Age Detection**: Determines age and categorizes into age groups (child, teenager, adult, senior)
- **Country Detection**: Identifies country of origin with probability scores
- **Async Support**: Full async/await support for high-performance operations
- **Error Handling**: Comprehensive exception handling with custom error responses

## Tech Stack 🛠️

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Uvicorn](https://img.shields.io/badge/Uvicorn-4B8BBE?style=for-the-badge&logo=uvicorn&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-2C3E50?style=for-the-badge&logo=pydantic&logoColor=white)
![Postgres](https://img.shields.io/badge/Postgres-336791?style=for-the-badge&logo=postgresql&logoColor=white)

## Prerequisites 📋

- Python 3.10+
- PostgreSQL 12+
- pip (Python package manager)

## Installation 📝

### Clone the Repository

```bash
git clone https://github.com/Samson23-ux/HNG-Stage1-Task.git
cd "HNG Stage1 Task"
```

### Create a Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Environment Configuration 🔧

Create a `.env` file and copy the environment template fixing replacing the values with your database URLs ([link to file](./env-demo.txt))

### Create Database

Create the API and Test database using bash or PgAdmin 4

### Run Database Migrations

```bash
# Upgrade to the latest migration
alembic upgrade head

# Downgrade to previous version (if needed)
alembic downgrade -1
```

## Running the Application 🚀

### Local
```bash
uvicorn app.main:app --reload
```

The API will be available at:
- **Base URL**: `http://localhost:8000`
- **API Documentation (Swagger UI)**: `http://localhost:8000/docs`
- **Alternative Docs (ReDoc)**: `http://localhost:8000/redoc`

### Deployed

- [Live App](<deployed url>)

- [API Documentation](<deployed url>)

## Running Tests 🧪

### Run All Tests

```bash
pytest
```

### Run Specific Test File

```bash
pytest tests/test_profiles.py
```

## External Integrations 🔗

This API integrates with external services to enrich profile data:

- **Gender API**: Predicts gender from names with probability scores
- **Age API**: Determines age based on name analysis
- **Country API**: Identifies country of origin based on name patterns

These integrations happen automatically when a profile is created.

## Troubleshooting 🔧

### Database Connection Issues

**Problem**: `could not connect to server`

**Solution**:
- Verify PostgreSQL is running: `pg_isready`
- Check database URL in `.env`
- Ensure database and user exist: `psql -l -U postgres`

### Migration Issues

**Problem**: Migration fails to apply

**Solution**:
```bash
# Check alembic version
alembic current

# Downgrade to previous version
alembic downgrade -1

# Review migration files in alembic/versions/
```

### Virtual Environment Issues

**Problem**: `ModuleNotFoundError` after installing dependencies

**Solution**:
- Ensure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt --force-reinstall`
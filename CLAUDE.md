# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Running the Application
- **Development server**: `./run.sh` (starts uvicorn with reload on port 8000)
- **Production server**: `uvicorn app.main:app --host 0.0.0.0 --port 8000`
- **Docker**: Build with `docker build -t user-profile-service .` and run with `docker run -p 8000:8000 user-profile-service`

### Dependencies
- Install dependencies: `pip install -r requirements.txt`
- Virtual environment should be activated before running (`.venv/bin/activate`)

## Architecture

This is a FastAPI-based user profile microservice with SQLModel/SQLAlchemy for database operations.

### Core Structure
- **app/main.py**: FastAPI application entry point
- **app/api/routes.py**: API endpoints (health check, user creation)
- **app/models.py**: SQLModel database models (UserProfile table)
- **app/schemas.py**: Pydantic models for API request/response validation
- **app/crud.py**: Database operations (create user, get user by email)
- **app/db.py**: Database connection and session management

### Database
- Uses PostgreSQL by default (DATABASE_URL env var)
- SQLModel for ORM with automatic table creation
- Default connection: `postgresql://postgres:postgres@db:5432/postgres`

### Key Design Patterns
- Repository pattern with CRUD operations separated from routes
- Dependency injection for database sessions
- Pydantic schemas for API validation separate from database models
- Environment variable configuration for database connection

### Data Model
The UserProfile model includes:
- UUID primary key with auto-generation
- Email (unique), full_name, optional avatar_url and bio
- Automatic created_at/updated_at timestamps

Note: There's a schema mismatch between models.py and schemas.py that should be addressed - models.py has UserProfileCreate/Read classes that don't match the actual UserProfile SQLModel.
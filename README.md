# Production Monitoring API

A robust backend service designed to monitor production line cycle times. This application is fully containerized with Docker, uses a secure JWT-based authentication system, and manages its database schema with Alembic migrations.

## ✨ Features

- **Modern API Framework**: Built with FastAPI for high performance and automatic interactive documentation.
- **Secure Authentication**: JWT token-based authentication with password hashing using `passlib` and `bcrypt`.
- **Segregated Databases**: Utilizes two separate PostgreSQL databases for enhanced security and scalability:
  - `auth_db`: Stores user credentials and authentication data.
  - `production_db`: Stores all core application and monitoring data.
- **Fully Containerized**: The entire stack (API, databases, admin tool) is managed by Docker Compose for a one-command startup.
- **Database Migrations**: Uses Alembic to provide safe, version-controlled updates to the database schema. No more manual table creation.
- **Data Validation**: Leverages Pydantic for robust data validation and settings management.
- **Asynchronous Support**: Ready for high-concurrency workloads.

## 🛠️ Tech Stack

- **Backend**: Python 3.12, FastAPI, Uvicorn
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Migrations**: Alembic
- **Containerization**: Docker, Docker Compose
- **Data Validation**: Pydantic
- **Authentication**: python-jose, passlib

## 🚀 Getting Started

Follow these instructions to get the project up and running on your local machine for development and testing.

### Prerequisites

You must have the following installed on your system:

- [Docker](https://www.docker.com/products/docker-desktop)
- [Python 3.12+](https://www.python.org/downloads/) and `pip` (for running Alembic commands locally)

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd zentrix-backend
```

### 2. Create the Environment File

The application requires an `.env` file for configuration. A template is provided in `.env.example`.

Copy the example file:

```powershell
# For Windows (PowerShell)
copy .env.example .env
```

```bash
# For macOS/Linux
cp .env.example .env
```

This file contains all the necessary credentials and configuration for the databases, API, and security settings. No modifications are needed to run the project locally.

### 3. Build the Docker Images

This command will build the custom Docker image for the FastAPI application based on the `Dockerfile`.

```bash
docker-compose build
```

## ▶️ Running the Application

### Starting the Services

Use this single command to start the entire application stack (API, both databases, and pgAdmin) in the foreground.

```bash
docker-compose up
```

You will see the logs from all services streamed to your terminal. The API will be available at `http://localhost:8000`.

- **Interactive API Docs (Swagger UI)**: `http://localhost:8000/api/v1/docs`
- **pgAdmin (Database GUI)**: `http://localhost:5050` (Login with credentials from `.env` file).

### Stopping the Services

When you are finished working, press `Ctrl + C` in the terminal where `docker-compose up` is running. Then, run the following command to completely stop and remove the containers and network.

```bash
docker-compose down
```

## 🗄️ Database Migrations (Alembic)

This project uses Alembic to manage the database schema. The tables are not created automatically on startup. You must generate and apply a migration.

**Important Note**: The `alembic.ini` file is configured to connect to the database via `localhost:5432`, allowing you to run these commands from your local terminal while the Docker containers are running.

### Generating a New Migration

After you make any changes to your SQLAlchemy models in the `app/models/` directory, run this command to have Alembic automatically generate a new migration script.

```bash
alembic revision --autogenerate -m "A descriptive message about your changes"
```

This will create a new file in the `alembic/versions/` directory.

### Applying a Migration

To apply all pending migrations and create/update the tables in your database, run:

```bash
alembic upgrade head
```

You only need to do this when you have new migration files to apply.

## 📂 Project Structure

```
.
├── alembic/              # Alembic migration scripts and environment
├── app/                  # Main application source code
│   ├── api/              # API endpoints (routers)
│   ├── core/             # Core logic (config, security)
│   ├── db/               # Database setup and session management
│   ├── models/           # SQLAlchemy ORM models
│   ├── schemas/          # Pydantic schemas for data validation
│   └── services/         # Business logic layer
├── .env                  # Local environment variables (DO NOT COMMIT)
├── .env.example          # Template for the .env file
├── .gitignore            # Files to be ignored by Git
├── alembic.ini           # Alembic configuration file
├── docker-compose.yml    # Docker Compose configuration
├── Dockerfile            # Docker instructions for the API service
├── main.py               # FastAPI application entry point
└── requirements.txt      # Python dependencies
```

# Production Monitoring API

A robust backend service designed to monitor production line cycle times. This application is fully containerized with Docker, uses a secure JWT-based authentication system, and manages its database schema with Alembic migrations.

## Key Features

*   **Modern API Framework**: Built with FastAPI for high performance, automatic interactive documentation, and robust data handling.
*   **Secure Authentication & Authorization**: Implements JWT token-based authentication with password hashing using `passlib` and `bcrypt`. Features Role-Based Access Control (RBAC) with Superuser privileges.
*   **Segregated Databases**: Utilizes two separate PostgreSQL databases for enhanced security and scalability:
    *   `auth_db`: Stores user credentials and authentication data.
    *   `production_db`: Stores all core application metrics and configuration data, including production line details, work elements, and cycle time records.
*   **Enhanced Analytics & Data Visualization**: Provides endpoints for detailed production analytics, including cycle time trends with outlier detection, production volume tracking, and operator performance data.
*   **Standard Time Management**: Allows for administrative management and updating of standard times for each work element on the production line.
*   **User Management**: Superusers can manage user accounts, including activating/deactivating users and assigning superuser privileges via a dedicated API.
*   **Fully Containerized**: The entire stack (API, both databases, and pgAdmin) is managed by Docker Compose for a streamlined, one-command setup and consistent deployment.
*   **Database Migrations**: Employs Alembic for safe, version-controlled updates to the database schema, ensuring data integrity across development and production environments.
*   **Robust Data Validation**: Leverages Pydantic for comprehensive data validation of all API requests and responses, ensuring data quality and system stability.
*   **Asynchronous Support**: Designed for high-concurrency workloads, optimizing responsiveness and throughput.

## Tech Stack

*   **Backend**: Python 3.12, FastAPI, Uvicorn
*   **Database**: PostgreSQL
*   **ORM**: SQLAlchemy
*   **Migrations**: Alembic
*   **Containerization**: Docker, Docker Compose
*   **Data Validation**: Pydantic
*   **Authentication**: PyJWT, python-jose, passlib

## Getting Started

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

## Running the Application

### Starting All Services

To start the entire application stack (API, both PostgreSQL databases, and pgAdmin) in detached mode (background):

```bash
docker-compose up -d
```

Once services are up:
*   **FastAPI Application**: Accessible at `http://localhost:8000`
*   **Interactive API Docs (Swagger UI)**: `http://localhost:8000/api/v1/docs`
*   **pgAdmin (Database GUI)**: `http://localhost:5050` (Login with credentials from your `.env` file)

### Stopping All Services

To stop and remove all containers, networks, and volumes (excluding named volumes like `auth_data` and `production_data`):

```bash
docker-compose down
```

To stop and remove containers and networks, but keep volumes:

```bash
docker-compose down --volumes
```

## Database Management

### Applying Database Migrations

This project uses Alembic for database schema management. Apply pending migrations to ensure your databases are up-to-date.

```bash
docker-compose exec api alembic upgrade head
```

### Seeding Initial Data

Populate the `stations` and `work_elements` tables with initial data.

```bash
docker-compose exec api python seed_database.py
```

### Importing Production Data

Import sample `CycleTimeRecord` data from `Tabledata.csv` and `Stattable-MP1.csv` into the database.

```bash
docker-compose exec api python import_data.py
```

### Granting Superuser Privileges

To promote a user to superuser status (admin access), use the `grant_superuser.py` script. Replace `<username>` with the actual username of the user to promote:

```bash
docker-compose exec api python grant_superuser.py <username>
```

After granting privileges, the user must **log out and log back in** to the frontend for changes to take effect.

## Project Structure

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
├── .env                  # Local environment variables (DO NOT COMMIT, Not in repo)
├── .gitignore            # Files to be ignored by Git
├── alembic.ini           # Alembic configuration file
├── docker-compose.yml    # Docker Compose configuration
├── Dockerfile            # Docker instructions for the API service
├── main.py               # FastAPI application entry point
├── requirements.txt      # Python dependencies
├── seed_database.py      # Script for seeding initial application data (Not in repo)
├── import_data.py        # Script for importing sample production data (Not in repo)
└── grant_superuser.py    # Script for granting superuser access (Not in repo)
```

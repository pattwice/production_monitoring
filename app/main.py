from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routes import auth
# Remove init_databases as it should not be run on startup in production
# from app.db.database import init_databases 

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
    docs_url=f"{settings.API_V1_PREFIX}/docs",
    redoc_url=f"{settings.API_V1_PREFIX}/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =================================================================
# NOTE: Database initialization on startup is removed.
# Use a migration tool like Alembic to manage database schema.
# For example, run `alembic upgrade head` from terminal.
# =================================================================
# @app.on_event("startup")
# def startup_event():
#     """Create all database tables on startup - NOT RECOMMENDED FOR PRODUCTION"""
#     from app.models.user import User
#     from app.models.production import Station, WorkElement, CycleTimeRecord, StatisticalThreshold    
#     init_databases()

# Include authentication routes
app.include_router(auth.router, prefix=settings.API_V1_PREFIX)

@app.get("/")
def root():
    """Root endpoint - health check"""
    return {
        "message": "Production Monitoring API is running!",
        "version": "1.0.0",
        "docs": f"{settings.API_V1_PREFIX}/docs",
    }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    # FIX: Removed references to settings attributes that no longer exist.
    # This endpoint now just confirms the API is responsive.
    # A more advanced health check might try to connect to the databases.
    return {"status": "healthy"}

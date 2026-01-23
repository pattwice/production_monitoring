from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routes import auth, production, analytics
from app.db.database import AuthBase, auth_engine
from app.models import user
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

@app.on_event("startup")
def create_auth_tables():
    """
    Create all tables in the auth_db database.
    This is safe because create_all(checkfirst=True) 
    will not modify existing tables.
    """
    print("Attempting to create Auth database tables...")
    try:
        AuthBase.metadata.create_all(bind=auth_engine, checkfirst=True)
        print("Auth database tables created (if they didn't exist).")
    except Exception as e:
        print(f"Error creating auth tables: {e}")

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
app.include_router(production.router, prefix=settings.API_V1_PREFIX)
app.include_router(analytics.router, prefix=settings.API_V1_PREFIX)

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
    return {"status": "healthy"}

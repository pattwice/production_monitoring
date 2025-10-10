from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routes import auth
from app.db.database import init_databases

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

# Initialize databases on startup
@app.on_event("startup")
def startup_event():
    """Create all database tables on startup"""
    from app.models.user import User
    from app.models.production import Station, WorkElement, CycleTimeRecord, StatisticalThreshold    
    init_databases()

# Include authentication routes
app.include_router(auth.router, prefix=settings.API_V1_PREFIX)

@app.get("/")
def root():
    """Root endpoint - health check"""
    return {
        "message": "Production Monitoring API",
        "version": "1.0.0",
        "docs": f"{settings.API_V1_PREFIX}/docs",
        "databases": {
            "auth": "auth_db (port 5433)",
            "production": "production_monitoring (port 5432)"
        }
    }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "auth_db": settings.AUTH_DB_NAME,
        "prod_db": settings.PROD_DB_NAME
    }
from sqlalchemy import create_engine as _create_engine
import sqlalchemy.ext.declarative as _declarative
import sqlalchemy.orm as _orm

from app.core.config import settings as _settings

# ============================================
# AUTHENTICATION DATABASE
# ============================================

# Create auth database engine
auth_engine = _create_engine(
    _settings.AUTH_DATABASE_URL,
    pool_pre_ping=True,
    echo=True  # Set to False in live production, True for debug
)

# Session factory for auth database
AuthSessionLocal = _orm.sessionmaker(autocommit=False, autoflush=False, bind=auth_engine)

# Base class for auth models
AuthBase = _declarative.declarative_base()

def get_auth_db():
    """
    Dependency to get auth database session.
    """
    db = AuthSessionLocal()
    try:
        yield db
    finally:
        db.close()


# ============================================
# PRODUCTION DATABASE
# ============================================

# Create production database engine
prod_engine = _create_engine(
    _settings.PROD_DATABASE_URL,
    pool_pre_ping=True,
    echo=True  # Set to False in live production, True for debug
)

# Session factory for production database
ProdSessionLocal = _orm.sessionmaker(autocommit=False, autoflush=False, bind=prod_engine)

# Base class for production models
ProdBase = _declarative.declarative_base()

def get_prod_db():
    """
    Dependency to get production database session.
    """
    db = ProdSessionLocal()
    try:
        yield db
    finally:
        db.close()


# ============================================
# INITIALIZATION FUNCTIONS
# ============================================

def init_auth_db():
    """Create all auth database tables"""
    AuthBase.metadata.create_all(bind=auth_engine)
    print("Auth database tables created")

def init_prod_db():
    """Create all production database tables"""
    ProdBase.metadata.create_all(bind=prod_engine)
    print("Production database tables created")

def init_databases():
    """Initialize both databases"""
    init_auth_db()
    init_prod_db()
    print("All databases initialized")
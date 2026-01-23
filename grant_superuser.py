import sys
import sqlalchemy.orm as _orm
from app.db.database import AuthSessionLocal
from app.models.user import User

def get_db():
    """Helper to get a database session."""
    db = AuthSessionLocal()
    try:
        yield db
    finally:
        db.close()

def grant_superuser_privileges(db: _orm.Session, username: str):
    """
    Finds a user by username and sets their is_superuser flag to True.
    """
    user = db.query(User).filter(User.username == username).first()

    if not user:
        print(f"Error: User '{username}' not found.")
        return

    if user.is_superuser:
        print(f"User '{username}' is already a superuser.")
        return

    user.is_superuser = True
    db.commit()
    print(f"✅ Success! User '{username}' has been granted superuser privileges.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python grant_superuser.py <username>")
        sys.exit(1)

    username_to_promote = sys.argv[1]
    
    db_session = next(get_db())
    grant_superuser_privileges(db_session, username_to_promote)
    db_session.close()
from app.database import Session


def get_db() -> Session:
    db = Session()
    try:
        yield db
    finally:
        db.close()
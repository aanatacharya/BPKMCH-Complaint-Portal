from app.db.base import SessionLocal

def get_db():
    this_session = SessionLocal() 
    try:
        yield this_session
    finally:
        this_session.close()